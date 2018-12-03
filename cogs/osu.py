import discord, discord.ext.commands
import requests
from osuapi import OsuApi, ReqConnector

api = OsuApi("7520b4755cfd7161b3da85be693bea51e49ba412", connector=ReqConnector())

class OsuCommands:

    def __init__(self, bot):
        self.bot = bot

    @discord.ext.commands.command(name="user")
    async def user(self, ctx):
        global api
        results = api.get_user('peppy')
        return await ctx.send(f"{results[0].username}")

def setup(bot):
    bot.add_cog(OsuCommands(bot))
