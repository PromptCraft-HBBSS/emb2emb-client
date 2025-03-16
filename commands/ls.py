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
from re import match
from utils.performance import PerformanceMetrics

@PerformanceMetrics.runtime_monitor
@Command.register('ls')
def ls(flags: Dict[FlagNameConfig, List[str]]):
    """Lists all datatables
    Arguments:
        flags (Dict[FlagNameConfig, List[str]]): Arguments
    """
    flags = flagconfiglist2dic(flags)
    query = '.+'
    useQ = False
    if len(flags) != 0:
        if 'help' in flags.keys():
            ClientConsole.help('ls');
            return
        if 'query' in flags.keys():
            query = flags['query'][0]
        if len(flags['ROOT']) == 0:
            tables = list(filter(lambda x: not match(query, x.name) is None, fetch_manager.tables()))
            if len(tables) == 0:
                ClientConsole.warn('No tables found.')
                if useQ:
                    if len(fetch_manager.tables()) != 0:
                        ClientConsole.warn(f'No tables matches regex query ({query}).')
                    else:
                        ClientConsole.warn('No tables exist')
                else:
                    ClientConsole.warn('No tables exist')
            tables_count = 0 # Counter for counting how many tables found.
            for table in tables:
                ClientConsole.print(
f"""
 {'*' if global_manager.get('tablename') == table.name else ' '} [#004499]({table.name})[/#004499] - {len(table.conversations)} Entries, last updated @ {
    max(conv.timestamp for conv in table.conversations if conv.timestamp is not None).strftime('%Y-%m-%d %H:%M') 
    if any(conv.timestamp is not None for conv in table.conversations) 
    else 'Never'
}
""")
        else:
            raise ExcessiveFlagsError(f'ls command expects --help or --query flags, got {' '.join(key for key in flags.keys() if key != 'ROOT')}')
        