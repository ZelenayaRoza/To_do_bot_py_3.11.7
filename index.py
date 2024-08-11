import telebot

token = "7189418573:AAGgh2uU2GwmEDCGagK_reLsDcTBqRhOGXc"

bot = telebot.TeleBot(token)

import random

RANDOM_TASKS = ['Покормить котиков', 'Написать письмо', 'Сделать чай']

HELP = """
/help - напечатать справку по программе.
/add - добавить задачу в список
/show - напечатать все добавленные задачи
/random - добавить случайную задачу на дату сегодня
"""

tasks = {}


def add_todo(date, task):
    if date in tasks:
        tasks[date].append(task)
    else:
        tasks[date] = [task]


@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.from_chat.id
    bot.send_message(message.chat.id, HELP)


@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, HELP)


@bot.message_handler(commands=["add"])
def add(message):
    text = "Введите дату задачи (в формате ГГГГ-ММ-ДД)"
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, ask_date)


def ask_date(message):
    date = message.text
    text = 'Введите название задачи'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, ask_task, date)


def ask_task(message, date):
    task = message.text
    add_todo(date, task)
    text = "Задача сохранена"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=["random"])
def random_add(message):
    date = "сегодня"
    task = random.choice(RANDOM_TASKS)
    add_todo(date, task)
    text = f'Задача "{task}" добавлена на дату {date}'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["show", "print"])
def show(message):
    text = "Введите дату"
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, send_task_list)


def send_task_list(message):
    date = message.text
    if date in tasks:
        text = date.upper() + "\n"
        for task in tasks[date]:
            text += "[] " + task + "\n"
    else:
        text = "Задач на эту дату нет"
    bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
