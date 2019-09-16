# bot.py
import os
import re
import discord
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()


def get_guild():
    return discord.utils.get(client.guilds, name=GUILD)


def get_channel(name):
    return discord.utils.get(get_guild().channels, name=name)


def get_role(name):
    return discord.utils.get(get_guild().roles, name=name)


@client.event
async def on_ready():
    guild = get_guild()
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


@client.event
async def on_member_join(member):
    welcome_room = get_channel("welcome-room")
    # maybe post reminder message to non member users ever so often
    await welcome_room.send("Hello and welcome " + member.mention + " Thank you for joining!" + """
We use bots on this server. Please follow the steps to gain access to the channels.
It is important we know who you are. We are going to need to change your nickname to the name you use or plan to use at ESC
Type `?student your name` using your name. For example in my case I would type,
```
?student Ethan Brierley
```
""")


@client.event
async def on_message(message):
    bot_commands = get_channel("bot-commands")
    if message.author == client.user:
        return

    print(message.channel.name)

    if message.channel.name == "welcome-room":
        username = re.search('\?student .*', message.content)
        if username != None:
            username = username.group(0)[9:]
            user = message.author
            await user.edit(nick=username)
            role = get_role("member")
            await message.author.add_roles(role)
            await bot_commands.send(user.mention + " I have changed your nickname to " + username + """
There are more channels to see. You can access them by adding ranks.
You can list ranks with,
```
?ranks
```
You can add ranks that apply to you with `?rank`. For example you could,
```
?rank a-level-student
""")


client.run(token)
