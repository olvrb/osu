import discord
from discord.ext import commands


class Meta:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping",aliases=['latency'])
    async def latency(self, ctx):
        return await ctx.send(f"⏱ `{round(self.bot.latency*1000)}ms`")


def setup(bot):
    bot.add_cog(Meta(bot))
