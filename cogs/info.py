import discord
import os
import sys
import random
import time
from random import choice
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure, Bot
from datetime import timedelta

footer = "Made with ❤️ by Tacoz!"
start_time = time.monotonic()


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help',
                      description='The help command',
                      aliases=['commands', 'command'],
                      usage='cog')
    async def help_command(self, ctx, cog='all'):
        ''' Replaces Default Command'''

        print("{} issued .help".format(ctx.author))

        if cog == 'all':
            help_embed = discord.Embed(title='RoxBot Commands', color=0x2ECC71)
            help_embed.add_field(name="Moderation",
                                 value=f"`{ctx.prefix}help moderator`")
            help_embed.add_field(name="Images",
                                 value=f"`{ctx.prefix}help image`")
            help_embed.add_field(name="Utility",
                                 value=f"`{ctx.prefix}help utility`")
            help_embed.add_field(name="Info", value=f"`{ctx.prefix}help info`")
            help_embed.add_field(name="Music",
                                 value=f"`{ctx.prefix}help music`")
            help_embed.add_field(name="Other",
                                 value=f"`{ctx.prefix}help other`")
        else:
            cogA = cog.lower()
            emojiCategory = {
                "Moderator": ":tools:",
                "Image": ":camera:",
                "General": ":tools:",
                "Info": ":question:",
                "Other": "",
                "Music": ":musical_note:",
                "Fun": ":wink:"
            }
            categoryAlias = {
                "mod": "moderator",
                "moderation": "moderator",
                "moderate": "moderator",
                "util": "utility",
                "utils": "utility",
                "utilities": "utility"
            }

            cogs = [c for c in self.bot.cogs.keys()]

            lower_cogs = [c.lower() for c in cogs]

            all_commands = {}
            for cog in cogs:
                all_commands[cog] = self.bot.get_cog(cogs[lower_cogs.index(
                    cog.lower())]).get_commands()

            for cog in all_commands:
                for c in all_commands[cog]:
                    pass  # print(c)

            all_commandsData = [
                c for cog in all_commands for c in all_commands[cog]
            ]
            all_commandsName = [
                c.name for cog in all_commands for c in all_commands[cog]
            ]

            if cogA in lower_cogs:
                help_embed = discord.Embed(
                    title=
                    f'{emojiCategory[cogA.title()]} {cogA.title()} Commands',
                    color=3066993)
                commands_list = self.bot.get_cog(
                    cogs[lower_cogs.index(cogA)]).get_commands()
                help_text = ''

                for command in commands_list:
                    help_text += f'`{command.name}` '
                help_embed.description = help_text

            elif cogA in all_commandsName:
                command = all_commandsData[all_commandsName.index(cogA)]
                help_embed = discord.Embed(
                    title=f'Information about {ctx.prefix}{command.name}',
                    color=3066993)
                help_embed.add_field(name="**Description**\n",
                                     value=f"{command.description}\n",
                                     inline=False)
                help_embed.add_field(name="**Aliases**\n",
                                     value=f"`{' '.join(command.aliases)}`",
                                     inline=False)

            else:
                await ctx.send('Invalid command/category specified.')
                return

        await ctx.send(embed=help_embed)

    @commands.command(name='ping',
                      description='Gets the response time of the bot',
                      aliases=['lag', 'responsetime', 'pingo'])
    async def ping(self, ctx):
        print("{} issued .ping 🏓".format(ctx.author))
        """ Pong! """
        message = await ctx.send("🏓Pong!")
        await message.edit(content=f"{round(Bot.latency * 1000)}ms")

    @commands.command(name='invite',
                      description='Gets the an invite link for the bot',
                      aliases=['botinvite', 'addbot', 'botinv'])
    async def botinvite(self, ctx):
        description = "Invite Link for TacoBOT"
        invite_embed = discord.Embed(title='Invite me to your Server!',
                                     color=3066993)
        print("{} issued .invite 😉".format(ctx.author))
        invite_embed.add_field(
            name=f"Full Permissions",
            value=
            f"https://discord.com/api/oauth2/authorize?client_id=566193825874182164&permissions=8&scope=bot"
        )
        invite_embed.set_footer(text=footer)
        await ctx.send(embed=invite_embed)

    @commands.command(name='support',
                      description='Gets the support server invite',
                      aliases=[
                          'server', 'supportserver', 'helpserver',
                          'helpinvite', 'devserver'
                      ])
    async def serverinvite(self, ctx):
        print("{} issued .serverinvite".format(ctx.author))
        invite_embed = discord.Embed(
            title='Official Tacoz & TacoBOT Development server!',
            description=f"https://discord.io/Tacoz",
            color=3066993)
        invite_embed.set_footer(text=footer)
        await ctx.send(embed=invite_embed)


"""
    @commands.command(
        name='source',
        description='Gets the source code link',
        aliases=['sourcecode']
    )
    async def sourceCode(self, ctx):
        source_embed = discord.Embed(
            title='Here is my Source Code!',
            description=f"https://github.com/NotTacoz/TacoBot",
            color=3066993
        )
        source_embed.set_footer(text=footer)
        await ctx.send(embed=source_embed)
"""


def setup(bot):
    bot.add_cog(Info(bot))