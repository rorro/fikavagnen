import discord
import json
import dbhelper
import constants
from commands import *
from pathlib import Path
from os import system
from configparser import ConfigParser
import datetime

client = discord.Client()
last_messages = {}
before_last_messages = {}

config_obj = ConfigParser()
ALLOWED_CHANNELS = []
MEETUP_START = datetime.time(17, 15)

# Get token
with open('auth.json') as f:
    TOKEN = json.load(f)['token']

# create config if it doesn't exist
if not Path('fikavagn.conf').is_file():
    config_obj["ALLOWED_CHANNELS"] = {}
    conf = open('fikavagn.conf', 'w+')
    config_obj.write(conf)
    conf.close()
else:
    # read config
    config_obj.read("fikavagn.conf")

    # get allowed channels config
    channels = config_obj["ALLOWED_CHANNELS"]

    for channel in channels:
        ALLOWED_CHANNELS.append(channel)


async def send_help(channel):
    embedMsg = discord.Embed(title="PANIC!", description="")
    embedMsg.add_field(name="!help", value="Shows this menu.", inline=False)
    embedMsg.add_field(name="!top10 {metric}", value="Shows top 10 for a specified metric.", inline=True)
    embedMsg.add_field(name="Valid metrics", value="tea, coffee, thanks, thanks_at, no_thanks", inline=True)
    embedMsg.add_field(name="!ranks", value="Shows your fika ranks.", inline=False)
    embedMsg.add_field(name="!totals", value="Shows total fika given out.", inline=False)
    embedMsg.add_field(name="!allowfika", value="Allows fikavagnen to servera fika. You have to be a board member to use this.", inline=False)
    embedMsg.add_field(name="!disallowfika", value="Revokes fikavagnens ability att servera fika. You have to be a board member to use this.", inline=False)

    await channel.send(embed=embedMsg)


async def send_top10(channel, top10, metric):
    metric = metric_to_emoji(metric)
    embedMsg = discord.Embed(title="Top 10 for " + metric, description="")

    ranks = ''
    users = ''
    scores = ''

    if not top10:
        embedMsg.add_field(name="Not enough data to show", value="-", inline=True)
        embedMsg.color = discord.Color(0xe74c3c)

    else:
        for i in range(len(top10)):
            ranks += str(i) + '\n'
            users += top10[i][0] + '\n'
            scores += str(top10[i][1]) + '\n'

        embedMsg.add_field(name="Rank", value=ranks, inline=True)
        embedMsg.add_field(name="User", value=users, inline=True)
        embedMsg.add_field(name="Score", value=scores, inline=True)

    await channel.send(embed=embedMsg)


async def send_ranks(channel, author_name, data):
    embedMsg = discord.Embed(title="Fika ranks for " + author_name, description="")

    metrics = ''
    ranks = ''
    scores = ''

    for metric, rank, score in data:
        metrics += metric_to_emoji(metric) + '\n'
        ranks += str(rank) + '\n'
        scores += str(score) + '\n'

    embedMsg.add_field(name="Metric", value=metrics, inline=True)
    embedMsg.add_field(name="Rank", value=ranks, inline=True)
    embedMsg.add_field(name="Score", value=scores, inline=True)

    await channel.send(embed=embedMsg)


async def send_totals(channel, totals):
    embedMsg = discord.Embed(title="Total fika given", description="")

    metrics = ''
    scores = ''

    for metric, score in totals:
        metrics += metric_to_emoji(metric) + '\n'
        scores += str(score) + '\n'

    embedMsg.add_field(name="Metric", value=metrics, inline=True)
    embedMsg.add_field(name="Score", value=scores, inline=True)

    await channel.send(embed=embedMsg)


@client.event
async def on_message(message):
    # Prevent from replying to self
    if message.author == client.user:
        return

    time = datetime.datetime.today()

    channel_id = message.channel.id
    author_id = message.author.id
    author_name = message.author.name
    is_board = "board" in [y.name.lower() for y in message.author.roles]

    if channel_id in last_messages:
        before_last_messages[channel_id] = last_messages[channel_id]

    last_messages[channel_id] = message

    msg = message.content.lower()

    if is_command(msg):
        cmd, args = parse_command(msg)

        if is_valid_command(cmd):
            if cmd == "allowfika" and is_board:
                if str(channel_id) in ALLOWED_CHANNELS:
                    return

                # read config
                config_obj.read("fikavagn.conf")

                # get allowed channels config
                channels = config_obj["ALLOWED_CHANNELS"]

                # add channel
                channels[str(channel_id)] = str(message.channel)
                ALLOWED_CHANNELS.append(str(channel_id))

                with open('fikavagn.conf', 'w') as conf:
                    config_obj.write(conf)

            elif cmd == "disallowfika" and is_board:
                if str(channel_id) not in ALLOWED_CHANNELS:
                    return

                # read config
                config_obj.read("fikavagn.conf")

                # get allowed channels config
                channels = config_obj["ALLOWED_CHANNELS"]

                # remove channel
                del channels[str(channel_id)]
                del ALLOWED_CHANNELS[ALLOWED_CHANNELS.index(str(channel_id))]

                with open('fikavagn.conf', 'w') as conf:
                    config_obj.write(conf)

            if str(channel_id) in ALLOWED_CHANNELS and is_meetup(time):
                if cmd == "help":
                    await send_help(message.channel)

                elif cmd == "top10":
                    if len(args) >= 1:
                        metric = args[0]
                    else:
                        return

                    if is_valid_metric(metric):
                        top10 = dbhelper.get_top10(metric)
                        await send_top10(message.channel, top10, metric)

                elif cmd == "ranks":
                    ranks = dbhelper.get_user_ranks(author_id)
                    await send_ranks(message.channel, author_name, ranks)

                elif cmd == "totals":
                    totals = dbhelper.get_total_data()
                    await send_totals(message.channel, totals)
    else:
        if str(channel_id) in ALLOWED_CHANNELS and is_meetup(time):
            for te in constants.TEA:
                if te in msg:
                    await message.add_reaction("🍵")
                    dbhelper.add_data(author_id, author_name, "tea")
                    break

            for coffee in constants.COFFEE:
                if coffee in msg:
                    await message.add_reaction("☕")
                    dbhelper.add_data(author_id, author_name, "coffee")
                    break

            if client.user.mentioned_in(message):
                for ty in constants.THANKS:
                    if ty in msg:
                        await message.add_reaction("🙂")
                        dbhelper.add_data(author_id, author_name, "thanks_at")
                        break

            for noty in constants.NO_THANKS:
                remove = False
                if noty in msg and channel_id in before_last_messages:
                    for reaction in before_last_messages[channel_id].reactions:
                        if reaction.me and reaction.emoji in "🍵☕" and before_last_messages[channel_id].author.id == author_id:
                                await before_last_messages[channel_id].remove_reaction(reaction.emoji, client.user)
                                remove = True
                    if remove:
                        await message.add_reaction("🙄")
                        dbhelper.add_data(author_id, author_name, "no_thanks")
                        return

            for ty in constants.THANKS:
                if ty in msg and channel_id in before_last_messages:
                    for reaction in before_last_messages[channel_id].reactions:
                        if reaction.me and reaction.emoji in "🍵☕" and before_last_messages[channel_id].author.id == author_id:
                            await message.add_reaction("🙂")
                            dbhelper.add_data(author_id, author_name, "thanks")


@client.event
async def on_ready():
    if not Path("database.db").is_file():
        system("sqlite3 database.db < schema.sql")

    await client.change_presence(activity=discord.Game('https://www.bestapi.nu/fikavagnen'))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
