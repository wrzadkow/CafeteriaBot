import telebot
from tinydb import TinyDB, Query
import datetime

with open('token.txt') as token_file:  #token from BotFather stored in separate token.txt file
    token=token_file.readline()
token=token.rstrip('\n') #readline() leaves '\n' at the end which causes 404 error
bot = telebot.TeleBot(token)
  
@bot.message_handler(commands = ['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, """Hi! I can send you the menu listing the gourmet delices of the canteen on demand or daily in the morning.\n
    To get today's menu, use the /menu command. \n
    To subscribe to daily morning menu updates, use the /sub command. \n
    To unsubscribe, use the /unsub command. \n
    Psst..., I don't store any of your personal data, the ID of this chat is enough for me:). Enjoy your day.""")

@bot.message_handler(commands = ['sub'])
def handle_sub(message):
    db = TinyDB('db.json')
    db_query = Query()
    request_chat_id = message.chat.id
    query_results = db.search(db_query.id_of_willing_chat == request_chat_id)
    if not query_results:
        db.insert({'id_of_willing_chat' : request_chat_id})
        bot.reply_to(message,"Thanks for subscribing, you will now receive lunch menu every morning.")
    else:
        bot.reply_to(message,"Our records show you're already subscribed. Nothing changes, you'll still receive the menu.")
    
@bot.message_handler(commands = ['unsub'])
def handle_unsub(message):
    db = TinyDB('db.json')
    db_query = Query()
    request_chat_id = message.chat.id
    query_results = db.search(db_query.id_of_willing_chat == request_chat_id)
    if not query_results:
        bot.reply_to(message,"Our records show you're unsubscribed. Nothing changes, use /sub if you'd like to receive the menu.")
    else:
        db.remove(db_query.id_of_willing_chat == request_chat_id)
        bot.reply_to(message,"You will no longer recive the menu daily. Hope to see you soon!")

@bot.message_handler(commands = ['menu'])
def handle_unsub(message):
    today = datetime.datetime.today().weekday() 
    if today > 4: 
        bot.reply_to(message,"Today is weekend, the canteen is closed, the choice is between vending machine, pub or staying hungry :-(.")
    else:
        weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday']
        with open(weekdays[today]+'.txt') as menu_file:
            to_send = menu_file.read()
        chat_id = message.chat.id
        bot.send_message(chat_id,to_send)

@bot.message_handler(func = lambda message: True) #handle all other messages
def echo_all(message):
    bot.reply_to(message, "Sorry, I can't help you with this ;-(  Use the /help command to see what I can do for you. ")

bot.polling()


