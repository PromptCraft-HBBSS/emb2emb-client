# Created by Sean L. on Mar 16
# 
# emb2emb client
# new.py
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
@Command.register('new')
def new(flags: Dict[FlagNameConfig, List[str]]):
    """Create a datatable.
    Arguments:
        flags (Dict[FlagNameConfig, List[str]]): Arguments
    """
    print(flags)
    flags = flagconfiglist2dic(flags);
    if len(flags) == 0:
        raise MissingFlagError(f"new command requires flags.")
    
    if 'help' in flags:
        ClientConsole.help('new')
        return

    ClientConsole.log('Creating table...')
    try:
        fetch_manager.create(flags['name'])
    except TableExistsError:
        ClientConsole.error(f'Table {flags['name']} already exists.')
        ClientConsole.warn(f'Use the command `cd {flags['name']}` to point datatable.')