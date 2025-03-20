from __future__ import annotations
from jaclang import *
import typing
from enum import Enum, auto
if typing.TYPE_CHECKING:
    import io
else:
    io, = jac_import('io', 'py')
if typing.TYPE_CHECKING:
    import os
else:
    os, = jac_import('os', 'py')
if typing.TYPE_CHECKING:
    import subprocess
else:
    subprocess, = jac_import('subprocess', 'py')
if typing.TYPE_CHECKING:
    import pkg_resources
else:
    pkg_resources, = jac_import('pkg_resources', 'py')
if typing.TYPE_CHECKING:
    import sys
else:
    sys, = jac_import('sys', 'py')
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
    import tarfile
else:
    tarfile, = jac_import('tarfile', 'py')
if typing.TYPE_CHECKING:
    import requests
else:
    requests, = jac_import('requests', 'py')
if typing.TYPE_CHECKING:
    from logging import Logger
else:
    Logger, = jac_import('logging', 'py', items={'Logger': None})
if typing.TYPE_CHECKING:
    from jaclang import jac_import
else:
    jac_import, = jac_import('jaclang', 'py', items={'jac_import': None})
if typing.TYPE_CHECKING:
    from jivas.agent.modules.agentlib.utils import Utils
else:
    Utils, = jac_import('jivas.agent.modules.agentlib.utils', 'py', items={'Utils': None})
if typing.TYPE_CHECKING:
    from jvcli.utils import is_version_compatible
else:
    is_version_compatible, = jac_import('jvcli.utils', 'py', items={'is_version_compatible': None})
if typing.TYPE_CHECKING:
    from jvcli.api import RegistryAPI
else:
    RegistryAPI, = jac_import('jvcli.api', 'py', items={'RegistryAPI': None})
if typing.TYPE_CHECKING:
    from jvserve.lib.agent_interface import AgentInterface
else:
    AgentInterface, = jac_import('jvserve.lib.agent_interface', 'py', items={'AgentInterface': None})
if typing.TYPE_CHECKING:
    from action import Action
else:
    Action, = jac_import('action', items={'Action': None})
if typing.TYPE_CHECKING:
    from interact_action import InteractAction
else:
    InteractAction, = jac_import('interact_action', items={'InteractAction': None})
if typing.TYPE_CHECKING:
    from interact_graph_walker import interact_graph_walker
else:
    interact_graph_walker, = jac_import('interact_graph_walker', items={'interact_graph_walker': None})
if typing.TYPE_CHECKING:
    from jivas.agent.core.graph_node import GraphNode
else:
    GraphNode, = jac_import('jivas.agent.core.graph_node', items={'GraphNode': None})
if typing.TYPE_CHECKING:
    from exit_interact_action import ExitInteractAction
else:
    ExitInteractAction, = jac_import('exit_interact_action', items={'ExitInteractAction': None})

class Actions(GraphNode, Node):
    logger: static[Logger] = logging.getLogger(__name__)
    package_root: static[str] = Utils.get_actions_root()

    def get(self, action_type: str='', action_label: str='') -> None:
        result = None
        if action_type and (not action_label):
            result = self.get_by_type(action_type)
        elif action_label and (not action_type):
            result = self.get_by_label(action_label)
        return result

    def get_by_label(self, action_label: str) -> Action:
        for action_node in self.get_all():
            if action_node.label == action_label:
                return action_node
        return None

    def get_by_type(self, action_type: str) -> list:
        result = JacList([])
        for action_node in self.get_all():
            if action_type == action_node.get_type():
                result.append(action_node)
        return result

    def get_all(self, filter_interact_actions: bool=False, filter_enabled_actions: bool=False) -> list:
        if filter_interact_actions:
            return self.spawn(_get_interact_actions(filter_enabled=filter_enabled_actions)).action_nodes
        return self.spawn(_get_actions(filter_enabled=filter_enabled_actions)).action_nodes

    def get_action_info(self, namespace_package_name: str, version: str=None, jpr_api_key: str=None) -> None:
        action_info = None
        namespace, package_name = namespace_package_name.split('/')
        if (package_path := Utils.find_package_folder(self.package_root, namespace_package_name)):
            info_yaml_path = os.path.join(package_path, 'info.yaml')
            with open(info_yaml_path, 'r') as file:
                try:
                    _info = yaml.safe_load(file)
                    package_version = _info.get('package', {}).get('version', None)
                    if is_version_compatible(version, package_version):
                        module_root = Utils.path_to_module(package_path)
                        has_app = os.path.isfile(os.path.join(package_path, 'app', 'app.py'))
                        action_info = _info['package']
                        action_info['config']['path'] = package_path
                        action_info['config']['app'] = has_app
                        action_info['config']['module_root'] = module_root
                        action_info['config']['module'] = f'{module_root}.{package_name}'
                except yaml.YAMLError as e:
                    self.logger.error(f'an exception occurred, {traceback.format_exc()}')
        if not action_info:
            self.logger.info(f'attempting to fetch action info remotely for {namespace_package_name}={version}')
            if (_info := RegistryAPI.get_action_info(namespace_package_name, version, api_key=jpr_api_key)):
                self.logger.info(f'found action info remotely for {namespace_package_name}={version}')
                action_info = _info.get('package', None)
        if action_info:
            action_info['config']['namespace'] = namespace
            action_info['config']['package_name'] = package_name
        return action_info

    def index_action_data(self, data: dict) -> None:
        action_data_index = {}

        def flatten_actions(action_list):
            for action_data in action_list:
                if (namespace_package_name := action_data.get('action', None)):
                    action_data_index[namespace_package_name] = action_data
                    if 'children' in action_data:
                        flatten_actions(action_data['children'])
        flatten_actions(data)
        return action_data_index

    def import_action(self, action_data: dict) -> None:
        module_root = action_data.get('context', {}).get('_package', {}).get('config', {}).get('module_root', None)
        if module_root:
            jac_import(f'{module_root}.lib', base_path='./')
            return True
        return False

    def load_pip_packages(self, action_data: dict) -> None:
        loaded = True
        pip_packages = action_data.get('context', {}).get('_package', {}).get('dependencies', {}).get('pip', {})
        for package, version in pip_packages.items():
            package_with_version = f'{package}=={version}'
            try:
                if not self.has_pip_package(package, version):
                    subprocess.check_call(JacList([sys.executable, '-m', 'pip', 'install', package_with_version, '--root-user-action=ignore']))
                if self.has_pip_package(package, version):
                    self.logger.info(f'pip package installed {package_with_version}')
                    loaded = True
                else:
                    loaded = False
                    break
            except subprocess.CalledProcessError as e:
                self.logger.error(f'failed to install {package_with_version}. Error: {e}')
                loaded = False
                break
        return loaded

    def has_pip_package(self, package_name: str, version: str=None) -> None:
        try:
            package_distribution = pkg_resources.get_distribution(package_name)
            if version is None:
                return True
            else:
                return package_distribution.version == version
        except pkg_resources.DistributionNotFound:
            return False

    def load_action_packages(self, agent_id: str, data: dict, jpr_api_key: str=None) -> None:
        action_data_index = self.index_action_data(data)
        try:
            action_data_index_copy = action_data_index.copy()
            for namespace_package_name, action_data in action_data_index_copy.items():
                namespace, package_name = namespace_package_name.split('/')
                package_version = action_data.get('context', {}).get('version', None)
                if (action_info := self.get_action_info(namespace_package_name, package_version, jpr_api_key)):
                    action_data['context']['_package'] = action_info
                    action_data['context']['agent_id'] = agent_id
                    architype = action_info.get('architype', None)
                    action_data['context']['label'] = action_data.get('context', {}).get('label', architype)
                    action_data['context']['description'] = action_info.get('meta', {}).get('description', '')
                    action_deps = action_info.get('dependencies', {}).get('actions', {})
                    loaded_action_deps = {}
                    for action_dep in action_deps.keys():
                        if action_dep not in action_data_index.keys():
                            action_dep_version = action_deps[action_dep]
                            if (dep_action_info := self.get_action_info(action_dep, action_dep_version, jpr_api_key)):
                                loaded_action_deps[action_dep] = {'action': action_dep, 'context': {'version': action_dep_version, 'enabled': True, 'agent_id': agent_id, '_package': dep_action_info, 'label': dep_action_info.get('architype', None), 'description': dep_action_info.get('meta', {}).get('description', '')}}
                            else:
                                self.logger.error(f'unable to find action {action_dep}={action_dep_version}')
                                continue
                    action_data_index.update(loaded_action_deps)
                    action_data_index[namespace_package_name] = action_data
                elif namespace_package_name in action_data_index:
                    del action_data_index[namespace_package_name]
                    self.logger.error(f'unable to find action {namespace_package_name}={package_version}')
                    continue
        except ImportError as e:
            self.logger.error(f'an exception occurred wile loading action, {traceback.format_exc()}')
        subprocess.check_call(JacList([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip', '--root-user-action=ignore']))
        action_data_index_copy = action_data_index.copy()
        for namespace_package_name, action_data in action_data_index_copy.items():
            package_path = action_data.get('context', {}).get('_package', {}).get('config', {}).get('path', None)
            if package_path is None:
                package_version = action_data.get('context', {}).get('version', None)
                self.logger.info(f'attempting to download action for {namespace_package_name}={package_version}')
                try:
                    package_data = RegistryAPI.download_package(namespace_package_name, package_version, api_key=jpr_api_key)
                    if not package_data:
                        if namespace_package_name in action_data_index:
                            del action_data_index[namespace_package_name]
                        self.logger.error(f'unable to download package {namespace_package_name}={package_version} ...skipping')
                        continue
                    package_file = requests.get(package_data['file'])
                    target_dir = os.path.join(self.package_root, namespace_package_name)
                    os.makedirs(target_dir, exist_ok=True)
                    with tarfile.open(fileobj=io.BytesIO(package_file.content), mode='r:gz') as tar_file:
                        tar_file.extractall(target_dir)
                    if (action_info := self.get_action_info(namespace_package_name, package_version, jpr_api_key)):
                        action_data['context']['_package'] = action_info
                        if not action_info.get('config', {}).get('path', None):
                            if namespace_package_name in action_data_index:
                                del action_data_index[namespace_package_name]
                            self.logger.error(f'unable to download package {namespace_package_name}...skipping')
                            continue
                except Exception as e:
                    if namespace_package_name in action_data_index:
                        del action_data_index[namespace_package_name]
                    self.logger.error(f'unable to download and load package {namespace_package_name}...skipping, {e}')
                    continue
            if self.load_pip_packages(action_data):
                self.import_action(action_data)
            elif namespace_package_name in action_data_index:
                del action_data_index[namespace_package_name]
                self.logger.error(f'unable to load pip packages for action {namespace_package_name}')
                continue

        def update_child_actions(child_action_list):
            for i, child_action_data in enumerate(child_action_list):
                action_type = child_action_data.get('context', {}).get('_package', {}).get('meta', {}).get('type', 'action')
                if (namespace_package_name := child_action_data.get('action', None)):
                    if namespace_package_name in action_data_index:
                        child_action_list[i] = action_data_index[namespace_package_name]
                        del action_data_index[namespace_package_name]
                    if 'children' in child_action_data and action_type == 'interact_action':
                        update_child_actions(child_action_data['children'])
        action_data_index_copy = action_data_index.copy()
        for namespace_package_name, action_data in action_data_index_copy.items():
            action_type = action_data.get('context', {}).get('_package', {}).get('meta', {}).get('type', 'action')
            if 'children' in action_data and action_type == 'interact_action':
                update_child_actions(action_data['children'])
        return Utils.order_interact_actions(action_data_index.values())

    def register_action(self, action_data: dict, parent: str='') -> Action:
        action_node = None
        if not action_data:
            self.logger.error(f'unable to register action {label}, missing or invalid action data')
            return None
        label = action_data.get('context', {}).get('label', action_data.get('action', None))
        architype = action_data.get('context', {}).get('_package', {}).get('architype', None)
        module = action_data.get('context', {}).get('_package', {}).get('config', {}).get('module', None)
        singleton = action_data.get('context', {}).get('_package', {}).get('config', {}).get('singleton', False)
        action_type = action_data.get('context', {}).get('_package', {}).get('meta', {}).get('type', 'action')
        if not architype or not module or (not label):
            self.logger.error(f'unable to register action {label}, missing label, architype or module name')
            return None
        try:
            if singleton:
                if (existing_action := self.get(action_type=label)):
                    self.logger.error(f'action already exists: {label}')
                    return None
            elif (existing_action := self.get(action_label=label)):
                self.logger.error(f'action already exists: {existing_action.label}')
                return None
            self.logger.info(f'Registering action {label} with architype {architype} from module {module}')
            action_node = AgentInterface.spawn_node(node_name=architype, attributes=action_data.get('context', {}), module_name=module)
            if action_node:
                if not parent:
                    action_parent_node = self
                else:
                    action_parent_node = self.get_by_type(action_type=parent)
                action_parent_node.connect(action_node)
                action_node.on_register()
                self.logger.info(f'registered action: {action_node.label}')
            if 'children' in action_data and action_type == 'interact_action':
                for child_data in action_data['children']:
                    self.register_action(action_data=child_data, parent=architype)
        except Exception as e:
            self.logger.error(f'an exception occurred wile registering action {label}, {traceback.format_exc()}')

    def install_actions(self, agent_id: str, data: dict) -> None:
        agent_node = jobj(id=agent_id)
        loaded_actions_data = self.load_action_packages(agent_id, data, jpr_api_key=agent_node.jpr_api_key)
        if not loaded_actions_data:
            self.logger.error('no actions loaded; unable to proceed with actions install')
            return None
        self.deregister_actions()
        for action_data in loaded_actions_data:
            self.register_action(action_data=action_data)
        self.connect(ExitInteractAction())
        for action_node in self.get_all():
            action_node.post_register()

    def deregister_action(self, action_type: str='', action_label: str='') -> None:
        target = JacList([])
        if action_type and (not action_label):
            target = self.get_by_type(action_type)
        elif action_label and (not action_type):
            target.append(self.get_by_label(action_label))
        for action_node in target:
            action_node.on_deregister()
            Jac.destroy(action_node)

    def deregister_actions(self) -> None:
        for action_node in self.get_all():
            action_node.on_deregister()
            Jac.destroy(action_node)

    def queue_interact_actions(self, actions: list) -> list:
        return sorted(actions, key=lambda action: InteractAction: action.weight)

class _get_actions(Walker):
    action_nodes: list = field(gen=lambda: JacList([]))
    filter_enabled: bool = field(False)

    class __specs__(Obj):
        private: static[bool] = True

    @with_entry
    def on_actions(self, here: Actions) -> None:
        if self.filter_enabled:
            self.visit(here.refs().filter(Action, None).filter(None, lambda item: item.enabled == True))
        else:
            self.visit(here.refs().filter(Action, None))

    @with_entry
    def on_action(self, here: Action) -> None:
        self.action_nodes.append(here)
        self.visit(here.refs().filter(Action, None))

class _get_interact_actions(Walker):
    action_nodes: list = field(gen=lambda: JacList([]))
    filter_enabled: bool = field(False)

    class __specs__(Obj):
        private: static[bool] = True

    @with_entry
    def on_actions(self, here: Actions) -> None:
        if self.filter_enabled:
            self.visit(here.refs().filter(InteractAction, None).filter(None, lambda item: item.enabled == True))
        else:
            self.visit(here.refs().filter(InteractAction, None))

    @with_entry
    def on_action(self, here: InteractAction) -> None:
        self.action_nodes.append(here)
        self.visit(here.refs().filter(InteractAction, None))