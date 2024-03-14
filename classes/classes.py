import psycopg2
import contextlib


class PostgresDB:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, dsn):
        self.dsn = dsn

    async def connect(self):
        self.conn = psycopg2.connect(self.dsn)
        self.cur = self.conn.cursor()  # cursor_factory=RealDictCursor) from psycopg2.extras import RealDictCursor

    async def execute_query(self, query: str, *args, one: bool = True) -> None:
        with contextlib.suppress(Exception):
            self.cur.execute(query, *args)
            self.conn.commit()
            return self.cur.fetchone() if one else self.cur.fetchall()

    async def close(self):
        self.cur.close()
        self.conn.close()