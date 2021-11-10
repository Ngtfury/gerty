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

    @commands.command(brief='util', description='Stop it get some help!', usage='(command)')
    async def help(self, ctx, *, command:str=None):
        if command:
            return await GertyHelpCommand(self.bot).send_command_help(ctx=ctx, command=command)
        
        MainEmbed=discord.Embed(description='`g!help [command]` - View help for specific command\nHover below categories for more help.\nReports bug if any via `g!report`\n```ml\n[] - Required Argument | () - Optional Argument```', color=BotColors.invis())
        MainEmbed.set_author(name=f'{self.bot.user.name} HelpDesk', icon_url=self.bot.user.avatar_url, url=discord.utils.oauth_url(self.bot.user.id))
        MainEmbed.add_field(name='<:modules:884784557822459985> Modules:', value='> <:cate:885482994452795413> Utilities\n> <:cate:885482994452795413> Miscellaneous\n> <:cate:885482994452795413> Fun\n> <:cate:885482994452795413> Moderation\n> <:cate:885482994452795413> Tags\n> <:cate:885482994452795413> Admin\n> <:cate:885482994452795413> Rtfm (docs)', inline=False)
        MainEmbed.add_field(name='<:news:885177157138145280> News', value='Don\'t use help command! under construction :warning:', inline=True)
        MainEmbed.add_field(name='<:links:885161311456071750> Links', value=f'[Invite me]({discord.utils.oauth_url(self.bot.user.id)}) | [About owner](https://discord.com/users/770646750804312105)', inline=True)
        MainEmbed.set_footer(text=f'Invoked by {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=MainEmbed)

    @commands.Cog.listener()
    async def on_command(self, ctx):
        if ctx.author.id in self.bot.owner_ids:
            return
        if not ctx.guild:
            return
        em=discord.Embed(description=f'Command “**{ctx.command.qualified_name}**“ used by **{ctx.author}** ({ctx.author.mention})\nIn server **{ctx.guild.name}**\nIn channel {ctx.channel.name} ({ctx.channel.mention})\n\n[Jump to message]({ctx.message.jump_url})', timestamp=datetime.datetime.now(), color=BotColors.invis())
        em.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        em.set_footer(text='Used command at')
        em.set_thumbnail(url=ctx.guild.icon_url)
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url('https://discord.com/api/webhooks/907593512856477717/OSHPK46rXV_jJCPIn_W9K71kRb_GqTeLzR2EXOs0Uzmf4FaVmVlrJdiJPkOsw8cXevYx', adapter=AsyncWebhookAdapter(session))
            await webhook.send(embed=em, username='Gerty command logs', avatar_url=self.bot.user.avatar_url)


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        em=discord.Embed(description=f'**Guild owner**: **{guild.owner.name}** ({guild.owner.mention})\n**Channels**: {len(guild.channels)}\n**Members**: {guild.member_count}', color=BotColors.invis(), timestamp=datetime.datetime.now())
        em.set_author(name=guild.name, icon_url=guild.icon_url)
        em.set_thumbnail(url=guild.icon_url)
        em.set_footer(text='Joined server at')
        async with aiohttp.ClientSession() as session:
            web=Webhook.from_url(url='https://discord.com/api/webhooks/907593485224386560/T6k31rtY8Yf_WsSjH77OW27bteM7Gnl7ve7q6rcRXfyQj6s5bLXsoYO97kHqo70MOtdH', adapter=AsyncWebhookAdapter(session))
            await web.send(embed=em, username='Gerty guild logs', avatar_url=self.bot.user.avatar_url)


    @commands.Cog.listener()
    async def on_ready(self):
        async with aiohttp.ClientSession() as session:
            web=Webhook.from_url(url='https://discord.com/api/webhooks/907681269452800061/-uEovWEWLcEXKNecuYe_1OlfkSAlCpv_fR8TcH2TsBJ9wab52GdB6QarlHaa3WqUotqR', adapter=AsyncWebhookAdapter(session))
            await web.send(content=f'⚠ <@&907682091595096084>\n<:success:893501515107557466> **Gerty is connected**', username='Gerty status logs', avatar_url=self.bot.user.avatar_url, allowed_mentions=discord.AllowedMentions.all())
    @commands.Cog.listener()
    async def on_shard_disconnect(self, shard_id):
        async with aiohttp.ClientSession() as session:
            web=Webhook.from_url(url='https://discord.com/api/webhooks/907681269452800061/-uEovWEWLcEXKNecuYe_1OlfkSAlCpv_fR8TcH2TsBJ9wab52GdB6QarlHaa3WqUotqR', adapter=AsyncWebhookAdapter(session))
            await web.send(content=f'⚠ <@&907682091595096084>\nSHARD ID **{shard_id}** HAS BEEN DISCONNECTED', username='Gerty status logs', avatar_url=self.bot.user.avatar_url, allowed_mentions=discord.AllowedMentions.all())

def setup(bot):
    bot.add_cog(Utils(bot))