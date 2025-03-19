from ..plugin import get_markers_from_modules
from .base import EndMarker, BreakMarker, ContinueMarker
from .var import *
from .env import *
from .if_ import *
from .while_ import *
from .for_ import *
from .default import *
from .comment import *
from .invoke import *
from .function import *
from .exec import *
from .echo import *
from .pip_ import *
from .shell import *
from .redirect import *
from .empty import *


def generate_markers(*args, **kwargs):
    return [
        *args,
        *get_markers_from_modules(**kwargs),
        ErrorEchoMarker, EchoMarker,
        AssignExecMarker, AssignEvalMixinMarker,
        AssignMultiLineRawStrMarker, AssignMultiLineStrMarker, AssignRawStrMarker, AssignStrMarker,
        DelVarMarker,
        ExecLinesUpdateMarker, ExecLinesMarker, ExecMarker, ExecCmdcallLinesMarker, ExecCmdcallMarker,
        EnvShellMarker, EnvMarker,
        IfMarker, IfElifMarker, IfElseMarker,
        WhileMarker,
        ForMarker, ForElseMarker,
        DefaultMarker,
        GotoMarker, InvokeMarker,
        FunctionMarker, CallMarker, EnvGlobalMarker, EnvNonlocalMarker, VarGlobalMarker, VarNonlocalMarker,
        EndMarker, BreakMarker, ContinueMarker,
        CommentMultiLineMarker, CommentMarker, CommentShebangMarker, CommentConfigMarker,
        PipMarker,
        ShellMarker,
        RedirectMarker, ShiftMarker,
        EmptyMarker,  # must be at the tail
    ]
