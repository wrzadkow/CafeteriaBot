import telebot
import datetime
import numpy as np

class RatingHandler:

    def __init__(self, init_bot = None, init_chatid = None):
        self.bot = init_bot or None 
        self.chat_id = init_chatid or None
    
    def MesCheat(self): 
        return "Don't cheat please ;). You already voted today." 

    def MesNoRatings(self): 
        return "Nobody voted today yet, sorry." 

    def MesThanks(self,rating):
        thanks = "All done, thanks for voting! "
        lunch_feeling = {
            1: "I'm sorry for your horrible experience with today's food. ",
            2: "Meh, hope next time you'll get better food. ",
            3: "I'm glad that you fairly enjoyed today's lunch! ",
            4: "I'm so excited about your food happiness! " }
        conclusion = "You can access today's stats using /stats command. We keep previous ones for further analyses."
        return thanks+lunch_feeling[rating]+conclusion

    def MesHelpless(self):
        return "Sorry, I can't help you with this ;-(  Use the /help command to see what I can do for you. "

    def MesAskDish(self):
        return "Okay, rating. Which dish did you have today?"

    def MesAskRating(self):
        return "Thanks for letting me know your dish. What was the taste?"
    
    def ReadLunchesFromTxt(self, truncation):
        #truncation -- after how many spaces to truncate lunch string 
        #(e.g. "international beef steak" insatead of full name if truncation=3)
        today = datetime.datetime.today().weekday() 
        weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday']
        with open(weekdays[today]+'.txt') as menu_file:
            menu = menu_file.read()
        menu=menu.splitlines()
        positions=[5,7,9] #lines corresponding to three menus
        def TruncAt(st, occurence, nth): #Returns string s truncated at the nth occurrence of the delimiter d.
            return occurence.join(st.split(occurence)[:nth])        
        lunches = [TruncAt(menu[position],' ',truncation) for position in positions]
        return lunches

    def GenerateStatsReport(self, responses, truncation):
        #responses: the query results from TinyDB
        #truncation: where to truncate the lnuches in the report
        votes = [[],[],[]] #lists of votes for each dish
        strings = [] #vote strings to display to users
        for entry in responses:
            dish = entry['Dish']
            rating = entry['Rating']
            votes[dish-1].append(rating)
        lunch_names = self.ReadLunchesFromTxt(truncation) 
        for i in range(len(votes)):
            if not votes[i]:
                auxiliary_string = "No ratings yet"
            else:
                auxiliary_string =  '%.1f/4' % np.mean(votes[i])  
                auxiliary_string += ' from ' +str(len(votes[i]))+' votes'
            strings.append( "Dish "+str(i+1)+':\n' + auxiliary_string + '\n'+lunch_names[i]+'\n' ) 
        return '\n'.join(strings)

    def DishKeyboard(self):
        lunches = self.ReadLunchesFromTxt(truncation = 3)
        markup = telebot.types.ReplyKeyboardMarkup()
        items = [telebot.types.KeyboardButton(str(i+1)+'. ' + lunches[i]) for i in range(len(lunches))]
        markup.row(items[0])
        markup.row(items[1])
        markup.row(items[2])
        return markup

    def RatingKeyboard(self):
        markup = telebot.types.ReplyKeyboardMarkup()
        item1 = telebot.types.KeyboardButton('4. Simply delectable!')
        item2 = telebot.types.KeyboardButton('3. So-so, but tasty.')
        item3 = telebot.types.KeyboardButton('2. Kinda insipid, but edible.')
        item4 = telebot.types.KeyboardButton('1. Simply stomach-churning :-(.')
        markup.row(item1, item2)
        markup.row(item3, item4)
        return markup

    #State is:
    #0 - user did not intend to vote
    #1 - user submitted /rate command
    #2 - user sumbmitted their dish
    #3 - user submitted its rating

    #Handles the case when a message from user starts from '1' '2' '3' '4'
    def HandleDigit(self, digit, state, message, database, query):
        if state == 0 or state == 3:
            self.bot.reply_to(message, self.MesHelpless())
            self.bot.send_message(self.chat_id, "", reply_markup=telebot.types.ReplyKeyboardRemove(selective=False))
            return 0
        if state == 1:
            if digit == 4:
                self.bot.reply_to(message, self.MesHelpless())
                self.bot.send_message(self.chat_id, "", reply_markup=telebot.types.ReplyKeyboardRemove(selective=False))
            else:
                database.update({'state':2,'Dish':digit}, query.id_of_rating_chat == self.chat_id)
                self.bot.send_message(self.chat_id, self.MesAskRating() , reply_markup = self.RatingKeyboard())
            return 0
        if state == 2:
            database.update({'state':3,'Rating':digit}, query.id_of_rating_chat == self.chat_id)
            self.bot.send_message(self.chat_id,self.MesThanks(digit), reply_markup=telebot.types.ReplyKeyboardRemove(selective=False))
        return 0

    #Handles the case when user sends /rate command
    def HandleRating(self, state, message, database):
        if state == 3:
            self.bot.reply_to(message, self.MesCheat(), reply_markup=telebot.types.ReplyKeyboardRemove(selective=False))
            return 0
        if state == 0:
            database.insert({'id_of_rating_chat' : message.chat.id, 'state': 1, 'Dish':None, 'Rating':None})
            self.bot.send_message(self.chat_id, self.MesAskDish() ,reply_markup = self.DishKeyboard())
            return 0
        if state == 1:
            self.bot.send_message(self.chat_id, self.MesAskDish() , reply_markup = self.DishKeyboard())
            return 0            
        if state == 2:  
            self.bot.send_message(self.chat_id, self.MesAskRating() , reply_markup = self.RatingKeyboard())
        return 0

    #Handles the case when user sends /stats command
    def HandleStats(self, message, database, query):
        responses = database.search( query.state == 3)
        if not responses:
            self.bot.reply_to(message, self.MesNoRatings() )
            return 0       
        else:
            report = self.GenerateStatsReport(responses, truncation=20)
            self.bot.reply_to(message, report )         
        return 0
    

