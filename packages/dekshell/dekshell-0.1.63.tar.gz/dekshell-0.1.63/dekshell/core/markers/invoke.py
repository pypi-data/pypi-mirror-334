import os
from dektools.file import normal_path
from .base import MarkerBase


class GotoMarker(MarkerBase):
    tag_head = "goto"

    def execute(self, context, command, marker_node, marker_set):
        argv = self.split(command)
        marker_set.shell_exec(normal_path(argv[1]), self.cmd2ak(argv[2:])[1])


class InvokeMarker(MarkerBase):
    tag_head = "invoke"

    def execute(self, context, command, marker_node, marker_set):
        argv = self.split(command)
        path_shell_file = normal_path(argv[1])
        cwd = os.getcwd()
        os.chdir(os.path.dirname(path_shell_file))
        marker_set.shell_exec(path_shell_file, self.cmd2ak(argv[2:])[1])
        os.chdir(cwd)
