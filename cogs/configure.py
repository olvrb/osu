import discord
from discord.ext import commands


class Configure:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def profile(self, ctx, target: discord.Member = None):
        '''Show the profile of you or another user. Modify it with [p]profile set'''
        if ctx.invoked_subcommand is None:
            if target is None:
                target = ctx.author
            prof = self.bot.profile_for(target)
            modes = {'osu': 'osu!', 'taiko': 'osu!taiko',
                     'mania': 'osu!mania', 'fruits': 'osu!catch'}
            if prof:
                colour = discord.Colour(
                    0xbb1177 if 'colour' not in prof else prof['colour'])
                embed = discord.Embed(
                    colour=colour, title=f'Profile for {target.name}')
                embed.add_field(
                    name='User Colour', value='Unset' if 'colour' not in prof else '#'+hex(prof['colour'])[2:])
                embed.add_field(name='osu! Username',
                                value=prof.get('username') or 'Unset')
                embed.add_field(name='Default osu! Mode',
                                value=modes.get(prof.get('mode')) or 'Unset')
                embed.set_footer(f'User Color: {'Unset' if 'colour' not in prof else '#'+hex(prof['colour'])[2:]}')
            else:
                embed = discord.Embed(colour=0xbb1177, title='An error occurred',
                                      description=f'{"You" if target == ctx.author else "They"} don\'t have a profile!')
            await ctx.send(embed=embed)

    @profile.group(invoke_without_command=True)
    async def set(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f'You need to specify a key and a value. See `{ctx.prefix}help profile set` for more')

    @set.command(aliases=['color'])
    async def colour(self, ctx, colour_code):
        '''Set the colour for embeds and banners.
        Provide a hex code like `[p]profile set colour #03dc03` or `[p]profile set colour 0088ff` or even `[p]profile set colour 0x123456`
        For the default colour, do:
        [p]profile set colour #bb1177'''
        colour_code = '0'+colour_code.lstrip('0x#')
        try:
            colour = int(colour_code, 16)
            if colour > 0xffffff:
                raise Exception
            await self.bot.modify_profile_for(ctx.author, colour=colour)
            await ctx.send('Your profile colour has been set.')
        except:
            await ctx.send('That colour code is invalid.')

    @set.command(aliases=['name'])
    async def username(self, ctx, *, username):
        '''Set your osu! username.
        Also sets the default user for [p]user and [p]banner.
        To make your osu! username the same as your Discord username, do:
        [p]profile set username INHERITED
        '''
        await self.bot.modify_profile_for(ctx.author, username=username)
        await ctx.send('Your osu! username has been set.')

    @set.command(aliases=['defaultmode'])
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
            await ctx.send('Your default mode has been set.')
        else:
            await ctx.send('That is not a valid mode.')
    @commands.command()
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
            return await ctx.send('In order to prevent abuse to my disk, the custom prefix length has been capped at 10. Sorry!')
        add = ('removed' if newprefix == '' else f'changed to `{newprefix}`') if ctx.guild.id in self.bot.prefixes else f'set to `{newprefix}`'
        outmsg = f'Your server\'s custom prefix has been {add}'
        self.bot.prefixes[ctx.guild.id] = newprefix
        if newprefix == '': del self.bot.prefixes[ctx.guild.id]
        await self.bot.save_prefixes()
        await ctx.send(outmsg)


def setup(bot):
    bot.add_cog(Configure(bot))
