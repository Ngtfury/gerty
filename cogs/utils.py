import asyncio
import discord
from discord.ext import commands
import discord_components
from discord_components import *
import aiohttp

class BotEmbed:
    def error(description:str):
        embed=discord.Embed(description=f'<:error:893501396161290320> {description}', color=0x2F3136)
        return embed
    def success(description:str):
        embed=discord.Embed(description=f'<:success:893501515107557466> {description}', color=0x2F3136)
        return embed

class Webhook:
    def __init__(self, url:str, username:str=None, avatar_url:str=None):
        self.url=url
        self.username=username
        self.avatar_url=avatar_url
    def embed(title:str=None,description:str=None,url:str=None):
        embed=[{
            "title": title,
            "description": description,
            "url": url
            }]
        return embed
    async def send(self,content=None, embeds=None):
        data={
            'username': self.username,
            'avatar_url': self.avatar_url,
            'content': content,
            'embeds': embeds
        }
        async with aiohttp.ClientSession() as ses:
            async with ses.post(url=self.url, json=data) as rep:
                pass


class GertyHelpCommand:
    def __init__(self, bot):
        self.bot=bot
    async def send_command_help(self, ctx, command:str, embed:bool=False):
        _command=self.bot.get_command(f'{command}')
        if not _command:
            return await ctx.send(embed=BotEmbed.error(f'There is no command called “{command}“'))
        t='`'
        em=discord.Embed(description=f'{t}{t}{t}ml\n[] - Required Argument | () - Optional Argument\n{t}{t}{t}', color=0x2F3136)
        em.set_footer(text=f'Invoked by {ctx.author.name}', icon_url=ctx.author.avatar_url)
        if _command.description:
            _des=_command.description
        else:
            _des='No description provided for this command'
        em.add_field(name='Description', value=f'{_des}', inline=False)
        if f'{ctx.prefix}' == f'<@!{self.bot.user.id}> ':
            _prefix=f'@{self.bot.user.name} '
        else:
            _prefix=ctx.prefix
        if _command.usage:
            _usage=f'{t}{t}{t}{_prefix}{_command.qualified_name} {_command.usage}{t}{t}{t}'
        else:
            _usage=f'```{_prefix}{_command.qualified_name}```'
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
        if embed==True:
            return em
        else:
            return await ctx.send(embed=em)
    


class Utils(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.command(brief='utility', description='Stop it get some help!', usage='(command)')
    async def help(self, ctx, *, command:str):
        await GertyHelpCommand(self.bot).send_command_help(ctx=ctx, command=command)


def setup(bot):
    bot.add_cog(Utils(bot))