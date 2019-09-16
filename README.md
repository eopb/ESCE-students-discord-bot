# ESCE students discord bot

https://realpython.com/how-to-make-a-discord-bot-python/
https://github.com/Rapptz/discord.py
https://discordpy.readthedocs.io/en/latest/
https://discordpy.readthedocs.io/en/latest/api.html#

python3
```
pip3 install -U discord.py
pip install -U python-dotenv
```

```
 Edit this file to introduce tasks to be run by cron.
# 
# Each task to run has to be defined through a single line
# indicating with different fields when the task will be run
# and what command to run for the task
# 
# To define the time you can provide concrete values for
# minute (m), hour (h), day of month (dom), month (mon),
# and day of week (dow) or use '*' in these fields (for 'any').
# 
# Notice that tasks will be started based on the cron's system
# daemon's notion of time and timezones.
# 
# Output of the crontab jobs (including errors) is sent through
# email to the user the crontab file belongs to (unless redirected).
# 
# For example, you can run a backup of all your user accounts
# at 5 a.m every week with:
# 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
# 
# For more information see the manual pages of crontab(5) and cron(8)
# 
# m h  dom mon dow   command

@reboot sh /home/pi/Documents/bot/esce-students-discord-bot/launch.sh 2>&1 | tee /home/pi/Documents/bot/esce-students-discord-bot/log

```