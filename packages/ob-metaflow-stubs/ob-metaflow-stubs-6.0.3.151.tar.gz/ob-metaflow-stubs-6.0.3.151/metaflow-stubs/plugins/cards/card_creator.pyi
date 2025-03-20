######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.6.1+obcheckpoint(0.1.9);ob(v1)                                                    #
# Generated on 2025-03-17T20:51:51.725928                                                            #
######################################################################################################

from __future__ import annotations


from ...metaflow_current import current as current

ASYNC_TIMEOUT: int

class CardProcessManager(object, metaclass=type):
    """
    This class is responsible for managing the card creation processes.
    """
    ...

class CardCreator(object, metaclass=type):
    def __init__(self, top_level_options):
        ...
    def create(self, card_uuid = None, user_set_card_id = None, runtime_card = False, decorator_attributes = None, card_options = None, logger = None, mode = 'render', final = False, sync = False):
        ...
    ...

