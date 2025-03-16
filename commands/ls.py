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
@Command.register('ls')
def ls(flags: Dict[str, List[str]]):
    """Lists all embeddings
    Arguments:
        flags (Dict[str, List[str]]): Arguments
    """
    flags = flagconfiglist2dic(flags);

    if len(flags) == 0:
        raise MissingFlagError(f"ls command requires flags.")

    if 'help' in flags:
        ClientConsole.help('ls')
        return

    if 'all' in flags:
        if len(flags['all']) > 0:  # Check for unexpected arguments
            raise ExcessiveArgsError(f"--all flag doesn't accept args, got {len(flags['all'])}")
        elif len(flags) > 1:  # Check for other flags
            raise ExcessiveFlagsError("--all must be used alone")
    elif 'limit' in flags:
        if len(flags['limit']) == 0:  # Missing required argument
            raise MissingArgError("--limit requires a numeric arg, got none")
        elif len(flags['limit']) > 1:  # Multiple arguments
            raise ExcessiveArgsError(f"--limit accepts 1 arg, got {len(flags['limit'])}")

    desc = 'desc' in flags.keys()
    old = 'old' in flags.keys()

    # Get stored conversations
    table = global_manager.get('tablename')
    conversations = fetch_manager.ls(
        table,
        None if 'all' in flags else flags['limit'][0],
        old,
        not desc
    )

    ClientConsole.log(f'Total of {len(conversations)} entries fetched.')
    if len(conversations) == 0:
        ClientConsole.warn('No conversations found.')
        return

    for converse in conversations:
        ClientConsole.print(converse.id, converse.prompt, converse.answer)

    return
