import os
import psycopg2


def get_db_connection():
    conn = psycopg2.connect(
        host="db",
        database="flask_db",
        user=os.environ["DB_USERNAME"],
        password=os.environ["DB_PASSWORD"],
    )
    return conn


def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")
    users = cur.fetchall()
    cur.close()
    conn.close()

    return users


def get_user(username):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username='{}';".format(username))
    users = cur.fetchone()
    cur.close()
    conn.close()

    return users


def remove_user(username):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE username = '{}';".format(username))
    conn.commit()
    users_deleted = cur.rowcount
    cur.close()
    conn.close()

    return users_deleted


def update_plan(username, new_plan):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET paid = {} WHERE username = '{}';".format(new_plan, username)
    )
    conn.commit()
    users_updated = cur.rowcount
    cur.close()
    conn.close()

    return users_updated


def insert_user(username, paid):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users(username, paid) VALUES ('{}', '{}') RETURNING *;".format(
            username, paid
        )
    )
    conn.commit()
    user_inserted = cur.fetchone
    print(user_inserted)
    cur.close()
    conn.close()

    return user_inserted
