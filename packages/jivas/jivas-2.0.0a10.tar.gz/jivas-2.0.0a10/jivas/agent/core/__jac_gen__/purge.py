from __future__ import annotations
from jaclang import *
import typing
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
    from graph_node import GraphNode
else:
    GraphNode, = jac_import('graph_node', items={'GraphNode': None})

class purge(Walker):
    logger: static[Logger] = logging.getLogger(__name__)

    @with_entry
    def delete(self, here: GraphNode) -> None:
        self.logger.info(f'deleting node: {here}')
        self.visit(here.refs())
        Jac.destroy(here)