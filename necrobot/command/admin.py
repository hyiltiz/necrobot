from .command import CommandType
from ..util import config


class Die(CommandType):
    def __init__(self, bot_channel):
        CommandType.__init__(self, bot_channel.necrobot, 'die')
        self.help_text = 'Tell the bot to log out. [Admin only]'
        self.admin_only = True

    async def _do_execute(self, cmd):
        await self.necrobot.logout()


class Help(CommandType):
    def __init__(self, bot_channel):
        CommandType.__init__(self, bot_channel.necrobot, 'help')
        self.help_text = 'Help.'
        self.bot_channel = bot_channel

    async def _do_execute(self, command):
        if len(command.args) == 0:
            command_list_text = ''
            for cmd_type in self.bot_channel.command_types:
                if (not cmd_type.secret_command) and (not cmd_type.admin_only or self.necrobot.is_admin(command.author)):
                    command_list_text += '`' + cmd_type.mention + '`, '
            command_list_text = command_list_text[:-2]
            await self.necrobot.client.send_message(
                command.channel,
                'Available commands in this channel: {0}\n\nType `{1} <command>` for more info about a particular'
                'command.'.format(command_list_text, self.mention))
        elif len(command.args) == 1:
            for cmd_type in self.bot_channel.command_types:
                if cmd_type.called_by(command.args[0]):
                    await self.necrobot.client.send_message(
                        command.channel, '`{0}`: {1}'.format(cmd_type.mention, cmd_type.help_text))
            return None


class Info(CommandType):
    def __init__(self, bot_channel):
        CommandType.__init__(self, 'info')
        self.help_text = "Necrobot version information."
        self.bot_channel = bot_channel

    async def _do_execute(self, cmd):
        await self.bot_channel.client.send_message(
            cmd.channel,
            'Necrobot v-{0} (alpha). See {1} for a list of commands.'.format(
                config.BOT_VERSION, self.bot_channel.necrobot.ref_channel.mention))


class Register(CommandType):
    def __init__(self, bot_channel):
        CommandType.__init__(self, bot_channel.necrobot, 'register')
        self.help_text = 'Register your current Discord name as the name to use for the bot.'

    async def _do_execute(self, cmd):
        self.necrobot.register_user(cmd.author)
        await self.necrobot.client.send_message(cmd.channel, 'Registered your name as {0}.'.format(cmd.author.mention))


class RegisterAll(CommandType):
    def __init__(self, bot_channel):
        CommandType.__init__(self, bot_channel.necrobot, 'registerall')
        self.help_text = 'Register all unregistered users. [Admin only]'
        self.admin_only = True

    async def _do_execute(self, cmd):
        if self.necrobot.is_admin(cmd.author):
            self.necrobot.register_all_users()
            await self.necrobot.client.send_message(cmd.channel, 'Registered all unregistered users.')