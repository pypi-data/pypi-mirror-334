from __future__ import annotations
from jaclang import *
import typing
from enum import Enum, auto
if typing.TYPE_CHECKING:
    from action import Action
else:
    Action, = jac_import('action', items={'Action': None})
if typing.TYPE_CHECKING:
    from jivas.agent.core.agent import Agent
else:
    Agent, = jac_import('jivas.agent.core.agent', items={'Agent': None})
if typing.TYPE_CHECKING:
    from jivas.agent.action.actions import Actions
else:
    Actions, = jac_import('jivas.agent.action.actions', items={'Actions': None})
if typing.TYPE_CHECKING:
    from interact_graph_walker import interact_graph_walker
else:
    interact_graph_walker, = jac_import('interact_graph_walker', items={'interact_graph_walker': None})

class healthcheck(interact_graph_walker, Walker):
    trace: dict = field(gen=lambda: {})

    class __specs__(Obj):
        private: static[bool] = False

    @with_entry
    def on_agent(self, here: Agent) -> None:
        self.visit(here.refs().filter(Actions, None))

    @with_entry
    def on_actions(self, here: Actions) -> None:
        self.visit(here.refs().filter(Action, None).filter(None, lambda item: item.enabled == True))

    @with_entry
    def on_action(self, here: Action) -> None:
        self.trace[here.label] = here.healthcheck()

    @with_exit
    def on_exit(self, here) -> None:
        if self.trace:
            Jac.get_context().status = 200
            health = {'agent': 'OK'}
            for action in self.trace:
                if self.trace[action] == False:
                    Jac.get_context().status = 503
                    health = self.trace
        else:
            Jac.get_context().status = 503
            health = self.trace
        Jac.report(health)