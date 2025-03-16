# Created by Sean L. on Mar 15
# 
# emb2emb client
# embed.py
# 
# PromptCraft, 2025. All rights reserved.

# Created by Sean L. on Mar 15
# 
# emb2emb client
# embed.py
# 
# PromptCraft, 2025. All rights reserved.

from sentence_transformers import SentenceTransformer
from numpy import ndarray
from typing import Optional
from utils.output import ClientConsole
from utils.const import EMBEDDING_MODEL_PATH

ClientConsole.log('Loading BERT model...')
model = SentenceTransformer(EMBEDDING_MODEL_PATH)
ClientConsole.done('Embedding model loaded.')

def embed(string: str) -> ndarray:
    """Generate embeddings with model verification
    
    Args:
        string: Input text to embed

    Returns:
        ndarray: 768-dimensional float32 embedding vector
        
    Raises:
        RuntimeError: If model initialization failed
    """
    try:
        return model.encode(string)
    except Exception as e:
        ClientConsole.error(f"Embedding failed: {str(e)}")
        raise