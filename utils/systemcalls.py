# Created by Sean L. on Mar 16
# 
# emb2emb client
# systemcalls.py
# 
# PromptCraft, 2025. All rights reserved.

def clear():
    try:
        from colorama import init
        init()
        print("\033[H\033[J", end='')
    except ImportError:
        import os
        os.system('cls||clear')

def width():
    import os
    import subprocess

    result = subprocess.run(['tput', 'cols'], stdout=subprocess.PIPE)
    return int(result.stdout.decode().strip())