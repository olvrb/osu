import discord
from discord.ext import commands

class Meta:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "ping", aliases = ['latency'])
    async def latency(self, ctx):
        ''' Get the bot latency. '''
        return await ctx.send(f"⏱ `{round(self.bot.latency*1000)}ms`")

    @commands.command(name="invite")
    async def invite(self, ctx):
        ''' Get a link to invite osu!bot into your server. '''
        return await ctx.send(':inbox_tray: Invite osu!bot to your server: https://discordapp.com/oauth2/authorize?client_id=421879566265614337&scope=bot&permissions=347136')

    @commands.command(name="support", aliases = ['server'])
    async def support(self, ctx):
        ''' Get a link to the support server. '''
        return await ctx.send(':grey_question: Join the support server here: discord.gg/uda4VuE')

def setup(bot):
    bot.add_cog(Meta(bot))