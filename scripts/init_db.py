import os
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="flask_db",
    user="postgres",
    password="postgres",
)

cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS users;")
cur.execute(
    "CREATE TABLE users (id serial PRIMARY KEY,"
    "username varchar (50) NOT NULL,"
    "paid BOOLEAN NOT NULL,"
    "date_added date DEFAULT CURRENT_TIMESTAMP);"
)

cur.execute("DROP TABLE IF EXISTS uploads;")
cur.execute(
    "CREATE TABLE uploads (id serial PRIMARY KEY,"
    "sid varchar (50) UNIQUE NOT NULL,"
    "remove varchar (50) NOT NULL,"
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
