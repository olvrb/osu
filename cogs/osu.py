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
            embed.add_field(name="user stats", value=f"id: {results[0].user_id}\nlevel: {results[0].level}\ncountry: {results[0].country}\ncountry rank: {results[0].pp_country_rank}")
            embed.set_footer(text=f"total plays: {results[0].playcount}")
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
