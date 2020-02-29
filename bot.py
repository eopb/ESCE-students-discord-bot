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

EIGHTBALLRESPONSES = [
    'As I see it, yes.',
    'Ask again later.',
    'Better not tell you now.',
    'Cannot predict now.',
    'Concentrate and ask again.',
    'Don’t count on it.',
    'It is certain.',
    'It is decidedly so.',
    'Most likely.',
    'My reply is no.',
    'My sources say no.',
    'Outlook not so good.',
    'Outlook good.',
    'Reply hazy, try again.',
    'Signs point to yes.',
    'Very doubtful.',
    'Without a doubt.',
    'Yes.',
    'Yes – definitely.',
    'You may rely on it.'
]


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

# 194782646843211777


def get_member(id):
    return discord.utils.get(get_guild().members, id=id)


def member_efun():
    return get_member(194782646843211777)


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


async def subject_prompt(user, s_list):
    await user.add_roles(get_role("member"))
    await get_channel("bot-commands").send(user.mention
                                           + " There are more channels to see. You can access them by adding your subjects with the `?subject` command.\n\n"
                                           + "You can add all of the subjects that apply.\n```"
                                           + list_subjects(s_list)
                                           + "```"
                                           )


# Main function that checks all messages for bot commands
async def on_message_or_edit(message):
    # Prevents the bot from talking to itself or in other guilds
    if message.author == client.user or str(message.guild) != GUILD:
        return

    print("New message in " + message.channel.name +
          "\n\nMessage Content: " + message.content)

    user = message.author
    if message.channel.name == "welcome-room":
        print("Message in welcome-room")
        if re.search('\?name .*', message.content) != None:
            username = message.content[6:].strip()

            print("Changing user " + user.name + " nickname to " + username)
            await user.edit(nick=username)
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
                await message.author.add_roles(get_role("a-level-student"))
                await subject_prompt(user, A_LEVEL_SUBJECTS)
            elif join_as == "btec":
                await message.author.add_roles(get_role("btec-student"))
                await subject_prompt(user, BTEC_SUBJECTS)
            elif join_as == "other":
                await message.author.add_roles(get_role("member"))
                await get_channel("general").send(user.mention
                                                  + " Does not fit in any category "
                                                  + member_efun().mention)
            else:
                await message.channel.send(
                    user.mention + " :negative_squared_cross_mark: Error: Invalid join: Please try again.")
    else:
        if re.search('\?subject .*', message.content) != None:
            subject = message.content[9:].strip().lower()
            named_roles = [role.name for role in user.roles]
            error_msg = user.mention + \
                " :negative_squared_cross_mark: Error: Invalid Subject: Please try again: " + \
                member_efun().mention
            if "a-level-student" in named_roles:
                if subject in A_LEVEL_SUBJECTS:
                    await message.author.add_roles(get_role(subject))
                    await message.channel.send("Adding you to A Level: " + subject)
                else:
                    await message.channel.send(error_msg)
            elif "btec-student" in named_roles:
                if subject in BTEC_SUBJECTS:
                    await message.author.add_roles(get_role(subject + "-btec"))
                    await message.channel.send("Adding you to BTEC: " + subject)
                else:
                    await message.channel.send(error_msg)
            else:
                await message.channel.send(
                    user.mention + " :negative_squared_cross_mark: Error: Not member of alevels or btec: " + member_efun().mention)


@client.command(aliases=['8ball', '8Ball'])
async def _8Ball(ctx, *, question):

    # awaits a question and then sends a random choice of preset answers

    await ctx.send(f'Question: {question}\n{random.choice(EIGHTBALLRESPONSES)}')


@client.event
async def on_message(message):
    await on_message_or_edit(message)


@client.event
async def on_message_edit(before, after):
    await on_message_or_edit(after)

client.run(token)
