from discord.ext import commands
from discord import *
from subprocess import run, PIPE
import aiofiles
import importlib as imp
import traceback


def check():
    async def pred(ctx):
        ids = {232948417087668235, 414950697398829077}
        return ctx.author.id in ids
    return commands.check(pred)


class OwnerCog:

    def __init__(self, bot):
        self.bot = bot

    # Hidden means it won't show up on the default help.

    @commands.command(name='load')
    @check()
    async def cog_load(self, ctx, *cogs):
        """Unload a cog.
        Remember to use dot path. e.g: cogs.owner"""
        for cog in cogs:
            try:
                try:
                    self.bot.load_extension(cog)
                except ModuleNotFoundError:
                    cog1 = 'cogs.' + cog
                    try:
                        self.bot.load_extension(cog1)
                    except Exception as e:
                        embed = Embed(colour=Colour(0xff0000))
                        embed.set_author(name="ERROR")
                        embed.add_field(name=type(e).__name__, value=e)
                        await ctx.send(embed=embed)
                    else:
                        embed = Embed(colour=Colour(0x00ff00))
                        embed.set_author(name="SUCCESS")
                        embed.add_field(name="Successfully loaded", value=cog1)
                        await ctx.send(embed=embed)
                except Exception as e:
                    embed = Embed(colour=Colour(0xff0000))
                    embed.set_author(name="ERROR")
                    embed.add_field(name=type(e).__name__, value=e)
                    await ctx.send(embed=embed)
                else:
                    embed = Embed(colour=Colour(0x00ff00))
                    embed.set_author(name="SUCCESS")
                    embed.add_field(name="Successfully loaded", value=cog)
                    await ctx.send(embed=embed)
            except Exception as e:
                trace = traceback.format_exception(type(e), e, e.__traceback__)
                out = '```'
                for i in trace:
                    if len(out+i+'```') > 2000:
                        await self.bot.channel.send(out+'```')
                        out = '```'
                    out += i
                await self.bot.channel.send(out+'```')

    @commands.command(name='unload')
    @check()
    async def cog_unload(self, ctx, *cogs):
        """Unload a cog.
        Remember to use dot path. e.g: cogs.owner"""
        for cog in cogs:
            try:
                try:
                    self.bot.unload_extension(cog)
                except ModuleNotFoundError:
                    cog1 = 'cogs.' + cog
                    try:
                        self.bot.unload_extension(cog1)
                    except Exception as e:
                        embed = Embed(colour=Colour(0xff0000))
                        embed.set_author(name="ERROR")
                        embed.add_field(name=type(e).__name__, value=e)
                        await ctx.send(embed=embed)
                    else:
                        embed = Embed(colour=Colour(0x00ff00))
                        embed.set_author(name="SUCCESS")
                        embed.add_field(
                            name="Successfully unloaded", value=cog1)
                        await ctx.send(embed=embed)
                except Exception as e:
                    embed = Embed(colour=Colour(0xff0000))
                    embed.set_author(name="ERROR")
                    embed.add_field(name=type(e).__name__, value=e)
                    await ctx.send(embed=embed)
                else:
                    embed = Embed(colour=Colour(0x00ff00))
                    embed.set_author(name="SUCCESS")
                    embed.add_field(name="Successfully unloaded", value=cog)
                    await ctx.send(embed=embed)
            except Exception as e:
                trace = traceback.format_exception(type(e), e, e.__traceback__)
                out = '```'
                for i in trace:
                    if len(out+i+'```') > 2000:
                        await self.bot.channel.send(out+'```')
                        out = '```'
                    out += i
                await self.bot.channel.send(out+'```')

    @commands.command(name='reload')
    @check()
    async def cog_reload(self, ctx, *cogs):
        """Reload a cog.
        Remember to use dot path. e.g: cogs.owner"""
        for cog in cogs:
            try:
                try:
                    self.bot.unload_extension(cog)
                    self.bot.load_extension(cog)
                except ModuleNotFoundError:
                    cog1 = 'cogs.' + cog
                    try:
                        self.bot.unload_extension(cog1)
                        self.bot.load_extension(cog1)
                    except ModuleNotFoundError:
                        cog = 'cogs.lib.'+cog
                        try:
                            mod = imp.import_module(cog)
                            imp.reload(mod)
                            embed = Embed(colour=Colour(0x00ff00))
                        except Exception as e:
                            embed = Embed(colour=Colour(0xff0000))
                            embed.set_author(name="ERROR")
                            embed.add_field(name=type(e).__name__, value=e)
                            await ctx.send(embed=embed)
                        else:
                            embed = Embed(colour=Colour(0x00ff00))
                            embed.set_author(name="SUCCESS")
                            embed.add_field(
                                name="Successfully reloaded", value=cog)
                            await ctx.send(embed=embed)
                    except Exception as e:
                        embed = Embed(colour=Colour(0xff0000))
                        embed.set_author(name="ERROR")
                        embed.add_field(name=type(e).__name__, value=e)
                        await ctx.send(embed=embed)
                    else:
                        embed = Embed(colour=Colour(0x00ff00))
                        embed.set_author(name="SUCCESS")
                        embed.add_field(
                            name="Successfully reloaded", value=cog1)
                        await ctx.send(embed=embed)
                except Exception as e:
                    if type(e).__name__ == 'ClientException' and str(e) == 'extension does not have a setup function':
                        mod = imp.import_module(cog)
                        imp.reload(mod)
                        embed = Embed(colour=Colour(0x00ff00))
                        embed.set_author(name="SUCCESS")
                        embed.add_field(
                            name="Successfully reloaded", value=cog)
                        await ctx.send(embed=embed)
                    else:
                        embed = Embed(colour=Colour(0xff0000))
                        embed.set_author(name="ERROR")
                        embed.add_field(name=type(e).__name__, value=e)
                        await ctx.send(embed=embed)
                else:
                    embed = Embed(colour=Colour(0x00ff00))
                    embed.set_author(name="SUCCESS")
                    embed.add_field(name="Successfully reloaded", value=cog)
                    await ctx.send(embed=embed)
            except Exception as e:
                trace = traceback.format_exception(type(e), e, e.__traceback__)
                out = '```'
                for i in trace:
                    if len(out+i+'```') > 2000:
                        await self.bot.channel.send(out+'```')
                        out = '```'
                    out += i
                await self.bot.channel.send(out+'```')

    @commands.command(name="stop")
    @check()
    async def bot_unload(self, ctx):
        """Stop the bot.
        Remember to use dot path. e.g: cogs.owner"""
        await self.bot.logout()

    @commands.command(name="update")
    @check()
    async def bot_update(self, ctx, cog=None):
        """Pull most recent commit from GitHub.
        Remember to use dot path. e.g: cogs.owner"""
        await ctx.send("```"+run(["git", "pull", 'https://github.com/jacc/osu.git'], stdout=PIPE, encoding="ASCII").stdout+"```")
        if cog:
            ctx.command = self.cog_reload
            await ctx.reinvoke()

    @commands.command()
    @check()
    async def prefixdebug(self, ctx, guild_id: int, prefix: str):
        """Prefix debug function.
        Remember to use dot path. e.g: cogs.owner"""
        self.bot.prefixes[guild_id] = prefix
        if prefix == '':
            del self.bot.prefixes[guild_id]
        await self.bot.save_prefixes()
        guild = self.bot.get_guild(guild_id)
        await ctx.send(f'Set prefix for {guild.name if guild else "[INVALID SERVER]"} to `{prefix}`')

    @commands.command()
    @check()
    async def run(self, ctx, *cmd):
        """Run command.
        Remember to use dot path. e.g: cogs.owner"""
        await ctx.send("```"+run(cmd, stdout=PIPE, encoding="ASCII", shell=True).stdout+"```")


def setup(bot):
    bot.add_cog(OwnerCog(bot))
