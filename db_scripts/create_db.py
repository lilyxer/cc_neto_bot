import psycopg2

from psycopg2 import sql
from config_data.config import _CONFIG


def create_database():
    """
    Производим подключение к серверу базы,
    проверяем есть ли уже бд которую мы создаём
    """
    status = True
    conn = psycopg2.connect(database = 'postgres',
                            user = _CONFIG.db.db_user,
                            password = _CONFIG.db.db_password,
                            host = _CONFIG.db.db_host,
                            port=_CONFIG.db.db_port)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("""SELECT datname
                     FROM pg_catalog.pg_database;""")

    if _CONFIG.db.database in [x[0] for x in cur.fetchall()]:
        print(f'{_CONFIG.db.database} была создана ранее')
        status = False
    else:
        cur.execute(
            sql.SQL("CREATE DATABASE {}").format(sql.Identifier(_CONFIG.db.database))
        )
        print(f'{_CONFIG.db.database} была создана')

    cur.close()
    conn.close()
    return status
