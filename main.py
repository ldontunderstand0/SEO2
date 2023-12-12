import telebot
import os

import contester
import strings as ss
import buttons
import dbase as db

bot = telebot.TeleBot("6536650678:AAFjKjrDqLEYhr2L6IgUu4tm-hKVZghqbds")
theme = 0
task = 0
admin_panel = [-1, -1, []]


@bot.message_handler(commands=['admin'])
def start_message(message):
    ss.state = 'admin'
    bot.send_message(message.chat.id, ss.hello, reply_markup=buttons.admin)


@bot.message_handler(commands=['start'])
def start_message(message):
    try:
        os.mkdir(f'users/{message.from_user.id}')
        os.mkdir(f'users/{message.from_user.id}/programs')
    except FileExistsError:
        pass
    ss.state = 'main'
    db.user(message.from_user.id, message.from_user.username)
    bot.send_message(message.chat.id, ss.hello, reply_markup=buttons.main)


@bot.message_handler(content_types=['text', 'document'])
def get_text_messages(message):
    global theme
    global task
    match ss.state:

        case 'admin':
            if admin_panel[1] > 0:
                admin_panel[2].append(message.text)
                admin_panel[1] -= 1
            else:
                match admin_panel[0]:
                    case 0:
                        db.user(admin_panel[2][0], admin_panel[2][1])
                        admin_panel[2] = []
                        admin_panel[0] = -1
                        bot.send_message(message.chat.id, 'Успешно', reply_markup=buttons.admin)
                    case 1:
                        db.theme(admin_panel[2][0], admin_panel[2][1], admin_panel[2][2])
                        admin_panel[2] = []
                        admin_panel[0] = -1
                        bot.send_message(message.chat.id, 'Успешно', reply_markup=buttons.admin)
                    case 2:
                        db.task(admin_panel[2][0], admin_panel[2][1], admin_panel[2][2], admin_panel[2][3],
                                admin_panel[2][4], admin_panel[2][5], admin_panel[2][6])
                        admin_panel[2] = []
                        admin_panel[0] = -1
                        bot.send_message(message.chat.id, 'Успешно', reply_markup=buttons.admin)
            match message.text:
                case 'Добавить пользователя':
                    admin_panel[0] = 0
                    admin_panel[1] = 2
                case 'Добавить раздел':
                    admin_panel[0] = 1
                    admin_panel[1] = 3
                case 'Добавить задачу':
                    admin_panel[0] = 2
                    admin_panel[1] = 7

        case 'main':
            match message.text:
                case 'Разделы':
                    ss.state = 'theme'
                    bot.send_message(message.from_user.id, ss.themes(message.from_user.id),
                                     reply_markup=buttons.group('number', 'themes'))
                case 'Профиль':
                    ss.state = 'profile'
                    bot.send_message(message.from_user.id, ss.profile(message.from_user.id, message.from_user.username),
                                     reply_markup=buttons.task)

        case 'theme':
            match message.text:
                case 'Назад':
                    ss.state = 'main'
                    bot.send_message(message.chat.id, ss.back)
                    bot.send_message(message.chat.id, ss.hello, reply_markup=buttons.main)
            if message.text.isdigit():
                ss.state = 'task'
                idx = int(message.text)
                theme = idx
                bot.send_message(message.chat.id, ss.tasks(message.from_user.id, idx),
                                 reply_markup=buttons.group('number', 'tasks', 'theme_id', idx))

        case 'task':
            match message.text:
                case 'Назад':
                    ss.state = 'theme'
                    bot.send_message(message.chat.id, ss.back)
                    bot.send_message(message.chat.id, ss.themes(message.from_user.id),
                                     reply_markup=buttons.group('number', 'themes'))
            if message.text.isdigit():
                ss.state = 'answer'
                idx = int(message.text)
                task = idx
                bot.send_message(message.chat.id, ss.question(theme, idx), reply_markup=buttons.task)

        case 'answer':
            idx = db.request('id', 'tasks', 'number', task, 'theme_id', theme)[0][0]
            path = f'users/{message.from_user.id}/programs/prog{idx}.py'
            mode = 'w'
            match message.text:
                case 'Назад':
                    ss.state = 'task'
                    bot.send_message(message.chat.id, ss.back)
                    bot.send_message(message.chat.id, ss.tasks(message.from_user.id, theme),
                                     reply_markup=buttons.group('number', 'tasks', 'theme_id', theme))
                case _:
                    downloaded_file = message.text
                    if message.document:
                        file = bot.get_file(message.document.file_id)
                        downloaded_file = bot.download_file(file.file_path)
                        mode = 'wb'
                    f = open(path, mode)
                    f.write(downloaded_file)
                    f.close()
                    err = contester.main('prog' + str(idx), f'users/{message.from_user.id}/programs/prog{idx}.py')
                    db.answer(len(db.request('id', 'answers')), message.from_user.id, idx, 0, err)
                    if not err:
                        err_message = '< Задача решена! >'
                    else:
                        err_message = f'< Неверный ответ : тест {err} >'
                    bot.send_message(message.chat.id, err_message, reply_markup=buttons.task)

        case 'profile':
            match message.text:
                case 'Назад':
                    ss.state = 'main'
                    bot.send_message(message.chat.id, ss.back)
                    bot.send_message(message.chat.id, ss.hello, reply_markup=buttons.main)


bot.polling(none_stop=True, interval=0)
