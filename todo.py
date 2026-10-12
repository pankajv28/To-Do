from datetime import date
import sqlite3

statuses = (
    'TOSTART',
    'ONGOING',
    'COMPLETED'
)

def init_db():
    connection = sqlite3.connect('tasks.db')

    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                title VARCHAR(50) NOT NULL,
                description TEXT,
                status VARCHAR(10)
                    CHECK (status IN ('TOSTART', 'ONGOING', 'COMPLETED')),
                createdate TEXT,
                user_id INTEGER
            )
        """)
        connection.commit()

        cursor = connection.cursor()
        cursor.execute("""
                        CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL UNIQUE,
                            password_hash TEXT NOT NULL
                        );
                    """)
        
        connection.commit()
        
    finally:
        connection.close()

def load_tasks(userid):
    connection = sqlite3.connect('tasks.db')
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM tasks where user_id = ?', (userid,))
        tasks = (cursor.fetchall())
        print (tasks)
        return tasks
    finally:
        connection.close()
    
def add_task(userid,title,description,status):
    title = title.strip()
    description = description.strip()

    connection = sqlite3.connect('tasks.db')
    if title :
        try:
            cursor = connection.cursor()
            cursor.execute('INSERT into tasks (title, description, status, createdate, user_id) VALUES (?,?,?,?,?)',
                           (title, description, status, date.today().isoformat(),userid))
            connection.commit()
        finally:
            connection.close()
    else : 
        raise ValueError('Description cannot be empty')

def edit_task(userid,number, new_title, new_description, new_status):
    new_title = new_title.strip()
    new_description = new_description.strip()
    
    connection = sqlite3.connect('tasks.db')

    try:
        cursor = connection.cursor()
        cursor.execute("""UPDATE tasks 
                       SET title = (?),
                       description = (?),
                       status = (?)
                       where id = (?) AND user_id = ?"""
                       , (new_title, new_description, new_status, number, userid))
        connection.commit()
    finally:
        connection.close()
            
def delete_task(userid, number):
    connection = sqlite3.connect('tasks.db')

    try:
        cursor = connection.cursor()
        cursor.execute("""DELETE from tasks
                       where id = ? AND user_id = ? """,(number, userid))
        connection.commit()
    finally:
        connection.close()

def ask_status(prompt):
    input_status = input(f'{prompt} {"/".join(statuses)} ').strip().upper()
    if input_status not in statuses:
        raise ValueError('Status is invalid')
    else:
        return input_status
    
def ask_number(prompt):
    try: 
        return int(input(prompt))
    except:
        raise ValueError('Input has to be a whole number')

def ask_user():
    try:
        return( int(input('USER ID : ')))
    except:
        raise ValueError('USER ID has to be a whole number')
    
def main():

    init_db()

    while True:
        command = input(' What to do add/edit/delete/list/quit > ')
        try:
            match(command.lower().strip()):
                case "add":
                    add_task(ask_user(), input("Title : "),input("Description : "),ask_status('Status : '))
                case "list":
                    load_tasks(ask_user())
                case "delete":
                    delete_task(ask_user(), ask_number('Task Number :'))
                case "edit":
                    edit_task(ask_user(), ask_number('Task Number : '),input("New Title : "),input("New Description : "),ask_status('New Status : '))
                case "quit":
                    print('Goodbye!')
                    break
                case _:
                    print("Unknown command")
        except (ValueError) as e:
            print(f'Invalid input: {e}')

if __name__ == '__main__':
    main()