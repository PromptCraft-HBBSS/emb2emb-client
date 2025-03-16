# Created by Sean L. on Mar 16
# 
# emb2emb client
# exceptions.py
# 
# PromptCraft, 2025. All rights reserved.

# MARK: Command REPL Exceptions

class CommandNotFoundError(Exception):
    """Exception raised when a cmd is not found.
    
    Usage: <cmd> is not a valid command.
    """
    ...

class ExcessiveArgsError(Exception):
    """Exception raised when more then required args are given
    
    Usage: 
        --<long-flag> accepts <valid> arg(s), got <actual>
        --<long-flag> accepts no args, got <actual>
    """
    ...

class MissingArgError(Exception):
    """Exception raised when less then required args are given
    
    Usage: 
        --<long-flag> requires <valid-count> <type> value, got <actual>
    """
    ...
    
class ExcessiveFlagsError(Exception):
    """Exception raised when more then required flags are stacked
    
    Usage:
        <cmd> command requires <valid-count> flags, got <actual>
        --<long-flag> must be with only *--<other-flags>
        --<long-flag> must be used alone
    """
    
    ...

class MissingFlagError(Exception):
    """Exception raised when less then required flags are stacked
    
    Usage:
        --<long-flag> must be with *--<other-flags>
        <cmd> command requires flags.
    """
    ...
    
# MARK: Database Manip Exceptions

class TableExistsError(Exception):
    """Exception raised when a datatable with destined name already exists
    
    Usage: Table <tablename> already exists.
    """
    ...

# MARK: Other Exceptions

class ProgramTermination(Exception):
    """Exception raised for program termination signal
    
    Usage: EXIT
    """
    ...