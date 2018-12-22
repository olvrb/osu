locale = {
    'meta': {
        'latency':{
            'help': 'Get the bot\'s latency.'
        },
        'invite': {
            'help': 'Get a link to invite osu!bot into your server.',
            'out': '📥 Invite osu!bot to your server: https://discordapp.com/oauth2/authorize?client_id=421879566265614337&scope=bot&permissions=347136'
        },
        'support': {
            'help': 'Get a link to the support server.',
            'out': '❔ Join the support server here: https://discord.gg/uda4VuE'
        },
        'stats': {
            'help': 'Get information about the bot.',
            'title': 'osu!bot Stats',
            'commit': 'Latest GitHub Commit',
            'message': ''' ```Commit {} made by {} - '{}'``` '''
        }
    },
    'help': {
        'help': {
            'header': 'osu!bot Help Manual',
            'page_msg': 'There are {} help pages. Send a number to see the corresponding page. Send any other message to exit.',
            'quit': 'Quit help menu.',
            'footer': "Type {0}help <command> for more info on a command.\nYou can also type {0}help <category> for more info on a category.",
            'description': 'osu!bot\'s commands',
            'syntax': '`Syntax: {0}`',
            'no_category': '**__\u200bNo Category:__**',
            'commands': '**__Commands:__**',
            'subcommands': '**__Subcommands:__**',
            'header_with_page': 'osu!bot Help Manual Page {}',
            'not_found': 'Commands are case sensitive. Please check your spelling and try again',
            'help': """Shows help documentation.
                       [p]**help**: Shows the help manual.
                       [p]**help** command: Show help for a command
                       [p]**help** Category: Show commands and description for a category""",
            'no_subcommands': 'Command "{0.name}" has no subcommands.'
        }
    },
    'osu': {
        'user': {
            'help': 'Fetch a user\'s profile',
            'name': 'osu! User: {}',
            'info': 'User Info',
            'general': '''User ID: {}
            Level: {}
            Country: {}
            Accuracy: {}%''',
            'stats': 'User Stats',
            'rank': '''PP: {}
            Global Rank: #{}
            Country Rank: #{}
            {} SS, {} S, {} A''',
            'total': 'Total Plays: {}'
        },
        'mode':{
            'osu': 'osu!',
            'taiko': 'osu!taiko',
            'mania': 'osu!mania',
            'fruits': 'osu!catch',
        }
    },
    'configure':{
        'profile': {
            'help': 'Show the profile of you or another user. Modify it with [p]profile set',
            'profile_for': 'Profile for {}',
            'name': 'osu! Username',
            'mode': 'Default osu! Mode',
            'colour': 'User Colour: {}',
            'error': 'An error occurred',
            'you_not': 'You do not have a profile',
            'they_not': 'They do not have a profile',
            'set': {
                'fail':'You need to specify a key and a value. See `{}help profile set` for more',
                'colour': {
                    'help': '''Set the colour for embeds and banners.
                               Provide a hex code like `[p]profile set colour #03dc03` or `[p]profile set colour 0088ff` or even `[p]profile set colour 0x123456`
                               For the default colour, do:
                               [p]profile set colour #bb1177''',
                    'set': 'Your profile colour has been set.',
                    'invalid': 'That colour code is invalid.',
                },
                'username': {
                    'help': '''Set your osu! username.
                               Also sets the default user for [p]user and [p]banner.
                               To make your osu! username the same as your Discord username, do:
                               [p]profile set username INHERITED''',
                    'set': 'Your osu! username has been set.'
                },
                'mode': {
                    'help': '''Set your preferred mode.
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
                               ­  - 3''',
                    'set': 'Your default mode has been set.',
                    'invalid': 'That is not a valid mode.'
                },
            }
        },
        'setprefix': {
            'help': '''Sets the server's custom prefix (the original will still work under most circumstances). Requires the Manage Server permission. To use spaces in your prefix quote it.
                       You can even use a space at the end of the prefix.
                       
                       Example 1 (no spaces):
                       [p]setprefix osu|
                       Example 2 (with trailing space):
                       [p]setprefix "osu "
                       
                       To remove your server's prefix:
                       [p]setprefix ""''',
            'abuse': 'In order to prevent abuse to my disk, the custom prefix length has been capped at 10. Sorry!',
            'added': 'Your server\'s custom prefix has been set to `{}`',
            'changed': 'Your server\'s custom prefix has been changed to `{}`',
            'removed': 'Your server\'s custom prefix has been removed',
        }
    },
    'error': {
        'permission': 'You do not have permission to use this command.',
        'arguments': 'You are missing required arguments.',
        'argument': 'You have given an invalid argument.',
        'error': 'An error occurred in the `{}` command. This has been reported for you automatically.'
    }
}