import discord
import json
import dbhelper
import constants
from unidecode import unidecode
from commands import *
from pathlib import Path
from os import system
import asyncio

# Get token
with open('auth.json') as f:
    TOKEN = json.load(f)['token']

client = discord.Client()
last_messages = {}
before_last_messages = {}


async def send_help(channel):
    embedMsg = discord.Embed(title="PANIC!", description="")
    embedMsg.add_field(name="!help", value="Shows this menu.", inline=False)
    embedMsg.add_field(name="!top10 {metric}", value="Shows top 10 for a specified metric.", inline=True)
    embedMsg.add_field(name="Valid metrics", value="tea, coffee, thanks, thanks_at", inline=True)
    embedMsg.add_field(name="!ranks", value="Shows your fika ranks.", inline=False)
    embedMsg.add_field(name="!totals", value="Shows total fika given out.", inline=False)

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
            user = await client.fetch_user(top10[i][0])

            ranks += str(i) + '\n'
            users += user.name + '\n'
            scores += str(top10[i][1]) + '\n'

        embedMsg.add_field(name="Rank", value=ranks, inline=True)
        embedMsg.add_field(name="User", value=users, inline=True)
        embedMsg.add_field(name="Score", value=scores, inline=True)

    await channel.send(embed=embedMsg)


async def send_ranks(channel, user_id, data):
    user = await client.fetch_user(user_id)
    embedMsg = discord.Embed(title="Fika ranks for " + user.name, description="")

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

    channel_id = message.channel.id
    user_id = message.author.id

    if channel_id in last_messages:
        before_last_messages[channel_id] = last_messages[channel_id]

    last_messages[channel_id] = message

    # I know this looks unecessary, but believe me when I say it's
    # neccessary. Tea and coffee need to be served even if Gabriel speaks
    # with wrong letters. We don't discriminate against weird letters.
    msg = message.content.lower()

    if is_command(msg):
        cmd, args = parse_command(msg)

        if is_valid_command(cmd):

            if cmd == "help":
                await send_help(message.channel)

            elif cmd == "top10":
                if len(args) >= 1:
                    metric = args[0]
                else:
                    await message.add_reaction("❌")
                    return

                if is_valid_metric(metric):
                    top10 = await dbhelper.get_top10(metric)
                    await send_top10(message.channel, top10, metric)
                else:
                    await message.add_reaction("❌")

            elif cmd == "ranks":
                ranks = await dbhelper.get_user_ranks(user_id)
                await send_ranks(message.channel, user_id, ranks)

            elif cmd == "totals":
                totals = await dbhelper.get_total_data()
                await send_totals(message.channel, totals)

        else:
            await message.add_reaction("❌")
    else:
        for te in constants.TEA:
            if te in msg:
                await message.add_reaction("🍵")
                await dbhelper.add_data(user_id, "tea")

        for coffee in constants.COFFEE:
            if coffee in msg:
                await message.add_reaction("☕")
                await dbhelper.add_data(user_id, "coffee")

        if client.user.mentioned_in(message):
            for ty in constants.THANKS:
                if ty in msg:
                    await message.add_reaction("🙂")
                    await dbhelper.add_data(user_id, "thanks_at")

        for ty in constants.THANKS:
            if ty in msg and channel_id in before_last_messages:
                for reaction in before_last_messages[channel_id].reactions:
                    if reaction.me and reaction.emoji in "🍵☕" and before_last_messages[channel_id].author.id == user_id:
                        await message.add_reaction("🙂")
                        await dbhelper.add_data(user_id, "thanks")

@client.event
async def on_ready():
    if not Path("database.db").is_file():
        system("sqlite3 database.db < schema.sql")

    await client.change_presence(activity=discord.Game('!help'))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
