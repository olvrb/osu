from discord.ext import commands
import discord
class osu_player_or_user(commands.Converter):
    async def convert(self,ctx,argument):
        return (await commands.MemberConverter.convert(self,ctx,argument)) or (await commands.UserConverter.convert(self,ctx,argument)) or argument
class target(commands.Converter):
    async def convert(self,ctx,argument):
        return (await commands.MemberConverter.convert(self,ctx,argument)) or (await commands.UserConverter.convert(self,ctx,argument))