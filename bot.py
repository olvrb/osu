import discord
import os
import os.path
from discord.ext import commands
import config
from ast import literal_eval
import traceback
import aiofiles

try:
    open('profiles.sav').close()
except:
    with open('profiles.sav', 'w')as file:
        file.write('{}')
with open('profiles.sav')as file:
    profiledata = literal_eval(file.read())

try:
    open('prefixes.sav').close()
except:
    with open('prefixes.sav', 'w')as file:
        file.write('{}')
with open('prefixes.sav')as file:
    prefixdata = literal_eval(file.read())


def prefix_func(bot, msg):
    try:
        extra = bot.prefixes[msg.guild.id]
    except KeyError:
        extra = None
    except AttributeError:
        extra = ''
    if extra is not None:
        prefixes = [extra, 'osu!', 'pysu!', 
                    '<@421879566265614337> ', '<@!421879566265614337> ']
    else:
        prefixes = ['osu!', 'pysu!', '<@421879566265614337> ', 
                    '<@!421879566265614337> ']
    return prefixes


class pysu(commands.Bot):

    def cog_loads(self):
        return ["cogs." + filename[:-3] for filename in os.listdir('cogs')if os.path.isfile(os.path.join("cogs", filename))and filename.endswith('.py')]

    def __init__(self):
        self.version = 1.0
        self.profiles = profiledata
        self.prefixes = prefixdata
        super().__init__(command_prefix = prefix_func)
        # self.remove_command("help")
        # we can do that in its own cog

        for ext in self.cog_loads():
            try:
                self.load_extension(ext)
            except:
                traceback.print_exc()
                print(f'[!] Failed to load cog {ext}')
            else:
                print(f"[+] Loaded cog {ext}")

    async def save_profiles(self):
        async with aiofiles.open('profiles.sav', 'w')as file:
            await file.write(repr(self.profiles))

    async def save_prefixes(self):
        async with aiofiles.open('prefixes.sav', 'w')as file:
            await file.write(repr(self.prefixes))

    def colour_for(self, user, default = 0xbb1177):
        try:
            colour = self.profiles[user.id]['colour']
        except:
            colour = default
        return discord.Colour(colour)

    def username_for(self, user, default = 'INHERITED'):
        if not user:
            return
        if default == 'INHERITED':
            default = user.name
        try:
            name = self.profiles[user.id]['username']
        except:
            name = default
        return name

    def mode_for(self, user, default = 'osu'):
        try:
            mode = self.profiles[user.id]['mode']
        except:
            mode = default
        return mode

    def profile_for(self, user):
        try:
            return self.profiles[user.id]
        except:
            return

    async def modify_profile_for(self, user, **kwargs):
        try:
            profile = self.profiles[user.id]
        except:
            profile = {}
        for key, value in kwargs:
            profile[key] = value
        self.profiles[user.id] = profile
        await self.save_profiles()

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            pass
        elif isinstance(error, discord.errors.Forbidden):
            pass
        elif isinstance(error, commands.errors.CheckFailure):
            await ctx.send('You do not have permission to use this command.')
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            formatter = commands.formatter.HelpFormatter()
            help = await formatter.format_help_for(ctx, ctx.command)
            await ctx.send('You are missing required arguments.' + "\n" + help[0])
        elif isinstance(error, commands.errors.BadArgument):
            await ctx.send('You have given an invalid argument.')
        else:
            await ctx.send('An error occurred in the `{}` command. This has been automatically reported for you.'.format(ctx.command.name))
            print("Ignoring exception in command {}".format(ctx.command.name))
            trace = traceback.format_exception(
                type(error), error, error.__traceback__)
            out = '```'
            for i in trace:
                if len(out + i + '```') > 2000:
                    await self.channel.send(out + '```')
                    out = '```'
                out += i
            await self.channel.send(out + '```')

    async def on_ready(self):
        print(' - ' * 25)
        print('{:^75}'.format(str(self.user)))
        print('{:^75}'.format(str(self.user.id)))
        print(' - ' * 25)
        self.channel = self.get_channel(521000713283829768)


bot = pysu()
if __name__ == "__main__":
    bot.run(config.token)
