import sqlite3
from db import queries
from config import db_path
import datetime

def init_db():
    # соединение с бд
    conn = sqlite3.connect(db_path)
    # курсор для выполнения sql запросов
    cursor = conn.cursor()
    # выполняем sql запрос
    cursor.execute(queries.CREATE_TABLE)
    conn.commit()
    conn.close()

def get_task(filter_type='all'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    if filter_type == 'completed':
        cursor.execute(queries.SELECT_COMPLETED)
    elif filter_type == 'not_completed':
        cursor.execute(queries.SELECT_NOT_COMPLETED)
    else:
        cursor.execute(queries.SELECTS)
    
    tasks = cursor.fetchall()
    conn.close()
    return tasks

# берем из поля ввода текст и добавляем его в список
def add_task_db(task):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    date_str = datetime.datetime.now().strftime("%d.%m.%Y") 
    cursor.execute(queries.INSERTS, (task, date_str))
    conn.commit()
    # получение id
    task_id = cursor.lastrowid
    conn.close()
    return task_id


def update_task_db(task_id, completed=None):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor() 
    if completed is not None:
        cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (completed, task_id))
    conn.commit()
    conn.close()


def delete_task_id(task_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(queries.DELETE, (task_id, ))
    conn.commit()


    

    rows = cursor.fetchall()
    conn.close()
    return rows
