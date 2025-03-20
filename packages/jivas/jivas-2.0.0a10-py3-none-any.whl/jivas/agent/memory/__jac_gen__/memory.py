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
    from jivas.agent.core.graph_node import GraphNode
else:
    GraphNode, = jac_import('jivas.agent.core.graph_node', items={'GraphNode': None})
if typing.TYPE_CHECKING:
    from frame import Frame
else:
    Frame, = jac_import('frame', items={'Frame': None})
if typing.TYPE_CHECKING:
    from retrace import Retrace
else:
    Retrace, = jac_import('retrace', items={'Retrace': None})
if typing.TYPE_CHECKING:
    from tail import Tail
else:
    Tail, = jac_import('tail', items={'Tail': None})
if typing.TYPE_CHECKING:
    from interaction import Interaction
else:
    Interaction, = jac_import('interaction', items={'Interaction': None})
if typing.TYPE_CHECKING:
    import dotenv
else:
    dotenv, = jac_import('dotenv', 'py')
if typing.TYPE_CHECKING:
    import os
else:
    os, = jac_import('os', 'py')
if typing.TYPE_CHECKING:
    import json
else:
    json, = jac_import('json', 'py')
if typing.TYPE_CHECKING:
    import uuid
else:
    uuid, = jac_import('uuid', 'py')
if typing.TYPE_CHECKING:
    import yaml
else:
    yaml, = jac_import('yaml', 'py')

class Memory(GraphNode, Node):
    logger: static[Logger] = logging.getLogger(__name__)

    def get_frame(self, agent_id: str, session_id: str, force_session: bool=False, lookup: bool=False) -> Frame:
        frame_node = Utils.node_obj(self.refs().filter(Frame, None).filter(None, lambda item: item.session_id == session_id))
        if not frame_node and (not lookup):
            if force_session:
                frame_node = Frame(agent_id=agent_id, session_id=session_id)
            else:
                frame_node = Frame(agent_id=agent_id)
            self.connect(frame_node)
        return frame_node

    def get_frames(self) -> list[Frame]:
        return self.refs().filter(Frame, None)

    def import_memory(self, data: dict, overwrite: bool=True) -> None:
        if not data or not isinstance(data, dict):
            return False
        if overwrite:
            self.purge()
        agent_node = self.get_agent()
        try:
            for frame_data in data.get('memory'):
                if (session_id := frame_data.get('frame', {}).get('context', {}).get('session_id', None)):
                    frame_node = self.get_frame(agent_id=agent_node.id, session_id=session_id, force_session=True)
                    frame_node.update(frame_data.get('frame', {}).get('context', {}))
                    for interaction_data in frame_data.get('frame', {}).get('interactions', JacList([])):
                        last_interaction_node = frame_node.get_last_interaction()
                        interaction_node = Interaction(agent_id=agent_node.id)
                        if not interaction_data.get('interaction', {}).get('context', {}).get('response', {}).get('session_id'):
                            interaction_data['interaction']['context']['response']['session_id'] = frame_node.session_id
                        interaction_node.update(interaction_data.get('interaction', {}).get('context', {}))
                        frame_node.insert_interaction(interaction_node, last_interaction_node)
                    self.logger.info(f'uploaded memory of: {frame_node.session_id}')
                else:
                    self.logger.error('invalid session ID on frame, skipping...')
            return True
        except Exception as e:
            self.logger.warning(f'uploaded memory failed: {e}')
        return False

    def export_memory(self, agent_id: str, session_id: str, json: bool, save_to_file: bool) -> None:
        return self.spawn(_export_memory(agent_id=agent_id, session_id=session_id, json=json, save_to_file=save_to_file)).frame_data

    def memory_healthcheck(self, agent_id: str, session_id: str='', verbose: bool=False) -> None:
        total_users = 0
        total_interactions = 0
        total_users = len(self.get_frames())
        for user in self.get_frames():
            total_interactions += len(user.get_interactions())
        return {'total_users': total_users, 'total_interactions': total_interactions}

    def purge(self, session_id: str=None) -> None:
        return self.spawn(_purge(session_id)).removed

    def refresh(self, session_id: str) -> None:
        if (frame_node := self.get_frame(None, session_id=session_id)):
            frame_node.refresh_interactions()
            return True
        return False

    def get_agent(self) -> None:
        return Utils.node_obj(self.refs(dir=EdgeDir.IN))

class _purge(Walker):
    session_id: str = field('')
    removed: list = field(gen=lambda: JacList([]))

    class __specs__(Obj):
        private: static[bool] = True

    @with_entry
    def on_memory(self, here: Memory) -> None:
        if self.session_id:
            self.visit(here.refs().filter(Frame, None).filter(None, lambda item: item.session_id == self.session_id))
        else:
            self.visit(here.refs().filter(Frame, None))

    @with_entry
    def on_frame(self, here: Frame) -> None:
        if not self.visit(here.refs(Tail)):
            self.removed.append(here)
            Jac.destroy(here)

    @with_entry
    def on_interaction(self, here: Interaction) -> None:
        self.visit(here.refs(Retrace))
        self.removed.append(here)
        Jac.destroy(here)

class _export_memory(Walker):
    logger: static[Logger] = logging.getLogger(__name__)
    status: int = field(200)
    response: str = field('')
    session_id: str = field('')
    agent_id: str = field('')
    frame_data: dict = field(gen=lambda: {})
    file_url: str = field('')
    file_path: str = field('')
    json: bool = field(gen=lambda: false)
    save_to_file: bool = field(gen=lambda: false)

    class __specs__(Obj):
        private: static[bool] = True

    @with_entry
    def on_memory(self, here: Memory) -> None:
        self.frame_data = {'memory': JacList([])}
        if self.session_id:
            self.visit(here.refs().filter(Frame, None).filter(None, lambda item: item.session_id == self.session_id))
        else:
            self.visit(here.refs().filter(Frame, None))

    @with_entry
    def on_frame(self, here: Frame) -> None:
        interactions = here.get_interactions()
        interaction_nodes = JacList([])
        for interaction_node in interactions:
            interaction_nodes.append({'interaction': {'context': interaction_node.export()}})
        self.frame_data['memory'].append({'frame': {'context': here.export(), 'interactions': interaction_nodes}})

    @with_exit
    def export_memory(self, here) -> None:
        dotenv.load_dotenv()
        if None:
            self.file_path = f"{os.getenv('JIVAS_FILES_ROOT_PATH')}/{str(uuid.uuid4())}"
            if not self.json:
                self.file_path = f'{self.file_path}.yaml'
                Utils.dump_yaml_file(self.file_path, self.frame_data)
            else:
                self.file_path = f'{self.file_path}.json'
                with open(self.file_path, 'w') as outfile:
                    json.dump(self.frame_data, outfile, indent=4)