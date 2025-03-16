# Created by Sean L. on Mar 15
# 
# emb2emb client
# main.py
# 
# PromptCraft, 2025. All rights reserved.

# MARK: Imports
from utils.systemcalls import clear
clear()
from utils.output import ClientConsole
ClientConsole.log('Loading app...')
from rich.console import Console
from utils.embed import embed
from platform import system
from models.command_model import Command
from utils.load_config import COMMANDS
from models.memglobalstore_model import MemGlobalStore
from utils.exceptions import *
from utils.commands import *
import sqlite3

ClientConsole.done('Dependencies loaded.')

if system() == 'Windows':
    import pyreadline3 as readline
else:
    import readline

memGlobalManger = MemGlobalStore()

# MARK: App
ClientConsole.print('[cyan]Welcome to Labelist Client for emb2emb.[/cyan]')

def repl():
    while True:
        try:
            statement = input(f'{memGlobalManger.get('tablename')} → ')
            for f in statement.split(';'):
                f = f.strip()
                if f == '':
                    continue
                if f == 'exit':
                    raise ProgramTermination('EXIT')
                if not f.split()[0] in COMMANDS.keys():
                    raise CommandNotFoundError(f'{f.split()[0]} is not a valid command.')
                flags = COMMANDS[f.split()[0]].flags.values();
                cmd = Command.parse(f, flags);
                cmd.act()
        except ProgramTermination:
            break;
        except KeyboardInterrupt:
            print();
            ClientConsole.warn(f'Use `exit` to exit shell')
        except EOFError:
            print();
            ClientConsole.warn(f'Use `exit` to exit shell')
        except CommandNotFoundError as e:
            ClientConsole.error(f'Command: {e}')
        except ExcessiveArgsError as e:
            ClientConsole.error(f'ExcessiveArgsError: {e}')
        except MissingArgError as e:
            ClientConsole.error(f'MissingArgsError: {e}')
        except MissingFlagError as e:
            ClientConsole.error(f'MissingFlagError: {e}')
        except KeyError as e:
            ClientConsole.error(f'KeyError: {e}')
        except ValueError as e:
            ClientConsole.error(f'ValueError: {e}')
        except sqlite3.OperationalError as e:
            ClientConsole.error(f'SQLITE OperationalError: {e}')
                

# MARK: Entrance
if __name__ == '__main__':
    if memGlobalManger.get('tablename') == None:
        memGlobalManger.set('tablename', 'main')
    repl()
    ClientConsole.warn('Goodbye')