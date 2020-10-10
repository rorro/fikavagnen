import discord
import json
import dbhelper
from pathlib import Path
from os import system

# Get token
with open('auth.json') as f:
    TOKEN = json.load(f)['token']

client = discord.Client()
last_messages = {}
before_last_messages = {}

thanks_yo = ["tack", "thank", "thx", "tks", "tnx", "10x", "tank", "tx", "thks", "ty"]

async def send_embed(cmd, message):
    hiscores = dbhelper.get_hiscores()

    embed_title = ""
    i = 0
    metric_1_name = ""
    metric_2_name = ""

    if cmd == "fika":
        embed_title = " 🍵 and ☕ scores"
        i = 0
        metric_1_name = "🍵"
        metric_2_name = "☕"
    elif cmd == "tackar":
        embed_title = "👍 scores"
        i = 2
        metric_1_name = "👍"
        metric_2_name = "@ 👍"
    else:
        return


    embedMsg = discord.Embed(title=embed_title, description="")

    names = ''
    metric_1 = ''
    metric_2 = ''

    for fikare in hiscores:
        user = await client.fetch_user(fikare[0])

        names += user.name + "\n"
        metric_1 += str(fikare[1+i]) + "\n"
        metric_2 += str(fikare[2+i]) + "\n"

    embedMsg.add_field(name="Name", value=names, inline=True)
    embedMsg.add_field(name=metric_1_name, value=metric_1, inline=True)
    embedMsg.add_field(name=metric_2_name, value=metric_2, inline=True)

    await message.channel.send(embed=embedMsg)


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

    msg = message.content.lower().encode('ascii', 'ignore').decode('utf-8')

    metric = ""
    split_msg = msg.split()
    if msg and len(split_msg) > 1 and split_msg[0] == "!scores":
        metric = split_msg[1]
        await send_embed(metric, message)

    if "te" in msg or "tea" in msg:
        await message.add_reaction("🍵")
        dbhelper.add_data(user_id, "tea")

    if "kaffe" in msg or "coffee" in msg:
        await message.add_reaction("☕")
        dbhelper.add_data(user_id, "coffee")

    if client.user.mentioned_in(message):
        for ty in thanks_yo:
            if ty in msg:
                await message.add_reaction("👍")
                dbhelper.add_data(user_id, "thanks_at")


    for ty in thanks_yo:
        if ty in msg and channel_id in before_last_messages:
            for reaction in before_last_messages[channel_id].reactions:
                if reaction.me and reaction.emoji in "🍵☕" and before_last_messages[channel_id].author.id == user_id:
                    await message.add_reaction("👍")
                    dbhelper.add_data(user_id, "thanks")

@client.event
async def on_ready():
    if not Path("database.db").is_file():
        system("sqlite3 database.db < schema.sql")

    await client.change_presence(activity=discord.Game('!scores [fika, tackar]'))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
