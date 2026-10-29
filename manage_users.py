from werkzeug.security import generate_password_hash,check_password_hash
import sqlite3

def create_user(username, displayname, password, role):
    connection = sqlite3.connect('todo.db')
    connection.execute('PRAGMA foreign_keys = ON')
    cur = connection.cursor()

    try: 
        cur.execute('INSERT INTO users (username,displayname, password_hash, role) VALUES (?,?,?,?)',
                       (username, displayname, generate_password_hash(password), role))
        connection.commit()
        return True
    
    finally:
        connection.close()

def edit_user(username, displayname, password):
    connection = sqlite3.connect('todo.db')
    connection.execute('PRAGMA foreign_keys = ON')
    cur = connection.cursor()

    try:
        cur.execute('UPDATE users SET displayname = ?, password_hash = ? where username = ?',
                           (displayname, generate_password_hash(password),username))
        if cur.rowcount > 0:
            connection.commit()
            return True
        else :
            return False

    finally:
        connection.close()

def login_user(username,password):
    connection = sqlite3.connect('todo.db')
    connection.execute('PRAGMA foreign_keys = ON')
    cur = connection.cursor()

    try:
        cur.execute('select password_hash, displayname, id, role from users where username = ?',
                           (username,))
        result = cur.fetchone()
        if result is None:
            return False, False, False

        password_hash, name, user_id, role = result
        return check_password_hash(password_hash,password), name, user_id, role


    finally:
        connection.close()

def show_users():
    connection = sqlite3.connect('todo.db')
    connection.execute('PRAGMA foreign_keys = ON')
    cur = connection.cursor()

    try:
        cur.execute('select username, displayname, role from users')
        users = cur.fetchall()
        if users is None:
            return False
        return users


    finally:
        connection.close()

def delete_user(username):
    connection = sqlite3.connect('todo.db')
    connection.execute('PRAGMA foreign_keys = ON')
    cur = connection.cursor()

    try: 
        cur.execute('DELETE from users where username = ?',(username,))
        connection.commit()
        return True
    
    finally:
        connection.close()