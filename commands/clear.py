# Created by Sean L. on Mar 16
# 
# emb2emb client
# clear.py
# 
# PromptCraft, 2025. All rights reserved.

from models.command_model import Command
from typing import Dict, List
from utils.output import ClientConsole
from models.dbmanip import fetch_manager
from models.config_model import *
from utils.exceptions import *
from models.memglobalstore_model import global_manager
from utils.systemcalls import clear

# MARK: COMMANDS:
@Command.register('clear')
def clear(flags: Dict[FlagNameConfig, List[str]]):
    """Clears TUI
    Arguments:
        flags (Dict[FlagNameConfig, List[str]]): Arguments
    """
    flags = flagconfiglist2dic(flags);
    if len(flags) != 0:
        if len(flags) == 1 and 'help' in flags.keys():
            ClientConsole.help('clear')
            return
        else:
            raise ExcessiveFlagsError(f'clear command requires no flags, got {[flag for flag in flags.keys()]}')
    else:
        clear()
        return