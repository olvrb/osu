import discord
from discord.ext import commands
import aiohttp
from lib import converters

class Meta:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "ping", aliases = ['latency'],help='meta.latency.help')
    async def latency(self, ctx):
        ''' Get the bot latency. '''
        return await ctx.send(f"⏱ `{round(self.bot.latency*1000)}ms`")

    @commands.command(name="invite",help='meta.invite.help')
    async def invite(self, ctx):
        ''' Get a link to invite osu!bot into your server. '''
        return await ctx.send(self.bot.translate_for(ctx.author,'meta.invite.out'))

    @commands.command(name="support", aliases = ['server'],help='meta.support.help')
    async def support(self, ctx):
        ''' Get a link to the support server. '''
        return await ctx.send(self.bot.translate_for(ctx.author,'meta.support.out'))

    @commands.command(name="stats", aliases = ['info'],help='meta.stats.help')
    async def info(self, ctx):
        ''' Get information about the bot. '''
        async with aiohttp.ClientSession() as session:
            resp = await session.get('https://api.github.com/repos/jacc/osu/commits')
            my_json = await resp.json()
            embed = discord.Embed(colour=self.bot.colour_for(ctx.author), title=self.bot.translate_for(ctx.author,'meta.stats.title'))
            embed.add_field(name=self.bot.translate_for(ctx.author,'meta.stats.commit'), value=self.bot.translate_for(ctx.author,'meta.stats.message').format(my_json[0]['sha'],my_json[0]['commit']['author']['name'],my_json[0]['commit']['message']))
            return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Meta(bot))