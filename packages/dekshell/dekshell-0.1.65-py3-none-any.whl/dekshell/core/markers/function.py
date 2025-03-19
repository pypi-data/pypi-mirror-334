from dektools.dict import assign_list
from .base import MarkerBase, MarkerWithEnd, cmd_call_prefix, cmd_call_prefix_simple


class CallMarker(MarkerBase):
    tag_head = "call"

    def execute(self, context, command, marker_node, marker_set):
        expression = self.split_raw(command, 1)[-1]
        if expression.startswith(cmd_call_prefix):
            name, args, kwargs = self.cmd_call_parse(context, expression[len(cmd_call_prefix):], False)
        elif expression.startswith(cmd_call_prefix_simple):
            name, args, kwargs = self.cmd_call_parse(context, expression[len(cmd_call_prefix_simple):], True)
        else:
            name = expression[:expression.find('(')]
            args, kwargs = self.eval(context, expression, {name: lambda *a, **k: (a, k)})
        function = self.eval(context, name)
        variables = self.eval(context, f"lambda {function.params}: locals()")(*args, **kwargs)
        return variables, function.body[:]


class Function:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def __call__(self, *args, **kwargs):
        raise RuntimeError(f"You can only call this function({self.name}) by using: {CallMarker.tag_head} ...")

    def __str__(self):
        return f"{self.__class__.__name__}<{self.name}>"


class FunctionMarker(MarkerWithEnd):
    tag_head = "function"

    def execute(self, context, command, marker_node, marker_set):
        name, params = assign_list([''] * 2, self.split_raw(command, 2)[1:])
        self.set_var_raw(context, name, Function(name, params, marker_node.children[:]))
        return []


class VarGlobalMarker(MarkerBase):
    tag_head = "global"

    def execute(self, context, command, marker_node, marker_set):
        context.variables.mark_global(self.split_raw(command, 1)[-1])


class VarNonlocalMarker(MarkerBase):
    tag_head = "nonlocal"

    def execute(self, context, command, marker_node, marker_set):
        context.variables.mark_nonlocal(self.split_raw(command, 1)[-1])


class EnvGlobalMarker(MarkerBase):
    tag_head = "global$"

    def execute(self, context, command, marker_node, marker_set):
        context.environ.mark_global(self.split_raw(command, 1)[-1])


class EnvNonlocalMarker(MarkerBase):
    tag_head = "nonlocal$"

    def execute(self, context, command, marker_node, marker_set):
        context.environ.mark_nonlocal(self.split_raw(command, 1)[-1])
