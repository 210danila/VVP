import telebot
from datetime import datetime, date, time
from telebot import types
import psycopg2

token = "5040350284:AAEzgUqVdWQLlGlv2fe0PqEZ334jkF6c2Ks"

bot = telebot.TeleBot(token)


conn = psycopg2.connect(database="timetable",
                        user="postgres",
                        password="1234",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()

start = date(2021, 12, 12) # Start date
d = datetime.now() # Today
week = (d.isocalendar()[1] - start.isocalendar()[1]) % 2 + 1 # Counting number of week now
print(week)
days_of_week = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота']


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row('Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Расписание на текущую неделю', 'Расписание на следующую неделю', "/help")
    bot.send_message(message.chat.id, 'Здравствуйте! Чего вы хотите?', reply_markup=keyboard)


@bot.message_handler(commands=['week'])
def start(message):
    bot.send_message(message.chat.id, week)


@bot.message_handler(commands=['mtuci'])
def start(message):
    bot.send_message(message.chat.id, "Офицальный сайт МТУСИ – https://mtuci.ru/")


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Я умею знакомиться и отвечать на глупые вопросы, например: \
        Где ты живешь?\
        Что ты любишь?')


@bot.message_handler(content_types=['text'])
def answer(message):
    text_input = message.text.lower()


    if days_of_week.count(text_input) != 0: # для одного из дней
        cursor.execute("SELECT * FROM struct.timetable WHERE day=%s", (str(text_input),))
        records = list(cursor.fetchall())

        message_ = ''
        bot.send_message(message.chat.id, text_input)
        for i in range(0, len(records)):
            if records[i][5] == str(week) or records[i][5] =='0':
                subject = records[i][2]
                cursor.execute("SELECT * FROM struct.teacher WHERE subject=%s", (str(subject),))
                records1 = list(cursor.fetchall())
                full_name = records1[0][1]

                message_ += str(records[i][2]) + '\n' + str(records[i][3]) + '\n' + str(records[i][4]) + '\n' + str(full_name)
                bot.send_message(message.chat.id, message_)
                message_ = ''


    elif text_input == 'расписание на текущую неделю' or text_input == 'расписание на следующую неделю':
        day_of_week = ''

        if text_input == 'расписание на следующую неделю':
            week1 = (week % 2) + 1
        else:
            week1 = week

        for j in range(0, len(days_of_week)):
            day_of_week = days_of_week[j]

            
            cursor.execute("SELECT * FROM struct.timetable WHERE day=%s", (str(day_of_week),))
            records = list(cursor.fetchall())

            message_ = ''
            bot.send_message(message.chat.id, day_of_week)
            for i in range(0, len(records)):
                if records[i][5] == str(week1) or records[i][5] =='0':
                    subject = records[i][2]
                    cursor.execute("SELECT * FROM struct.teacher WHERE subject=%s", (str(subject),))
                    records1 = list(cursor.fetchall())
                    full_name = records1[0][1]

                    message_ += str(records[i][2]) + '\n' + str(records[i][3]) + '\n' + str(records[i][4]) + '\n' + str(full_name)
                    bot.send_message(message.chat.id, message_)
                    message_ = ''
    

    else:
        bot.send_message(message.chat.id, 'Извините, я вас не понял.')


bot.polling(none_stop=True, interval=0)