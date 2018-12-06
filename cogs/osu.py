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
        await ctx.send(f"{results[0].username}")

    @user.command(name='standard')
    async def osu(self, ctx, *, name):
        results = await self.api.get_user(name)
        await ctx.send(f"{results[0].username}")

    @user.command()
    async def taiko(self, ctx, *, name):
        results = await self.api.get_user(name, mode=enums.OsuMode.taiko)
        await ctx.send(f"{results[0].username}")

    @user.command()
    async def mania(self, ctx, *, name):
        results = await self.api.get_user(name, mode=enums.OsuMode.mania)
        await ctx.send(f"{results[0].username}")

    @user.command()
    async def catch(self, ctx, *, name):
        results = await self.api.get_user(name, mode=enums.OsuMode.ctb)
        await ctx.send(f"{results[0].username}")

    @commands.group(invoke_without_command=True)
    async def banner(self, ctx, *, name):
        results = await self.api.get_user(name)
        await ctx.send(f"{results[0].username}")

    @banner.command(name='standard')
    async def osu_(self, ctx, *, name):
        results = await self.api.get_user(name)
        embed = discord.Embed(colour=discord.Colour(0xbb1177),title=results[0].username,url=f'https://osu.ppy.sh/users/{results[0].user_id}')
        embed.set_image(url=self.banner_url(0,name))
        await ctx.send(embed=embed)

    @banner.command(name='taiko')
    async def taiko_(self, ctx, *, name):
        results = await self.api.get_user(name, mode=enums.OsuMode.taiko)
        await ctx.send(f"{results[0].username}")

    @banner.command(name='mania')
    async def mania_(self, ctx, *, name):
        results = await self.api.get_user(name, mode=enums.OsuMode.mania)
        await ctx.send(f"{results[0].username}")

    @banner.command(name='catch')
    async def catch_(self, ctx, *, name):
        results = await self.api.get_user(name, mode=enums.OsuMode.ctb)
        await ctx.send(f"{results[0].username}")


def setup(bot):
    bot.add_cog(Osu(bot))
