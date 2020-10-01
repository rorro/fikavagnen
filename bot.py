import discord
import json

# Get token
with open('auth.json') as f:
    TOKEN = json.load(f)['token']

client = discord.Client()
last_messages = {}

thanks_yo = ["tack", "thank", "thx", "tks", "tnx", "10x", "tank", "tx", "thks", "ty"]

@client.event
async def on_message(message):
    # Prevent from replying to self
    if message.author == client.user:
        return


    channel_id = message.channel.id

    msg = message.content.lower()

    msg_list = msg.split(" ")

    if "te" in msg or "tea" in msg:
        last_messages[channel_id] = message
        await message.add_reaction(u"\U0001F375")
    if "kaffe" in msg or "coffee" in msg:
        last_messages[channel_id] = message
        await message.add_reaction(u"\u2615")
    if client.user.mentioned_in(message):
        for ty in thanks_yo:
            if ty in msg:
                await message.add_reaction(u"\U0001F642")

    for ty in thanks_yo:
        if ty in msg and channel_id in last_messages:
            for reaction in last_messages[channel_id].reactions:
                if reaction.me:
                    await message.add_reaction(u"\U0001F642")

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
