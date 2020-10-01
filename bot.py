import discord
import json

# Get token
with open('auth.json') as f:
    TOKEN = json.load(f)['token']

client = discord.Client()
last_messages = {}
before_last_messages = {}

thanks_yo = ["tack", "thank", "thx", "tks", "tnx", "10x", "tank", "tx", "thks", "ty"]

@client.event
async def on_message(message):
    # Prevent from replying to self
    if message.author == client.user:
        return


    channel_id = message.channel.id

    if channel_id in last_messages:
        before_last_messages[channel_id] = last_messages[channel_id]
    last_messages[channel_id] = message


    msg = message.content.lower()

    msg_list = msg.split(" ")

    if "te" in msg or "tea" in msg:
        await message.add_reaction(u"\U0001F375")
    if "kaffe" in msg or "coffee" in msg:
        await message.add_reaction(u"\u2615")
    if client.user.mentioned_in(message):
        for ty in thanks_yo:
            if ty in msg:
                await message.add_reaction(u"\U0001F642")

    for ty in thanks_yo:
        if ty in msg and channel_id in before_last_messages:
            for reaction in before_last_messages[channel_id].reactions:
                if reaction.me and reaction.emoji in "🍵☕":
                    await message.add_reaction(u"\U0001F642")

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
