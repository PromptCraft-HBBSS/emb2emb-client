# Created by Sean L. on Mar 16
# 
# emb2emb client
# const.py
# 
# PromptCraft, 2025. All rights reserved.

import dotenv
import os

dotenv.load_dotenv('../.env')
OLLAMA_ENPOINT = os.getenv('OLLAMA_ENDPOINT')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL')
DB_PATH = os.getenv('DB_PATH')
CONFIG_PATH = os.getenv('CONFIG_PATH')
EMBEDDING_MODEL_PATH = os.getenv('EMBEDDING_MODEL_PATH')