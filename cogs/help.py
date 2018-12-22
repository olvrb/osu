import discord
from discord.ext import commands
from discord.ext.commands import formatter
import asyncio
import sys
import re
import inspect
import itertools
import traceback

empty = u'\u200b'


_mentions_transforms = {
    '@everyone': '@\u200beveryone',
    '@here': '@\u200bhere'
}


_mention_pattern = re.compile('|'.join(_mentions_transforms.keys()))


orig_help = None


class Help(formatter.HelpFormatter):
    """Formats help for commands."""

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot
        global orig_help
        orig_help = bot.get_command('help')
        self.bot.remove_command('help')
        self.bot.formatter = self
        self.bot.help_formatter = self
        super().__init__(*args, **kwargs)

    # Shortcuts that allow cog to run on 0.16.8 and 1.0.0a

    def pm_check(self, ctx):
        return isinstance(ctx.channel, discord.abc.PrivateChannel)

    @property
    def me(self):
        return self.context.me

    @property
    def bot_all_commands(self):
        return self.bot.all_commands

    @property
    def avatar(self):
        return self.bot.user.avatar_url_as(format='png')

    def colour(self, ctx):
        return self.bot.colour_for(ctx)

    async def send(self, dest, content=None, embeds=None):
        if len(embeds) == 1:
            embed = embeds[0]
            embed.set_author(name=self.bot.translate_for(self.context.author,'help.help.header'),
                             icon_url=self.bot.user.avatar_url)
            await dest.send(embed=embed)
            return
        help_msg = await dest.send(embed=embeds[0])
        if dest.permissions_for(self.context.me).value & 65600 == 65600 or dest.permissions_for(self.context.me).value & 8 == 8:
            home, back, forward, end = '⏮', '◀', '▶', '⏭'
            stop = '⏹'
            valid_r = [home, back, forward, end, stop]
            page = 0
            max_page = len(embeds)
            for i in valid_r:
                await help_msg.add_reaction(i)
            await asyncio.sleep(0.1)

            def check(reaction, user):
                return reaction.emoji in valid_r and reaction.message.id == help_msg.id
            try:
                while True:
                    reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=120)
                    try:
                        await help_msg.remove_reaction(reaction, user)
                    except:
                        pass
                    if reaction.emoji == home:
                        page = 0
                    elif reaction.emoji == back:
                        page -= 1
                    elif reaction.emoji == forward:
                        page += 1
                    elif reaction.emoji == end:
                        page = max_page - 1
                    elif reaction.emoji == stop:
                        break

                    page %= max_page
                    await help_msg.edit(embed=embeds[page])
            except:
                pass
            await help_msg.delete()
        else:
            page_msg = await dest.send(self.bot.translate_for(self.context.author,'help.help.page_msg').format(len(embeds)))

            def is_not_me(msg):
                if msg.author.id != self.bot.user.id and msg.channel == dest.channel:
                    return True
            while True:
                reply = await self.bot.wait_for('message', check=is_not_me)
                try:
                    page_number = int(reply.content) - 1
                    if page_number < 0:
                        page_number = 0
                    elif page_number >= len(embeds):
                        page_number = len(embeds)-1
                    await help_msg.edit(embed=embeds[page_number])
                    try:
                        await reply.delete()
                    except:
                        pass
                except ValueError:
                    await page_msg.edit(content=self.bot.translate_for(self.context.author,'help.help.quit'))
                    break

    @property
    def author(self):
        # Get author dict with username if PM and display name in guild
        if self.pm_check(self.context):
            name = self.bot.user.name
        else:
            name = self.me.display_name if not '' else self.bot.user.name
        author = {
            'name': self.bot.translate_for(self.context.author,'help.help.header'),
            'icon_url': self.avatar
        }
        return author

    @property
    def destination(self):
        return self.context.message.author if self.bot.pm_help else self.context.message.channel

    async def _add_subcommands(self, cmds):
        list_entries = []
        entries = ''
        for name, command in cmds:
            if name in command.aliases:
                # skip aliases
                continue
            new_short_doc = self.bot.translate_for(self.context.author,command.short_doc).replace(
                '[p]', self.bot.command_prefix(self.bot, self.context)[0])
            if self.is_cog() or self.is_bot():
                name = '{0}{1}'.format(self.bot.command_prefix(
                    self.bot, self.context)[0], name)

            if len(entries + '**{0}**  -  {1}\n'.format(name, new_short_doc)) > 1000:
                list_entries.append(entries)
                entries = ''
            entries += '**{0}**  -  {1}\n'.format(name, new_short_doc)
        list_entries.append(entries)
        return list_entries

    def get_ending_note(self):
        # command_name = self.context.invoked_with
        return self.bot.translate_for(self.context.author,'help.help.footer').format(
                   self.bot.command_prefix(self.bot, self.context)[0])

    async def format(self, ctx, command):
        """Formats command for output.
        Returns a dict used to build embed"""

        # All default values for embed dict
        self.command = command
        self.context = ctx
        emb = {
            'embed': {
                'title': '',
                'description': self.bot.translate_for(self.context.author,'help.help.description'),
            },
            'footer': {
                'text': self.get_ending_note()
            },
            'fields': []
        }

        if isinstance(command, discord.ext.commands.core.Command):
            # <signature portion>
            # emb['embed']['title'] = emb['embed']['description']
            emb['embed']['description'] = self.bot.translate_for(self.context.author,'help.help.syntax').format(
                self.get_command_signature())

            # <long doc> section
            if command.help:
                name = '{0}'.format(self.bot.translate_for(self.context.author,command.help).split('\n\n')[0])
                name_length = len(name)
                name = name.replace('[p]', self.bot.command_prefix(
                    self.bot, self.context)[0])
                value = self.bot.translate_for(self.context.author,command.help)[name_length:].replace(
                    '[p]', self.bot.command_prefix(self.bot, self.context)[0])
                if value == '':
                    name = '{0}'.format(self.bot.translate_for(self.context.author,command.help).split('\n')[0])
                    name_length = len(name)
                    value = self.bot.translate_for(self.context.author,command.help)[name_length:].replace(
                        '[p]', self.bot.command_prefix(self.bot, self.context)[0])
                if value == '':
                    value = empty
                if len(value) > 1024:
                    first = value[:1024].rsplit('\n', 1)[0]
                    list_values = [first, value[len(first):]]
                    while len(list_values[-1]) > 1024:
                        next_val = list_values[-1][:1024].rsplit('\n', 1)[0]
                        remaining = [next_val, list_values[-1][len(next_val):]]
                        list_values = list_values[:-1] + remaining
                    for new_val in list_values:
                        field = {
                            'name': name,
                            'value': new_val,
                            'inline': False
                        }
                        emb['fields'].append(field)
                else:
                    field = {
                        'name': name,
                        'value': value,
                        'inline': False
                    }
                    emb['fields'].append(field)

            # end it here if it's just a regular command
            if not self.has_subcommands():
                return emb

        def category(tup):
            # Turn get cog (Category) name from cog/list tuples
            cog = tup[1].cog_name
            return '**__{0}:__**'.format(cog) if cog is not None else self.bot.translate_for(self.context.author,'help.help.no_category')

        # Get subcommands for bot or category
        filtered = await self.filter_command_list()

        if self.is_bot():
            # Get list of non-hidden commands for bot.
            data = sorted(filtered, key=category)
            for category, commands in itertools.groupby(data, key=category):
                # there simply is no prettier way of doing this.

                commands = sorted(commands)
                if len(commands) > 0:
                    for count, subcommands in enumerate(await self._add_subcommands(commands)):
                        field = {
                            'inline': False
                        }
                        if count > 0:
                            field['name'] = category + \
                                ' pt. {}'.format(count+1)
                        else:
                            field['name'] = category
                        field['value'] = subcommands  # May need paginated
                        emb['fields'].append(field)

        else:
            # Get list of commands for category
            filtered = sorted(filtered)
            if filtered:
                for subcommands in await self._add_subcommands(filtered):
                    field = {
                        'name': self.bot.translate_for(self.context.author,'help.help.commands') if not self.is_bot() and self.is_cog() else self.bot.translate_for(self.context.author,'help.help.subcommands'),
                        'value': subcommands,  # May need paginated
                        'inline': False
                    }

                    emb['fields'].append(field)

        return emb

    async def format_help_for(self, ctx, command_or_bot, reason: str = None):
        """Formats the help page and handles the actual heavy lifting of how
        the help command looks like. To change the behaviour, override the
        :method:`~.HelpFormatter.format` method.
        Parameters
        -----------
        ctx: :class:`.Context`
            The context of the invoked help command.
        command_or_bot: :class:`.Command` or :class:`.Bot`
            The bot or command that we are getting the help of.
        Returns
        --------
        list
            A paginated output of the help command.
        """
        self.context = ctx
        self.command = command_or_bot
        emb = await self.format(ctx, command_or_bot)

        if reason:
            emb['embed']['title'] = "{0}".format(reason)

        embeds = []
        embed = discord.Embed(colour=self.colour(ctx), **emb['embed'])
        embed.set_author(name=self.bot.translate_for(self.context.author,'help.help.header_with_page').format(1),
                         icon_url=self.avatar)
        embed.set_footer(**emb['footer'])
        txt = ""
        for field in emb['fields']:
            txt += field["name"] + field["value"]
            if len(txt) > 1000:
                embeds.append(embed)
                txt = field["name"] + field["value"]
                del embed
                embed = discord.Embed(colour=self.colour(ctx), **emb['embed'])
                embed.set_author(name=self.bot.translate_for(self.context.author,'help.help.header_with_page').format(
                    len(embeds)+1), icon_url=self.avatar)
                embed.set_footer(**emb['footer'])
            embed.add_field(**field)
        embeds.append(embed)

        embed.set_footer(**emb['footer'])
        await self.send(self.destination, embeds=embeds)

    def simple_embed(self, title=None, description=None, colour=None, author=None):
        # Shortcut
        embed = discord.Embed(
            title=title, description=description, colour=colour)
        embed.set_footer(text=self.bot.formatter.get_ending_note())
        if author:
            embed.set_author(**author)
        return embed

    def cmd_not_found(self, cmd, colour=0):
        # Shortcut for a shortcut. Sue me
        embed = self.simple_embed(title=self.bot.command_not_found.format(cmd),
                                  description=self.bot.translate_for(self.context.author,'help.help.not_found'),
                                  colour=colour, author=self.author)
        return embed

    @commands.command(name='help', pass_context=True,help='help.help.help')
    async def help(self, ctx, *cmds: str):
        """Shows help documentation.
        [p]**help**: Shows the help manual.
        [p]**help** command: Show help for a command
        [p]**help** Category: Show commands and description for a category"""
        self.context = ctx

        def repl(obj):
            return _mentions_transforms.get(obj.group(0), '')

        # help by itself just lists our own commands.
        if len(cmds) == 0:
            await self.bot.formatter.format_help_for(ctx, self.bot)
            return

        elif len(cmds) == 1:
            # try to see if it is a cog name
            name = _mention_pattern.sub(repl, cmds[0])
            command = None
            if name in self.bot.cogs:
                command = self.bot.cogs[name]
            else:
                command = self.bot_all_commands.get(name)
                if command is None:
                    await self.send(self.destination, embeds=[self.cmd_not_found(name, self.colour(ctx))])
                    return

            await self.bot.formatter.format_help_for(ctx, command)
        else:
            name = _mention_pattern.sub(repl, cmds[0])
            command = self.bot_all_commands.get(name)
            if command is None:
                await self.send(self.destination, embeds=[self.cmd_not_found(name, self.colour(ctx))])
                return

            for key in cmds[1:]:
                try:
                    key = _mention_pattern.sub(repl, key)
                    command = command.all_commands.get(key)
                    if command is None:
                        await self.send(self.destination, embeds=[self.cmd_not_found(key, self.colour(ctx))])
                        return
                except AttributeError:
                    await self.send(self.destination,
                                    embeds=[self.simple_embed(title=self.bot.translate_for(self.context.author,'help.help.no_subcommands').format(command),
                                                              colour=self.colour(
                                                                  ctx),
                                                              author=self.author)])
                    return

            await self.bot.formatter.format_help_for(ctx, command)

    def __unload(self):
        self.bot.formatter = formatter.HelpFormatter()
        self.bot.add_command(orig_help)


def setup(bot):
    bot.add_cog(Help(bot))
