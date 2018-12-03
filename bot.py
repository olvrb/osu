# The current Yak edition of Jailbreak Bot.
# Y'all can use this
# Boonk Gang by jacc

# Imports
import discord, os, discord.ext.commands, os.path

def prefix_func(bot, msg):
    return ['osu!']

class pysu(discord.ext.commands.Bot):

    def cog_loads(self):
        return ["cogs." + filename[:-3] for filename in os.listdir('cogs') if os.path.isfile(os.path.join("cogs", filename)) and filename.endswith('.py')]

    def __init__(self):
        self.token = "NDk4MTMwMTE2NzU3Njg0MjM0.DuYTgw.4PI1H10Z3goH_8xMZlS29oCFoWY"
        self.version = 1.0
        self.osu = "7520b4755cfd7161b3da85be693bea51e49ba412"
        super().__init__(command_prefix=prefix_func)
        self.remove_command("help")

        for ext in self.cog_loads():
            print(f"[+] Loaded cog {ext}")
            self.load_extension(ext)

        if __name__=="__main__":
            super().run(self.token)

# Runs the bot.
pysu()