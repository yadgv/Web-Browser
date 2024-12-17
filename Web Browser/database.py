import sqlite3

CREATE_TASKS_TABLE = "CREATE TABLE IF NOT EXISTS Tasks(id INTEGER PRIMARY KEY, name TEXT, Difficulty INTEGER, Do TEXT);"

INSERT_TASK = "INSERT INTO Tasks(name, Difficulty, Do) VALUES(?,?,?);"

GET_ALL_TASKS = "SELECT * FROM Tasks;"
GET_TASKS_BY_NAME = "SELECT * FROM Tasks WHERE name = ?;"





def connect():
    return sqlite3.connect("date.db")

def create_tables(connection):
  with connection:
    connection.execute(CREATE_TASKS_TABLE)

def addTask(connection, name, Difficulty, Do):
    with connection:
        connection.execute(INSERT_TASK, (name, Difficulty, Do))

def getAllTasks(connection):
    with connection:
        return connection.execute(GET_ALL_TASKS).fetchall()

def getTasksByName(connection, name):
    with connection:
        return connection.execute(GET_TASKS_BY_NAME, (name,)).fetchall()

def deleteTask(connection, id):
    with connection:
        connection.execute("DELETE FROM Tasks WHERE id=?;", (id,))