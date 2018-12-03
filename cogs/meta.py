import discord, discord.ext.commands

class MetaCommands:

    def __init__(self, bot):
        self.bot = bot

    @discord.ext.commands.command(name="ping")
    async def latency(self, ctx):
        return await ctx.send(f":stopwatch: `{round(self.bot.latency*1000)}ms`")

def setup(bot):
    bot.add_cog(MetaCommands(bot))
