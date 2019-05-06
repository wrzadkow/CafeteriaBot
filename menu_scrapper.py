from bs4 import BeautifulSoup
from urllib.request import urlopen

weekdays=['Monday','Tuesday','Wednesday','Thursday','Friday']
ist_menu_url = 'http://screens.app.ist.ac.at/menu_weekly'

#removes a line 'line' from a string 'string'
def RemoveGivenLine(string,line):
    lines = string.splitlines()
    lines.pop(line)
    string_joined_again = "\n".join(lines)
    return string_joined_again

def GetMenu(menu_url):
    page = urlopen(menu_url)
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.find( "table")#, {"title":"TheTitle"} )
    rows = table.findAll("tr")
    texts = [row.get_text().splitlines() for row in rows]
    texts.pop(0) #remove 1st row (table header)
    meaningful_lines = [2,6,10,16,20,24,30] #lines corresponding to food items in each day
    days = [[text[i].replace("\t","") for i in meaningful_lines] for text in texts]
    day_strings = ["\n\n".join(day) for day in days]
    #remove the (whitespace b/w soups) for a nicer look
    day_strings = [RemoveGivenLine(day_string,3) for day_string in day_strings]    
    return day_strings

day_menus = GetMenu(ist_menu_url)

for i in range(len(weekdays)):
	with open(weekdays[i]+".txt","w+") as f:
		f.write(day_menus[i])
	


