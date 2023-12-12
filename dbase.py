import sqlite3


def tables():
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                id INTEGER,
                username TEXT
            )""")
    connect.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS themes(
                        id INTEGER,
                        number INTEGER,
                        title TEXT
                    )""")
    connect.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS tasks(
                        id INTEGER,
                        theme_id INTEGER,
                        number INTEGER,
                        title TEXT,
                        description TEXT,
                        input_text TEXT,
                        output_text TEXT
                    )""")
    connect.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS examples(
                            id INTEGER,
                            task_id INTEGER,
                            number INTEGER
                        )""")
    connect.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS answers(
                                id INTEGER,
                                user_id INTEGER,
                                task_id INTEGER,
                                number INTEGER,
                                error_number INTEGER
                            )""")
    connect.commit()


def user(idx, username):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()

    cursor.execute(f'SELECT id FROM users WHERE id = {idx}')
    data = cursor.fetchone()
    if data is None:
        cursor.execute(
            'INSERT INTO users (id, username) VALUES (?, ?);',
            [idx, username])
        connect.commit()


def theme(idx, number, title):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()

    cursor.execute(f'SELECT id FROM themes WHERE id = {idx}')
    data = cursor.fetchone()
    if data is None:
        cursor.execute(
            'INSERT INTO themes (id, number, title) VALUES (?, ?, ?);',
            [idx, number, title])
        connect.commit()


def task(idx, theme_id, number, title, description, input_text, output_text):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()

    cursor.execute(f'SELECT id FROM tasks WHERE id = {idx}')
    data = cursor.fetchone()
    if data is None:
        cursor.execute(
            'INSERT INTO tasks (id, theme_id, number, title, description, input_text, output_text)'
            ' VALUES (?, ?, ?, ?, ?, ?, ?);',
            [idx, theme_id, number, title, description, input_text, output_text])
        connect.commit()


def example(idx, task_id, number):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()

    cursor.execute(f'SELECT id FROM examples WHERE id = {idx}')
    data = cursor.fetchone()
    if data is None:
        cursor.execute(
            'INSERT INTO examples (id, task_id, number) VALUES (?, ?, ?);',
            [idx, task_id, number])
        connect.commit()


def answer(idx, user_id, task_id, number, error_number):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()

    cursor.execute(f'SELECT id FROM answers WHERE id = {idx}')
    data = cursor.fetchone()
    if data is None:
        cursor.execute(
            'INSERT INTO answers (id, user_id, task_id, number, error_number) VALUES (?, ?, ?, ?, ?);',
            [idx, user_id, task_id, number, error_number])
        connect.commit()


def request(select, table, param_name1=None, param1=None, param_name2=None, param2=None):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    if param_name1 is None:
        return cursor.execute(f'SELECT {select} FROM {table}').fetchall()
    if param_name2 is None:
        return cursor.execute(f'SELECT {select} FROM {table} WHERE {param_name1} = {param1}').fetchall()
    return cursor.execute(f'SELECT {select} FROM {table} '
                          f'WHERE {param_name1} = {param1} AND {param_name2} = {param2}').fetchall()
