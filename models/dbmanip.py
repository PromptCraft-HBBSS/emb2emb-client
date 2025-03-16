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
from models.memglobalstore_model import global_manager
from models.converse_model import Converse, StoredConverse, ConverseTable
from utils.exceptions import TableExistsError
from utils.const import DB_PATH



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
        # table = global_manager.get('tablename')
        table = 'main'
        self.cursor.execute(f'''
                       INSERT INTO {table} (text, answer, veci, veco) values
                       (?, ?, ?, ?)
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
        global_manager.set('table', table)
        return self.conn
    
    def fetch(self, table: str, limit: Optional[int] = 10, 
        old: bool = True, asc: bool = True) -> ConverseTable:
        """Retrieve conversations as a structured table with metadata.
        
        Parameters:
            table (str): Target table name used for both SQL query and result labeling
            limit (Optional[int]): Max records to return (10 default)
            old (bool): True = prioritize older entries in initial selection
            asc (bool): True = final output in ascending order
        
        Returns:
            ConverseTable: Structured result container with:
            - name: Original table name from database
            - conversations: List of StoredConverse records with full metadata
        
        Example:
            >>> table = db.fetch("chat_logs", limit=5)
            >>> print(f"Table {table.name} has {len(table.conversations)} records")
            Table chat_logs has 5 records
            >>> isinstance(table.conversations[0], StoredConverse)
            True
        """
        # Parameter validation
        if not isinstance(table, str) or not table.isidentifier():
            raise ValueError(f"Invalid table name: {table}")

        # Query construction
        inner_order = "ASC" if old else "DESC"
        outer_order = "ASC" if asc else "DESC"
        limit_clause = f"LIMIT {limit}" if limit is not None else ""
        
        query = f"""
        SELECT id, timestamp, prompt, answer, veci, veco 
        FROM (
            SELECT * FROM {table}
            ORDER BY id {inner_order}
            {limit_clause}
        )
        ORDER BY id {outer_order}
        """
        
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        
        return ConverseTable(
            name=table,
            conversations=[self._row_to_converse(row) for row in rows]
        )

    def tables(self) -> List[ConverseTable]:
        """Retrieves all conversation tables with their metadata and contents.
        
        Returns:
            List[ConverseTable]: Structured tables containing:
            - Table name from SQL schema [1](@ref)
            - Full conversation history with embeddings
            - Database metadata including timestamps
        
        Example:
            >>> db.tables()
            [<ConverseTable name=main (15 convs)>, <ConverseTable name=chat_logs (203 convs)>]
        """
        self.cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' 
            AND name NOT LIKE 'sqlite_%'
        """)
        
        return [
            ConverseTable(
                name=row[0],
                conversations=[
                    StoredConverse(
                        id=conv.id,
                        timestamp=conv.timestamp,
                        prompt=conv.prompt,
                        answer=conv.answer,
                        veci=conv.veci,
                        veco=conv.veco
                    ) for conv in self.fetch(table=row[0], limit=None)
                ]
            ) for row in self.cursor.fetchall()
        ]
        
    def _row_to_converse(self, row: tuple) -> StoredConverse:
        """Convert database row to StoredConverse instance.
        
        """
        conv = StoredConverse(
            id=row[0],
            timestamp=row[1],
            prompt=row[2], 
            answer=row[3],
            veci=np.fromstring(row[4], sep=' ', dtype=np.float32),
            veco=np.fromstring(row[5], sep=' ', dtype=np.float32)
        )
        conv.id = row[0]
        conv.timestamp = row[1]
        return conv


# Managers
fetch_manager = DatabaseManager()