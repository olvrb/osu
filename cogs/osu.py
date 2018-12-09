import discord
from discord.ext import commands
import requests
from osuapi import OsuApi, AHConnector, enums
import config
from urllib.parse import quote


class Osu:

    def __init__(self, bot):
        self.api = OsuApi(config.osu, connector=AHConnector())
        self.bot = bot

    def banner_url(self, mode, user, colour='bb1177'):
        return f'https://lemmmy.pw/osusig/sig.php?colour=hex{colour}&mode={mode}&uname={quote(user)}&pp=2&countryrank&flagstroke&darktriangles&onlineindicator=undefined&xpbar&xpbarhex'

    @commands.group(invoke_without_command=True)
    async def user(self, ctx, *, name):
        results = await self.api.get_user(name) # empty list if not found
        if results:
            print(f"{results[0]}")
            embed= discord.Embed(colour=self.bot.colour_for(ctx.author))
            embed.title=f"osu! user - {results[0].username}"
            embed.add_field(name="User Info", value=f"User ID: {results[0].user_id}\nLevel: {results[0].level}\nCountry: {results[0].country}\nAccuracy: {results[0].accuracy}",inline=True)
            ss = results[0].count_rank_ss+results[0].count_rank_ssh
            s = results[0].count_rank_s+results[0].count_rank_sh
            a = results[0].count_rank_a
            embed.add_field(name="User Stats", value=f"PP: {results[0].pp_raw}\nGlobal Rank: #{results[0].pp_rank}\nCountry Rank: {results[0].pp_country_rank}\n{ss} SS-ranked play{'s' if ss != 1 else ''}, {s} S-ranked play{'s' if s != 1 else ''},\n{a} A-ranked play{'s' if a != 1 else ''}",inline=True)
            embed.set_footer(text=f"Total Plays: {results[0].playcount}")
            await ctx.send(embed=embed)

    @user.command(name='standard')
    async def osu(self, ctx, *, name):
        results = await self.api.get_user(name)
        if results:
            await ctx.send(f"{results[0].username}")

    @user.command()
    async def taiko(self, ctx, *, name):
        results = await self.api.get_user(name, mode=enums.OsuMode.taiko)
        if results:
            await ctx.send(f"{results[0].username}")

    @user.command()
    async def mania(self, ctx, *, name):
        results = await self.api.get_user(name, mode=enums.OsuMode.mania)
        if results:
            await ctx.send(f"{results[0].username}")

    @user.command()
    async def catch(self, ctx, *, name):
        results = await self.api.get_user(name, mode=enums.OsuMode.ctb)
        if results:
            await ctx.send(f"{results[0].username}")

    @commands.group(invoke_without_command=True)
    async def banner(self, ctx, *, name):
        results = await self.api.get_user(name)
        if results:
            embed = discord.Embed(colour=discord.Colour(0xbb1177),title=results[0].username,url=f'https://osu.ppy.sh/users/{results[0].user_id}')
            embed.set_image(url=self.banner_url(0,name))
            await ctx.send(embed=embed)

    @banner.command(name='standard')
    async def osu_(self, ctx, *, name):
        results = await self.api.get_user(name)
        if results:
            embed = discord.Embed(colour=discord.Colour(0xbb1177),title=results[0].username,url=f'https://osu.ppy.sh/users/{results[0].user_id}')
            embed.set_image(url=self.banner_url(0,name))
            await ctx.send(embed=embed)

    @banner.command(name='taiko')
    async def taiko_(self, ctx, *, name):
        results = await self.api.get_user(name, mode=enums.OsuMode.taiko)
        if results:
            embed = discord.Embed(colour=discord.Colour(0xbb1177),title=results[0].username,url=f'https://osu.ppy.sh/users/{results[0].user_id}')
            embed.set_image(url=self.banner_url(1,name))
            await ctx.send(embed=embed)

    @banner.command(name='mania')
    async def mania_(self, ctx, *, name):
        results = await self.api.get_user(name, mode=enums.OsuMode.mania)
        if results:
            embed = discord.Embed(colour=discord.Colour(0xbb1177),title=results[0].username,url=f'https://osu.ppy.sh/users/{results[0].user_id}')
            embed.set_image(url=self.banner_url(2,name))
            await ctx.send(embed=embed)

    @banner.command(name='catch')
    async def catch_(self, ctx, *, name):
        results = await self.api.get_user(name, mode=enums.OsuMode.ctb)
        if results:
            embed = discord.Embed(colour=discord.Colour(0xbb1177),title=results[0].username,url=f'https://osu.ppy.sh/users/{results[0].user_id}')
            embed.set_image(url=self.banner_url(3,name))
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Osu(bot))
