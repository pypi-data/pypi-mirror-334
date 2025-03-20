from __future__ import annotations
from jaclang import *
import typing
from enum import Enum, auto
if typing.TYPE_CHECKING:
    from graph_walker import graph_walker
else:
    graph_walker, = jac_import('graph_walker', items={'graph_walker': None})
if typing.TYPE_CHECKING:
    from agents import Agents
else:
    Agents, = jac_import('agents', items={'Agents': None})

class list_agents(graph_walker, Walker):

    class __specs__(Obj):
        private: static[bool] = False

    @with_entry
    def on_agents(self, here: Agents) -> None:
        if (agents := here.get_all()):
            for agent in agents:
                Jac.report(agent.export())