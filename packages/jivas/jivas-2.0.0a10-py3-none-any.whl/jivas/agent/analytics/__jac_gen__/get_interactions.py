from __future__ import annotations
from jaclang import *
import typing
from enum import Enum, auto
if typing.TYPE_CHECKING:
    import os
else:
    os, = jac_import('os', 'py')
if typing.TYPE_CHECKING:
    import logging
else:
    logging, = jac_import('logging', 'py')
if typing.TYPE_CHECKING:
    import traceback
else:
    traceback, = jac_import('traceback', 'py')
if typing.TYPE_CHECKING:
    from logging import Logger
else:
    Logger, = jac_import('logging', 'py', items={'Logger': None})
if typing.TYPE_CHECKING:
    from jivas.agent.core.agent import Agent
else:
    Agent, = jac_import('jivas.agent.core.agent', items={'Agent': None})
if typing.TYPE_CHECKING:
    from jivas.agent.action.action import Action
else:
    Action, = jac_import('jivas.agent.action.action', items={'Action': None})
if typing.TYPE_CHECKING:
    from jivas.agent.core.graph_walker import graph_walker
else:
    graph_walker, = jac_import('jivas.agent.core.graph_walker', items={'graph_walker': None})
if typing.TYPE_CHECKING:
    from jivas.agent.action.actions import Actions
else:
    Actions, = jac_import('jivas.agent.action.actions', items={'Actions': None})
if typing.TYPE_CHECKING:
    from jivas.agent.memory.memory import Memory
else:
    Memory, = jac_import('jivas.agent.memory.memory', items={'Memory': None})
if typing.TYPE_CHECKING:
    from jivas.agent.memory.frame import Frame
else:
    Frame, = jac_import('jivas.agent.memory.frame', items={'Frame': None})

class get_interactions(graph_walker, Walker):
    interactions: dict = field(gen=lambda: {})
    session_id: str = field('')
    logger: static[Logger] = logging.getLogger(__name__)

    class __specs__(Obj):
        private: static[bool] = False

    @with_entry
    def on_agent(self, here: Agent) -> None:
        self.visit(here.refs().filter(Memory, None))

    @with_entry
    def on_memory(self, here: Memory) -> None:
        if self.session_id:
            self.visit(here.refs().filter(Frame, None).filter(None, lambda item: item.session_id == self.session_id))
        else:
            self.visit(here.refs().filter(Frame, None))

    @with_entry
    def on_frame(self, here: Frame) -> None:
        interaction_list = here.get_interactions()
        self.interactions[here.session_id] = interaction_list

    @with_exit
    def on_exit(self, here) -> None:
        Jac.report(self.interactions)