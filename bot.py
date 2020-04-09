import discord
import json

# Get token
with open('auth.json') as f:
    TOKEN = json.load(f)['token']

client = discord.Client()

@client.event
async def on_message(message):
    # Prevent from replying to self
    if message.author == client.user:
        return

    msg_list = message.content.split(" ")

    if "te" in msg_list or "tea" in msg_list:
        await message.add_reaction(u"\U0001F375")
    if "kaffe" in msg_list or "coffee" in msg_list:
        await message.add_reaction(u"\u2615")

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
