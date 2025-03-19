from .base import MarkerBase, MarkerWithEnd, MarkerNoTranslator, cmd_call_prefix


class MarkerAssignBase(MarkerBase):
    tag_head_re = r"[^\W\d]\w*[ \t\f\r\n]*%s"


class MarkerAssignValueBase(MarkerAssignBase):
    def execute(self, context, command, marker_node, marker_set):
        args = self.split_raw(command, 1, self.tag_head_re_args)
        self.set_var(context, args, 0, self.get_value(context, args[1]))

    def get_value(self, context, args):
        raise NotImplementedError


class AssignStrMarker(MarkerAssignValueBase):
    tag_head_re_args = ':'

    def get_value(self, context, expression):
        return expression


class AssignRawStrMarker(AssignStrMarker, MarkerNoTranslator):
    tag_head_re_args = '&:'


class AssignMultiLineStrMarker(MarkerAssignBase, MarkerWithEnd):
    tag_head_re_args = '::'

    def execute(self, context, command, marker_node, marker_set):
        text = self.get_inner_content(context, marker_node)
        args = self.split_raw(command, 1, self.tag_head_re_args)
        self.set_var(context, args, 0, text)
        return []


class AssignMultiLineRawStrMarker(AssignMultiLineStrMarker, MarkerNoTranslator):
    tag_head_re_args = '&::'


class AssignEvalMixinMarker(MarkerAssignValueBase):
    tag_head_re_args = '='

    def get_value(self, context, expression):
        return self.eval_mixin(context, expression)


class AssignExecMarker(MarkerAssignBase, MarkerWithEnd):
    tag_head_re_args = '=='

    def execute(self, context, command, marker_node, marker_set):
        code = self.get_inner_content(context, marker_node)
        result = self.eval_codes(context, code)
        args = self.split_raw(command, 1, self.tag_head_re_args)
        self.set_var(context, args, 0, result)
        return []


class DelVarMarker(MarkerBase):
    tag_head = "del"

    def execute(self, context, command, marker_node, marker_set):
        name = self.split_raw(command, 1, self.tag_head)[-1]
        if name:
            context.remove_variable(name)
