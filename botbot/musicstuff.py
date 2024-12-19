import discord
import yt_dlp
import os
import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot token from .env
TOKEN = os.getenv("DISCORD_TOKEN")  # Get the bot token

# Bot intents and client setup
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# YouTube-DLP and FFMPEG setup
yt_dl_options = {"format": "bestaudio", "quiet": True}
ytdl = yt_dlp.YoutubeDL(yt_dl_options)
ffmpeg_options = {"options": "-vn"}

# Dictionary to track voice clients
voice_clients = {}


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")


@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    if message.content.startswith('!play'):
        try:
            # Check if the user provided a URL
            args = message.content.split()
            if len(args) < 2:
                await message.channel.send("Please provide a valid YouTube URL after the command.")
                return
            url = args[1]

            # Ensure the user is connected to a voice channel
            if message.author.voice is None:
                await message.channel.send("You need to join a voice channel first.")
                return

            # Check if the bot is already connected to a voice channel
            voice_client = voice_clients.get(message.guild.id)
            if not voice_client or not voice_client.is_connected():
                # Connect to the user's voice channel
                voice_channel = message.author.voice.channel
                voice_client = await voice_channel.connect()
                voice_clients[message.guild.id] = voice_client
            else:
                await message.channel.send("I'm already connected to a voice channel!")

            # Check if the bot is already playing audio
            if voice_client.is_playing():
                await message.channel.send("I'm already playing a song! Wait until it finishes.")
                return

            # Download song information
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
            song_url = data['url']

            # Play the song
            player = discord.FFmpegPCMAudio(song_url, **ffmpeg_options)
            voice_client.play(player, after=lambda e: print(f"Player error: {e}") if e else None)
            await message.channel.send(f"Now playing: {data['title']}")

        except Exception as e:
            print(f"Error: {e}")
            await message.channel.send("An error occurred while trying to play the song.")

    elif message.content.startswith('!disconnect'):
        # Disconnect the bot from the voice channel
        try:
            voice_client = voice_clients.get(message.guild.id)
            if voice_client and voice_client.is_connected():
                await voice_client.disconnect()
                del voice_clients[message.guild.id]
                await message.channel.send("Disconnected from the voice channel.")
            else:
                await message.channel.send("I'm not connected to a voice channel.")
        except Exception as e:
            print(f"Error disconnecting: {e}")
            await message.channel.send("An error occurred while trying to disconnect.")


# Function to run the bot
def run_bot():
    client.run(TOKEN)
