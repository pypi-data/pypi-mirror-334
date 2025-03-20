######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.6.1+obcheckpoint(0.1.9);ob(v1)                                                    #
# Generated on 2025-03-17T20:51:51.708676                                                            #
######################################################################################################

from __future__ import annotations

import typing
import metaflow
if typing.TYPE_CHECKING:
    import metaflow
    import metaflow.exception

from ......exception import MetaflowException as MetaflowException
from .core import resolve_root as resolve_root

TYPE_CHECKING: bool

class UnresolvableDatastoreException(metaflow.exception.MetaflowException, metaclass=type):
    ...

def init_datastorage_object():
    ...

def resolve_storage_backend(pathspec: typing.Union[str, "metaflow.Task"] = None):
    ...

