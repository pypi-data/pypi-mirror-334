import os
import sys
from types import NoneType
from dektools.output import obj2str
from dektools.str import hex_random
from dektools.dict import MapChainContext
from . import MarkerBase, TransformerMarker, ExitException


class MarkerContext:
    def __init__(self, parent=None):
        self.variables = parent.variables.derive() if parent else MapChainContext()
        self.environ = parent.environ.derive() if parent else MapChainContext()

    def __str__(self):
        return obj2str(dict(variable=self.variables, environ=self.environ))

    def derive(self):
        return self.__class__(self)

    def variables_full(self):
        return self.variables.flat()

    def update_variables(self, context):
        self.variables.update(context)
        return self

    def remove_variable(self, name):
        if isinstance(name, str):
            self.variables.remove_item(name)
        else:
            for x in name:
                self.remove_variable(x)

    def add_variable(self, k, v):
        self.variables.add_item(k, v)

    def add_variable_temp(self, value):
        while True:
            name = f'_temp_var_{hex_random(16)}'
            if name not in self.variables:
                break
        self.add_variable(name, value)
        return name

    def environ_full(self):
        environ = os.environ.copy()
        environ.update(self.environ.flat())
        return environ

    def get_env(self, name, default=None):
        empty = object()
        value = self.environ.get_item(name, empty)
        if value is not empty:
            return value
        return os.environ.get(name, default)


class HiddenVarSet:
    def __init__(self):
        self._data = {}

    def add_item(self, k, v):
        self._data[k] = v

    def remove_item(self, name):
        if isinstance(name, str):
            self._data.pop(name, None)
        else:
            for x in name:
                self.remove_item(x)

    def get_item(self, name, default=None):
        return self._data.get(name, default)


class PlaceholderMarker(MarkerBase):
    tag_head = ""


class MarkerNode:
    def __init__(self, marker, command, index, parent=None, command_old=None, payload=None):
        self.marker = marker
        self.command = command
        self.command_old = command_old
        self.index = index
        self.parent = parent
        self.children = []
        self.payload = payload

    def __repr__(self):
        return f'Node({self.marker.__class__.__name__})'

    def clone(self):
        node = self.__class__(
            self.marker, self.command, self.index, self.parent, self.command_old, self.payload)
        node.children = self.clone_children(node)
        return node

    def clone_children(self, parent=None):
        result = []
        for child in self.children:
            node = child.clone()
            node.parent = parent or self
            result.append(node)
        return result

    @property
    def debug_info(self):
        def walk(node):
            return dict(
                marker=node.marker,
                command=node.command,
                index=node.index,
                children=[walk(child) for child in node.children]
            )

        return obj2str(walk(self))

    def is_type(self, *markers_cls):
        return isinstance(self.marker, tuple(markers_cls))

    def add_child(self, node):
        node.parent = self
        self.children.append(node)
        return node

    def bubble_continue(self, context, marker_set, node):
        cursor = self
        while cursor:
            # result is (x, [y]) =>  x: location exec depth, [y]: insert to loop
            result = cursor.marker.bubble_continue(context, marker_set, cursor, node)
            if result is None:
                cursor = cursor.parent
            else:
                return result
        return None

    @classmethod
    def execute_nodes(cls, context, marker_set, nodes):
        while nodes:
            node = nodes.pop(0)
            result = node.bubble_continue(context, marker_set, node)
            if result is not None:
                return result
            else:
                try:
                    changes = node.marker.execute(
                        context,
                        node.marker.translate(context, node.command or ''),
                        node, marker_set
                    )
                except ExitException:
                    raise
                except Exception as e:
                    sys.stderr.write(f"Execute error {node.marker}:\n\
                    command=> {node.command if node.command_old is None else node.command_old}\n\
                    line=> {node.line_number}\n\
                    context=>\n\
                    {context}")
                    raise e from None
                if changes is None:
                    context_ = context
                    nodes_ = node.children[:]
                elif isinstance(changes, list):
                    context_ = context
                    nodes_ = changes
                elif isinstance(changes, tuple):
                    variables, nodes_ = changes
                    context_ = context.derive().update_variables(variables)
                else:
                    raise TypeError(f"Unknown type of changes: {changes}")
                result = cls.execute_nodes(
                    context_,
                    marker_set,
                    nodes_
                )
                if result is not None:
                    node_cursor, node_loop_list = result
                    if node is node_cursor:  # location of the depth
                        nodes[:0] = node_loop_list
                    else:
                        return result

    def execute(self, context, marker_set):
        self.execute_nodes(context, marker_set, [self])

    def walk(self, cb, depth=0):
        cb(self, depth)
        for child in self.children:
            child.walk(cb, depth + 1)

    @classmethod
    def root(cls):
        return cls(PlaceholderMarker(), None, None)

    @property
    def line_number(self):
        if self.index is None:
            return None
        return self.index + 1


class MarkerSet:
    node_cls = MarkerNode
    context_cls = MarkerContext
    transformer_cls = TransformerMarker
    hidden_var_set_cls = HiddenVarSet

    def __init__(self, markers_cls, shell_exec, shell_cmd):
        markers = []
        self.markers_branch_set = set()
        for marker_cls in markers_cls:
            markers.append(marker_cls())
            for branch_cls in marker_cls.final_branch_set:
                self.markers_branch_set.add(branch_cls)
        self.vars = self.hidden_var_set_cls()
        self.markers = self.transformer_cls.inject(markers)
        self.shell_exec = shell_exec
        self.shell_cmd = shell_cmd

    def is_marker_branch(self, marker):
        return marker.__class__ in self.markers_branch_set

    def find_marker_by_cls(self, marker_cls):
        for marker in self.markers:
            if isinstance(marker, marker_cls):
                return marker

    def find_marker_by_command(self, command):
        for marker in self.markers:
            if marker.recognize(command):
                return marker

    def generate_tree(self, commands):
        stack = [self.node_cls.root()]
        for index, command in enumerate(commands):
            marker = self.find_marker_by_command(command)
            while isinstance(marker, stack[-1].marker.tag_tail or NoneType):
                node_tail = stack.pop()
                if not self.is_marker_branch(node_tail.marker):
                    break
            parent = stack[-1]
            marker = marker.transform(parent.marker)
            node = self.node_cls(marker, command, index)
            parent.add_child(node)
            if marker.tag_tail is not None:  # block command
                stack.append(node)
        if len(stack) != 1:
            raise Exception(f'Stack should have just a root node in final: {stack}')
        return stack[0]

    def execute(self, commands, context):
        try:
            root = self.generate_tree(commands)
            root.execute(self.context_cls().update_variables(context or {}), self)
        except ExitException:
            pass
