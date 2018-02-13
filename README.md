# killbot - Rewrite

This branch is for development with discord.py-1.0. 

## Major Dependencies

* discord.py 1.0.0a0 (rewrite)
* aiohttp
* requests
* python-memcached (and a memcache server)

## Setup and Launcher Commands
There are a few things that have to be done to setup the bot before it can be used.

### Cache
You will need to set up memcache so the bot can cache esi requests. 

More info can be found here:
* **Memcache project page:** http://memcached.org/
* **Installing Memcache on Windows:** https://commaster.net/content/installing-memcached-windows

Most linux distros should have a memcache package on their package manager.

### Bot
Firstly, the bot does not ship with a copy of the Static Data Export. Secondly, the config file has to be copied and edited.

Using the setup command `python3 launcher.py setup` will download the SDE and copy the config file for editing.
(In the future I might allow editing the config file through launcher commands.) This command will also make the log directory.

If the SDE is out of date, and you need to update it, run `python3 launcher.py update` and the launcher will fetch and unzip the SDE for you.

## The Config File

* `token` is your bot token from the discord site.
* `prefix` is the symbol that will come before all your commands.
  * Default is `/`
* `msg` this is the message that you would like to see in the bot's "playing" status.
  * Default is `''`. 
  * This can also be set after the bot has been started with the `/presence` command by the bot owner.
* `app` is the name of your bot. (include a link to your github if you made any changes.)
  * Default is `''`
* `contact` is your contact information to be sent in HTTP headers to CCP and zKillboard in case something goes wrong and they need to contact you.
  * Default is `''`
  * Good options are discord tag, tweetfleet slack id, email, and eve name.
* `logginglevel` is the level of information to log.
    * Default is `'DEBUG'`
    * Options are `CRITICAL`, `ERROR`, `WARNING`, `INFO`, and `DEBUG`
* `kill_channel` is the channel to post the kills into.
    * Default is `''`. When set remove the `''`
* `kill_ids` is the list of ids to watch for.
    * Default is `{'alliance_id': [], 'corporation_id': [], 'character_id': [], 'ship_type_id': []}`
    * Example `{'alliance_id': ['12345', '12234'], 'corporation_id': [], 'character_id': [], 'ship_type_id': []}`