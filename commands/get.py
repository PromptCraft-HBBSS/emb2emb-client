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

@Command.register('get')
def get_env(flags: Dict[FlagNameConfig, List[str]]):
    flags = flagconfiglist2dic(flags)
    
    if not 'key' in flags.keys():
        raise MissingFlagError('set command requires flag --key.')
    if len(flags['key']) == 0:
        raise MissingArgError(f'--key requires 1 str value, got {len(flags['key'])}')
    if len(flags['key']) > 1:
        raise ExcessiveArgsError(f'--key requires 1 str value, got {len(flags['key'])}')
    
    ClientConsole.print(
f'''[bold]KEY[/bold] {flags['key'][0]}
[bold]VALUE[/bold] {global_manager.get(flags['key'][0])}''')