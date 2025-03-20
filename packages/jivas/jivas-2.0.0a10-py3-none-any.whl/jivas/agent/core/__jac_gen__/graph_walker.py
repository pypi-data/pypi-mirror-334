from __future__ import annotations
from jaclang import *
import typing
from enum import Enum, auto
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
    from jivas.agent.modules.agentlib.utils import Utils
else:
    Utils, = jac_import('jivas.agent.modules.agentlib.utils', 'py', items={'Utils': None})
if typing.TYPE_CHECKING:
    from app import App
else:
    App, = jac_import('app', items={'App': None})
if typing.TYPE_CHECKING:
    from agents import Agents
else:
    Agents, = jac_import('agents', items={'Agents': None})

class graph_walker(Walker):
    agent_id: str = field('')
    reporting: bool = field(True)
    logger: static[Logger] = logging.getLogger(__name__)

    class __specs__(Obj):
        private: static[bool] = True

    def export(self, ignore_keys: list=JacList(['__jac__'])) -> None:
        node_export = Utils.export_to_dict(self, ignore_keys)
        return node_export

    def update(self, data: dict={}) -> graph_walker:
        if data:
            for attr in data.keys():
                if hasattr(self, attr):
                    self.attr = data[attr]
        self.postupdate()
        return self

    def postupdate(self) -> None:
        pass

    @with_entry
    def on_root(self, here: Root) -> None:
        if not self.visit(here.refs().filter(App, None)):
            self.logger.debug('app node created')
            app_node = here.connect(App())
            self.visit(app_node)

    @with_entry
    def on_app(self, here: App) -> None:
        if not self.visit(here.refs().filter(Agents, None)):
            self.logger.debug('agents node created')
            agents_node = here.connect(Agents())
            self.visit(agents_node)

    @with_entry
    def on_agents(self, here: Agents) -> None:
        if self.agent_id:
            try:
                if (agent_node := jobj(id=self.agent_id)):
                    if agent_node.published:
                        self.visit(agent_node)
            except Exception as e:
                Jac.get_context().status = 400
                Jac.report('Invalid agent id')
                return self.disengage()