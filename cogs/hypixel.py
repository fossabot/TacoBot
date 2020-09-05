import discord
import os
import sys
import random
import asyncio
import time
import requests
import math
from random import choice
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure, Bot
from datetime import timedelta

footer = "『 TacoBot ✦ Tacoz 』"
start_time = time.monotonic()
apikey = "a54ce218-4fd5-4798-9b4b-6c74efac3456"


class Hypixel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["generalhelp"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def general(self, ctx, *, message):
        data = requests.get(
            f"https://api.hypixel.net/player?key={apikey}&name={message.lower()}"
        ).json()
        if data["success"] == True and data["player"] != None:
            try:
                rank = data["player"]["prefix"]
                rank = rank.replace("§c", "")
                rank = rank.replace("§e", "")
                rank = rank.replace("§a", "")
                rank = rank.replace("§b", "")
                rank = rank.replace("§9", "")
                rank = rank.replace("§d", "")
                rank = rank.replace("§4", "")
                rank = rank.replace("§7", "")
                rank = rank.replace("§4", "")
                rank = rank.replace("§6", "")
                rank = rank.replace("§2", "")
                rank = rank.replace("§3", "")
                rank = rank.replace("§1", "")
                rank = rank.replace("§5", "")
                rank = rank.replace("§8", "")
                rank = rank.replace("§0", "")
                rank = rank.replace("§1", "")
                rank = rank.replace("§m", "")
                rank = rank.replace("§n", "")
                rank = rank.replace("§o", "")
                rank = rank.replace("§k", "")
                rank = rank.replace("§r", "")
                rank = rank.replace("[", "")
                rank = rank.replace("]", "")
            except:
                try:
                    rank = data["player"]["rank"]
                except:
                    try:
                        rank = data["player"]["monthlyPackageRank"]
                        rank = rank.replace("SUPERSTAR", "MVP++")
                    except:
                        try:
                            rank = data["player"]["newPackageRank"]
                            rank = rank.replace("_PLUS", "+")
                        except:
                            try:
                                rank = data["player"]["packageRank"]
                                rank = rank.replace("_PLUS", "+")
                            except:
                                rank = "NON"
            networkExp = data["player"]["networkExp"]
            uuid = data["player"]["uuid"]
            networkLevel = (math.sqrt(networkExp + 15312.5) - 125 / math.sqrt(2)) / (
                25 * math.sqrt(2)
            )
            networkLevel = round(networkLevel, 2)
            name = data["player"]["displayname"]
            full = f"[{rank}] {name}"
            firstloginunix = data["player"]["firstLogin"]
            firstlogin = time.strftime(
                "%Y-%m-%d %H:%M", time.localtime(int(firstloginunix) / 1000.0)
            )
            try:
                lastloginunix = data["player"]["lastLogin"]
                lastlogin = time.strftime(
                    "%Y-%m-%d %H:%M", time.localtime(int(lastloginunix) / 1000.0)
                )
            except:
                pass
            pastusernames = ", ".join(data["player"]["knownAliases"])
            karma = data["player"]["karma"]
            achievementPoints = data["player"]["achievementPoints"]
            guild = requests.get(
                f"https://api.hypixel.net/guild?key={apikey}&player={uuid}"
            ).json()
            if guild["success"] == True:
                try:
                    guildtag = guild["guild"]["tag"]
                    full = f"[{rank}] {name} [{guildtag}]"
                except:
                    full = f"[{rank}] {name}"

            try:
                friends = requests.get(
                    f"https://api.hypixel.net/friends?key={apikey}&uuid={uuid}"
                ).json()
                friendlen = len(list(friends["records"]))
            except:
                friends = 0

        if data["success"] == False:
            embedVar = discord.Embed(
                title=":no_entry_sign: Something went wrong", color=13381166
            )
            error = data["cause"]
            embedVar.add_field(name="Error", value=f"``{error}``", inline=True)
            embedVar.set_footer(text=footer)
            await ctx.send(embed=embedVar)
        elif data["player"] == None:
            embedVar = discord.Embed(
                title=":no_entry_sign: Something went wrong", color=13381166
            )
            error = data["cause"]
            embedVar.add_field(
                name="Error", value=f"``❌ The player is probably banned``", inline=True
            )
            embedVar.set_footer(text=footer)
            await ctx.send(embed=embedVar)
        else:
            embedVar = discord.Embed(
                title=f"{full}",
                url=f"http://hypixel.net/player/{message}",
                color=15105570,
            )
            embedVar.set_author(name="Hypixel Stats - General [BETA]")
            embedVar.add_field(name="UUID", value=f"``{uuid}``", inline=True)
            embedVar.add_field(
                name="Network Level", value=f"``{networkLevel}``", inline=True
            )
            embedVar.add_field(
                name="Network Exp", value=f"``{networkExp}``", inline=True
            )
            embedVar.add_field(name="Karma", value=f"``{karma}``", inline=True)
            embedVar.add_field(name="Friends", value=f"``{friendlen}``", inline=True)
            embedVar.add_field(
                name="Achivement Points", value=f"``{achievementPoints}``", inline=True
            )
            try:
                embedVar.add_field(
                    name="First • Last Login",
                    value=f"``{firstlogin} • {lastlogin} (EDT)``",
                    inline=True,
                )
            except:
                embedVar.add_field(
                    name="First Login", value=f"``{firstlogin} (EDT)``", inline=True
                )
            embedVar.add_field(
                name="Past usernames", value=f"``{pastusernames}``", inline=True
            )

            embedVar.set_thumbnail(
                url=f"https://crafatar.com/avatars/{uuid}?default=MHF_Steve&overlay"
            )  # alternatives: https://crafatar.com/avatars/uuid https://crafatar.com/renders/head/uuid https://crafatar.com/renders/body/uuid
            embedVar.set_footer(text=footer)
            await ctx.send(embed=embedVar)

    @general.error
    async def general_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please Input something after the command")
        else:
            raise (error)

    @commands.command(aliases=["watchdog", "banstats", "hypixelban"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def watchdogstats(self, ctx):
        watchdog = requests.get(
            f"https://api.hypixel.net/watchdogstats?key={apikey}"
        ).json()
        lastminute = watchdog["watchdog_lastMinute"]
        watchdogtotal = watchdog["watchdog_total"]
        watchdogdaily = watchdog["watchdog_rollingDaily"]
        staffdaily = watchdog["staff_rollingDaily"]
        stafftotal = watchdog["staff_total"]
        embedVar = discord.Embed(title=f"Hypixel Ban Stats", color=15105570)
        embedVar.add_field(
            name="Watchdog Bans",
            value=f"Last Minute - `{lastminute}`\nToday - `{watchdogdaily}`\nTotal - `{watchdogtotal}`",
            inline=True,
        )
        embedVar.add_field(
            name="Staff Bans",
            value=f"Today - `{staffdaily}`\nTotal - `{stafftotal}`",
            inline=True,
        )

        embedVar.set_thumbnail(
            url=f"https://render.namemc.com/skin/3d/body.png?skin=2d1f536e7e659774&model=classic&width=175&height=350"
        )
        embedVar.set_footer(text=footer)
        await ctx.send(embed=embedVar)

    @commands.command(
        aliases=["bedwarshelp", "bedwarsstats", "bedwarstats", "bedwarstat"]
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def bedwars(self, ctx, msg: str):
        msg = msg.lower()
        data = requests.get(
            f"https://api.hypixel.net/player?key={apikey}&name={msg}"
        ).json()

        if data["success"] == True and data["player"] != None:
            try:
                rank = data["player"]["prefix"]
                rank = rank.replace("§c", "")
                rank = rank.replace("§e", "")
                rank = rank.replace("§a", "")
                rank = rank.replace("§b", "")
                rank = rank.replace("§9", "")
                rank = rank.replace("§d", "")
                rank = rank.replace("§4", "")
                rank = rank.replace("§7", "")
                rank = rank.replace("§4", "")
                rank = rank.replace("§6", "")
                rank = rank.replace("§2", "")
                rank = rank.replace("§3", "")
                rank = rank.replace("§1", "")
                rank = rank.replace("§5", "")
                rank = rank.replace("§8", "")
                rank = rank.replace("§0", "")
                rank = rank.replace("§1", "")
                rank = rank.replace("§m", "")
                rank = rank.replace("§n", "")
                rank = rank.replace("§o", "")
                rank = rank.replace("§k", "")
                rank = rank.replace("§r", "")
                rank = rank.replace("[", "")
                rank = rank.replace("]", "")
            except:
                try:
                    rank = data["player"]["rank"]
                except:
                    try:
                        rank = data["player"]["monthlyPackageRank"]
                        rank = rank.replace("SUPERSTAR", "MVP++")
                    except:
                        try:
                            rank = data["player"]["newPackageRank"]
                            rank = rank.replace("_PLUS", "+")
                        except:
                            try:
                                rank = data["player"]["packageRank"]
                                rank = rank.replace("_PLUS", "+")
                            except:
                                rank = "NON"
            bwdata = data["player"]["stats"]["Bedwars"]
            bwlevel = data["player"]["achievements"]["bedwars_level"]
            bwcoins = bwdata["coins"]
            bwwinstreak = bwdata["winstreak"]
            bwwins = bwdata["wins_bedwars"]
            bwlosses = bwdata["losses_bedwars"]
            bwwinlossratio = round(bwwins / bwlosses, 2)
            bwkills = bwdata["kills_bedwars"]
            bwdeaths = bwdata["deaths_bedwars"]
            bwkdr = round(bwkills / bwdeaths, 2)
            bwfinalkills = bwdata["final_kills_bedwars"]
            bwfinaldeaths = bwdata["final_deaths_bedwars"]
            bwfkdr = round(bwfinalkills / bwfinaldeaths, 2)
            bwbedlost = bwdata["beds_lost_bedwars"]
            bwbedbreak = bwdata["beds_broken_bedwars"]
            bblr = bwbedbreak / bwbedlost
            gamesplayed = bwdata["games_played_bedwars"]
            finalspergame = bwfinalkills / gamesplayed
            bedspergame = bwbedbreak / gamesplayed

            bwwinstreak1 = bwdata["eight_one_winstreak"]
            bwwins1 = bwdata["eight_one_wins_bedwars"]
            bwlosses1 = bwdata["eight_one_losses_bedwars"]
            bwwinlossratio1 = round(bwwins1 / bwlosses1, 2)
            bwkills1 = bwdata["eight_one_kills_bedwars"]
            bwdeaths1 = bwdata["eight_one_deaths_bedwars"]
            bwkdr1 = round(bwkills1 / bwdeaths1, 2)
            bwfinalkills1 = bwdata["eight_one_final_kills_bedwars"]
            bwfinaldeaths1 = bwdata["eight_one_final_deaths_bedwars"]
            bwfkdr1 = round(bwfinalkills1 / bwfinaldeaths1, 2)
            bwbedlost1 = bwdata["eight_one_beds_lost_bedwars"]
            bwbedbreak1 = bwdata["eight_one_beds_broken_bedwars"]
            bblr1 = bwbedbreak1 / bwbedlost1
            gamesplayed1 = bwdata["eight_one_games_played_bedwars"]
            finalspergame1 = bwfinalkills1 / gamesplayed1
            bedspergame1 = bwbedbreak1 / gamesplayed1

            bwwinstreak2 = bwdata["eight_two_winstreak"]
            bwwins2 = bwdata["eight_two_wins_bedwars"]
            bwlosses2 = bwdata["eight_two_losses_bedwars"]
            bwwinlossratio2 = round(bwwins2 / bwlosses2, 2)
            bwkills2 = bwdata["eight_two_kills_bedwars"]
            bwdeaths2 = bwdata["eight_two_deaths_bedwars"]
            bwkdr2 = round(bwkills2 / bwdeaths2, 2)
            bwfinalkills2 = bwdata["eight_two_final_kills_bedwars"]
            bwfinaldeaths2 = bwdata["eight_two_final_deaths_bedwars"]
            bwfkdr2 = round(bwfinalkills2 / bwfinaldeaths2, 2)
            bwbedlost2 = bwdata["eight_two_beds_lost_bedwars"]
            bwbedbreak2 = bwdata["eight_two_beds_broken_bedwars"]
            bblr2 = bwbedbreak2 / bwbedlost2
            gamesplayed2 = bwdata["eight_two_games_played_bedwars"]
            finalspergame2 = bwfinalkills2 / gamesplayed2
            bedspergame2 = bwbedbreak2 / gamesplayed2

            bwwinstreak3 = bwdata["four_three_winstreak"]
            bwwins3 = bwdata["four_three_wins_bedwars"]
            bwlosses3 = bwdata["four_three_losses_bedwars"]
            bwwinlossratio3 = round(bwwins3 / bwlosses3, 2)
            bwkills3 = bwdata["four_three_kills_bedwars"]
            bwdeaths3 = bwdata["four_three_deaths_bedwars"]
            bwkdr3 = round(bwkills3 / bwdeaths3, 2)
            bwfinalkills3 = bwdata["four_three_final_kills_bedwars"]
            bwfinaldeaths3 = bwdata["four_three_final_deaths_bedwars"]
            bwfkdr3 = round(bwfinalkills3 / bwfinaldeaths3, 2)
            bwbedlost3 = bwdata["four_three_beds_lost_bedwars"]
            bwbedbreak3 = bwdata["four_three_beds_broken_bedwars"]
            bblr3 = bwbedbreak3 / bwbedlost3
            gamesplayed3 = bwdata["four_three_games_played_bedwars"]
            finalspergame3 = bwfinalkills3 / gamesplayed3
            bedspergame3 = bwbedbreak3 / gamesplayed3

            bwwinstreak4 = bwdata["four_four_winstreak"]
            bwwins4 = bwdata["four_four_wins_bedwars"]
            bwlosses4 = bwdata["four_four_losses_bedwars"]
            bwwinlossratio4 = round(bwwins4 / bwlosses4, 2)
            bwkills4 = bwdata["four_four_kills_bedwars"]
            bwdeaths4 = bwdata["four_four_deaths_bedwars"]
            bwkdr4 = round(bwkills4 / bwdeaths4, 2)
            bwfinalkills4 = bwdata["four_four_final_kills_bedwars"]
            bwfinaldeaths4 = bwdata["four_four_final_deaths_bedwars"]
            bwfkdr4 = round(bwfinalkills4 / bwfinaldeaths4, 2)
            bwbedlost4 = bwdata["four_four_beds_lost_bedwars"]
            bwbedbreak4 = bwdata["four_four_beds_broken_bedwars"]
            bblr4 = bwbedbreak4 / bwbedlost4
            gamesplayed4 = bwdata["four_four_games_played_bedwars"]
            finalspergame4 = bwfinalkills4 / gamesplayed4
            bedspergame4 = bwbedbreak4 / gamesplayed4

            bwwinstreak4v4 = bwdata["two_four_winstreak"]
            bwwins4v4 = bwdata["two_four_wins_bedwars"]
            bwlosses4v4 = bwdata["two_four_losses_bedwars"]
            bwwinlossratio4v4 = round(bwwins4v4 / bwlosses4v4, 2)
            bwkills4v4 = bwdata["two_four_kills_bedwars"]
            bwdeaths4v4 = bwdata["two_four_deaths_bedwars"]
            bwkdr4v4 = round(bwkills4v4 / bwdeaths4v4, 2)
            bwfinalkills4v4 = bwdata["two_four_final_kills_bedwars"]
            bwfinaldeaths4v4 = bwdata["two_four_final_deaths_bedwars"]
            bwfkdr4v4 = round(bwfinalkills4v4 / bwfinaldeaths4v4, 2)
            bwbedlost4v4 = bwdata["two_four_beds_lost_bedwars"]
            bwbedbreak4v4 = bwdata["two_four_beds_broken_bedwars"]
            bblr4v4 = bwbedbreak4v4 / bwbedlost4v4
            gamesplayed4v4 = bwdata["two_four_games_played_bedwars"]
            finalspergame4v4 = bwfinalkills4v4 / gamesplayed4v4
            bedspergame4v4 = bwbedbreak4v4 / gamesplayed4v4

            bblr = round(bblr, 2)
            bblr1 = round(bblr1, 2)
            bblr2 = round(bblr2, 2)
            bblr3 = round(bblr3, 2)
            bblr4 = round(bblr4, 2)
            bblr4v4 = round(bblr4v4, 2)

            finalspergame = round(finalspergame, 2)
            finalspergame1 = round(finalspergame1, 2)
            finalspergame2 = round(finalspergame2, 2)
            finalspergame3 = round(finalspergame3, 2)
            finalspergame4 = round(finalspergame4, 2)
            finalspergame4v4 = round(finalspergame4v4, 2)

            bedspergame = round(bedspergame, 2)
            bedspergame1 = round(bedspergame1, 2)
            bedspergame2 = round(bedspergame2, 2)
            bedspergame3 = round(bedspergame3, 2)
            bedspergame4 = round(bedspergame4, 2)
            bedspergame4v4 = round(bedspergame4v4, 2)

        if data["success"] == False:
            embedVar = discord.Embed(
                title=":no_entry_sign: Something went wrong", color=13381166
            )
            error = data["cause"]
            embedVar.add_field(name="Error", value=f"``{error}``", inline=True)
            embedVar.set_footer(text=footer)
            await ctx.send(embed=embedVar)
        elif data["player"] == None:
            embedVar = discord.Embed(
                title=":no_entry_sign: Something went wrong", color=13381166
            )
            error = data["cause"]
            embedVar.add_field(
                name="Error", value=f"``❌ The player is probably banned``", inline=True
            )
            embedVar.set_footer(text=footer)
            await ctx.send(embed=embedVar)
        else:
            displayname = data["player"]["displayname"]
            full = f"[{rank}] {displayname}"
            uuid = data["player"]["uuid"]
            embedVar = discord.Embed(
                title=f"{full}",
                color=15105570,
                url=f"https://hypixel.net/player/{msg}",
            )
            embedVar.set_author(
                name="Overall Bedwars Stats",
                icon_url="https://statsify.net/img/assets/hypixel/bedwars.png",
            )
            embedVar.add_field(name="Stars", value=f"``{bwlevel}☆``", inline=True)
            embedVar.add_field(name="Coins", value=f"``{bwcoins:,}``", inline=True)
            embedVar.add_field(
                name="Winstreak", value=f"``{bwwinstreak:,}``", inline=True
            )
            embedVar.add_field(name="Wins", value=f"``{bwwins}``", inline=True)
            embedVar.add_field(name="Losses", value=f"``{bwlosses:,}``", inline=True)
            embedVar.add_field(
                name="Win Loss Ratio", value=f"``{bwwinlossratio:,}``", inline=True
            )
            embedVar.add_field(name="Kills", value=f"``{bwkills:,}``", inline=True)
            embedVar.add_field(name="Deaths", value=f"``{bwdeaths:,}``", inline=True)
            embedVar.add_field(name="KDR", value=f"``{bwkdr}``", inline=True)
            embedVar.add_field(
                name="Final Kills", value=f"``{bwfinalkills:,}``", inline=True
            )
            embedVar.add_field(
                name="Final Deaths", value=f"``{bwfinaldeaths:,}``", inline=True
            )
            embedVar.add_field(name="Final KDR", value=f"``{bwfkdr:,}``", inline=True)
            embedVar.add_field(
                name="Beds Lost", value=f"``{bwbedlost:,}``", inline=True
            )
            embedVar.add_field(
                name="Beds Broken", value=f"``{bwbedbreak:,}``", inline=True
            )
            embedVar.add_field(name="BBLR", value=f"``{bblr:,}``", inline=True)
            embedVar.add_field(
                name="Finals/Game", value=f"``{finalspergame:,}``", inline=True
            )
            embedVar.add_field(
                name="Beds/Game", value=f"``{bedspergame:,}``", inline=True
            )
            embedVar.add_field(
                name="Games Played", value=f"``{gamesplayed:,}``", inline=True
            )

            solo = discord.Embed(
                title=f"{full}",
                color=15105570,
                url=f"https://hypixel.net/player/{msg}",
            )
            solo.set_author(
                name="Overall Bedwars Stats",
                icon_url="https://statsify.net/img/assets/hypixel/bedwars.png",
            )
            solo.add_field(name="Stars", value=f"``{bwlevel}☆``", inline=True)
            solo.add_field(name="Coins", value=f"``{bwcoins:,}``", inline=True)
            solo.add_field(name="Winstreak", value=f"``{bwwinstreak1:,}``", inline=True)
            solo.add_field(name="Wins", value=f"``{bwwins1}``", inline=True)
            solo.add_field(name="Losses", value=f"``{bwlosses1:,}``", inline=True)
            solo.add_field(
                name="Win Loss Ratio", value=f"``{bwwinlossratio1:,}``", inline=True
            )
            solo.add_field(name="Kills", value=f"``{bwkills1:,}``", inline=True)
            solo.add_field(name="Deaths", value=f"``{bwdeaths1:,}``", inline=True)
            solo.add_field(name="KDR", value=f"``{bwkdr1}``", inline=True)
            solo.add_field(
                name="Final Kills", value=f"``{bwfinalkills1:,}``", inline=True
            )
            solo.add_field(
                name="Final Deaths", value=f"``{bwfinaldeaths1:,}``", inline=True
            )
            solo.add_field(name="Final KDR", value=f"``{bwfkdr1:,}``", inline=True)
            solo.add_field(name="Beds Lost", value=f"``{bwbedlost1:,}``", inline=True)
            solo.add_field(
                name="Beds Broken", value=f"``{bwbedbreak1:,}``", inline=True
            )
            solo.add_field(name="BBLR", value=f"``{bblr1:,}``", inline=True)
            solo.add_field(
                name="Finals/Game", value=f"``{finalspergame1:,}``", inline=True
            )
            solo.add_field(name="Beds/Game", value=f"``{bedspergame1:,}``", inline=True)
            solo.add_field(
                name="Games Played", value=f"``{gamesplayed1:,}``", inline=True
            )

            doubles = discord.Embed(
                title=f"{full}",
                color=15105570,
                url=f"https://hypixel.net/player/{msg}",
            )
            doubles.set_author(
                name="Overall Bedwars Stats",
                icon_url="https://statsify.net/img/assets/hypixel/bedwars.png",
            )
            doubles.add_field(name="Stars", value=f"``{bwlevel}☆``", inline=True)
            doubles.add_field(name="Coins", value=f"``{bwcoins:,}``", inline=True)
            doubles.add_field(
                name="Winstreak", value=f"``{bwwinstreak2:,}``", inline=True
            )
            doubles.add_field(name="Wins", value=f"``{bwwins2}``", inline=True)
            doubles.add_field(name="Losses", value=f"``{bwlosses2:,}``", inline=True)
            doubles.add_field(
                name="Win Loss Ratio", value=f"``{bwwinlossratio2:,}``", inline=True
            )
            doubles.add_field(name="Kills", value=f"``{bwkills2:,}``", inline=True)
            doubles.add_field(name="Deaths", value=f"``{bwdeaths2:,}``", inline=True)
            doubles.add_field(name="KDR", value=f"``{bwkdr2}``", inline=True)
            doubles.add_field(
                name="Final Kills", value=f"``{bwfinalkills2:,}``", inline=True
            )
            doubles.add_field(
                name="Final Deaths", value=f"``{bwfinaldeaths2:,}``", inline=True
            )
            doubles.add_field(name="Final KDR", value=f"``{bwfkdr2:,}``", inline=True)
            doubles.add_field(
                name="Beds Lost", value=f"``{bwbedlost2:,}``", inline=True
            )
            doubles.add_field(
                name="Beds Broken", value=f"``{bwbedbreak2:,}``", inline=True
            )
            doubles.add_field(name="BBLR", value=f"``{bblr2:,}``", inline=True)
            doubles.add_field(
                name="Finals/Game", value=f"``{finalspergame2:,}``", inline=True
            )
            doubles.add_field(
                name="Beds/Game", value=f"``{bedspergame2:,}``", inline=True
            )
            doubles.add_field(
                name="Games Played", value=f"``{gamesplayed2:,}``", inline=True
            )

            threes = discord.Embed(
                title=f"{full}",
                color=15105570,
                url=f"https://hypixel.net/player/{msg}",
            )
            threes.set_author(
                name="Overall Bedwars Stats",
                icon_url="https://statsify.net/img/assets/hypixel/bedwars.png",
            )
            threes.add_field(name="Stars", value=f"``{bwlevel}☆``", inline=True)
            threes.add_field(name="Coins", value=f"``{bwcoins:,}``", inline=True)
            threes.add_field(
                name="Winstreak", value=f"``{bwwinstreak3:,}``", inline=True
            )
            threes.add_field(name="Wins", value=f"``{bwwins3}``", inline=True)
            threes.add_field(name="Losses", value=f"``{bwlosses3:,}``", inline=True)
            threes.add_field(
                name="Win Loss Ratio", value=f"``{bwwinlossratio3:,}``", inline=True
            )
            threes.add_field(name="Kills", value=f"``{bwkills3:,}``", inline=True)
            threes.add_field(name="Deaths", value=f"``{bwdeaths3:,}``", inline=True)
            threes.add_field(name="KDR", value=f"``{bwkdr3}``", inline=True)
            threes.add_field(
                name="Final Kills", value=f"``{bwfinalkills3:,}``", inline=True
            )
            threes.add_field(
                name="Final Deaths", value=f"``{bwfinaldeaths3:,}``", inline=True
            )
            threes.add_field(name="Final KDR", value=f"``{bwfkdr3:,}``", inline=True)
            threes.add_field(name="Beds Lost", value=f"``{bwbedlost3:,}``", inline=True)
            threes.add_field(
                name="Beds Broken", value=f"``{bwbedbreak3:,}``", inline=True
            )
            threes.add_field(name="BBLR", value=f"``{bblr3:,}``", inline=True)
            threes.add_field(
                name="Finals/Game", value=f"``{finalspergame3:,}``", inline=True
            )
            threes.add_field(
                name="Beds/Game", value=f"``{bedspergame3:,}``", inline=True
            )
            threes.add_field(
                name="Games Played", value=f"``{gamesplayed3:,}``", inline=True
            )

            fours = discord.Embed(
                title=f"{full}",
                color=15105570,
                url=f"https://hypixel.net/player/{msg}",
            )
            fours.set_author(
                name="Overall Bedwars Stats",
                icon_url="https://statsify.net/img/assets/hypixel/bedwars.png",
            )
            fours.add_field(name="Stars", value=f"``{bwlevel}☆``", inline=True)
            fours.add_field(name="Coins", value=f"``{bwcoins:,}``", inline=True)
            fours.add_field(
                name="Winstreak", value=f"``{bwwinstreak4:,}``", inline=True
            )
            fours.add_field(name="Wins", value=f"``{bwwins4}``", inline=True)
            fours.add_field(name="Losses", value=f"``{bwlosses4:,}``", inline=True)
            fours.add_field(
                name="Win Loss Ratio", value=f"``{bwwinlossratio4:,}``", inline=True
            )
            fours.add_field(name="Kills", value=f"``{bwkills4:,}``", inline=True)
            fours.add_field(name="Deaths", value=f"``{bwdeaths4:,}``", inline=True)
            fours.add_field(name="KDR", value=f"``{bwkdr4}``", inline=True)
            fours.add_field(
                name="Final Kills", value=f"``{bwfinalkills4:,}``", inline=True
            )
            fours.add_field(
                name="Final Deaths", value=f"``{bwfinaldeaths4:,}``", inline=True
            )
            fours.add_field(name="Final KDR", value=f"``{bwfkdr4:,}``", inline=True)
            fours.add_field(name="Beds Lost", value=f"``{bwbedlost4:,}``", inline=True)
            fours.add_field(
                name="Beds Broken", value=f"``{bwbedbreak4:,}``", inline=True
            )
            fours.add_field(name="BBLR", value=f"``{bblr4:,}``", inline=True)
            fours.add_field(
                name="Finals/Game", value=f"``{finalspergame4:,}``", inline=True
            )
            fours.add_field(
                name="Beds/Game", value=f"``{bedspergame4:,}``", inline=True
            )
            fours.add_field(
                name="Games Played", value=f"``{gamesplayed4:,}``", inline=True
            )

            fours2 = discord.Embed(
                title=f"{full}",
                color=15105570,
                url=f"https://hypixel.net/player/{msg}",
            )
            fours2.set_author(
                name="Overall Bedwars Stats",
                icon_url="https://statsify.net/img/assets/hypixel/bedwars.png",
            )
            fours2.add_field(name="Stars", value=f"``{bwlevel}☆``", inline=True)
            fours2.add_field(name="Coins", value=f"``{bwcoins:,}``", inline=True)
            fours2.add_field(
                name="Winstreak", value=f"``{bwwinstreak4v4:,}``", inline=True
            )
            fours2.add_field(name="Wins", value=f"``{bwwins4v4}``", inline=True)
            fours2.add_field(name="Losses", value=f"``{bwlosses4v4:,}``", inline=True)
            fours2.add_field(
                name="Win Loss Ratio", value=f"``{bwwinlossratio4v4:,}``", inline=True
            )
            fours2.add_field(name="Kills", value=f"``{bwkills4v4:,}``", inline=True)
            fours2.add_field(name="Deaths", value=f"``{bwdeaths4v4:,}``", inline=True)
            fours2.add_field(name="KDR", value=f"``{bwkdr4v4}``", inline=True)
            fours2.add_field(
                name="Final Kills", value=f"``{bwfinalkills4v4:,}``", inline=True
            )
            fours2.add_field(
                name="Final Deaths", value=f"``{bwfinaldeaths4v4:,}``", inline=True
            )
            fours2.add_field(name="Final KDR", value=f"``{bwfkdr4v4:,}``", inline=True)
            fours2.add_field(
                name="Beds Lost", value=f"``{bwbedlost4v4:,}``", inline=True
            )
            fours2.add_field(
                name="Beds Broken", value=f"``{bwbedbreak4v4:,}``", inline=True
            )
            fours2.add_field(name="BBLR", value=f"``{bblr4v4:,}``", inline=True)
            fours2.add_field(
                name="Finals/Game", value=f"``{finalspergame4v4:,}``", inline=True
            )
            fours2.add_field(
                name="Beds/Game", value=f"``{bedspergame4v4:,}``", inline=True
            )
            fours2.add_field(
                name="Games Played", value=f"``{gamesplayed4v4:,}``", inline=True
            )

            solo.set_thumbnail(
                url=f"https://crafatar.com/avatars/{uuid}?default=MHF_Steve&overlay"
            )  # alternatives: https://crafatar.com/avatars/uuid https://crafatar.com/renders/head/uuid https://crafatar.com/renders/body/uuid
            solo.set_footer(text=footer)
            doubles.set_thumbnail(
                url=f"https://crafatar.com/avatars/{uuid}?default=MHF_Steve&overlay"
            )  # alternatives: https://crafatar.com/avatars/uuid https://crafatar.com/renders/head/uuid https://crafatar.com/renders/body/uuid
            doubles.set_footer(text=footer)
            threes.set_thumbnail(
                url=f"https://crafatar.com/avatars/{uuid}?default=MHF_Steve&overlay"
            )  # alternatives: https://crafatar.com/avatars/uuid https://crafatar.com/renders/head/uuid https://crafatar.com/renders/body/uuid
            threes.set_footer(text=footer)
            fours.set_thumbnail(
                url=f"https://crafatar.com/avatars/{uuid}?default=MHF_Steve&overlay"
            )  # alternatives: https://crafatar.com/avatars/uuid https://crafatar.com/renders/head/uuid https://crafatar.com/renders/body/uuid
            fours.set_footer(text=footer)
            fours2.set_thumbnail(
                url=f"https://crafatar.com/avatars/{uuid}?default=MHF_Steve&overlay"
            )  # alternatives: https://crafatar.com/avatars/uuid https://crafatar.com/renders/head/uuid https://crafatar.com/renders/body/uuid
            fours2.set_footer(text=footer)
            embedVar.set_thumbnail(
                url=f"https://crafatar.com/avatars/{uuid}?default=MHF_Steve&overlay"
            )  # alternatives: https://crafatar.com/avatars/uuid https://crafatar.com/renders/head/uuid https://crafatar.com/renders/body/uuid
            embedVar.set_footer(text=footer)

            message = await ctx.send(embed=embedVar)

            Left = await message.add_reaction("◀")
            Right = await message.add_reaction("▶")
            Stop = await message.add_reaction("⏹")

            start_time = time.time()  # remember when we started
            while (time.time() - start_time) < 6.0:
                pass

            await message.clear_reaction("◀")
            await message.clear_reaction("▶")
            await message.clear_reaction("⏹")

    @bedwars.error
    async def bedwars_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please Input something after the command")
        else:
            raise (error)


def setup(bot):
    bot.add_cog(Hypixel(bot))
