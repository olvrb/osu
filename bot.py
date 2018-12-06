# The current Yak edition of Jailbreak Bot.
# Y'all can use this
# Boonk Gang by jacc

# Imports
import discord
import os
import os.path
from discord.ext import commands
import config


def prefix_func(bot, msg):
    return ['osu!']


class pysu(commands.Bot):

    def cog_loads(self):
        return ["cogs." + filename[:-3] for filename in os.listdir('cogs') if os.path.isfile(os.path.join("cogs", filename)) and filename.endswith('.py')]

    def __init__(self):
        self.version = 1.0
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
