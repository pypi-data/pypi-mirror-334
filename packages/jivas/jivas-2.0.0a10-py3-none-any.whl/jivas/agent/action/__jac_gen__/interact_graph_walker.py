from __future__ import annotations
from jaclang import *
import typing
from enum import Enum, auto
if typing.TYPE_CHECKING:
    from jivas.agent.core.graph_walker import graph_walker
else:
    graph_walker, = jac_import('jivas.agent.core.graph_walker', items={'graph_walker': None})

class interact_graph_walker(graph_walker, Walker):
    pass