from Functions.admin import admin as activate_admin
import sqlite3 as sq
import os

os.chdir('Database')
db = sq.connect('shop.db')
cur = db.cursor()
os.chdir('..')

#Инициализация БД
async def db_start():

    cur.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER     PRIMARY KEY, 
    username            TEXT, 
    name                TEXT, 
    balance             INTEGER)''') # ТАБЛИЦА ПОЛЬЗОВАТЕЛЕЙ
    db.commit()

    cur.execute('''CREATE TABLE IF NOT EXISTS goods (
    good_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    good_name        TEXT,
    good_cost        INTEGER,
    good_code        TEXT,
    good_category    TEXT,
    good_description TEXT,
    good_photo       TEXT)''') # ТАБЛИЦА ТОВАРОВ
    db.commit()

    cur.execute('''CREATE TABLE IF NOT EXISTS checks (
    check_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id  INTEGER,
    money    INTEGER,
    bill_id  TEXT)''') # ТАБЛИЦА ВЫПИСАННЫХ СЧЕТОВ
    db.commit()

    cur.execute('''CREATE TABLE IF NOT EXISTS comments (
    id_comment INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER,
    username   TEXT,
    comment    TEXT,
    rate       INTEGER)''') # ТАБЛИЦА ОТЗЫВОВ
    db.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS admins(username TEXT PRIMARY KEY)")  # ТАБЛИЦА АДМИНОВ
    db.commit()

# Создание профиля пользователя
async def create_profile(user_id, username, user_firstname):
    user = cur.execute(f"SELECT 1 FROM users WHERE user_id == '{user_id}'").fetchone()
    # Если пользователя с данным id нет, создается новый
    if not user:

        # Вносятся данные, собранные при нажатии /start и баланс, равный 0
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


async def check_admin(bot, dp, username, user_id):
    cur.execute(f"SELECT username FROM admins WHERE username == '{username}'")  # берем список админов
    admin = cur.fetchone()
    if admin == None:

        pass

    else:

        # Если username есть в списке, то активируется функция админа
        await activate_admin(bot, dp, user_id, db)
