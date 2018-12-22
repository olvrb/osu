import discord
from discord.ext import commands
from lib import converters

class Configure:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True,help='configure.profile.help')
    async def profile(self, ctx, target: converters.target):
        '''Show the profile of you or another user. Modify it with [p]profile set'''
        if ctx.invoked_subcommand is None:
            prof = self.bot.profile_for(target)
            modes = {'osu': 'osu!', 'taiko': 'osu!taiko',
                     'mania': 'osu!mania', 'fruits': 'osu!catch'}
            if prof:
                colour = discord.Colour(
                    0xbb1177 if 'colour' not in prof else prof['colour'])
                embed = discord.Embed(
                    colour=colour, title=self.bot.translate_for(ctx.author,'configure.profile.profile_for').format(target.name))
                # embed.add_field(
                #     name='User Colour', value='Unset' if 'colour' not in prof else '#'+hex(prof['colour'])[2:])
                embed.add_field(name=self.bot.translate_for(ctx.author,'configure.profile.name'),
                                value=prof.get('username') or 'Unset')
                embed.add_field(name=self.bot.translate_for(ctx.author,'configure.profile.mode'),
                                value=modes.get(prof.get('mode')) or 'Unset')
                embed.set_footer(text=self.bot.translate_for(ctx.author,'configure.profile.colour').format('Unset' if 'colour' not in prof else '#'+hex(prof['colour'])[2:]))
            else:
                embed = discord.Embed(colour=0xbb1177, title=self.bot.translate_for(ctx.author,'configure.profile.error'),
                                      description=self.bot.translate_for(ctx.author,'configure.profile.you_not') if target == ctx.author else self.bot.translate_for(ctx.author,'configure.profile.they_not'))
            await ctx.send(embed=embed)

    @profile.group(invoke_without_command=True)
    async def set(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(self.bot.translate_for(ctx.author,'configure.profile.set.fail').format(ctx.prefix))

    @set.command(aliases=['color'],help='configure.profile.colour.help')
    async def colour(self, ctx, colour_code):
        '''Set the colour for embeds and banners.
        Provide a hex code like `[p]profile set colour #03dc03` or `[p]profile set colour 0088ff` or even `[p]profile set colour 0x123456`
        For the default colour, do:
        [p]profile set colour #bb1177'''
        colour_code = '0'+colour_code.lstrip('0x#')
        try:
            colour = int(colour_code, 16)
            if colour > 0xffffff:
                raise ValueError
            await self.bot.modify_profile_for(ctx.author, colour=colour)
            await ctx.send(self.bot.translate_for(ctx.author,'configure.profile.set.colour.set'))
        except ValueError:
            await ctx.send(self.bot.translate_for(ctx.author,'configure.profile.set.colour.invalid'))

    @set.command(aliases=['name'],help='configure.profile.set.username.help')
    async def username(self, ctx, *, username):
        '''Set your osu! username.
        Also sets the default user for [p]user and [p]banner.
        To make your osu! username the same as your Discord username, do:
        [p]profile set username INHERITED
        '''
        await self.bot.modify_profile_for(ctx.author, username=username)
        await ctx.send(self.bot.translate_for(ctx.author,'configure.profile.set.username.set'))

    @set.command(aliases=['defaultmode'],help='configure.profile.set.mode.help')
    async def mode(self, ctx, default_mode):
        '''Set your preferred mode.
        Also sets the default mode for [p]user and [p]banner.
        Options:
        ­ osu!standard:
        ­  - osu
        ­  - osu!std
        ­  - osu!standard
        ­  - std
        ­  - standard
        ­  - 0
        ­ osu!taiko:
        ­  - taiko
        ­  - osu!taiko
        ­  - 1
        ­ osu!mania:
        ­  - mania
        ­  - osu!mania
        ­  - 2
        ­ osu!catch:
        ­  - catch
        ­  - ctb
        ­  - fruits
        ­  - osu!catch
        ­  - osu!ctb
        ­  - osu!fruits
        ­  - 3
        '''
        bindings = {
            'osu': 'osu',
            'osu!std': 'osu',
            'osu!standard': 'osu',
            'std': 'osu',
            'standard': 'osu',
            '0': 'osu',
            'taiko': 'taiko',
            'osu!taiko': 'taiko',
            '1': 'taiko',
            'mania': 'mania',
            'osu!mania': 'mania',
            '2': 'mania',
            'catch': 'fruits',
            'ctb': 'fruits',
            'fruits': 'fruits',
            'osu!catch': 'fruits',
            'osu!ctb': 'fruits',
            'osu!fruits': 'fruits',
            '3': 'fruits',
        }
        if default_mode in bindings:
            await self.bot.modify_profile_for(ctx.author, mode=bindings[default_mode])
            await ctx.send(self.bot.translate_for(ctx.author,'configure.profile.set.mode.set'))
        else:
            await ctx.send(self.bot.translate_for(ctx.author,'configure.profile.set.mode.invalid'))
    @set.command(help='configure.profile.set.locale.help')
    async def locale(self,ctx,locale:str):
        locale = locale.lower()
        await self.bot.modify_profile_for(ctx.author,locale=locale)
        awaif ctx.send(self.bot.translate_for(ctx.author,'configure.profile.set.locale.set').format(locale.upper()))
    @commands.command(help='configure.setprefix.help')
    @commands.has_permissions(manage_guild=True)
    async def setprefix(self,ctx,newprefix):
        '''Sets the server's custom prefix (the original will still work under most circumstances). Requires the Manage Server permission. To use spaces in your prefix quote it.
        You can even use a space at the end of the prefix.
        
        Example 1 (no spaces):
        [p]setprefix osu|
        Example 2 (with trailing space):
        [p]setprefix "osu "
        
        To remove your server's prefix:
        [p]setprefix ""'''
        newprefix = newprefix.lstrip(' ')
        if len(newprefix) > 10:
            return await ctx.send(self.bot.translate_for(ctx.author,'configure.setprefix.abuse'))
        outmsg = (self.bot.translate_for(ctx.author,'configure.setprefix.removed') if newprefix == '' else self.bot.translate_for(ctx.author,'configure.setprefix.changed').format(newprefix)) if ctx.guild.id in self.bot.prefixes else self.bot.translate_for(ctx.author,'configure.setprefix.added').format(newprefix)
        self.bot.prefixes[ctx.guild.id] = newprefix
        if newprefix == '': del self.bot.prefixes[ctx.guild.id]
        await self.bot.save_prefixes()
        await ctx.send(outmsg)


def setup(bot):
    bot.add_cog(Configure(bot))
