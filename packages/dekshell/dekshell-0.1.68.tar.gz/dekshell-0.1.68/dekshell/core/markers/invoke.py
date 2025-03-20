import os
from dektools.file import normal_path
from ...utils.cmd import pack_context
from .base import MarkerBase


class MarkerInvokerBase(MarkerBase):
    def execute(self, context, command, marker_node, marker_set):
        self.execute_core(context, marker_set, self.split_raw(command, 1, self.tag_head)[-1])

    def execute_core(self, context, marker_set, s):
        argv = self.split(s)
        args, kwargs = self.cmd2ak(argv[1:])
        args, kwargs = self.var_map_batch(context, *args, **kwargs)
        return self.run_file(marker_set, normal_path(argv[0]), pack_context(args, kwargs))

    def run_file(self, marker_set, filepath, attrs):
        raise NotImplementedError


class GotoMarker(MarkerInvokerBase):
    tag_head = "goto"

    def run_file(self, marker_set, filepath, attrs):
        return marker_set.shell_exec(filepath, attrs)


class InvokeMarker(MarkerInvokerBase):
    tag_head = "invoke"

    def run_file(self, marker_set, filepath, attrs):
        cwd = os.getcwd()
        os.chdir(os.path.dirname(filepath))
        ret_value = marker_set.shell_exec(filepath, attrs)
        os.chdir(cwd)
        return ret_value
