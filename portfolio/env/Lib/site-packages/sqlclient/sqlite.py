import sqlite3
from typing import List

from .sql import SQLClient, Connection, AsyncConnection


class SqliteConnection(Connection):
    def get_tables(self) -> List[str]:
        sql = '''\
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name NOT LIKE 'sqlite_%' '''
        z = self.execute(sql).fetchall()
        return [v[0] for v in z]


class SqliteAsyncConnection(AsyncConnection):
    async def get_tables(self):
        return await self._a_call(self._sync_conn.get_tables)


class SQLite(SQLClient):
    def __init__(self,
                 database: str,
                 isolation_level: str = 'IMMEDIATE'):
        super().__init__()
        self.database = database
        self.isolation_level = isolation_level

    def connect(self):
        return sqlite3.connect(
            self.database, isolation_level=self.isolation_level)

    def get_connection(self):
        return SqliteConnection(self, self.execute_config)

    def get_async_connection(self):
        return SqliteAsyncConnection(self.get_connection())
