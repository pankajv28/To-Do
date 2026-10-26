import sqlite3

def init_db():
    connection = sqlite3.connect('todo.db')
    cur = connection.cursor()

    try:
        #create users table
        cur.execute("""CREATE TABLE IF NOT EXISTS 
                        users (
                        user_id INTEGER PRIMARY KEY,
                        username TEXT UNIQUE NOT NULL CHECK (length(username)<=15),
                        password_hash TEXT NOT NULL);""")
        
        #create tasks table
        cur.execute("""CREATE TABLE IF NOT EXISTS 
                    tasks (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL CHECK (length(title)<=50),
                    description TEXT,
                    status TEXT CHECK (status in ('tostart','ongoing','done')),
                    created_date TEXT,
                    user_id INT,
                    
                    FOREIGN KEY (user_id) REFERENCES users(user_id));""")
        
        connection.commit()

    finally:    
        connection.close()

if __name__=='__main__':
    init_db()