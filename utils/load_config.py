# Created by Sean L. on Mar 15
# 
# emb2emb client
# commands.py
# 
# PromptCraft, 2025. All rights reserved.

import json
from utils.const import CONFIG_PATH
from models.config_model import *

CONFIG = ShellLexicalConfig.load(CONFIG_PATH)
COMMANDS = CONFIG.commands