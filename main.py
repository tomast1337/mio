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

    # help, license and source functions {{{
    if message.content.startswith("$help"):
        await message.channel.send("Hello, I'm Mio Akiyama, I'll help you download and listen to music.")
        await message.channel.send(help_content)

    elif message.content.startswith("$license"):
        await message.channel.send(content="GNU General Public License, third version.", file=File("LICENSE"))

    elif message.content.startswith("$source"):
        await message.channel.send("If you have git installed, you can do 'git clone https://github.com/gioiacyberpunk/mio' to download the source code.\nIf not, go to that url, click on 'Code' green button and 'Download ZIP'. Unzip the downloaded file to any location.")

    # }}}


client.run(auth_file.read())
help_file.close()

