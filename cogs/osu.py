import discord
from discord.ext import commands
import requests
from osuapi import OsuApi, AHConnector, enums
import config


class Osu:

    def __init__(self, bot):
        self.api = OsuApi(config.osu, connector=AHConnector())
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def user(self, ctx, *, name):
        results = await self.api.get_user(name)
        await ctx.send(f"{results[0].username}")

    @user.command()
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


def setup(bot):
    bot.add_cog(Osu(bot))
