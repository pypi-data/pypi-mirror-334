from __future__ import annotations
from jaclang import *
import typing
from enum import Enum, auto
if typing.TYPE_CHECKING:
    import os
else:
    os, = jac_import('os', 'py')
if typing.TYPE_CHECKING:
    import yaml
else:
    yaml, = jac_import('yaml', 'py')
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
    from jivas.agent.core.agent import Agent
else:
    Agent, = jac_import('jivas.agent.core.agent', items={'Agent': None})
if typing.TYPE_CHECKING:
    from jivas.agent.action.actions import Actions
else:
    Actions, = jac_import('jivas.agent.action.actions', items={'Actions': None})
if typing.TYPE_CHECKING:
    from jivas.agent.core.graph_walker import graph_walker
else:
    graph_walker, = jac_import('jivas.agent.core.graph_walker', items={'graph_walker': None})
if typing.TYPE_CHECKING:
    from jivas.agent.core.import_agent import import_agent
else:
    import_agent, = jac_import('jivas.agent.core.import_agent', items={'import_agent': None})

class install_action(graph_walker, Walker):
    reporting: bool = field(False)
    override_action: bool = field(True)
    package_name: str = field('')
    version: str = field('')
    logger: static[Logger] = logging.getLogger(__name__)

    class __specs__(Obj):
        private: static[bool] = False

    @with_entry
    def on_agent(self, here: Agent) -> None:
        descriptor_data = None
        try:
            with open(here.descriptor, 'r') as file:
                descriptor_data = yaml.safe_load(file)
            if not descriptor_data:
                self.logger.error(f'unable to load descriptor: {here.descriptor}')
                return None
        except Exception as e:
            self.logger.error(f'an exception occurred, {traceback.format_exc()}')
            return None
        jpr_api_key = descriptor_data.get('jpr_api_key')
        dep_action_info = here.get_actions().get_action_info(namespace_package_name=self.package_name, version=self.version, jpr_api_key=jpr_api_key)
        if dep_action_info:
            action_info = {'action': dep_action_info.get('name'), 'context': {'version': dep_action_info.get('version'), 'enabled': True}}
            action_exists = False
            for action in descriptor_data['actions']:
                if action['action'] == self.package_name:
                    if self.override_action:
                        action['context'] = action_info['context']
                    else:
                        action['context'].update(action_info['context'])
                    action_exists = True
            if not action_exists:
                descriptor_data['actions'].append(action_info)
            self.import_from_descriptor(descriptor_data)

    def import_from_descriptor(self, descriptor: dict) -> Agent:
        if descriptor.get('id', None):
            try:
                agent_node = jobj(id=descriptor['id'])
            except Exception as e:
                self.logger.error(f'an exception occurred, {traceback.format_exc()}')
                return None
        else:
            agent_name = descriptor.get('name')
            if (_node := agents_node.get_by_name(agent_name)):
                agent_node = _node
            elif (agent_node := Agent(name=agent_name, description=descriptor.get('description', ''))):
                if not agents_node.get_by_id(agent_node.id):
                    agents_node.connect(agent_node)
                self.logger.info(f'agent created: {agent_node.name}')
            else:
                self.logger.error(f'unable to create agent: {agent_name}')
        if agent_node:
            descriptor_root = Utils.get_descriptor_root()
            agent_node.descriptor = f'{descriptor_root}/{agent_node.id}.yaml'
            agent_node.get_memory()
            agent_node.get_actions()
            if (agent_node := agent_node.update(data=descriptor, with_actions=True)):
                agent_node.export_descriptor()
                return agent_node
        return None