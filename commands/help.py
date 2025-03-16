# Created by Sean L. on Mar 16
# 
# emb2emb client
# ls.py
# 
# PromptCraft, 2025. All rights reserved.

from models.command_model import Command
from typing import Dict, List
from utils.output import ClientConsole
from models.dbmanip import fetch_manager
from models.config_model import *
from utils.exceptions import *
from models.memglobalstore_model import global_manager

# MARK: COMMANDS:
@Command.register('help')
def help(flags: Dict[str, List[FlagNameConfig]]):
    """Gives help on TUI interface
    Arguments:
        flags (Dict[str, List[str]]): Arguments
    """

    if len(flags) == 0:
        ...
    else:
        if len(flags) == 1:
            if flags[0] == 'help':
                ClientConsole.help('help')
            if flags[0] == 'name':
                for command in flags['name']:
                    ClientConsole.help(command.long)
        else:
            raise ExcessiveFlagsError('')
    
    ClientConsole.warn('FEATURE UNDER DEVELOPMENT')