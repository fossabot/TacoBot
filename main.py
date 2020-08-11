import discord
import math
import time
import os
import random
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure
from discord.ext.commands import Bot

TOKEN = 'NTY2MTkzODI1ODc0MTgyMTY0.XLBbFw.o0yHAbU7R2yq5GnpdO7P7pzJyRY'
PREFIX = (".", ">")
client = commands.Bot(command_prefix=PREFIX)


@client.event
async def on_ready():
  activity = discord.Game(name=".help | http://youtube.com/tacozlmao", type=1)
  await client.change_presence(status=discord.Status.idle, activity=activity)
  print(f"{client.user.name} is Launched")
  print(client.user.id)
  print('-------------')

@client.command()
async def hello(ctx):
    message_author = ctx.author
    message_channel = ctx.channel
    print("{} issued .hello 👋".format(message_author))
    await message_channel.send("Hello, {}! 👋".format(message_author.name))


@client.command()
async def ping(ctx):
    message_author = ctx.author
    print("{} issued .ping 🏓".format(message_author))
    await ctx.send(f'🏓 Pong! {round(client.latency * 1000)}ms')


@client.command()
async def invite(ctx):
    message_author = ctx.author
    message_channel = ctx.channel

    print("{} issued .invite 😉".format(message_author))

    await ctx.send("Check Your Dm's :wink:")
    await message_author.send('https://discord.com/api/oauth2/authorize?client_id=566193825874182164&permissions=8&scope=bot')


@client.command()
async def dankrate(ctx):
    message_author = ctx.author
    message_channel = ctx.channel

    aaaaa = random.randint(1, 101)
    print("{} issued .dankrate 💸".format(message_author))
    
    if aaaaa == 101:
        embedVar = discord.Embed(
            title="Dank r8 Machine", description=f"you broke the dank machine >:( :fire:", color=ff9933)
    else:
        embedVar = discord.Embed(title="Dank r8 Machine", description=f"you are {aaaaa}% dank", color=ff9933)
    await message_channel.send(embed=embedVar)


client.run(TOKEN)
