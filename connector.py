import sqlite3
from sqlite3 import Error


def select_user(conn,user):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users where name=?", (user,))
    rows = cur.fetchall()
    print(rows)
    if len(rows) == 0:
        cur.execute("INSERT into users(id,name,score) VALUES (null,?,0)",(user,))
        conn.commit()
        return 0
    return rows[0][2]


def get_score(conn, user):
    score = select_user(conn, user)
    return score


def get_scores(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users order by score desc")
    rows = cur.fetchall()
    return rows

def update_score(conn, user):
    score = select_user(conn, user)
    score = score + 10
    cur = conn.cursor()
    cur.execute("UPDATE users set score=? where name=?", (score,user,))
    conn.commit()
    return score

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

