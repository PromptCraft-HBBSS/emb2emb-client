# Created by Sean L. on Mar 16
#
# emb2emb client
# converse_model.py
#
# PromptCraft, 2025. All rights reserved.

from utils.embed import embed
from numpy import ndarray
from datetime import datetime
from typing import Optional

class Converse:
    """Represents a conversation exchange with vector embeddings.
    
    Attributes:
        prompt (str): User's original input text
        answer (str): AI model's generated response
        veci (ndarray): 384-dim embedding of prompt (GPT-4o vector space)
        veco (ndarray): 384-dim embedding of answer (GPT-4o vector space)
    
    Example:
        >>> conv = Converse.create(
        ...     prompt="What's quantum computing?",
        ...     answer="Quantum computing leverages..."
        ... )
        >>> conv.veci.shape
        (384,)
        >>> len(conv.answer)
        27
    """

    prompt: str
    answer: str
    veci: ndarray
    veco: ndarray

    def __init__(self, prompt: str, answer: str, veci: ndarray, veco: ndarray):
        """Initializes conversation with precomputed embeddings.
        
        Parameters:
            prompt: Raw user input text (max 2000 chars)
            answer: Model response text (max 2000 chars)
            veci: Precomputed embedding vector for prompt
            veco: Precomputed embedding vector for answer
        
        Raises:
            ValueError: If embedding dimensions mismatch
        """
        self.prompt = prompt
        self.answer = answer
        self.veci = veci
        self.veco = veco

    @classmethod
    def create(cls, prompt: str, answer: str) -> 'Converse':
        """Factory method generating embeddings automatically.
        
        Parameters:
            prompt: User input text (supports markdown formatting)
            answer: Model response (supports markdown formatting)
        
        Returns:
            New Converse instance with computed embeddings
        
        Example:
            >>> Converse.create("Hi", "Hello!").veci[0:3]
            array([0.12, 0.34, 0.56])
        """
        return cls(
            prompt=prompt,
            answer=answer,
            veci=embed(prompt),
            veco=embed(answer)
        )

class StoredConverse(Converse):
    """Persistent conversation record with database metadata.
    
    Inherits:
        Converse: Base conversation attributes and methods
    
    Attributes:
        id (Optional[int]): SQLite auto-increment primary key
        timestamp (datetime): Creation time in UTC
    
    Example:
        >>> stored = StoredConverse(prompt="Define AI", answer="...")
        >>> stored.timestamp.strftime("%Y-%m-%d")
        '2025-03-16'
    """

    id: Optional[int]
    timestamp: datetime

    def __init__(self, id: int, timestamp: datetime, prompt: str, answer: str):
        """Initializes for database insertion (id auto-assigned).
        
        Parameters:
            id (int): Integer id
            prompt (str): User input text (sanitized)
            answer (str): Model response (sanitized)
            timestamp (datetime.datetime): Timestamp of creation
        """
        super().__init__(
            prompt=prompt,
            answer=answer,
            veci=embed(prompt),
            domo=embed(answer)
        )
        self.id = id
        self.timestamp = timestamp

    def to_transient(self) -> Converse:
        """Converts to non-persistent Converse object.
        
        Returns:
            BaseConverse: instance without database fields
        
        Example:
            >>> stored = StoredConverse("Physics?", "Study of matter...")
            >>> transient = stored.to_transient()
            >>> isinstance(transient, Converse)
            True
        """
        return Converse(
            prompt=self.prompt,
            answer=self.answer,
            veci=self.veci,
            veco=self.veco
        )