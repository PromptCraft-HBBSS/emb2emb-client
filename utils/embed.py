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

class EmbeddingModel:
    """Singleton wrapper for sentence-transformers model with thread-safe initialization"""
    _instance: Optional[SentenceTransformer] = None
    _initialized: bool = False

    @classmethod
    def initialize(cls, model_name: str = EMBEDDING_MODEL_PATH):
        """Initialize model once with loading indicator"""
        if not cls._initialized:
            with ClientConsole.loading(spinner='dots', message=f"Loading {model_name}"):
                cls._instance = SentenceTransformer(model_name)
                cls._initialized = True
            ClientConsole.done(f"Model {model_name} ready")

    @classmethod
    def get_model(cls) -> SentenceTransformer:
        """Get model instance with initialization check"""
        if not cls._initialized:
            raise RuntimeError("Model not initialized. Call EmbeddingModel.initialize() first")
        return cls._instance

# Initialize during module import
EmbeddingModel.initialize()  # Default to bert-base-uncased

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
        model = EmbeddingModel.get_model()
        return model.encode(string)
    except Exception as e:
        ClientConsole.error(f"Embedding failed: {str(e)}")
        raise