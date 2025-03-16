# Created by Sean L. on Mar 16
# 
# emb2emb client
# config_model.py
# 
# PromptCraft, 2025. All rights reserved.

from dataclasses import dataclass
from typing import Dict, List, Optional
import json

@dataclass(frozen=True)
class FlagNameConfig:
    """Represents a command line flag naming convention"""
    short: str
    long: str

    @classmethod
    def from_dict(cls, data: dict) -> 'FlagNameConfig':
        return cls(short=data['short'], long=data['long'])

@dataclass
class FlagDocConfig:
    """Documentation for a specific flag with validation"""
    flag: str
    description: str

    def __post_init__(self):
        if len(self.flag) != 1:
            raise ValueError("Flag must be single character")

@dataclass
class DocConfig:
    """Command documentation structure with nested parsing"""
    description: str
    additions: Dict[str, str]

    @classmethod
    def from_dict(cls, data: dict) -> 'DocConfig':
        return cls(
            description=data['description'],
            additions={item['flag']: item['add'] for item in data['additions']}
        )

@dataclass
class CommandConfig:
    """Complete command configuration with optional docs"""
    flags: Dict[str, FlagNameConfig]
    doc: Optional[DocConfig] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'CommandConfig':
        return cls(
            flags={f['short']: FlagNameConfig.from_dict(f) for f in data.get('flags', [])},
            doc=DocConfig.from_dict(data['docs']) if 'docs' in data else None
        )

@dataclass
class ShellLexicalConfig:
    """Top-level configuration container with safe loading"""
    commands: Dict[str, CommandConfig]

    @classmethod
    def load(cls, config_path: str) -> 'ShellLexicalConfig':
        with open(config_path, 'r', encoding='utf8') as f:
            raw_data = json.load(f)
        
        return cls(
            commands={
                cmd_name: CommandConfig.from_dict(cmd_data)
                for cmd_name, cmd_data in raw_data['commands'].items()
            }
        )

# MARK: Helpers
def find_flag(flags_list, target: str) -> FlagNameConfig | None:
    """Find flag by short or long name with O(n) complexity"""
    return next(
        (flag for flag in flags_list 
         if flag.short == target or flag.long == target),
        None
    )

def flagconfiglist2dic(flags_list: Dict[FlagNameConfig, List[str]]) -> Dict[str, List[str]]:
    """Turns a dictionary of FlagNameConfig instances into a long-flagname to arguments dict.
    
    Converts keys from FlagNameConfig objects to their long-form string representations,
    preserving the original argument lists. This enables seamless transition between
    short/long flag name usage in CLI applications.
    
    Example:
        Input: {FlagNameConfig(short='l', long='limit'): ['10']}
        Output: {'limit': ['10']}

    Args:
        flags_list (Dict[FlagNameConfig, List[str]]): Dictionary mapping flag configs to arguments

    Returns:
        Dict[str, List[str]]: New dict with long flag names as keys
    """
    return {
        flag_config.long: arguments 
        for flag_config, arguments in flags_list.items()
        if isinstance(flag_config, FlagNameConfig)  # Type safety check
    }
    