# killbot

A discord bot to pull killmails from zkill and maybe more.

# Dependencies
 * discord.py
 * requests (used for hourly pulling of system info)

 # Other Requirements
 * Get the SDE in SQLite format here: https://www.fuzzwork.co.uk/dump/sqlite-latest.sqlite.bz2
    * Unpack the archive in the same folder as the rest of the bot files.
    * Rename the sqlite file to sde.sqlite
  * Get the empty systems database here https://nyc3.digitaloceanspaces.com/colsfiles/systems.sqlite
    * This should be in the bot's root folder.

# Config
Remember to rename `config.py.empty` to `config.py`, and to fill it in.

* `BOT_TOKEN` : You get this from the discord bot app that you make. More specifically it comes from the bot user you make to go along with your app.
* `PREFIX` : This is the symbol that you want to have before all the commands. Use something that is easy to type, but not all that common.
  * Default is `]`
* `msg` is the message that you would like to have in the playing status of your bot.
  * Default is `''`. In order to show the full message, and help command please limit your message to 12 characters.
* `KILLWATCH_ENABLED` : Set this to TRUE to watch zkill for kills!
  * Default is `FALSE`
* `KILLWATCH_CHANNEL` : This is where you set the channel id that you want to have kills posted in.
  * Default is `''` however when you set it there should be no quotes. EX: `KILLWATCH_CHANNEL = 1234546`
* `watchids` : This is a dict of lists of IDs for the bot to watch for on zkill.
  * Note: All IDs should be in string format, and separated with commas. EX: `'corps': ["1234","5678"]`
* `system_cmd` : This is where you set whether or not you want to pull from the esi for the last hour, or set up a cron job and (in 24 short hours) be able to have info for the past 24 hours.
    * Default is `ESI`
    * If you would like to use the cron option you will want to use `0 * * * * cd /PATH/TO/killbot && /usr/bin/python3 /PATH/TO/syscron.py > /PATH/TO/killbot/logs/syscron.log 2>&1`
