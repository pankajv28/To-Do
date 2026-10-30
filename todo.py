from datetime import date
import sqlite3

def add_task(title, description, status, project_id, user_id):
    connection = sqlite3.connect('todo.db')
    connection.execute('PRAGMA foreign_keys = on')
    if not title:
        raise ValueError("Task title cannot be empty.")
    if len(title) > 50:
        raise ValueError("Task title cannot exceed 50 characters.")
    cur = connection.cursor()
    try : 
        cur.execute("INSERT INTO tasks (title, description, status, project_id, creator_id, doer_id) VALUES (?,?,?,?,?,?)",
                    (title, description, status, project_id, user_id, user_id))
        connection.commit()
    finally:
        connection.close()

def edit_task(task_number, new_title, new_description, new_status):
    connection = sqlite3.connect('todo.db')
    connection.execute('PRAGMA foreign_keys = on')
    cur = connection.cursor()
    try : 
        cur.execute("""UPDATE tasks
                        SET title = ?,
                            description = ?,
                            status = ?
                            where id = ?""",
                            (new_title, new_description, new_status, task_number))
        connection.commit()
    finally:
        connection.close()    

def delete_task(task_number):
    connection = sqlite3.connect('todo.db')
    connection.execute('PRAGMA foreign_keys = on')
    cur = connection.cursor()
    try : 
        cur.execute("""delete from tasks
                        where id = ?""",
                            (task_number,))
        connection.commit()
    finally:
        connection.close()   

def archive_task(task_number):
    connection = sqlite3.connect('todo.db')
    connection.execute('PRAGMA foreign_keys = on')
    cur = connection.cursor()
    try : 
        cur.execute("""UPDATE tasks
                        SET status = "archived"
                        where id = ? """,
                            (task_number,))
        connection.commit()
    finally:
        connection.close()

def restore_task(task_number):
    connection = sqlite3.connect('todo.db')
    connection.execute('PRAGMA foreign_keys = on')
    cur = connection.cursor()
    try : 
        cur.execute("""UPDATE tasks
                        SET status = "done"
                        where id = ? """,
                            (task_number,))
        connection.commit()
    finally:
        connection.close() 

def load_tasks(project_id):
    connection = sqlite3.connect('todo.db')
    connection.execute('PRAGMA foreign_keys = ON')
    cur = connection.cursor()
    try : 
        cur.execute('Select * from tasks where project_id = ?', (project_id,))
        return cur.fetchall()
    finally:
        connection.close()

def get_user_projects(user_id):
    connection = sqlite3.connect('todo.db')
    connection.execute('PRAGMA foreign_keys = ON')
    cur = connection.cursor()
    try :
        cur.execute("""SELECT p.id, p.name
            FROM projects AS p
            JOIN user_project_mapping AS m
                ON p.id = m.project_id
            WHERE m.user_id = ?
            ORDER BY p.name""", (user_id,))
        return cur.fetchall();
    finally:
        connection.close()
