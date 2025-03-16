# Created by Sean L. on Mar 16
# 
# emb2emb client
# set.py
# 
# PromptCraft, 2025. All rights reserved.

from models.command_model import Command
from typing import Dict, List
from utils.output import ClientConsole
from models.dbmanip import fetch_manager
from models.config_model import *
from utils.exceptions import *
from models.memglobalstore_model import global_manager

@Command.register('set')
def set_env(flags: Dict[FlagNameConfig, List[str]]):
    flags = flagconfiglist2dic(flags)
    
    if not 'key' in flags.keys():
        raise MissingFlagError('set command requires flag --key.')
    if not 'value' in flags.keys():
        raise MissingFlagError('set command requires flag --value.')
    if len(flags['key']) == 0:
        raise MissingArgError(f'--key requires 1 str value, got {len(flags['key'])}')
    if len(flags['value']) == 0:
        raise MissingArgError(f'--value requires 1 str value, got {len(flags['value'])}')
    if len(flags['key']) > 1:
        raise ExcessiveArgsError(f'--key requires 1 str value, got {len(flags['key'])}')
    if len(flags['value']) > 1:
        raise ExcessiveArgsError(f'--value requires 1 str value, got {len(flags['value'])}')
    
    global_manager.set(flags['key'][0], flags['value'][0])
    ClientConsole.done(f'Set key {flags['key'][0]} to {flags['value'][0]}.')