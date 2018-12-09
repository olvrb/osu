import discord
from discord.ext import commands
import requests
from osuapi import OsuApi, AHConnector, enums
import config
from urllib.parse import quote


class Osu:

    def __init__(self, bot):
        self.api = OsuApi(config.osu, connector=AHConnector())
        self.bot = bot

    def banner_url(self, mode, user, colour='bb1177'):
        return f'https://lemmmy.pw/osusig/sig.php?colour=hex{colour}&mode={mode}&uname={quote(user)}&pp=2&countryrank&flagstroke&darktriangles&onlineindicator=undefined&xpbar&xpbarhex'

    @commands.group(invoke_without_command=True)
    async def user(self, ctx, *, name):
        mode = self.bot.mode_for(ctx.author)
        results = await self.api.get_user(name,mode={'osu':enums.OsuMode.osu,'taiko':enums.OsuMode.taiko,'mania':enums.OsuMode.mania,'fruits':enums.OsuMode.ctb}[mode])  # empty list if not found
        if results:
            embed = discord.Embed(colour=self.bot.colour_for(ctx.author), title='osu! User: ' +
                                  results[0].username, url=f'https://osu.ppy.sh/users/{results[0].user_id}/osu')
            embed.add_field(
                name="User Info", value=f"""User ID: {results[0].user_id}
                Level: {int(results[0].level)}
                Country: {results[0].country}
                Accuracy: {round(results[0].accuracy,2)}%""", inline=True)
            ss = results[0].count_rank_ss+results[0].count_rank_ssh
            s = results[0].count_rank_s+results[0].count_rank_sh
            a = results[0].count_rank_a
            embed.add_field(name="User Stats", value=f'''PP: {results[0].pp_raw}
            Global Rank: #{results[0].pp_rank}
            Country Rank: {results[0].pp_country_rank}
            SS ranks: {ss}
            S ranks: {s}
            A ranks: {a}''', inline=True)
            embed.set_footer(text=f"Total Plays: {results[0].playcount}")
            await ctx.send(embed=embed)

    @user.command(name='standard')
    async def osu(self, ctx, *, name):
        results = await self.api.get_user(name)
        if results:
            embed = discord.Embed(colour=self.bot.colour_for(ctx.author), title='osu! User: ' +
                                  results[0].username, url=f'https://osu.ppy.sh/users/{results[0].user_id}/osu')
            embed.add_field(
                name="User Info", value=f"""User ID: {results[0].user_id}
                Level: {int(results[0].level)}
                Country: {results[0].country}
                Accuracy: {round(results[0].accuracy,2)}%""", inline=True)
            ss = results[0].count_rank_ss+results[0].count_rank_ssh
            s = results[0].count_rank_s+results[0].count_rank_sh
            a = results[0].count_rank_a
            embed.add_field(name="User Stats", value=f'''PP: {results[0].pp_raw}
            Global Rank: #{results[0].pp_rank}
            Country Rank: {results[0].pp_country_rank}
            SS ranks: {ss}
            S ranks: {s}
            A ranks: {a}''', inline=True)
            embed.set_footer(text=f"Total Plays: {results[0].playcount}")
            await ctx.send(embed=embed)

    @user.command()
    async def taiko(self, ctx, *, name):
        results = await self.api.get_user(name, mode=enums.OsuMode.taiko)
        if results:
            embed = discord.Embed(colour=self.bot.colour_for(ctx.author), title='osu!taiko User: ' +
                                  results[0].username, url=f'https://osu.ppy.sh/users/{results[0].user_id}/taiko')
            embed.add_field(
                name="User Info", value=f"""User ID: {results[0].user_id}
                Level: {int(results[0].level)}
                Country: {results[0].country}
                Accuracy: {round(results[0].accuracy,2)}%""", inline=True)
            ss = results[0].count_rank_ss+results[0].count_rank_ssh
            s = results[0].count_rank_s+results[0].count_rank_sh
            a = results[0].count_rank_a
            embed.add_field(name="User Stats", value=f'''PP: {results[0].pp_raw}
            Global Rank: #{results[0].pp_rank}
            Country Rank: {results[0].pp_country_rank}
            SS ranks: {ss}
            S ranks: {s}
            A ranks: {a}''', inline=True)
            embed.set_footer(text=f"Total Plays: {results[0].playcount}")
            await ctx.send(embed=embed)

    @user.command()
    async def mania(self, ctx, *, name):
        results = await self.api.get_user(name, mode=enums.OsuMode.mania)
        if results:
            embed = discord.Embed(colour=self.bot.colour_for(ctx.author), title='osu!mania User: ' +
                                  results[0].username, url=f'https://osu.ppy.sh/users/{results[0].user_id}/mania')
            embed.add_field(
                name="User Info", value=f"""User ID: {results[0].user_id}
                Level: {int(results[0].level)}
                Country: {results[0].country}
                Accuracy: {round(results[0].accuracy,2)}%""", inline=True)
            ss = results[0].count_rank_ss+results[0].count_rank_ssh
            s = results[0].count_rank_s+results[0].count_rank_sh
            a = results[0].count_rank_a
            embed.add_field(name="User Stats", value=f'''PP: {results[0].pp_raw}
            Global Rank: #{results[0].pp_rank}
            Country Rank: {results[0].pp_country_rank}
            SS ranks: {ss}
            S ranks: {s}
            A ranks: {a}''', inline=True)
            embed.set_footer(text=f"Total Plays: {results[0].playcount}")
            await ctx.send(embed=embed)

    @user.command(aliases=['ctb','fruits'])
    async def catch(self, ctx, *, name):
        results = await self.api.get_user(name, mode=enums.OsuMode.ctb)
        if results:
            embed = discord.Embed(colour=self.bot.colour_for(ctx.author), title='osu! User: ' +
                                  results[0].username, url=f'https://osu.ppy.sh/users/{results[0].user_id}/fruits')
            embed.add_field(
                name="User Info", value=f"""User ID: {results[0].user_id}
                Level: {int(results[0].level)}
                Country: {results[0].country}
                Accuracy: {round(results[0].accuracy,2)}%""", inline=True)
            ss = results[0].count_rank_ss+results[0].count_rank_ssh
            s = results[0].count_rank_s+results[0].count_rank_sh
            a = results[0].count_rank_a
            embed.add_field(name="User Stats", value=f'''PP: {results[0].pp_raw}
            Global Rank: #{results[0].pp_rank}
            Country Rank: {results[0].pp_country_rank}
            SS ranks: {ss}
            S ranks: {s}
            A ranks: {a}''', inline=True)
            embed.set_footer(text=f"Total Plays: {results[0].playcount}")
            await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    async def banner(self, ctx, *, name):
        mode = self.bot.mode_for(ctx.author)
        results = await self.api.get_user(name,mode={'osu':enums.OsuMode.osu,'taiko':enums.OsuMode.taiko,'mania':enums.OsuMode.mania,'fruits':enums.OsuMode.ctb}[mode])
        if results:
            embed = discord.Embed(colour=discord.Colour(
                0xbb1177), title=results[0].username, url=f'https://osu.ppy.sh/users/{results[0].user_id}/osu')
            embed.set_image(url=self.banner_url(0, name))
            await ctx.send(embed=embed)

    @banner.command(name='standard')
    async def osu_(self, ctx, *, name):
        results = await self.api.get_user(name)
        if results:
            embed = discord.Embed(colour=discord.Colour(
                0xbb1177), title=results[0].username, url=f'https://osu.ppy.sh/users/{results[0].user_id}/osu')
            embed.set_image(url=self.banner_url(0, name))
            await ctx.send(embed=embed)

    @banner.command(name='taiko')
    async def taiko_(self, ctx, *, name):
        results = await self.api.get_user(name, mode=enums.OsuMode.taiko)
        if results:
            embed = discord.Embed(colour=discord.Colour(
                0xbb1177), title=results[0].username, url=f'https://osu.ppy.sh/users/{results[0].user_id}/taiko')
            embed.set_image(url=self.banner_url(1, name))
            await ctx.send(embed=embed)

    @banner.command(name='mania')
    async def mania_(self, ctx, *, name):
        results = await self.api.get_user(name, mode=enums.OsuMode.mania)
        if results:
            embed = discord.Embed(colour=discord.Colour(
                0xbb1177), title=results[0].username, url=f'https://osu.ppy.sh/users/{results[0].user_id}/mania')
            embed.set_image(url=self.banner_url(2, name))
            await ctx.send(embed=embed)

    @banner.command(name='catch',aliases=['ctb','fruits'])
    async def catch_(self, ctx, *, name):
        results = await self.api.get_user(name, mode=enums.OsuMode.ctb)
        if results:
            embed = discord.Embed(colour=discord.Colour(
                0xbb1177), title=results[0].username, url=f'https://osu.ppy.sh/users/{results[0].user_id}/fruits')
            embed.set_image(url=self.banner_url(3, name))
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Osu(bot))
