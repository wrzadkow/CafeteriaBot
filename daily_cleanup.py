import Ratings
from tinydb import TinyDB, Query
import datetime
import shutil


date_string = datetime.datetime.now().strftime('%Y-%m-%d')

#create a backup of subscribers database
shutil.copyfile('db.json','subscribers_archive/'+date_string+'db.json')

#generate rating stats report and save it
db = TinyDB('ratings_db.json')
query = Query()
responses = db.search( query.state == 3)
handler = Ratings.RatingHandler()

if datetime.datetime.today().weekday() < 5: #on weekdays only
	report = handler.GenerateStatsReport(responses, truncation=20)
	filename = 'stats_archive/'+date_string+'txt'
	with open(filename, 'w+') as report_file:
	    report_file.write(report)
   
#flush the ratings database
db.purge()

