from discord.ext import commands
import discord
class osu_player_or_user(commands.Converter):
    async def convert(self,ctx,argument):
        try:
            Mc = await commands.MemberConverter().convert(ctx,argument)
        except:
            Mc = None
        try:
            Uc = await commands.UserConverter().convert(ctx,argument)
        except:
            Uc = None
        return Mc or Uc or argument
class player(commands.Converter):
    async def convert(self,ctx,argument):
        try:
            Mc = await commands.MemberConverter().convert(ctx,argument)
        except:
            Mc = None
        try:
            Uc = await commands.UserConverter().convert(ctx,argument)
        except:
            Uc = None
        return ctx.bot.username_for(Mc or Uc or argument)
class target(commands.Converter):
    async def convert(self,ctx,argument):
        try:
            Mc = await commands.MemberConverter().convert(ctx,argument)
        except:
            Mc = None
        try:
            Uc = await commands.UserConverter().convert(ctx,argument)
        except:
            Uc = None
        return Mc or Uc or ctx.author