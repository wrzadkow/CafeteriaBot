import telebot
from tinydb import TinyDB, Query
import datetime

weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday']
db = TinyDB('db.json')
db_query = Query()

interested_chats = db.all()

with open('token.txt') as token_file:  # BotFather token stored in token.txt.
    token = token_file.readline()
token = token.rstrip('\n')  # readline() leaves '\n' at the end.
bot = telebot.TeleBot(token)

today = datetime.datetime.today().weekday()  # Today's day of the week

counter_attempts = 0
counter_fails = 0

if today < 5:  # Today is weekday
    with open(weekdays[today] + '.txt') as menu_file:
        message = menu_file.read()
    for chat in interested_chats:
        chat_id = chat['id_of_willing_chat']
        counter_attempts += 1
        try:
            bot.send_message(chat_id,message)
        except telebot.apihelper.ApiException as e:
            print(e)
            counter_fails += 1

print("Attempted to send to", counter_attempts, "people, failed in",
      counter_fails,"cases")



