# killbot

Killbot is discord bot built using python3 and discord.py for use with EVE Online. 

## Major Dependencies

* python3.6
  * f-strings are not supported on earlier versions.
* discord.py 1.0.0a0 (rewrite)
  * **NOTE:** discord.py 1.0.0a0 is NOT in requiremenst.txt. You will have to install it using the following command: `python3 -m pip install -U git+https://github.com/Rapptz/discord.py@rewrite`
* aiohttp
* aioxmpp
  * **NOTE:** This is required for the JabberPings extension, and requires libxml, which means you must be running the bot on a linux distro to use this feature.
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
You will need to copy `config.py.example` in `utils` to `config.py` and fill it out.


Using the setup command `python3 launcher.py setup` will download the SDE and make the log directory as well as the bot database.
(In the future I might allow editing the config file through launcher commands.)

If the SDE is out of date, and you need to update it, run `python3 launcher.py update` and the launcher will fetch and unzip the SDE for you.

## The Config File

This section will be moved to the repo wiki.