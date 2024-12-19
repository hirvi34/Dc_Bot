import discord
from discord.ext import commands
import os
import yt_dlp as youtube_dl
import asyncio
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

queue = []

@bot.event
async def on_ready():
    print("bot ready")
    print('------')


@bot.command()
async def hello(ctx):
    await ctx.send(f'fuck u all')

@bot.command()
async def miksi(ctx):
    await ctx.send("koska prkl yt_dl vittu toimi saatana toimi homo huora")

@bot.command()
async def kiitos(ctx):
    await ctx.send("ole hyvä")