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
async def play(ctx, url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voiceChannel = utils.get(ctx.guild.voice_channels, name='General')
    await voiceChannel.connect()
    voice = utils.get(client.voice_clients, guild=ctx.guild)



    os.system(f"yt-dlp -x --audio-format mp3 {url}")

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(FFmpegPCMAudio("song.mp3"))


@client.command()
async def leave(ctx):
    voice = utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def help(ctx):
    await ctx.send("Hello, I'm Mio Akiyama, I'll help you download and listen to music.")
    await ctx.send(help_content)


@client.command()
async def license(ctx):
    await ctx.send("GNU General Public License, third version.", file=File("LICENSE"))


@client.command()
async def source(ctx):
    await ctx.send("If you have git installed, you can do 'git clone https://github.com/gioiacyberpunk/mio' to download the source code.\nIf not, go to that url, click on 'Code' green button and 'Download ZIP'. Unzip the downloaded file to any location.")


@client.command()
async def video(ctx, url: str):
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
    # Downloading video using yt-dlp
    os.system(
        f"yt-dlp -x --audio-format mp3 -o '{str(channel.id)}/%(title)s.%(ext)s' {url}")

    await ctx.send("Done downloading.")

    # After downloading, send the file to the channel
    for file in os.listdir(str(channel.id)):
        if file.endswith(".mp3"):
            await ctx.send(file=File(f"{str(channel.id)}/{file}"))
    shutil.rmtree(str(channel.id))

client.run(auth_file.read())
help_file.close()
auth_file.close()
