import discord
from discord.ext import commands


class Configure:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def profile(self, ctx, target: discord.Member = None):
        '''Show the profile of you or another user. Modify it with [p]profile set'''
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
                name='User Colour', value='Unset' if colour not in prof else '#'+prof['colour'])
            embed.add_field(name='osu! Username',
                            value=prof.get('username') or 'Unset')
            embed.add_field(name='Default osu! Mode',
                            value=modes.get(prof.get('mode')) or 'Unset')
        else:
            embed = discord.Embed(colour=0xbb1177, title='An error occurred',
                                  description=f'{"You" if target == ctx.author else "They"} don\'t have a profile!')
        await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(Configure(bot))