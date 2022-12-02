import asyncio
import logging
from abc import ABCMeta, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from typing import (
    Sequence, List, Tuple,
    Callable, Optional,
    Iterator, AsyncIterator,
)

import pandas as pd  # type: ignore


logger = logging.getLogger(__name__)


class Connection:
    def __init__(self, client: 'SQLClient', execute_config: dict = None):
        self._client = client
        self._conn = None
        self._cursor = None
        self._execute_config = execute_config

    def _open(self) -> 'Connection':
        self._conn = self._client.connect()
        self._cursor = self._conn.cursor()  # type: ignore
        return self

    def _close(self) -> None:
        if self._cursor is not None:
            self._cursor.close()
            self._cursor = None
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def __del__(self):
        self._close()

    def __enter__(self):
        return self._open()

    def __exit__(self, *args, **kwargs):
        self._close()

    def execute(self, sql: str, *args, **kwargs) -> 'Connection':
        logger.debug('executing SQL statement\n%s\nargs:\n%s\nkwargs:\n%s',
                     sql, str(args), str(kwargs))
        if self._execute_config:
            self._cursor.execute(  # type: ignore
                sql,
                *args,
                configuration=self._execute_config,
                **kwargs)
        else:
            self._cursor.execute(  # type: ignore
                sql,
                *args,
                **kwargs)
        return self

    def executemany(self, sql: str, *args, **kwargs):
        return self._cursor.executemany(sql, *args, **kwargs)  # type: ignore

    @property
    def headers(self) -> List[str]:
        """
        Return column headers after calling ``read``.

        This can be used to augment the returns of `fetchone`, `fetchmany`, `fetchall`,
        which return values only, i.e. they do not return column headers.
        """
        return [x[0] for x in self._cursor.description]  # type: ignore

    def fetchone(self) -> Optional[Tuple]:
        """
        Fetch the next row of a query result set, returning a single sequence, 
        or None when no more data is available.

        An Error (or subclass) exception is raised if the previous call to 
        ``read`` did not produce any result set or no call to ``read``
        was issued yet.
        """
        return self._cursor.fetchone()  # type: ignore

    def fetchone_pandas(self, cols: Sequence[str] = None) -> Optional[pd.DataFrame]:
        row = self.fetchone()
        if row is None:
            return None
        return pd.DataFrame.from_records(
            [row], columns=cols or self.headers)

    def fetchmany(self, size: int = None) -> List[Tuple]:
        """
        Fetch the next set of rows of a query result, returning a sequence of sequences
        (e.g. a list of tuples). 
        An empty sequence is returned when no more rows are available.

        An Error (or subclass) exception is raised if the previous call to 
        ``read`` did not produce any result set or no call to ``read`` was issued yet.
        """
        if size is None:
            size = self._cursor.arraysize  # type: ignore
        return self._cursor.fetchmany(size)  # type: ignore

    def fetchmany_pandas(self, n: int, cols: Sequence[str] = None) -> Optional[pd.DataFrame]:
        rows = self.fetchmany(n)
        if not rows:
            return None
        return pd.DataFrame.from_records(list(rows), columns=cols or self.headers)

    def fetchall(self) -> List[Tuple]:
        """
        Fetch all (remaining) rows of a query result, returning them 
        as a sequence of sequences (e.g. a tuple of tuples).

        Note that the cursor's arraysize attribute can affect the performance 
        of this operation.

        An Error (or subclass) exception is raised if the previous call to 
        ``read`` did not produce any result set or no call to ``read`` 
        was issued yet.
        """
        return self._cursor.fetchall()  # type: ignore

    def fetchall_pandas(self, cols: Sequence[str] = None) -> Optional[pd.DataFrame]:
        """
        This method is called after ``read`` to fetch the results as a ``pandas.DataFrame``.

        Warning: do not use this if the result contains a large number of rows.
        """
        rows = self.fetchall()
        if not rows:
            return None
        return pd.DataFrame.from_records(list(rows), columns=cols or self.headers)

    def iterrows(self) -> Iterator[Tuple]:
        """
        Iterate over rows in result after calling ``read``,
        one row at a time.
        """
        while True:
            v = self.fetchone()
            if v is None:
                break
            yield v

    def iterbatches(self, batch_size: int) -> Iterator[List[Tuple]]:
        """
        This method is called after ``read`` to iter over results,
        one batch at a time.
        """
        while True:
            rows = self.fetchmany(batch_size)
            if rows:
                yield rows
            else:
                break


class AsyncConnection:
    def __init__(self, conn: Connection):
        assert conn._conn is None  # `open` is not called yet
        self._sync_conn = conn
        self._executor = ThreadPoolExecutor(  # pylint: disable=consider-using-with
            1)

    async def _a_call(self, f: Callable, *args, **kwargs):
        t = self._executor.submit(f, *args, **kwargs)
        while not t.done():
            await asyncio.sleep(0.011)
        return t.result()

    async def _open(self) -> 'AsyncConnection':
        await self._a_call(self._sync_conn._open)  # pylint: disable=protected-access
        return self

    async def _close(self) -> None:
        await self._a_call(self._sync_conn._close)  # pylint: disable=protected-access

    def __del__(self):
        self._sync_conn.close()

    async def __aenter__(self):
        await self._open()
        return self

    async def __aexit__(self, *args, **kwargs):
        await self._close()

    async def execute(self, sql: str, *args, **kwargs) -> 'AsyncConnection':
        await self._a_call(self._sync_conn.execute, sql, *args, **kwargs)
        return self

    @property
    def headers(self) -> List[str]:
        return self._sync_conn.headers

    async def fetchone(self):
        return await self._a_call(self._sync_conn.fetchone)

    async def fetchone_pandas(self, cols=None):
        return await self._a_call(self._sync_conn.fetchone_pandas, cols)

    async def fetchmany(self, n):
        return await self._a_call(self._sync_conn.fetchmany, n)

    async def fetchmany_pandas(self, n, cols=None):
        return await self._a_call(self._sync_conn.fetchmany_pandas, n, cols)

    async def fetchall(self):
        return await self._a_call(self._sync_conn.fetchall)

    async def fetchall_pandas(self, cols=None):
        return await self._a_call(self._sync_conn.fetchall_pandas, cols)

    async def iterrows(self) -> AsyncIterator[Tuple]:
        while True:
            row = await self._a_call(self._sync_conn.fetchone)
            if row is None:
                break
            yield row

    async def iterbatches(self, batch_size: int) -> AsyncIterator[List[Tuple]]:
        while True:
            rows = await self._a_call(self._sync_conn.fetchmany, batch_size)
            if rows:
                yield rows
            else:
                break


class SQLClient(metaclass=ABCMeta):
    def __init__(self, execute_config: dict = None):
        self.execute_config = execute_config

    @abstractmethod
    def connect(self):
        # This should return a connection object
        # w/o changing the state of `self`.
        raise NotImplementedError

    def get_connection(self) -> Connection:
        # Typical usage:
        #
        #   obj = Sql(...)
        #   with obj.get_connection() as conn:
        #     conn.execute(...)
        #     x = conn.fetchall()
        #     conn.execute(...)
        #     ...
        return Connection(self, self.execute_config)

    def get_async_connection(self) -> AsyncConnection:
        # Typical usage:
        #
        #   obj = Sql(...)
        #   async with obj.get_async_connection() as conn:
        #     await conn.execute(...)
        #     x = await conn.fetchall()
        #     await conn.execute(...)
        #     ...
        return AsyncConnection(self.get_connection())
