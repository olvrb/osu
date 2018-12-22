import discord
from discord.ext import commands
import requests
from osuapi import OsuApi, AHConnector, enums
import config
from urllib.parse import quote
from lib import converters


class Osu:

    def __init__(self, bot):
        self.api = OsuApi(config.osu, connector=AHConnector())
        self.bot = bot

    def banner_url(self, mode, user, colour='bb1177'):
        return f'https://lemmmy.pw/osusig/sig.php?colour=hex{colour}&mode={mode}&uname={quote(user)}&pp=2&countryrank&flagstroke&darktriangles&onlineindicator=undefined&xpbar&xpbarhex'

    @commands.group(invoke_without_command=True)
    async def user(self, ctx, *, name: converters.player):
        '''Fetch a user's profile. Usage: osu!user <username> <optional: osu/taiko/mania/fruits>'''
        mode = self.bot.mode_for(ctx.author)
        # empty list if not found
        results = await self.api.get_user(name, mode={'osu': enums.OsuMode.osu, 'taiko': enums.OsuMode.taiko, 'mania': enums.OsuMode.mania, 'fruits': enums.OsuMode.ctb}[mode])
        if results:
            embed = discord.Embed(colour=self.bot.colour_for(ctx.author), title='osu! user: ' +
                                  results[0].username, url=f'https://osu.ppy.sh/users/{results[0].user_id}/{mode}')
            embed.add_field(
                name="User Info", value=f"""User ID: {results[0].user_id}
                Level: {int(results[0].level)}
                Country: {results[0].country}
                Accuracy: {round(results[0].accuracy,2)}%""", inline=True)
            ss = results[0].count_rank_ss+results[0].count_rank_ssh
            s = results[0].count_rank_s+results[0].count_rank_sh
            a = results[0].count_rank_a
            embed.add_field(name="User Stats", value=f'''PP: {results[0].pp_raw}
            Global Rank: #{results[0].pp_rank}
            Country Rank: #{results[0].pp_country_rank}
            {ss} SS plays, {s} S plays, {a} A plays''', inline=True)
            embed.set_footer(text=f"total plays: {results[0].playcount}")
            await ctx.send(embed=embed)

    @user.command(name='standard')
    async def osu(self, ctx, *, name: converters.player):
        results = await self.api.get_user(name)
        if results:
            embed = discord.Embed(colour=self.bot.colour_for(ctx.author), title='osu! User: ' +
                                  results[0].username, url=f'https://osu.ppy.sh/users/{results[0].user_id}/osu')
            embed.add_field(
                name="User Info", value=f"""User ID: {results[0].user_id}
                Level: {int(results[0].level)}
                Country: {results[0].country}
                Accuracy: {round(results[0].accuracy,2)}%""", inline=True)
            ss = results[0].count_rank_ss+results[0].count_rank_ssh
            s = results[0].count_rank_s+results[0].count_rank_sh
            a = results[0].count_rank_a
            embed.add_field(name="User Stats", value=f'''PP: {results[0].pp_raw}
            Global Rank: #{results[0].pp_rank}
            Country Rank: #{results[0].pp_country_rank}
            {ss} SS plays, {s} S plays, {a} A plays''', inline=True)
            embed.set_footer(text=f"Total Plays: {results[0].playcount}")
            await ctx.send(embed=embed)

    @user.command()
    async def taiko(self, ctx, *, name: converters.player):
        results = await self.api.get_user(name, mode=enums.OsuMode.taiko)
        if results:
            embed = discord.Embed(colour=self.bot.colour_for(ctx.author), title='osu!taiko User: ' +
                                  results[0].username, url=f'https://osu.ppy.sh/users/{results[0].user_id}/taiko')
            embed.add_field(
                name="User Info", value=f"""User ID: {results[0].user_id}
                Level: {int(results[0].level)}
                Country: {results[0].country}
                Accuracy: {round(results[0].accuracy,2)}%""", inline=True)
            ss = results[0].count_rank_ss+results[0].count_rank_ssh
            s = results[0].count_rank_s+results[0].count_rank_sh
            a = results[0].count_rank_a
            embed.add_field(name="User Stats", value=f'''PP: {results[0].pp_raw}
            Global Rank: #{results[0].pp_rank}
            Country Rank: #{results[0].pp_country_rank}
            S{ss} SS plays, {s} S plays, {a} A plays''', inline=True)
            embed.set_footer(text=f"Total Plays: {results[0].playcount}")
            await ctx.send(embed=embed)

    @user.command()
    async def mania(self, ctx, *, name: converters.player):
        results = await self.api.get_user(name, mode=enums.OsuMode.mania)
        if results:
            embed = discord.Embed(colour=self.bot.colour_for(ctx.author), title='osu!mania User: ' +
                                  results[0].username, url=f'https://osu.ppy.sh/users/{results[0].user_id}/mania')
            embed.add_field(
                name="User Info", value=f"""User ID: {results[0].user_id}
                Level: {int(results[0].level)}
                Country: {results[0].country}
                Accuracy: {round(results[0].accuracy,2)}%""", inline=True)
            ss = results[0].count_rank_ss+results[0].count_rank_ssh
            s = results[0].count_rank_s+results[0].count_rank_sh
            a = results[0].count_rank_a
            embed.add_field(name="User Stats", value=f'''PP: {results[0].pp_raw}
            Global Rank: #{results[0].pp_rank}
            Country Rank: #{results[0].pp_country_rank}
            {ss} SS plays, {s} S plays, {a} A plays''', inline=True)
            embed.set_footer(text=f"Total Plays: {results[0].playcount}")
            await ctx.send(embed=embed)

    @user.command(aliases=['ctb', 'fruits'])
    async def catch(self, ctx, *, name: converters.player):
        results = await self.api.get_user(name, mode=enums.OsuMode.ctb)
        if results:
            embed = discord.Embed(colour=self.bot.colour_for(ctx.author), title='osu! User: ' +
                                  results[0].username, url=f'https://osu.ppy.sh/users/{results[0].user_id}/fruits')
            embed.add_field(
                name="User Info", value=f"""User ID: {results[0].user_id}
                Level: {int(results[0].level)}
                Country: {results[0].country}
                Accuracy: {round(results[0].accuracy,2)}%""", inline=True)
            ss = results[0].count_rank_ss+results[0].count_rank_ssh
            s = results[0].count_rank_s+results[0].count_rank_sh
            a = results[0].count_rank_a
            embed.add_field(name="User Stats", value=f'''PP: {results[0].pp_raw}
            Global Rank: #{results[0].pp_rank}
            Country Rank: #{results[0].pp_country_rank}
            {ss} SS plays, {s} S plays, {a} A plays''', inline=True)
            embed.set_footer(text=f"Total Plays: {results[0].playcount}")
            await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    async def banner(self, ctx, *, name: converters.player):
        '''Fetch a user's profile as a banner.'''
        mode = self.bot.mode_for(ctx.author)
        results = await self.api.get_user(name, mode={'osu': enums.OsuMode.osu, 'taiko': enums.OsuMode.taiko, 'mania': enums.OsuMode.mania, 'fruits': enums.OsuMode.ctb}[mode])
        if results:
            embed = discord.Embed(colour=self.bot.colour_for(ctx.author), title=results[0].username, url=f'https://osu.ppy.sh/users/{results[0].user_id}/{mode}')
            embed.set_image(url=self.banner_url(
                {'osu': 0, 'taiko': 1, 'mania': 2, 'fruits': 3}[mode], name, hex(self.bot.colour_for(ctx.author).value)[2:]))
            await ctx.send(embed=embed)

    @banner.command(name='standard')
    async def osu_(self, ctx, *, name: converters.player):
        results = await self.api.get_user(name)
        if results:
            embed = discord.Embed(colour=self.bot.colour_for(ctx.author), title=results[0].username, url=f'https://osu.ppy.sh/users/{results[0].user_id}/osu')
            embed.set_image(url=self.banner_url(0, name, hex(self.bot.colour_for(ctx.author).value)[2:]))
            await ctx.send(embed=embed)

    @banner.command(name='taiko')
    async def taiko_(self, ctx, *, name: converters.player):
        results = await self.api.get_user(name, mode=enums.OsuMode.taiko)
        if results:
            embed = discord.Embed(colour=self.bot.colour_for(ctx.author), title=results[0].username, url=f'https://osu.ppy.sh/users/{results[0].user_id}/taiko')
            embed.set_image(url=self.banner_url(1, name, hex(self.bot.colour_for(ctx.author).value)[2:]))
            await ctx.send(embed=embed)

    @banner.command(name='mania')
    async def mania_(self, ctx, *, name: converters.player):
        results = await self.api.get_user(name, mode=enums.OsuMode.mania)
        if results:
            embed = discord.Embed(colour=self.bot.colour_for(ctx.author), title=results[0].username, url=f'https://osu.ppy.sh/users/{results[0].user_id}/mania')
            embed.set_image(url=self.banner_url(2, name, hex(self.bot.colour_for(ctx.author).value)[2:]))
            await ctx.send(embed=embed)

    @banner.command(name='catch', aliases=['ctb', 'fruits'])
    async def catch_(self, ctx, *, name: converters.player):
        results = await self.api.get_user(name, mode=enums.OsuMode.ctb)
        if results:
            embed = discord.Embed(colour=self.bot.colour_for(ctx.author), title=results[0].username, url=f'https://osu.ppy.sh/users/{results[0].user_id}/fruits')
            embed.set_image(url=self.banner_url(3, name, hex(self.bot.colour_for(ctx.author).value)[2:]))
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Osu(bot))
