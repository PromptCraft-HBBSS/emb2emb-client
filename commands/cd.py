# Created by Sean L. on Mar 16
# 
# emb2emb client
# cd.py
# 
# PromptCraft, 2025. All rights reserved.

from models.command_model import Command
from typing import Dict, List
from utils.output import ClientConsole
from models.dbmanip import fetch_manager
from models.config_model import *
from utils.exceptions import *
from models.memglobalstore_model import global_manager
from utils.performance import PerformanceMetrics

# MARK: COMMANDS:
@PerformanceMetrics.runtime_monitor
@Command.register('cd')
def cd(flags: Dict[FlagNameConfig, List[str]]):
    """Changes tablename pointer
    Arguments:
        flags (Dict[FlagNameConfig, List[str]]): Arguments
    """
    flags = flagconfiglist2dic(flags);
    if len(flags) != 0:
        if 'help' in flags:
            ClientConsole.help('cd')
            return
        elif 'ROOT' in flags:
            ...
        else:
            raise ExcessiveFlagsError(f"cd command does not require flags.")

    if len(flags['ROOT']) == 1:
        global_manager.set('tablename', flags['ROOT'][0])
    else:
        raise ExcessiveArgsError(f"--ROOT accepts 1 arg, got {len(flags['ROOT'])}")
    
    return
