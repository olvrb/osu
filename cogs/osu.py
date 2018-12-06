import discord
from discord.ext import commands
import requests
from osuapi import OsuApi, AHConnector
import config


class Osu:

    def __init__(self, bot):
        self.api = OsuApi(config.osu, connector=AHConnector())
        self.bot = bot

    @commands.command(name="user")
    async def user(self, ctx, *, name):
        results = await self.api.get_user(name)
        await ctx.send(f"{results[0].username}")


def setup(bot):
    bot.add_cog(Osu(bot))
