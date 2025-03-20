import os
from dektools.file import normal_path
from ...utils.cmd import pack_context
from .base import MarkerBase


class MarkerInvokerBase(MarkerBase):
    def execute(self, context, command, marker_node, marker_set):
        argv = self.split(command)
        args, kwargs = self.cmd2ak(argv[2:])
        args, kwargs = self.var_map_batch(context, *args, **kwargs)
        self.run_file(marker_set, normal_path(argv[1]), pack_context(args, kwargs))

    def run_file(self, marker_set, filepath, contexts):
        raise NotImplementedError


class GotoMarker(MarkerInvokerBase):
    tag_head = "goto"

    def run_file(self, marker_set, filepath, contexts):
        marker_set.shell_exec(filepath, contexts)


class InvokeMarker(MarkerInvokerBase):
    tag_head = "invoke"

    def run_file(self, marker_set, filepath, contexts):
        cwd = os.getcwd()
        os.chdir(os.path.dirname(filepath))
        marker_set.shell_exec(filepath, contexts)
        os.chdir(cwd)
