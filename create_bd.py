import sqlite3


def create_connection(db_file: str) -> sqlite3.connect:
    """create a database connection to the SQLite database
        specified by db_file

    Args:
        db_file (str): database name

    Returns:
        sqlite3.connect: Connection to database
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)

    return conn


def create_table(conn):
    countries_file = open('create_countries_table.sql', 'r')
    sql_file = countries_file.read()
    countries_file.close()
    try:
        c = conn.cursor()
        c.execute(sql_file)
    except Exception as e:
        print(e)