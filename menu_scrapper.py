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
    string=soup.get_text()
    lines=string.splitlines()
    lines = list(filter(None, lines))

    #stores lines that correspond to [monday,tuesday,...,friday] respectively
    days_in_menu = [[9,10,13,16,19,22,25],
     [28,29,32,35,38,41,44],
     [47,48,51,54,57,60,63],
     [66,67,70,73,76,79,82],
     [85,86,89,92,95,98,101]]

    all_day_list=[]
    for j in range(len(weekdays)):
        day_string = "\n\n".join([lines[i] for i in days_in_menu[j]]) #string corresponding to menu for a given weekday
        day_string = day_string.replace("\t","")
        day_string = RemoveGivenLine(day_string,3) #remove the (whitespace b/w soups) for a nicer look
        all_day_list.append(day_string)
        
    return all_day_list


day_menus = GetMenu(ist_menu_url)

for i in range(len(weekdays)):
	with open(weekdays[i]+".txt","w+") as f:
		f.write(day_menus[i])
	


