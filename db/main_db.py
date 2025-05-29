import sqlite3
from db import queries
from config import db_path

def init_db():
    # соединение с бд
    conn = sqlite3.connect(db_path)
    # курсор для выполнения sql запросов
    cursor = conn.cursor()
    # выполняем sql запрос
    cursor.execute(queries.CREATE_TABLE)
    conn.commit()
    conn.close()

def get_buys(filter_type='all'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    if filter_type == 'bought':
        cursor.execute(queries.SELECT_BOUGHT)
    elif filter_type == 'not_bought':
        cursor.execute(queries.SELECT_NOT_BOUGHT)
    else:
        cursor.execute(queries.SELECTS)
    
    buys = cursor.fetchall()
    conn.close()
    return buys

# берем из поля ввода текст и добавляем его в список
def add_buy_db(purchase):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(queries.INSERTS, (purchase, ))
    conn.commit()
    # получение id
    purchase_id = cursor.lastrowid
    conn.close()
    return purchase_id


def update_buy_db(purchase_id, is_bought=None):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor() 
    if is_bought is not None:
        cursor.execute("UPDATE buys SET bought = ? WHERE id = ?", (is_bought, purchase_id))
    conn.commit()
    conn.close()


def delete_buy_id(purchase_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(queries.DELETE, (purchase_id, ))
    conn.commit()


def get_buys(filter_type='all'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if filter_type == 'bought':
        cursor.execute("SELECT id, purchase, bought FROM buys WHERE bought = 1")
    elif filter_type == 'not_bought':
        cursor.execute("SELECT id, purchase, bought FROM buys WHERE bought = 0")
    else:
        cursor.execute("SELECT id, purchase, bought FROM buys")

    rows = cursor.fetchall()
    conn.close()
    return rows
