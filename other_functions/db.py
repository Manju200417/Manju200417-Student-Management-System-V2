import sqlite3

def get_db():
    db = sqlite3.connect("Data_base.db")
    db.execute("PRAGMA foreign_keys = ON")
    return db
    

def init_db():
    with get_db() as db:

        

        #for user data table
        db.execute('''
                create table if not exists users (
                    id integer primary key autoincrement,
                    Name text,
                    Email text,
                    username text unique,
                    password text ,
                    is_admin integer default 0
                   )'''
                   )

        # for student data table
        db.execute('''
                create table if not exists students (
                id integer,
                name text, 
                age integer,
                course text,
                year integer,
                username text,
                user_id integer, 
                unique(id, user_id),
                foreign key(user_id) references users(id) on delete cascade)''')