from datetime import date
import sqlite3

def add_task(title, description, status, user_id):
    connection = sqlite3.connect('todo.db')
    connection.execute('PRAGMA foreign_keys = on')
    if not title:
        raise ValueError("Task title cannot be empty.")
    if len(title) > 50:
        raise ValueError("Task title cannot exceed 50 characters.")
    cur = connection.cursor()
    try : 
        cur.execute("INSERT INTO tasks (title, description,created_date,status, user_id) VALUES (?,?,?,?,?)",
                    (title, description, date.today().isoformat(), status, user_id))
        connection.commit()
    finally:
        connection.close()

def edit_task(task_number, new_title, new_description, new_status, user_id):
    connection = sqlite3.connect('todo.db')
    connection.execute('PRAGMA foreign_keys = on')
    cur = connection.cursor()
    try : 
        cur.execute("""UPDATE tasks
                        SET title = ?,
                            description = ?,
                            status = ?
                            where id = ? and user_id = ?""",
                            (new_title, new_description, new_status, task_number, user_id))
        connection.commit()
    finally:
        connection.close()    

def delete_task(task_number, user_id):
    connection = sqlite3.connect('todo.db')
    connection.execute('PRAGMA foreign_keys = on')
    cur = connection.cursor()
    try : 
        cur.execute("""delete from tasks
                        where id = ? and user_id = ?""",
                            (task_number,user_id))
        connection.commit()
    finally:
        connection.close()   

def load_tasks(user_id):
    connection = sqlite3.connect('todo.db')
    cur = connection.cursor()
    try : 
        cur.execute('Select * from tasks where user_id = ?', (user_id,))
        return cur.fetchall()
    finally:
        connection.close()