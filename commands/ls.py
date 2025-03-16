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

@Command.register('ls')
def ls(flags: Dict[FlagNameConfig, List[str]]):
    """Lists all datatables
    Arguments:
        flags (Dict[FlagNameConfig, List[str]]): Arguments
    """
    flags = flagconfiglist2dic(flags)
    
    if len(flags) != 0:
        if 'help' in flags.keys():
            ClientConsole.help('ls');
            return
        if 'query' in flags.keys():
            ClientConsole.warn('FEATURE IN DEV')
        if len(flags['ROOT']) == 0:
            for table in fetch_manager.tables():
                ClientConsole.print(table)
            ClientConsole.warn('FEATURE IN DEV - ls -a')
        else:
            raise ExcessiveFlagsError(f'ls command expects --help or --query flags, got {' '.join(key for key in flags.keys() if key != 'ROOT')}')
        