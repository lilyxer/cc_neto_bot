import psycopg2

from psycopg2 import sql
from config_data.config import DatabaseConfig


def create_database(_db: DatabaseConfig):
    """
    Производим подключение к серверу базы,
    проверяем есть ли уже бд которую мы создаём
    """
    status = True
    conn = psycopg2.connect(database = 'postgres',
                            user = _db.db_user,
                            password = _db.db_password,
                            host = _db.db_host,
                            port=_db.db_port)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("""SELECT datname
                     FROM pg_catalog.pg_database;""")

    if _db.database in [x[0] for x in cur.fetchall()]:
        print(f'{_db.database} была создана ранее')
        status = False
    else:
        cur.execute(
            sql.SQL("CREATE DATABASE {}").format(sql.Identifier(_db.database))
        )
        print(f'{_db.database} была создана')

    cur.close()
    conn.close()
    return status
