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

class delete_agent(graph_walker, Walker):
    agent_id: str = field('')

    class __specs__(Obj):
        private: static[bool] = False

    @with_entry
    def on_agents(self, here: Agents) -> None:
        agent_node = here.delete(self.agent_id)
        if self.reporting:
            Jac.report(agent_node)