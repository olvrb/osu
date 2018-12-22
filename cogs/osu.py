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

    @commands.group(invoke_without_command=True, help='osu.user.help')
    async def user(self, ctx, *, name: converters.player):
        '''Fetch a user's profile. Usage: osu!user <username> <optional: osu/taiko/maina/fruits>'''
        mode = self.bot.mode_for(ctx.author)
        results = await self.api.get_user(name,mode={'osu':enums.OsuMode.osu,'taiko':enums.OsuMode.taiko,'mania':enums.OsuMode.mania,'fruits':enums.OsuMode.ctb}[mode])  # empty list if not found
        if results:
            embed = discord.Embed(description=self.bot.translate_for(ctx.author,f'osu.mode.{mode}'),colour=self.bot.colour_for(ctx.author), title=self.bot.translate_for(ctx.author,'osu.user.name') +
                                  results[0].username, url=f'https://osu.ppy.sh/users/{results[0].user_id}/{mode}')
            embed.add_field(
                name=self.bot.translate_for(ctx.author,'osu.user.info'), value=self.bot.translate_for(ctx.author,'osu.user.general').format(results[0].user_id,int(results[0].level),results[0].country,round(results[0].accuracy,2)), inline=True)
            ss = results[0].count_rank_ss+results[0].count_rank_ssh
            s = results[0].count_rank_s+results[0].count_rank_sh
            a = results[0].count_rank_a
            embed.add_field(name=self.bot.translate_for(ctx.author,'osu.user.stats'), value=self.bot.translate_for(ctx.author,'osu.user.rank').format(results[0].pp_raw,results[0].pp_rank,results[0].pp_country_rank,ss,s,a), inline=True)
            embed.set_footer(text=self.bot.translate_for(ctx.author,'osu.user.total').format(results[0].playcount))
            await ctx.send(embed=embed)

    @user.command(name='standard', help='osu.user.help')
    async def osu(self, ctx, *, name: converters.player):
        results = await self.api.get_user(name)
        mode = 'osu'
        if results:
            embed = discord.Embed(description=self.bot.translate_for(ctx.author,f'osu.mode.{mode}'),colour=self.bot.colour_for(ctx.author), title=self.bot.translate_for(ctx.author,'osu.user.name') +
                                  results[0].username, url=f'https://osu.ppy.sh/users/{results[0].user_id}/{mode}')
            embed.add_field(
                name=self.bot.translate_for(ctx.author,'osu.user.info'), value=self.bot.translate_for(ctx.author,'osu.user.general').format(results[0].user_id,int(results[0].level),results[0].country,round(results[0].accuracy,2)), inline=True)
            ss = results[0].count_rank_ss+results[0].count_rank_ssh
            s = results[0].count_rank_s+results[0].count_rank_sh
            a = results[0].count_rank_a
            embed.add_field(name=self.bot.translate_for(ctx.author,'osu.user.stats'), value=self.bot.translate_for(ctx.author,'osu.user.rank').format(results[0].pp_raw,results[0].pp_rank,results[0].pp_country_rank,ss,s,a), inline=True)
            embed.set_footer(text=self.bot.translate_for(ctx.author,'osu.user.total').format(results[0].playcount))
            await ctx.send(embed=embed)

    @user.command(help='osu.user.help')
    async def taiko(self, ctx, *, name: converters.player):
        results = await self.api.get_user(name, mode=enums.OsuMode.taiko)
        mode = 'taiko'
        if results:
            embed = discord.Embed(description=self.bot.translate_for(ctx.author,f'osu.mode.{mode}'),colour=self.bot.colour_for(ctx.author), title=self.bot.translate_for(ctx.author,'osu.user.name') +
                                  results[0].username, url=f'https://osu.ppy.sh/users/{results[0].user_id}/{mode}')
            embed.add_field(
                name=self.bot.translate_for(ctx.author,'osu.user.info'), value=self.bot.translate_for(ctx.author,'osu.user.general').format(results[0].user_id,int(results[0].level),results[0].country,round(results[0].accuracy,2)), inline=True)
            ss = results[0].count_rank_ss+results[0].count_rank_ssh
            s = results[0].count_rank_s+results[0].count_rank_sh
            a = results[0].count_rank_a
            embed.add_field(name=self.bot.translate_for(ctx.author,'osu.user.stats'), value=self.bot.translate_for(ctx.author,'osu.user.rank').format(results[0].pp_raw,results[0].pp_rank,results[0].pp_country_rank,ss,s,a), inline=True)
            embed.set_footer(text=self.bot.translate_for(ctx.author,'osu.user.total').format(results[0].playcount))
            await ctx.send(embed=embed)

    @user.command(help='osu.user.help')
    async def mania(self, ctx, *, name: converters.player):
        results = await self.api.get_user(name, mode=enums.OsuMode.mania)
        mode = 'mania'
        if results:
            embed = discord.Embed(description=self.bot.translate_for(ctx.author,f'osu.mode.{mode}'),colour=self.bot.colour_for(ctx.author), title=self.bot.translate_for(ctx.author,'osu.user.name') +
                                  results[0].username, url=f'https://osu.ppy.sh/users/{results[0].user_id}/{mode}')
            embed.add_field(
                name=self.bot.translate_for(ctx.author,'osu.user.info'), value=self.bot.translate_for(ctx.author,'osu.user.general').format(results[0].user_id,int(results[0].level),results[0].country,round(results[0].accuracy,2)), inline=True)
            ss = results[0].count_rank_ss+results[0].count_rank_ssh
            s = results[0].count_rank_s+results[0].count_rank_sh
            a = results[0].count_rank_a
            embed.add_field(name=self.bot.translate_for(ctx.author,'osu.user.stats'), value=self.bot.translate_for(ctx.author,'osu.user.rank').format(results[0].pp_raw,results[0].pp_rank,results[0].pp_country_rank,ss,s,a), inline=True)
            embed.set_footer(text=self.bot.translate_for(ctx.author,'osu.user.total').format(results[0].playcount))
            await ctx.send(embed=embed)

    @user.command(aliases=['ctb','fruits'], help='osu.user.help')
    async def catch(self, ctx, *, name: converters.player):
        results = await self.api.get_user(name, mode=enums.OsuMode.ctb)
        mode = 'fruits'
        if results:
            embed = discord.Embed(description=self.bot.translate_for(ctx.author,f'osu.mode.{mode}'),colour=self.bot.colour_for(ctx.author), title=self.bot.translate_for(ctx.author,'osu.user.name') +
                                  results[0].username, url=f'https://osu.ppy.sh/users/{results[0].user_id}/{mode}')
            embed.add_field(
                name=self.bot.translate_for(ctx.author,'osu.user.info'), value=self.bot.translate_for(ctx.author,'osu.user.general').format(results[0].user_id,int(results[0].level),results[0].country,round(results[0].accuracy,2)), inline=True)
            ss = results[0].count_rank_ss+results[0].count_rank_ssh
            s = results[0].count_rank_s+results[0].count_rank_sh
            a = results[0].count_rank_a
            embed.add_field(name=self.bot.translate_for(ctx.author,'osu.user.stats'), value=self.bot.translate_for(ctx.author,'osu.user.rank').format(results[0].pp_raw,results[0].pp_rank,results[0].pp_country_rank,ss,s,a), inline=True)
            embed.set_footer(text=self.bot.translate_for(ctx.author,'osu.user.total').format(results[0].playcount))
            await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True, help='osu.banner.help')
    async def banner(self, ctx, *, name: converters.player):
        '''Fetch a user's profile as a banner.'''
        mode = self.bot.mode_for(ctx.author)
        results = await self.api.get_user(name,mode={'osu':enums.OsuMode.osu,'taiko':enums.OsuMode.taiko,'mania':enums.OsuMode.mania,'fruits':enums.OsuMode.ctb}[mode])
        if results:
            embed = discord.Embed(colour=discord.Colour(
                0xbb1177), title=results[0].username, url=f'https://osu.ppy.sh/users/{results[0].user_id}/{mode}')
            embed.set_image(url=self.banner_url({'osu':0,'taiko':1,'mania':2,'fruits':3}[mode], name))
            await ctx.send(embed=embed)

    @banner.command(name='standard', help='osu.banner.help')
    async def osu_(self, ctx, *, name: converters.player):
        results = await self.api.get_user(name)
        if results:
            embed = discord.Embed(colour=discord.Colour(
                0xbb1177), title=results[0].username, url=f'https://osu.ppy.sh/users/{results[0].user_id}/osu')
            embed.set_image(url=self.banner_url(0, name))
            await ctx.send(embed=embed)

    @banner.command(name='taiko', help='osu.banner.help')
    async def taiko_(self, ctx, *, name: converters.player):
        results = await self.api.get_user(name, mode=enums.OsuMode.taiko)
        if results:
            embed = discord.Embed(colour=discord.Colour(
                0xbb1177), title=results[0].username, url=f'https://osu.ppy.sh/users/{results[0].user_id}/taiko')
            embed.set_image(url=self.banner_url(1, name))
            await ctx.send(embed=embed)

    @banner.command(name='mania', help='osu.banner.help')
    async def mania_(self, ctx, *, name: converters.player):
        results = await self.api.get_user(name, mode=enums.OsuMode.mania)
        if results:
            embed = discord.Embed(colour=discord.Colour(
                0xbb1177), title=results[0].username, url=f'https://osu.ppy.sh/users/{results[0].user_id}/mania')
            embed.set_image(url=self.banner_url(2, name))
            await ctx.send(embed=embed)

    @banner.command(name='catch',aliases=['ctb','fruits'], help='osu.banner.help')
    async def catch_(self, ctx, *, name: converters.player):
        results = await self.api.get_user(name, mode=enums.OsuMode.ctb)
        if results:
            embed = discord.Embed(colour=discord.Colour(
                0xbb1177), title=results[0].username, url=f'https://osu.ppy.sh/users/{results[0].user_id}/fruits')
            embed.set_image(url=self.banner_url(3, name))
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Osu(bot))
