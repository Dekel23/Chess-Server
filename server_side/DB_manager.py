import sqlite3
from typing import Callable

class DB_Manager():
    def __init__(self, conn: sqlite3.Connection, c: sqlite3.Cursor) -> None:
        self.conn = conn
        self.c = c
    
    def changes(func: Callable):
        def inner(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.conn.commit()
        return inner
    
    @changes
    def create_table(self, table_name: str, columns: str):
        self.c.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({columns})')
    
    @changes
    def insert_data(self, table_name: str, data: str):
        placeholders = ','.join(['?'] * len(data))
        self.c.execute(f'INSERT INTO {table_name} VALUES ({placeholders})', data)

    @changes
    def remove_row(self, table_name: str, **kwargs: dict):
        conditions = []
        values = []
        for key, value in kwargs.items():
            conditions.append(f"{key} = ?")
            values.append(value)
        conditions_str = " AND ".join(conditions)
        self.c.execute(f'DELETE FROM {table_name} WHERE {conditions_str}', tuple(values))
    
    def execute_query(self, query: str, params=None):
        if params:
            self.c.execute(query, params)
        else:
            self.c.execute(query)
        return self.c.fetchall()