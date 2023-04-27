import sqlite3 as sq

db = sq.connect('shop.db')
cur = db.cursor()


async def db_start():

    cur.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER     PRIMARY KEY, 
    username            TEXT, 
    name                TEXT, 
    balance             INTEGER)''') #ТАБЛИЦА ПОЛЬЗОВАТЕЛЕЙ
    db.commit()

    cur.execute('''CREATE TABLE IF NOT EXISTS goods (
    good_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    good_name     TEXT,
    good_cost     INTEGER,
    good_code     TEXT,
    good_category TEXT)''') #ТАБЛИЦА ТОВАРОВ
    db.commit()

    cur.execute('''CREATE TABLE IF NOT EXISTS checks (
    check_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id  INTEGER,
    money    INTEGER,
    bill_id  TEXT)''') #ТАБЛИЦА ВЫПИСАННЫХ СЧЕТОВ
    db.commit()

    cur.execute('''CREATE TABLE IF NOT EXISTS comments (
    id_comment INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER,
    username   TEXT,
    comment    TEXT,
    rate       INTEGER)''') #ТАБЛИЦА ОТЗЫВОВ


async def create_profile(user_id, username, user_firstname):
    user = cur.execute(f"SELECT 1 FROM users WHERE user_id == '{user_id}'").fetchone()
    if not user:
        cur.execute("INSERT INTO users VALUES(?, ?, ?, 0)", (user_id, username, user_firstname))
        db.commit()

async def set_money(user_id, money):

    bal = cur.execute(f'SELECT balance FROM users WHERE user_id == "{user_id}"').fetchone()
    balance = int(bal[0])

    new_balance = balance + money

    cur.execute(f'UPDATE users SET balance = "{new_balance}"')
    db.commit()

async def create_check(user_id, money, bill_id):

    cur.execute(f'INSERT INTO checks (user_id, money, bill_id) VALUES ({user_id}, {money}, {bill_id})')
    db.commit()
