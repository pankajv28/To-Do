import sqlite3

def init_db():
    connection = sqlite3.connect('todo.db')
    connection.execute('PRAGMA foreign_keys = ON')

    try:
        cur = connection.cursor()
        #create users table
        cur.execute("""CREATE TABLE IF NOT EXISTS "users" (
                        id INTEGER PRIMARY KEY,

                        username TEXT NOT NULL UNIQUE
                            CHECK (length(username) BETWEEN 1 AND 15),

                        displayname TEXT NOT NULL CHECK (length(displayname) BETWEEN 1 AND 15),

                        password_hash TEXT NOT NULL,

                        creator_id INTEGER,

                        created_at TEXT NOT NULL
                            DEFAULT (datetime('now')),

                        role TEXT NOT NULL DEFAULT 'app'
                            CHECK (role IN ('app', 'admin', 'super')),

                        FOREIGN KEY (creator_id)
                            REFERENCES "users"(id)
                            ON DELETE SET NULL
                    );""")

        #create projects table
        cur.execute("""CREATE TABLE IF NOT EXISTS "projects" (
                        id INTEGER PRIMARY KEY,

                        name TEXT NOT NULL
                            CHECK (length(name) BETWEEN 1 AND 30),

                        description TEXT,

                        creator_id INTEGER NOT NULL,

                        created_at TEXT NOT NULL
                            DEFAULT (datetime('now')),

                        FOREIGN KEY (creator_id)
                            REFERENCES "users"(id)
                            ON DELETE RESTRICT
                    );""")

        #create user_project_mapping table
        cur.execute("""CREATE TABLE IF NOT EXISTS "user_project_mapping" (
                        user_id INTEGER NOT NULL,

                        project_id INTEGER NOT NULL,

                        PRIMARY KEY (user_id, project_id),

                        FOREIGN KEY (user_id)
                            REFERENCES "users"(id)
                            ON DELETE CASCADE,

                        FOREIGN KEY (project_id)
                            REFERENCES "projects"(id)
                            ON DELETE CASCADE
                    );""")
        
        #create tasks table
        cur.execute("""CREATE TABLE IF NOT EXISTS 
                    tasks (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL
                            CHECK (length(title) BETWEEN 1 AND 50),

                        description TEXT,

                        status TEXT NOT NULL DEFAULT 'tostart'
                            CHECK (status IN (
                                'tostart',
                                'ongoing',
                                'done',
                                'skipped',
                                'archived',
                                'deleted'
                            )),

                        created_at TEXT NOT NULL DEFAULT (datetime('now')),

                        creator_id INTEGER NOT NULL,
                        project_id INTEGER NOT NULL,
                        doer_id INTEGER,

                        FOREIGN KEY (creator_id)
                            REFERENCES "users"(id)
                            ON DELETE RESTRICT,

                        FOREIGN KEY (project_id)
                            REFERENCES "projects"(id)
                            ON DELETE RESTRICT,

                        FOREIGN KEY (doer_id)
                            REFERENCES "users"(id)
                            ON DELETE SET NULL
                    );""")
        
        connection.commit()
    
    except Exception:
        connection.rollback()
        raise

    finally:    
        connection.close()

if __name__=='__main__':
    init_db()