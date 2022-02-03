from calendar import c
from discord import *
from discord.ext import commands
import os
import shutil

client = commands.Bot(command_prefix='$')
client.remove_command('help')

auth_file = open("auth.txt", "r")

help_file = open("help.txt", "r")
help_content = help_file.read()

@client.event
async def on_ready():
    print(f"logged in as {client.user}")


@client.command()
async def play(ctx, url:str,channel:str):
    pass

@client.command()
async def quit(ctx):
    pass

@client.command()
async def stop(ctx):
    pass

@client.command()
async def pause(ctx):
    pass

@client.command()
async def resume(ctx):
    pass

@client.command()
async def help(ctx):
    await ctx.send("Hello, I'm Mio Akiyama, I'll help you download and listen to music.")
    await ctx.send(help_content)

@client.command()
async def license(ctx):
    await ctx.send("GNU General Public License, third version.", file = File("LICENSE"))

@client.command()
async def source(ctx):
    await ctx.send("If you have git installed, you can do 'git clone https://github.com/gioiacyberpunk/mio' to download the source code.\nIf not, go to that url, click on 'Code' green button and 'Download ZIP'. Unzip the downloaded file to any location.")

@client.command()
async def video(ctx,url:str):
    await ctx.send("Downloading videos, please wait...")

    channel = ctx.channel
    try:
        os.mkdir(str(channel.id))
    except FileExistsError:
        print()

    ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        
    links = url
    #Downloading video using yt-dlp
    os.system(f"yt-dlp -x --audio-format mp3 -o '{str(channel.id)}/%(title)s.%(ext)s' {url}")

    await ctx.send("Done downloading.")

    #After downloading, send the file to the channel
    for  file in os.listdir(str(channel.id)):
        if file.endswith(".mp3"):
            await ctx.send(file=File(f"{str(channel.id)}/{file}"))
    shutil.rmtree(str(channel.id))

client.run(auth_file.read())
help_file.close()

