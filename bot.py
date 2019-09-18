# bot.py
import os
import re
import discord
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

A_LEVEL_SUBJECTS = ["maths", "physics", "computer-science",
                    "further-maths", "chemistry", "biology", "accounting"]
BTEC_SUBJECTS = ["art"]


def list_subjects(subject_array):
    subjects = ""
    for subject in subject_array:
        subjects = subjects + "?subject " + subject + "\n"
    return subjects


def get_guild():  # Guild is an other word for server
    return discord.utils.get(client.guilds, name=GUILD)


def get_channel(name):
    return discord.utils.get(get_guild().channels, name=name)


def get_role(name):
    return discord.utils.get(get_guild().roles, name=name)


@client.event
async def on_ready():  # Just prints some basic info to console when the bot is run
    guild = get_guild()
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


@client.event
async def on_member_join(member):  # Post tutorial message to new users
    print("A member has joined I will greet them.")
    welcome_room = get_channel("welcome-room")
    # maybe post reminder message to non member users ever so often
    await welcome_room.send("Hello and welcome " + member.mention + " Thank you for joining!" + """
We use bots on this server. Please follow the steps to gain access to the channels.
It is important we know who you are. We are going to need to change your nickname to the name you use or plan to use at ESC
Type `?name your name` using your name. For example in my case I would type,
```
?name Ethan Brierley
```
""")


@client.event
async def on_message(message):  # Main function that checks all messages for bot commands
    if message.author == client.user:  # Prevents the bot from talking to itself
        return

    print("New message in " + message.channel.name)

    user = message.author
    bot_commands = get_channel("bot-commands")
    if message.channel.name == "welcome-room":
        print("Message in welcome-room")
        if re.search('\?name .*', message.content) != None:
            username = message.content[6:].strip()

            print("Changing user " + user.name + " nickname to " + username)
            await user.edit(nick=username)
            # role = get_role("member")
            # await message.author.add_roles(role)
            await message.channel.send(user.mention + " I have changed your nickname to " + username + "." + """
If you are a A level student enter
```
?join alevel
```
If you are a BTEC student enter
```
?join btec
```
If you don't fit in any of those categories enter
```
?join other
```
""")
        elif re.search('\?join .*', message.content) != None:
            join_as = message.content[6:].strip().lower()
            if join_as == "alevel":
                await message.author.add_roles(get_role("member"))
                await message.author.add_roles(get_role("a-level-student"))
                await get_channel("bot-commands").send(user.mention
                                                       + " There are more channels to see. You can access them by adding your subjects with the `?subject` command.\n\n"
                                                       + "You can add any of these subjects.\n```"
                                                       + list_subjects(A_LEVEL_SUBJECTS)
                                                       + "```"
                                                       )
            elif join_as == "btec":
                await message.author.add_roles(get_role("member"))
                await message.author.add_roles(get_role("btec-student"))
            elif join_as == "other":
                await message.author.add_roles(get_role("member"))
            else:
                print("invalid")

client.run(token)
