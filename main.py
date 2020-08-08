import discord
from discord.ext import commands
import math
import os

TOKEN = 'NTY2MTkzODI1ODc0MTgyMTY0.XLBbFw.o0yHAbU7R2yq5GnpdO7P7pzJyRY'
PREFIX = (".", ">")
client = commands.Bot(command_prefix=".")

@client.event
async def on_ready():
    activity = discord.Game(name=".help | http://youtube.com/tacozlmao", type=1)
    await client.change_presence(status=discord.Status.idle, activity=activity)
    print(f"{client.user.name} is Launched") 
    print(client.user.name)
    print(client.user.id)
    print('------')


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

    print("{} issued .invite 👋".format(message_author))

    await message_channel.send(f'https://discord.com/api/oauth2/authorize?client_id=566193825874182164&permissions=8&scope=bot')

@client.event
async def on_member_join(self, member):
      guild = member.guild
      if guild.system_channel is not None:
          to_send = 'Welcome {0.mention} to {1.name}!'.format(member, guild)
          await guild.system_channel.send(to_send)

client.run(TOKEN)