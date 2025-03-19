import sys
from .base import MarkerBase


class EchoMarker(MarkerBase):
    tag_head = "echo"

    def execute(self, context, command, marker_node, marker_set):
        print(self.split_raw(command, 1, self.tag_head)[-1])


class ErrorEchoMarker(MarkerBase):
    tag_head = "echox"

    def execute(self, context, command, marker_node, marker_set):
        print(self.split_raw(command, 1, self.tag_head)[-1], file=sys.stderr)
