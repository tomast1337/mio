from discord import *
from pytube import *
import os
import shutil
import sys

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

    # HELP, LICENSE AND SOURCE {{{
    if message.content.startswith("$help"):
        await message.channel.send("Hello, I'm Mio Akiyama, I'll help you download and listen to music.")
        await message.channel.send(help_content)

    elif message.content.startswith("$license"):
        await message.channel.send(content="GNU General Public License, third version.", file=File("LICENSE"))

    elif message.content.startswith("$source"):
        await message.channel.send("If you have git installed, you can do 'git clone https://github.com/gioiacyberpunk/mio' to download the source code.\nIf not, go to that url, click on 'Code' green button and 'Download ZIP'. Unzip the downloaded file to any location.")

    # }}}

    # MAIN BOT FUNCTIONS {{{

    elif message.content.startswith("$video"):

        await message.channel.send("Downloading videos, please wait...")

        channel_id = str(message.channel.id)
        try:
            os.mkdir(channel_id)
        except FileExistsError:
            print()

        spl_message = message.content.split()
        links = spl_message[1:]

        for link in links:
            
            # this is ugly but it's the only way to do it
            await message.channel.send(file=File(YouTube(link).streams.filter(only_audio=True).first().download(channel_id)))

        shutil.rmtree(channel_id)

    # }}}


client.run(auth_file.read())
help_file.close()

