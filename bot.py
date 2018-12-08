# The current Yak edition of Jailbreak Bot.
# Y'all can use this
# Boonk Gang by jacc

# Imports
import discord
import os
import os.path
from discord.ext import commands
import config
from ast import literal_eval


try:
    open('profiles.sav').close()
except:
    with open('profiles.sav','w') as file:
        file.write('{}')
with open('profiles.sav') as file:
    profiledata = literal_eval(file.read())

try:
    open('prefixes.sav').close()
except:
    with open('prefixes.sav','w') as file:
        file.write('{}')
with open('prefixes.sav') as file:
    prefixdata = literal_eval(file.read())

async def prefix_func(bot, msg):
    try:
        extra = bot.prefixes[msg.guild.id]
    except KeyError:
        extra = None
    except AttributeError:
        extra = ''
    if extra is not None:
        prefixes = [extra, 'osu!','pysu!', '<@421879566265614337>', '<@!421879566265614337>']
    else:
        prefixes = ['osu!','pysu!', '<@421879566265614337>', '<@!421879566265614337>']
    return prefixes


class pysu(commands.Bot):

    def cog_loads(self):
        return ["cogs." + filename[:-3] for filename in os.listdir('cogs') if os.path.isfile(os.path.join("cogs", filename)) and filename.endswith('.py')]

    def __init__(self):
        self.version = 1.0
        self.profiles = profiledata
        self.prefixes = prefixdata
        super().__init__(command_prefix=prefix_func)
        # self.remove_command("help")
        # we can do that in its own cog

        for ext in self.cog_loads():
            print(f"[+] Loaded cog {ext}")
            self.load_extension(ext)

    async def on_ready(self):
        print('-'*40)
        print('{:^40}'.format(str(self.user)))
        print('{:^40}'.format(str(self.user.id)))
        print('-'*40)


# Runs the bot.
bot = pysu()
if __name__ == "__main__":
    bot.run(config.token)
