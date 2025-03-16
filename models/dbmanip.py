# Created by Sean L. on Mar 16
# 
# emb2emb client
# dbmanip.py
# 
# PromptCraft, 2025. All rights reserved.

import sqlite3
import datetime
from typing import Dict, List, Optional
import numpy as np
from models.memglobalstore_model import MemGlobalStore
from models.converse_model import Converse, StoredConverse
from utils.exceptions import TableExistsError
from utils.const import DB_PATH

store = MemGlobalStore(':memory:')

class DatabaseManager:
    """A class for managing transactions with the db
    
    Example:
    >>> db = DatabaseManager()
    >>> db.insert('test', [0 for _ in range(0, 384)], [0 for _ in range(0, 384)])
    
    """
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        """Initializes a DatabaseManager
        """
        pass
    
    def insert(self, converse: Converse):
        """Inserts a set of prompt & answer embedding arrays

        Args:
            converse (Converse): A peice of conversation between the model and the user, along with embedded vectors.
        """
        table = store.get('tablename')
        self.cursor.execute(f'''
                       INSERT INTO {table} (text, answer, veci, veco) values
                       (?{', ?' * 769})
                       ''', (converse.prompt, converse.answer, ' '.join(map(str, converse.veci)), ' '.join(map(str, converse.veco))))
        self.conn.commit()
    
    def create(self, table: str) -> sqlite3.Connection:
        """Creates a table in the database.

        Args:
            table (str): Name of table to create

        Raises:
            TableExistsError: When table of the same name already exists

        Returns:
            sqlite3.Connection: A live connection with the database
        """
        
        create_sql = f'''
            CREATE TABLE {table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                prompt TEXT NOT NULL,
                answer TEXT NOT NULL,
                veci TEXT NOT NULL,
                veco TEXT NOT NULL
            )
        '''
        
        try:
            self.cursor.execute(create_sql)
        except sqlite3.OperationalError as e:
            if "already exists" in str(e):
                raise TableExistsError(f"Table {table} already exists.") from e
            else:
                raise
        self.conn.commit()
        store.set('table', table)
        return self.conn
    
    def ls(self, table: str, limit: Optional[int] = 10, 
           old: bool = True, asc: bool = True) -> List[StoredConverse]:
        """Retrieve stored conversations with flexible temporal ordering.
        
        Implements a double-sorted query pattern to first select historical records
        then reorder results. Combines SQL-level sorting with application-level
        validation.
        
        Parameters:
            table (str): Target SQL table name (sanitized)
            limit (Optional[int]): Max records to return (10 default)
            old (bool): True = prioritize older entries in initial selection
            asc (bool): True = final output in ascending order
        
        Returns:
            List[StoredConverse]: Conversation records with DB metadata
        
        Example:
            >>> db.ls("chat_logs", limit=5, old=False, asc=True)
            [<StoredConverse id=115>, <StoredConverse id=114>...]
        
        Raises:
            sqlite3.OperationalError: On invalid table name or SQL syntax
            ValueError: If input parameters fail validation
        """
        # Parameter validation
        if not isinstance(table, str) or not table.isidentifier():
            raise ValueError(f"Invalid table name: {table}")
        
        # Query construction with injection protection
        inner_order = "ASC" if old else "DESC"
        outer_order = "ASC" if asc else "DESC"
        limit_clause = f"LIMIT {limit}" if limit is not None else ""
        
        query = f"""
        SELECT id, timestamp, prompt, answer 
        FROM (
            SELECT * FROM {table}
            ORDER BY id {inner_order}
            {limit_clause}
        )
        ORDER BY id {outer_order}
        """
        
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return [self._row_to_converse(row) for row in rows]

    def _row_to_converse(self, row: tuple) -> StoredConverse:
        """Convert database row to StoredConverse instance.
        
        """
        conv = StoredConverse(
            prompt=row[2], 
            answer=row[3],
            veci=np.fromstring(row['veci'], sep=' ', dtype=np.float32),
            veco=np.fromstring(row['veco'], sep=' ', dtype=np.float32)
        )
        conv.id = row[0]
        conv.timestamp = datetime.fromisoformat(row[1])
        return conv


# Managers
fetch_manager = DatabaseManager()