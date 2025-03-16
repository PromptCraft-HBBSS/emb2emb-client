# Created by Sean L. on Mar 16
# 
# emb2emb client
# fetch.py
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
@Command.register('fetch')
def fetch(flags: Dict[FlagNameConfig, List[str]]):
    """Fetches current embedded converses.
    Arguments:
        flags (Dict[FlagNameConfig, List[str]]): Arguments
    """
    flags = flagconfiglist2dic(flags);
    if len(flags) == 0:
        raise MissingFlagError(f"ls command requires flags.")

    if 'help' in flags.keys():
        ClientConsole.help('ls')
        return

    if 'all' in flags.keys():
        if len(flags['all']) > 0:  # Check for 
            raise ExcessiveArgsError(f"--all flag doesn't accept args, got {len(flags['all'])}")
        elif 'limit' in flags.keys():  # Check for other flags
            raise ExcessiveFlagsError("--all must be used independent of limit")

    elif 'limit' in flags.keys():
        if len(flags['limit']) == 0:  # Missing required argument
            raise MissingArgError("--limit requires a numeric arg, got none")
        elif len(flags['limit']) > 1:  # Multiple arguments
            raise ExcessiveArgsError(f"--limit accepts 1 arg, got {len(flags['limit'])}")

    maxl = None
    
    if 'max-length' in flags.keys():
        if len(flags['max-length']) == 0:  # Missing required argument
            raise MissingArgError("--max-length requires a numeric arg, got none")
        elif len(flags['max-length']) > 1:  # Missing required argument
            raise ExcessiveArgsError(f"--max-length requires a numeric arg, got {len(flags['max-length'])}")
        else:
            try:
                maxl = int(flags['max-length'][0])
            except ValueError as e:
                raise ArgumentValueError(f'--max-length required arg of type int, got str ({maxl})')
            
    desc = 'desc' in flags.keys()
    old = 'old' in flags.keys()

    if 'all' in flags:
        limit = None
    elif 'limit' in flags:
        limit = flags['limit'][0]
    else:
        raise MissingFlagError("fetch requires either a flag --all or --limit")
    
    # Get stored conversations
    table = global_manager.get('tablename')
    table = fetch_manager.fetch(
        table,
        None if 'all' in flags else flags['limit'][0],
        old,
        not desc
    )

    ClientConsole.log(f'Total of {len(table.conversations)} entries fetched.')
    if len(table.conversations) == 0:
        ClientConsole.warn('No conversations found.')
        return
    for converse in table.conversations:
        ClientConsole.print(
f"""
[#004499]({converse.id}) [{converse.timestamp}][/#004499] 
[bold]PROMPT[/bold] {converse.prompt}
[bold]PROMPT[/bold] {converse.answer}""")
    return
