import asyncio
import datetime
import discord
from discord.ext import commands
import discord_components
from discord_components import *
from discord import Webhook, AsyncWebhookAdapter
import aiohttp

class BotEmbed:
    def error(description:str):
        embed=discord.Embed(description=f'<:error:893501396161290320> {description}', color=0x2F3136)
        return embed
    def success(description:str):
        embed=discord.Embed(description=f'<:success:893501515107557466> {description}', color=0x2F3136)
        return embed

class BotColors:
    def invis():
        return 0x2F3136


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


    @commands.Cog.listener()
    async def on_command(self, ctx):
        em=discord.Embed(description=f'Command “**{ctx.command.qualified_name}**“ used by **{ctx.author.name}** ({ctx.author.mention})\nIn server **{ctx.guild.name}**\nIn channel {ctx.channel.name} ({ctx.channel.mention})\n\n[Jump to message]({ctx.message.jump_url})', timestamp=datetime.datetime.now(), color=BotColors.invis())
        em.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        em.set_footer(text='Used command at')
        em.set_thumbnail(url=ctx.guild.icon_url)
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url('https://discord.com/api/webhooks/907593512856477717/OSHPK46rXV_jJCPIn_W9K71kRb_GqTeLzR2EXOs0Uzmf4FaVmVlrJdiJPkOsw8cXevYx', adapter=AsyncWebhookAdapter(session))
            await webhook.send(embed=em, username='Gerty command logs', avatar_url=self.bot.user.avatar_url)



def setup(bot):
    bot.add_cog(Utils(bot))