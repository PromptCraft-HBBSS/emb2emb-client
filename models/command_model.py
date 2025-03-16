# Created by Sean L. on Mar 15
# 
# emb2emb client
# embed.py
# 
# PromptCraft, 2025. All rights reserved.

import shlex
from typing import Dict, List
from models.config_model import *

class Command:
    """Represents a parsed command with flags and arguments for REPL handling.
    
    Attributes:
        name (str): The base command name extracted from input
        flags (Dict[str, List[str]]): Dictionary mapping flag names to arguments,
            where keys are long-form flag names and values are argument lists
            
    Example:
        py3 >>> cmd = Command.parse('ls -a dir --verbose', {'a': 'all'})
        py3 >>> cmd.name
        'ls'
        py3 >>> cmd.flags
        {'all': ['dir'], 'verbose': []}
    """
        
    _method_registry = {}
    
    def __init__(self, name: str, flags: Dict[FlagNameConfig, List[str]]):
        """Initialize a Command instance with parsed components.
        
        Args:
            name: Base command string extracted from input
            flags: Processed flags dictionary containing:
                - Key: Flag name config instance (e.g., 'all' for '-a')
                - Value: List of arguments associated with the flag
        """
        self.name = name
        self.flags = flags

    @classmethod
    def parse(cls, cmd_str: str, flag_map: List[FlagNameConfig]):
        """Parse raw command string into structured Command object.
        
        Parsing Logic:
        1. Split command into tokens using whitespace
        2. Validate flags against mapping
        3. Group arguments under their corresponding flags

        Args:
            cmd_str (str): Raw command input string to parse
            flag_map (List[FlagNameConfig]): For each element
                - short (str): Single-character short flag (e.g., 'a')
                - long (str): Corresponding long flag name (e.g., 'all')

        Returns:
            Command: Structured representation of parsed command

        Raises:
            ValueError: For various parsing failures including:
                - Empty command input
                - Unrecognized long flags
                - Unmapped short flags
                - Arguments appearing before any flag

        Example:
            py3 >>> Command.parse('find -name *.txt', {'name': 'search'})
            Command(name='find', flags={'search': ['*.txt']})
            py3 >>> Command('find -name *.txt', {'name': 'search'})
            Command(name='find', flags={'search': ['*.txt']})
        """
        tokens = cmd_str.split()
        if not tokens:
            raise ValueError("Empty command")

        name = tokens[0]
        flags = {}
        current_flag = None
        
        for token in tokens[1:]:
            if token.startswith('--'):
                long_flag = token[2:]
                if long_flag not in [flag.long for flag in flag_map]:
                    raise ValueError(f"Unknown long flag: {token}")
                current_flag = long_flag
                flags[current_flag] = []
            elif token.startswith('-'):
                short_flag = token[1:]
                if short_flag not in [flag.short for flag in flag_map]:
                    raise ValueError(f"Unmapped short flag: {token}")
                current_flag = find_flag(flag_map, short_flag)
                flags[current_flag] = []
            else:
                if not current_flag:
                    raise ValueError(f"Argument before flags: {token}")
                flags[current_flag].append(token)
                
        return cls(name, flags)

    @classmethod
    def register(cls, command_name: str):
        """Decorator to register command execution methods [3,7](@ref)"""
        def decorator(func):
            cls._method_registry[command_name] = func
            return func
        return decorator

    def act(self):
        """Execute the registered command method with parsed flags"""
        if self.name not in self._method_registry:
            raise ValueError(f"No handler for command: {self.name}")
        
        return self._method_registry[self.name](self.flags)
        
    def obj(self):
        """Returns a lexical descriptive dictionary of the command.

        Returns:
            dict: A dictionary describing the Command object. Includes
                - cmd (str): The command name (eg. 'ask')
                - flags (List[str]): A list of long flags contained (eg. {'-n': ['a string here']})
        """
        return {'cmd': self.name, 'flags': self.flags}
    
