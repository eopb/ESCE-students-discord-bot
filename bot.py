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
    await welcome_room.send("Hi")


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
