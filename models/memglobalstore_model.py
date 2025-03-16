# Created by Sean L. on Mar 16
# 
# emb2emb client
# globals.py
# 
# PromptCraft, 2025. All rights reserved.

import sqlite3
import json
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Optional, Union
import time
import threading

class MemGlobalStore:
    """A persistent in-memory key-value store using SQLite as backend.
    
    Provides thread-safe storage and retrieval of various data types with 
    automatic serialization/deserialization. Values persist across connections
    when using file-based storage.
    
    Attributes:
        db_path (str, optional): Path to SQLite database file. Defaults to 
            'file:mem_global_store?mode=memory&cache=shared' for transient storage.
            
    Example:
        >>> store = MemGlobalStore()
        >>> store.set('config', {'theme': 'dark'})
        >>> store.get('config')
        {'theme': 'dark'}
    """
    
    def __init__(self, db_path: Union[str, Path] = None):
        self.db_path = self._resolve_db_path(db_path)
        self._conn_pool = {}
        
    def _resolve_db_path(self, path):
        """Handle storage location defaults"""
        if path:
            return str(path)
            
        # Default to user config directory
        config_dir = Path.home() / ".config/emb2emb"
        config_dir.mkdir(parents=True, exist_ok=True)
        return str(config_dir / "global_store.db")

    
    @contextmanager
    def _connection(self):
        """Thread-aware connection manager with connection reuse"""
        thread_id = threading.get_ident()
        
        # Reuse or create connection
        if thread_id not in self._conn_pool:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.execute('''
                CREATE TABLE IF NOT EXISTS mem_global_store (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    type TEXT,
                    created_at REAL,
                    updated_at REAL
                )
            ''')
            self._conn_pool[thread_id] = conn
            
        try:
            yield self._conn_pool[thread_id]
        finally:
            # Keep connections open for reuse
            pass
    
    def set(self, key: str, value: Any):
        """Atomic insert/update with type handling"""
        with self._connection() as conn:
            conn.execute('''
                INSERT OR REPLACE INTO mem_global_store 
                (key, value, type, created_at, updated_at)
                VALUES (?, ?, ?, COALESCE(
                    (SELECT created_at FROM mem_global_store WHERE key = ?), 
                    ?
                ), ?)
            ''', (
                key,
                self._serialize(value),
                self._infer_type(value),
                key,  # For COALESCE
                time.time(),
                time.time()
            ))
            conn.commit()

    def get(self, key: str) -> Optional[Any]:
        """Safe retrieval with type reconstruction
        """
        with self._connection() as conn:
            # Explicit column selection with index access
            cursor = conn.execute('''
                SELECT value, type 
                FROM mem_global_store 
                WHERE key = ?
            ''', (key,))
            row = cursor.fetchone()
            
        if row:
            # Access columns by index instead of name
            return self._deserialize(row[0], row[1])

        return None
    
    def _infer_type(self, value: Any) -> str:
        """Infers data type from Python object type.
        
        Arguments:
            value: Object to analyze
            
        Returns:
            str: One of ('json', 'bool', 'int', 'float', 'bytes', 'str')
        """
        if isinstance(value, (dict, list)):
            return 'json'
        elif isinstance(value, bool):
            return 'bool'
        elif isinstance(value, int):
            return 'int'
        elif isinstance(value, float):
            return 'float'
        elif isinstance(value, bytes):
            return 'bytes'
        return 'str'

    def _serialize(self, value: Any) -> str:
        """Converts Python objects to storable formats.
        
        Arguments:
            value: Object to serialize
            data_type (str): Target storage type
            
        Returns:
            str: Serialized string representation
        """
        if isinstance(value, (dict, list)):
            return json.dumps(value)
        elif isinstance(value, bytes):
            return value.hex()
        elif isinstance(value, bool):
            return '1' if value else '0'
        return str(value)

    def _deserialize(self, value: str, type_str: str) -> Any:
        """Restores stored values to native Python objects.
        
        Arguments:
            value (str): Serialized string from database
            data_type (str): Original storage type
            
        Returns:
            object: Deserialized Python object
        """
        type_map = {
            'json': lambda v: json.loads(v),
            'bool': lambda v: bool(int(v)),
            'int': lambda v: int(v),
            'float': lambda v: float(v),
            'bytes': lambda v: bytes.fromhex(v),
            'str': lambda v: v
        }
        return type_map[type_str](value)

global_manager = MemGlobalStore()