from discord.ext import commands
import discord
class osu_player_or_user(commands.Converter):
    async def convert(self,ctx,argument):
        return (await commands.MemberConverter.convert(self,ctx,argument)) or (await commands.UserConverter.convert(self,ctx,argument)) or argument
class player(commands.Converter):
    async def convert(self,ctx,argument):
        return ctx.bot.username_for(await commands.MemberConverter.convert(self,ctx,argument)) or ctx.bot.username_for(await commands.UserConverter.convert(self,ctx,argument)) or argument or ctx.bot.username_for(ctx.author)
class target(commands.Converter):
    async def convert(self,ctx,argument):
        return (await commands.MemberConverter.convert(self,ctx,argument)) or (await commands.UserConverter.convert(self,ctx,argument)) or ctx.author