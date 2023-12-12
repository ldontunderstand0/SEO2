from telebot import types
import dbase as db


def group(select, table, param_name=None, param=None):
    tasks = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = []
    for elem in db.request(select, table, param_name, param):
        item.append(types.KeyboardButton(f'{elem[0]}'))
    item.append(types.KeyboardButton('Назад'))
    tasks.add(*item)
    return tasks


main = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton('Разделы')
item2 = types.KeyboardButton('Профиль')
main.add(item1, item2)

empty = types.ReplyKeyboardRemove()

task = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton('Назад')
task.add(item1)

admin = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton('Добавить пользователя')
item2 = types.KeyboardButton('Добавить раздел')
item3 = types.KeyboardButton('Добавить задачу')
admin.add(item1, item2, item3)
