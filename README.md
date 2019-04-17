This is a Telegram bot to rate cafeteria dishes in my institute. Apart from that, it features on-demand or daily updates on the menu.

### User commands
* rate given day's dishes with `/rate` command
* see the current rating results with `/stats` command
* get current menu with `/menu` command
* subsribe to (`/sub`) and unsubscribe from (`/unsub`) daily menu updates

### How it works
* `message_handler.py` is a script that handles all incoming messages. It should be running permanently. It handles all bot logic by itself, apart from dish rating. This, due to larger complexity then the rest of the logic, is done in a separate module `Ratings.py`. This module implements a class `RatingHandler`. An object of this class is created when a user requests a 
* `daily_cleanup.py` should be run daily in the evening. It flushes the rating database `ratings_db.json` and archives the daily statistics as well as makes a backup of the subscribers database `db.json`. The daily statistics are stored in `stats_archive/` while 
* both `db.json` and `ratings_db.json` are simple databases implemented using the TinyDB package
* `menu_scrapper.py` scraps the menu from the Institute website using BeautifulSoup and saves it to files named from `Monday.txt` till `Friday.txt`. In principle it is enough to run it on Monday when a new weekly menu is updated but due to possible changes I run it daily.
* the Telegram API token is stored in `token.txt` file, which is obviously not included in the repository

