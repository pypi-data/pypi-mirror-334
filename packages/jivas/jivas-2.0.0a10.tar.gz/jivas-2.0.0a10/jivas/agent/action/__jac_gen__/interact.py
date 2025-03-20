from __future__ import annotations
from jaclang import *
import typing
from enum import Enum, auto
if typing.TYPE_CHECKING:
    import os
else:
    os, = jac_import('os', 'py')
if typing.TYPE_CHECKING:
    import pytz
else:
    pytz, = jac_import('pytz', 'py')
if typing.TYPE_CHECKING:
    import json
else:
    json, = jac_import('json', 'py')
if typing.TYPE_CHECKING:
    import logging
else:
    logging, = jac_import('logging', 'py')
if typing.TYPE_CHECKING:
    import traceback
else:
    traceback, = jac_import('traceback', 'py')
if typing.TYPE_CHECKING:
    from typing import Optional
else:
    Optional, = jac_import('typing', 'py', items={'Optional': None})
if typing.TYPE_CHECKING:
    from logging import Logger
else:
    Logger, = jac_import('logging', 'py', items={'Logger': None})
if typing.TYPE_CHECKING:
    from jivas.agent.modules.agentlib.utils import Utils
else:
    Utils, = jac_import('jivas.agent.modules.agentlib.utils', 'py', items={'Utils': None})
if typing.TYPE_CHECKING:
    from datetime import datetime, timezone, timedelta
else:
    datetime, timezone, timedelta = jac_import('datetime', 'py', items={'datetime': None, 'timezone': None, 'timedelta': None})
if typing.TYPE_CHECKING:
    from jivas.agent.action.actions import Actions
else:
    Actions, = jac_import('jivas.agent.action.actions', items={'Actions': None})
if typing.TYPE_CHECKING:
    from interact_action import InteractAction
else:
    InteractAction, = jac_import('interact_action', items={'InteractAction': None})
if typing.TYPE_CHECKING:
    from exit_interact_action import ExitInteractAction
else:
    ExitInteractAction, = jac_import('exit_interact_action', items={'ExitInteractAction': None})
if typing.TYPE_CHECKING:
    from jivas.agent.memory.memory import Memory
else:
    Memory, = jac_import('jivas.agent.memory.memory', items={'Memory': None})
if typing.TYPE_CHECKING:
    from jivas.agent.memory.frame import Frame
else:
    Frame, = jac_import('jivas.agent.memory.frame', items={'Frame': None})
if typing.TYPE_CHECKING:
    from jivas.agent.memory.interaction import Interaction
else:
    Interaction, = jac_import('jivas.agent.memory.interaction', items={'Interaction': None})
if typing.TYPE_CHECKING:
    from jivas.agent.memory.interaction_response import InteractionResponse, InteractionMessage, SilentInteractionMessage
else:
    InteractionResponse, InteractionMessage, SilentInteractionMessage = jac_import('jivas.agent.memory.interaction_response', items={'InteractionResponse': None, 'InteractionMessage': None, 'SilentInteractionMessage': None})
if typing.TYPE_CHECKING:
    from jivas.agent.core.agent import Agent
else:
    Agent, = jac_import('jivas.agent.core.agent', items={'Agent': None})
if typing.TYPE_CHECKING:
    from jivas.agent.core.agents import Agents
else:
    Agents, = jac_import('jivas.agent.core.agents', items={'Agents': None})
if typing.TYPE_CHECKING:
    from jivas.agent.core.app import App
else:
    App, = jac_import('jivas.agent.core.app', items={'App': None})
if typing.TYPE_CHECKING:
    from jivas.agent.action import interact_graph_walker
else:
    interact_graph_walker, = jac_import('jivas.agent.action', items={'interact_graph_walker': None})
if typing.TYPE_CHECKING:
    from jac_cloud.core.architype import NodeAnchor
else:
    NodeAnchor, = jac_import('jac_cloud.core.architype', 'py', items={'NodeAnchor': None})
if typing.TYPE_CHECKING:
    import json
else:
    json, = jac_import('json', 'py')

class interact(interact_graph_walker, Walker):
    logger: static[Logger] = logging.getLogger(__name__)
    agent_id: str = field('')
    session_id: str = field('')
    utterance: str = field('')
    channel: str = field('default')
    data: dict = field(gen=lambda: {})
    verbose: bool = field(False)
    tts: bool = field(False)
    response: dict = field(gen=lambda: {})
    message: InteractionMessage = field(None)
    execute: bool = field(False)
    context_data: dict = field(gen=lambda: {})
    frame_node: Frame = field(None)
    interaction_node: Interaction = field(None)
    last_interaction_node: InteractAction = field(None)
    agent_node: Agent = field(None)

    class __specs__(Obj):
        auth: static[bool] = True
        private: static[bool] = True
        excluded: static[list] = JacList(['response', 'execute', 'context_data', 'frame_node', 'interaction_node', 'last_interaction_node', 'agent_node'])

    @with_entry
    def on_root(self, here: Root) -> None:
        if self.init_interaction():
            self.visit(self.agent_node)
        else:
            return self.disengage()

    @with_entry
    def on_agent(self, here: Agent) -> None:
        self.visit(here.refs().filter(Actions, None))

    @with_entry
    def on_actions(self, here: Actions) -> None:
        if (resume_action_node := self.frame_node.get_resume_action(self.last_interaction_node)):
            root_action_node = resume_action_node.get_root_action()
            self.interaction_node.add_intent(root_action_node.label)
            self.visit(here.queue_interact_actions(here.refs().filter(InteractAction, None).filter(None, lambda item: item.enabled == True)))
            if self.subqueue_interact_action(resume_action_node, root_action_node):
                self.interaction_node.context_data['resumed'] = True
        else:
            queued_actions = here.queue_interact_actions(here.refs().filter(InteractAction, None).filter(None, lambda item: item.enabled == True))
            self.visit(queued_actions)
        self.logger.debug(f'Utterance: {self.utterance}')

    @with_entry
    def on_action(self, here: InteractAction) -> None:
        result = {}
        intended = self.is_intended(here)
        has_access = self.has_access(here)
        has_function = self.has_function(here)
        if intended:
            if has_access:
                self.logger.debug(f'Touching: {here.label}')
                self.execute = here.touch(visitor=self)
                if self.execute:
                    self.logger.debug(f'Executing: {here.label}')
                    if (result := here.execute(visitor=self)):
                        self.update(result)
                    self.interaction_node.trail.append(here.label)
                    self.execute = False
                self.update(result)
            else:
                here.deny(visitor=self)

    @with_exit
    def on_exit(self, here) -> None:
        self.respond()

    def init_interaction(self) -> bool:
        try:
            self.agent_node = jobj(id=self.agent_id)
            if not self.agent_node:
                return False
        except Exception as e:
            Jac.get_context().status = 400
            self.logger.error('invalid agent id')
            return False
        message_limit = self.agent_node.message_limit
        flood_block_time = self.agent_node.flood_block_time
        window_time = self.agent_node.window_time
        flood_threshold = self.agent_node.flood_threshold
        self.frame_node = self.agent_node.get_memory().get_frame(agent_id=self.agent_node.id, session_id=self.session_id)
        if not self.frame_node:
            Jac.get_context().status = 500
            self.logger.error('unable to initiate a frame')
            return False
        chunks = Utils.chunk_long_message(message=self.utterance, max_length=message_limit, chunk_length=message_limit)
        if len(chunks) > 1:
            Jac.get_context().status = 400
            self.logger.warning('unable to process message; message length exceeds limit')
            return False
        utc = pytz.UTC
        now = datetime.now(timezone.utc)
        flood = self.frame_node.variable_get(key='flood')
        if flood:
            if utc.localize(flood['expiration']) > now:
                Jac.get_context().status = 429
                self.logger.warning('flood control active')
                return False
        message_window = self.frame_node.variable_get(key='message_window')
        if message_window:
            keys = JacList(['start', 'end'])
            message_window = {key: utc.localize(value) if isinstance(value, datetime) else datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f') for key, value in message_window.items() if key in keys}
            if message_window.get('end', 0) <= now:
                message_window['start'] = now
                message_window['end'] = now + timedelta(seconds=window_time)
                message_window['count'] = 0
            else:
                message_window['count'] = message_window.get('count', 0) + 1
            if message_window.get('count', 0) > flood_threshold:
                flood = {'expiration': now + timedelta(seconds=flood_block_time)}
                self.frame_node.variable_set(key='flood', value=flood)
                Jac.get_context().status = 429
                self.logger.warning('flood control active')
                return False
        else:
            message_window = {'start': now, 'end': now + timedelta(seconds=window_time), 'count': 1}
            self.frame_node.variable_set(key='message_window', value=message_window)
        self.last_interaction_node = self.frame_node.get_last_interaction()
        self.interaction_node = self.frame_node.add_interaction(utterance=self.utterance, channel=self.channel)
        if not self.interaction_node:
            return False
        if self.data:
            required_fields = JacList(['label', 'data_type', 'content'])
            if all(JacList([field in self.data for field in required_fields])):
                if self.data['label'] and self.data['data_type'] and self.data['content']:
                    self.interaction_node.set_data_item(label=self.data['label'], meta={'type': self.data['data_type']}, content=self.data['content'])
                else:
                    Jac.get_context().status = 400
                    self.logger.error(f'malformed data payload; requires {required_fields} {values}')
            else:
                Jac.get_context().status = 400
                self.logger.error(f'malformed data payload; requires {required_fields} {values}')
        return True

    def set_next_action(self, action_label: str, action_node: Optional[InteractAction]=None) -> None:
        next_action_node = None
        if action_label:
            next_action_node = self.agent_node.get_actions().get(action_label=action_label)
        elif action_node:
            next_action_node = action_node
        if next_action_node:
            self.prepend_interact_action(next_action_node)

    def set_resume_action(self, action_label: str, action_node: Optional[InteractAction]=None) -> None:
        resume_action_label = None
        if action_label:
            resume_action_label = action_label
        elif action_node:
            resume_action_label = action_node.label
        if resume_action_label:
            self.frame_node.set_resume_action(action_label=resume_action_label)

    def append_action(self, action_label: str, action_node: Optional[InteractAction]=None) -> None:
        append_action_node = None
        if action_label:
            append_action_node = self.agent_node.get_actions().get(action_label=action_label)
        elif action_node:
            append_action_node = action_node
        if append_action_node:
            self.append_interact_action(append_action_node)

    def dequeue_action(self, action_label: str, action_node: Optional[InteractAction]=None) -> None:
        if action_label:
            action_node = self.agent_node.get_actions().get(action_label=action_label)
        if action_node:
            self.dequeue_interact_action(action_node)

    def append_interact_action(self, interact_action: InteractAction) -> None:
        if (exit_action := self.agent_node.get_actions().get(action_label='ExitInteractAction')):
            exit_action_node_ref = None
            for i, node_ref in enumerate(self.__jac__.next):
                if f'{node_ref.id}' == f'{exit_action.__jac__.id}':
                    exit_action_node_ref = self.__jac__.next[i]
                    self.__jac__.next.pop(i)
                    break
            self.dequeue_interact_action(interact_action)
            self.visit(interact_action)
            self.__jac__.next.append(exit_action_node_ref)
            return self.__jac__.next
        else:
            self.visit(interact_action)
        return None

    def dequeue_interact_action(self, interact_action: InteractAction) -> None:
        if self.__jac__.next and interact_action:
            for i, node_ref in enumerate(self.__jac__.next):
                if f'{node_ref.id}' == f'{interact_action.__jac__.id}':
                    self.__jac__.next.pop(i)
                    break
            return self.__jac__.next
        return None

    def prepend_interact_action(self, interact_action: InteractAction) -> None:
        if self.dequeue_interact_action(interact_action):
            path = self.__jac__.next
            self.__jac__.next = JacList([])
            self.visit(interact_action)
            self.__jac__.next.extend(path)
            return self.__jac__.next
        return None

    def subqueue_interact_action(self, interact_action: InteractAction, index_interact_action: InteractAction) -> None:
        if interact_action and index_interact_action:
            if (exit_action := self.agent_node.get_actions().get(action_label='ExitInteractAction')) and self.in_next_queue(index_interact_action):
                jac_next_copy = self.__jac__.next.copy()
                jac_trail = enumerate(jac_next_copy, start=0)
                for i, node_ref in jac_trail:
                    if f'{node_ref.id}' == f'{index_interact_action.__jac__.id}':
                        break
                    elif f'{node_ref.id}' != f'{exit_action.__jac__.id}':
                        self.__jac__.next.pop(0)
            if self.prepend_interact_action(interact_action):
                return self.__jac__.next
        return None

    def in_next_queue(self, action_node: InteractAction) -> bool:
        if action_node:
            for node_ref in self.__jac__.next:
                if f'{node_ref.id}' == f'{action_node.__jac__.id}':
                    return True
        return False

    def has_access(self, action_node: Action) -> bool:
        access = True
        if action_node.get_type() in JacList(['AccessControlAction', 'ExitInteractAction']):
            return True
        if (access_control_action_node := self.agent_node.get_actions().get(action_label='AccessControlAction')):
            access = access_control_action_node.has_action_access(session_id=self.frame_node.session_id, action_label=action_node.get_type(), channel=self.interaction_node.channel)
        return access

    def has_function(self, action_node: InteractAction) -> bool:
        if action_node.get_type() in JacList(['IntentInteractAction', 'FunctionInteractAction', 'ExitInteractAction']):
            return True
        if (function_interact_action_node := self.agent_node.get_actions().get(action_label='FunctionInteractAction')):
            if function_interact_action_node.enabled and function_interact_action_node.strict:
                if action_node.label not in self.interaction_node.get_intents() + function_interact_action_node.exceptions:
                    return False
        return True

    def is_intended(self, action_node: InteractAction) -> bool:
        if action_node.get_type() in JacList(['IntentInteractAction', 'FunctionInteractAction', 'ExitInteractAction']):
            return True
        if (intent_interact_action_node := self.agent_node.get_actions().get(action_label='IntentInteractAction')):
            if intent_interact_action_node.enabled and intent_interact_action_node.strict:
                if action_node.label not in self.interaction_node.get_intents() + intent_interact_action_node.exceptions:
                    return False
        return True

    def respond(self) -> None:
        if self.agent_node and self.interaction_node:
            interaction_data = {}
            has_response = self.interaction_node.has_response()
            if has_response:
                try:
                    self.message = self.interaction_node.get_message()
                    interaction_data = self.interaction_node.export()
                    if self.verbose:
                        interaction_data['frame'] = self.frame_node.export()
                        self.response = interaction_data
                    else:
                        self.response = {'response': self.interaction_node.get_response().export()}
                    if self.agent_node.is_logging():
                        self.log_interaction(data=interaction_data)
                except Exception as e:
                    self.logger.error(f'an exception occurred, {traceback.format_exc()}')
            if not has_response or not self.response:
                self.message = SilentInteractionMessage()
                self.response = InteractionResponse(session_id=self.frame_node.session_id, message=self.message.export()).export()
            self.frame_node.prune_interactions(frame_size=self.agent_node.frame_size)
        else:
            self.message = SilentInteractionMessage()
            self.response = InteractionResponse(message=self.message.export()).export()
        if self.tts:
            if (tts_action := self.agent_node.get_tts_action()):
                content = self.message.get_meta('phoneme_content') or self.message.get_content()
                audio = tts_action.invoke(text=content, as_url=True)
                if audio:
                    self.response['response'].update({'audio_url': audio})
        if self.reporting:
            Jac.report(self.response)

    def log_interaction(self, data: dict) -> None:
        collection = NodeAnchor.Collection.get_collection('interactions')
        collection.insert_one(json.loads(json.dumps(data)))