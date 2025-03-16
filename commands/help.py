# Created by Sean L. on Mar 16
# 
# emb2emb client
# help.py
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
def help(flags: Dict[FlagNameConfig, List[str]]):
    """Gives help on TUI interface
    Arguments:
        flags (Dict[FlagNameConfig, List[str]]): Arguments
    """
    flags = flagconfiglist2dic(flags)
    
    if len(flags) == 0:
        raise MissingFlagError('help command requires flags.')
    else:
        if len(flags) == 1:
            if 'help' in flags:
                ClientConsole.help('help')
            if 'name' in flags:
                for command in flags['name']:
                    ClientConsole.help(command.long)
        else:
            raise ExcessiveFlagsError(f'help command requires 1 flag, got {len(flags)}')
    
    ClientConsole.warn('FEATURE UNDER DEVELOPMENT')