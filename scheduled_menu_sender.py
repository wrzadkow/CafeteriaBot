import telebot
from tinydb import TinyDB, Query
import datetime

weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday']
db = TinyDB('db.json')
db_query = Query()

interested_chats = db.all()

with open('token.txt') as token_file:  #token from BotFather stored in separate token.txt file
    token=token_file.readline()
token=token.rstrip('\n') #readline() leaves '\n' at the end which causes 404 error
bot = telebot.TeleBot(token)

today = datetime.datetime.today().weekday() #today's day of the week

if today<5: # week, not weekend
    with open(weekdays[today]+'.txt') as menu_file:
        message = menu_file.read()
    for chat in interested_chats:
        chat_id=chat['id_of_willing_chat']
        try:
            bot.send_message(chat_id,message)
        except telebot.apihelper.ApiException as e:
            print(e)



