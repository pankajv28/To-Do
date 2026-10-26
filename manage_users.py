from werkzeug.security import generate_password_hash,check_password_hash
import sqlite3

def create_user(username, password, group):
    connection = sqlite3.connect('todo.db')
    cur = connection.cursor()

    try: 
        cur.execute('INSERT INTO users (username,password_hash,"group") VALUES (?,?,?)',
                       (username,generate_password_hash(password), group))
        connection.commit()
        return True
    
    finally:
        connection.close()

def edit_password(username, password):
    connection = sqlite3.connect('todo.db')
    cur = connection.cursor()

    try:
        cur.execute('UPDATE users SET password_hash = ? where username = ?',
                           (generate_password_hash(password),username))
        if cur.rowcount > 0:
            connection.commit()
            return True
        else :
            return False

    finally:
        connection.close()

def login_user(username,password):
    connection = sqlite3.connect('todo.db')
    cur = connection.cursor()

    try:
        cur.execute('select password_hash, user_id, "group" from users where username = ?',
                           (username,))
        result = cur.fetchone()
        if result is None:
            return False, False, False

        password_hash, user_id, group = result
        return check_password_hash(password_hash,password), user_id, group


    finally:
        connection.close()

def show_users():
    connection = sqlite3.connect('todo.db')
    cur = connection.cursor()

    try:
        cur.execute('select username, "group" from users')
        users = cur.fetchall()
        if users is None:
            return False
        return users


    finally:
        connection.close()

def delete_user(username):
    connection = sqlite3.connect('todo.db')
    cur = connection.cursor()

    try: 
        cur.execute('DELETE from users where username = ?',(username,))
        connection.commit()
        return True
    
    finally:
        connection.close()