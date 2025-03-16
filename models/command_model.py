# Created by Sean L. on Mar 15
# 
# emb2emb client
# embed.py
# 
# PromptCraft, 2025. All rights reserved.

import shlex
from typing import Dict, List, Tuple
from models.config_model import *
from utils.exceptions import ArgumentValueError

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
        """Parse command string into structured Command object with type conversion.

        Handles quoted arguments and automatic type conversion of unquoted values using
        the following logic:
        - Quoted values preserve exact string content
        - Unquoted values attempt conversion: bool → int → float → string fallback
        - Validates flag existence and argument positioning

        Arguments:
            cmd_str (str): Raw command input to parse (e.g. "cmd -f 'value'")
            flag_map (List[FlagNameConfig]): Supported flags configuration containing:
                - short (str): Single-character flag identifier
                - long (str): Full flag name

        Returns:
            Command: Structured representation with:
                - name: Base command identifier
                - flags: Dictionary mapping FlagNameConfig to parsed arguments

        Raises:
            ValueError: For empty commands or unrecognized flags
            ArgumentValueError: For type conversion failures or unclosed quotes

        Example:
            >>> flag_conf = [FlagNameConfig(short='p', long='param')]
            >>> cmd = Command.parse("test 'root arg' -p 'hello' 123 True", flag_conf)
            >>> cmd.flags
            {
                FlagNameConfig(short='p', long='param'): ['hello', 123, True],
                FlagNameConfig(short='', long='ROOT'): ['root arg']
            }

        Parsing Logic:
            1. Tokenize input with quote preservation using shlex
            2. Validate command structure and flag existence
            3. Convert arguments using type-aware parsing:
            - Quoted → raw string (strip surrounding quotes)
            - Unquoted → bool/int/float autoconversion
            4. Group arguments under their corresponding flags
        """
        try:
            tokens, quoted = cls._tokenize(cmd_str)
        except ValueError as e:
            raise ArgumentValueError(f"Open quote detected") from e

        if not tokens:
            raise ValueError("Empty command")

        name = tokens[0]
        flags = {FlagNameConfig('', 'ROOT'): []}
        current_flag = None

        for i in range(1, len(tokens)):
            token = tokens[i]
            is_quoted = quoted[i]

            # Flag detection logic remains unchanged
            if token.startswith('--'):
                long_flag = token[2:]
                if long_flag not in [flag.long for flag in flag_map]:
                    raise ValueError(f"Unknown long flag: {token}")
                current_flag = find_flag(flag_map, long_flag)
                flags[current_flag] = []
            elif token.startswith('-'):
                short_flag = token[1:]
                if short_flag not in [flag.short for flag in flag_map]:
                    raise ValueError(f"Unmapped short flag: {token}")
                current_flag = find_flag(flag_map, short_flag)
                flags[current_flag] = []
            else:
                try:
                    # Process value with quote awareness
                    parsed = cls._parse_value(token, is_quoted)
                except ValueError as e:
                    flag_name = current_flag.long if current_flag else 'ROOT'
                    raise ArgumentValueError(f"{flag_name}: {str(e)}")

                # Store parsed value
                if current_flag:
                    flags[current_flag].append(parsed)
                else:
                    flags[FlagNameConfig('', 'ROOT')].append(parsed)
        
        return cls(name, flags)

    @staticmethod
    def _tokenize(s: str) -> tuple[list[str], list[bool]]:
        """Tokenize with quote preservation using shlex non-POSIX mode"""
        lex = shlex.shlex(s, posix=False)
        lex.whitespace_split = True
        lex.commenters = ''
        
        tokens = []
        quoted = []
        while True:
            tok = lex.get_token()
            if not tok: break
            
            # Detect quoting status from token boundaries
            has_quotes = (tok.startswith("'") and tok.endswith("'")) or \
                        (tok.startswith('"') and tok.endswith('"'))
            
            tokens.append(tok)
            quoted.append(has_quotes)
        return tokens, quoted

    @staticmethod
    def _parse_value(token: str, is_quoted: bool):
        """Convert token to Python type with quote handling"""
        if is_quoted:
            # Strip quotes and preserve inner content
            stripped = token[1:-1]
            return stripped
            
        # Type conversion cascade
        if token in ('True', 'False'):
            return token == 'True'
        try:
            return int(token)
        except ValueError:
            try:
                return float(token)
            except ValueError:
                raise ValueError(f"Unparsable token '{token}'")

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
    
