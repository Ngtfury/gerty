import discord
from discord.ext import commands
import discord_components
from discord_components import *

class GertyHelpCommand:
    def __init__(self, bot):
        self.bot=bot
    async def send_command_help(self, ctx, command:str):
        _command=self.bot.get_command(f'{command}')
        if not _command:
            return await ctx.send(f'There is no command called `{command}`')
        t='`'
        em=discord.Embed(description=f'{t}{t}{t}ml\n[] - Required Argument | () - Optional Argument\n{t}{t}{t}', color=0x2F3136)
        if _command.description:
            _des=_command.description
        else:
            _des='No description provided for this command'
        em.add_field(name='Description', value=f'{_des}', inline=False)
        if _command.usage:
            _usage=f'{t}{t}{t}{ctx.prefix}{_command.qualified_name} {_command.usage}{t}{t}{t}'
        else:
            _usage=f'```{ctx.prefix}{_command.qualified_name}```'
        em.add_field(name='Usage', value=_usage)
        em.set_author(name=f'Help - {_command.qualified_name}', icon_url=self.bot.user.avatar_url)
        if _command.aliases:
            aliases=[]
            for x in _command.aliases:
                aliases.append(f'`{x}`')
            em.add_field(name='Aliases', value=', '.join(aliases))
        try:
            subcommands=[]
            for cmd in _command.commands:
                subcommands.append(f'{cmd.name}')
            _subcommands=[]
            for sub in subcommands:
                _subcommands.append(f'`{sub}`')
            em.add_field(name='Subcommands', value=', '.join(_subcommands), inline=False)
        except AttributeError:
            pass
        return await ctx.send(embed=em)


class Help(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.command()
    @commands.is_owner()
    async def help(self, ctx, *, command:str):
        await GertyHelpCommand(self.bot).send_command_help(ctx=ctx, command=command)


def setup(bot):
    bot.add_cog(Help(bot))