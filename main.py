from typing import Optional
from fastapi import FastAPI
import mariadb
import sys
from user import User

app = FastAPI()

def connect_to_db():
    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user="root",
            password="coscu2404",
            host="127.0.0.1",
            port=3306,
            database="redflix")
        conn.autocommit = True
        # Get Cursor
        return conn.cursor()
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

def get_users(cursor):
    cursor.execute("SELECT id, name, lastname, identity_number, phone, email FROM users")
    return cursor

def get_user_by_id(cursor, id):
    cursor.execute("SELECT id, name, lastname, identity_number, phone, email FROM users WHERE id=?", (id,))
    return cursor

def add_user(cursor, user: User):
    cursor.execute("INSERT INTO users (name, lastname, identity_number, phone, email) VALUES (?, ?, ?, ?, ?)", 
    (user.name, user.lastname, user.identity_number, user.phone, user.email,))

cur = connect_to_db()



@app.get("/users")
def read_users():
    users_db = get_users(cur)
    if users_db is None:
        return []
    users = []
    for (id, name, lastname, identity_number, phone, email) in users_db:
        user = User(id = id, identity_number = identity_number, name = name, lastname = lastname, phone = phone, email = email)
        users.append(user)
    
    return users

@app.get("/users/{user_id}")
def read_user_by_id(user_id: int):
    user_db = get_user_by_id(cur, user_id)
    for (id, name, lastname, identity_number, phone, email) in user_db:
        user = User(id = id, identity_number = identity_number, name = name, lastname = lastname, phone = phone, email = email)
        return user


@app.post("/users")
def read_item(user: User):
    try:
        add_user(cur, user)
    except Exception as e:
        print(e)
        return False
    return True
