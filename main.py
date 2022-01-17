from discord import *

client = Client()

auth_file = open("auth.txt", "r")

help_file = open("help.txt", "r")
help_content = help_file.read()

@client.event
async def on_ready():
    print("logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$help"):
        await message.channel.send("Hello, I'm Mio Akiyama, I'll help you download and listen to music.")
        await message.channel.send(help_content)


client.run(auth_file.read())

