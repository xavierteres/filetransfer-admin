import os
import psycopg2

conn = psycopg2.connect(
    host="host",
    port="port",
    database="flask_db",
    user=os.environ["DB_USERNAME"],
    password=os.environ["DB_PASSWORD"],
)

cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS users;")
cur.execute(
    "CREATE TABLE users (id serial PRIMARY KEY,"
    "username varchar (50) NOT NULL,"
    "paid BOOLEAN NOT NULL,"
    "date_added date DEFAULT CURRENT_TIMESTAMP);"
)

cur.execute(
    "INSERT INTO users(username, paid)"
    "VALUES ('paidPlan', '1');"
)

cur.execute(
    "INSERT INTO users(username, paid)"
    "VALUES ('freePlan', '0');"
)

cur.execute(
    "INSERT INTO users(username, paid)"
    "VALUES ('Xavier', '0');"
)

cur.execute(
    "INSERT INTO users(username, paid)"
    "VALUES ('Pol', '1');"
)

conn.commit()

cur.close()
conn.close()
