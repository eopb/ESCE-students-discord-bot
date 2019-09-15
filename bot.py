# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()


@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


@client.event
async def on_member_join(member):
    guild = discord.utils.get(client.guilds, name=GUILD)
    welcome_room = discord.utils.get(guild.channels, name="welcome-room")
    # maybe post reminder message to non member users ever so often
    await welcome_room.send("Hello and welcome " + member.mention + " Thank you for joining" + """
We use bots on this server. Please follow the steps to gain access to the channels.
It is important we know who you are so we are going to need to change your nickname to the name you use or plan to use at ESC
Type `?username your name` using your name. For example in my case I would type,
```
?username Ethan Brierley
```""")


@client.event
async def on_message(message):
    guild = discord.utils.get(client.guilds, name=GUILD)
    if message.author == client.user:
        return

    print(message.channel.name)

    if message.content.lower() == '?join':
        await message.channel.send("Hi")
        role = discord.utils.get(guild.roles, name="member")
        await message.author.add_roles(role)


client.run(token)
