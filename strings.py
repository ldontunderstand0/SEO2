import dbase as db


def profile(user_id, user_name):
    accepted = db.request('DISTINCT task_id', 'answers', 'user_id', user_id, 'error_number', 0)
    th = f'<\n\nПрофиль {user_name}\n\nВаши кубки:\n'
    for t in db.request('*', 'themes'):
        count = 0
        for elem in accepted:
            if t[1] == db.request('theme_id', 'tasks', 'id', elem[0])[0][0]:
                count += 1
        full = len(db.request('id', 'tasks', 'theme_id', t[0]))
        if full == 0:
            full += 1
        if count / full > 0.75:
            th += f'\n🏆 Раздел {t[1]}'
    th += '\n\nКубки выдаются, только если вы решили более 75% раздела\n\n>'
    return th


def themes(user_id):
    accepted = db.request('DISTINCT task_id', 'answers', 'user_id', user_id, 'error_number', 0)
    th = '<\n\nВыберите раздел для решения задач:\n'
    for t in db.request('*', 'themes'):
        count = 0
        for elem in accepted:
            if t[1] == db.request('theme_id', 'tasks', 'id', elem[0])[0][0]:
                count += 1
        full = len(db.request('id', 'tasks', 'theme_id', t[0]))
        th += f'\n{t[1]}) {t[2]}'
        th += f'\nрешено задач: {count} из {full}\n'
    th += '\n>'
    return th


def tasks(user_id, idx):
    accepted = db.request('DISTINCT task_id', 'answers', 'user_id', user_id, 'error_number', 0)
    th = '<\n\nВыберите задачу:\n'
    symbol = '🟡'
    for elem in db.request('*', 'tasks', 'theme_id', idx):
        for el in accepted:
            if el[0] == elem[0]:
                symbol = '🟢'
                break
            symbol = '🟡'
        th += f'\n{symbol} Задача {elem[2]}. "{elem[3]}"'
    th += '\n\n>'
    return th


def question(theme, idx):
    th = db.request('title, description, input_text, output_text', 'tasks', 'theme_id', theme, 'number', idx)
    return f'<\n\nЗадача "{th[0][0]}"\n\n{th[0][1]}\n\nВходные данные:\n{th[0][2]}\n\nВыходные данные:\n{th[0][3]}\n\n>'


state = ''

hello = '< Добро пожаловать! >'

back = '< возвращаемся назад >'
