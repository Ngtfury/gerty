import discord
import asyncio
import traceback
import json
from __main__ import UserBlacklisted, DisabledCommand, NoDmCommands, MaintenanceMode
from discord.ext import commands
from cogs.utils import Utils
from difflib import get_close_matches
import io
import os
import sys


class events(commands.Cog):
    def __init__(self, bot):
        self.client = bot
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content != after.content:
            await self.client.process_commands(after)



    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(description="<:error:893501396161290320> Please wait **{:.2f}** seconds before using this command again".format(error.retry_after), color=0x2F3136)
            await ctx.send(embed=em)
        elif isinstance(error, commands.MissingRequiredArgument):
            em = discord.Embed(
            color=Utils.BotColors.invis(),
            title = 'Incorrect usage',
            #description = 
            description=f'```ml\n[] - Required Argument | () - Optional Argument```'
            )
            em.add_field(name='Missing', value=f'`{str(error.param.name)}` is a required argument that is missing', inline=False)
            _usage = f' {ctx.command.usage}' if ctx.command.usage else ''
            em.add_field(name='Usage', value=f'```{Utils.clean_prefix(ctx)}{ctx.command.name}{_usage}```')
            await ctx.reply(embed=em, mention_author=False)
        elif isinstance(error, commands.MissingPermissions):
            _oh=[f'`{x.capitalize()}`' for x in error.missing_perms]
            oh_=', '.join(_oh)
            _perms=oh_.replace('_', " ")
            em = discord.Embed(description=f"<:error:893501396161290320> You are missing {_perms} permission(s) to run this command", color=0x2F3136)
            await ctx.reply(embed=em, mention_author=False)
        elif isinstance(error, commands.NotOwner):
            em = discord.Embed(description="<a:zpanda_heart:907292207604723743> This is an owner-only command and you don't look like `Nιgнт Fυяу ♪🤍#4371`", color=0x2F3136)
            await ctx.send(embed=em)
        elif isinstance(error, commands.BotMissingPermissions):
            _oh=[f'`{x.capitalize()}`' for x in error.missing_perms]
            oh_=', '.join(_oh)
            _perms=oh_.replace('_', " ")
            em = discord.Embed(description=f"<:error:893501396161290320> The bot is missing {_perms} permission(s) to run this command", color=0x2F3136)
            await ctx.reply(embed=em, mention_author=False)
        elif isinstance(error, UserBlacklisted):
            em = discord.Embed(description=f"<:error:893501396161290320> You are blacklisted from using commands for reason `{error.reason}`", color=0x2F3136)
            await ctx.send(embed=em)
        elif isinstance(error, MaintenanceMode):
            await ctx.send(
                embed = discord.Embed(
                    color = Utils.BotColors.invis(),
                    description = f'<:maintenance:923486040738652220> Sorry, I\'m on **maintenance mode**, I\'ll not respond to commands until <t:{ctx.bot.maintenance_timestamp}:t>'
                )
            )
        elif isinstance(error, NoDmCommands):
            await ctx.send(embed = Utils.BotEmbed.error('Sorry, commands will not work on DMs'))
        elif f"{error}" == "Command raised an exception: Forbidden: 403 Forbidden (error code: 50013): Missing Permissions":
            em = discord.Embed(description=f"<:error:893501396161290320> The bot is missing permissions to run this command", color=0x2F3136)
            await ctx.reply(embed=em, mention_author=False)
        elif isinstance(error, commands.MemberNotFound):
            em = discord.Embed(description=f"<:error:893501396161290320> Member `{error.argument}` was not found in this server", color=0x2F3136)
            await ctx.reply(embed=em, mention_author=False)
        elif isinstance(error, commands.ChannelNotFound):
            em = discord.Embed(description=f"<:error:893501396161290320> Channel `{error.argument}` was not found in this server", color=0x2F3136)
            await ctx.reply(embed=em, mention_author=False)
        elif isinstance(error, commands.ChannelNotReadable):
            em = discord.Embed(description=f"<:error:893501396161290320> Bot does not have permissions to read messages in `{error.argument}`", color=0x2F3136)
            await ctx.reply(embed=em, mention_author=False)
        elif isinstance(error, commands.RoleNotFound):
            em = discord.Embed(description=f"<:error:893501396161290320> Role `{error.argument}` was not found in this server", color=0x2F3136)
            await ctx.reply(embed=em, mention_author=False)
        elif isinstance(error, commands.BadArgument):
            em = discord.Embed(description=f"<:error:893501396161290320> {error}", color=0x2F3136)
            await ctx.reply(embed=em, mention_author=False)
        elif isinstance(error, DisabledCommand):
            em=discord.Embed(description=f'<:error:893501396161290320> Commands in {ctx.channel.mention} are disabled', color=0x2F3136)
            await ctx.reply(embed=em, mention_author=False)
        elif isinstance(error, commands.DisabledCommand):
            embed=Utils.BotEmbed.error(f'Command “{ctx.command.qualified_name}“ is now globally disabled, Maybe under development')
            await ctx.reply(embed=embed, mention_author=False)
        elif isinstance(error, commands.MaxConcurrencyReached):
            types={
            commands.BucketType.user: 'user',
            commands.BucketType.channel: 'channel',
            commands.BucketType.guild: 'server',
            commands.BucketType.member: 'member',
            commands.BucketType.category: 'category',
            commands.BucketType.role: 'role',
            commands.BucketType.default: 'global commands'
            }
            em=Utils.BotEmbed.error(f'Too many people are using this command. It can only be used **{error.number}** time per **{types[error.per]}**')
            await ctx.reply(embed=em, mention_author=False)
        elif isinstance(error, commands.CommandNotFound):
            command_names = [str(x) for x in ctx.bot.commands]
            matches = get_close_matches(ctx.invoked_with, command_names)
            if matches:
                matches_=[]
            num=0
            for x in matches:
                num=num+1
                matches_.append(f'> {num}. {x}')
            _matches='\n'.join(matches_)
            await ctx.send(embed=Utils.BotEmbed.error(f'Command `{ctx.invoked_with}` does\'t exists\nDid you mean...\n{_matches}'))
        else:
            await ctx.reply('An unexpected error ocurred... Error has been reported to our devs, will be fixed soon...', mention_author=False, delete_after=5)
            error_log_channel=self.bot.get_channel(906874671847333899)

            traceback_string = "".join(traceback.format_exception(type(error), error, error.__traceback__)).replace("``", "`\u200b`")

            try:
                await error_log_channel.send(f'__**AN ERROR OCCURED**__\n```yml\nInvoked by: {ctx.author}\nServer: {ctx.guild.name}\nCommand: {ctx.command.name}```\n__**TRACEBACK**__\n```py\n{traceback_string}```')
            except (discord.Forbidden, discord.HTTPException):
                await error_log_channel.send(
                    f'__**AN ERROR OCCURED**__\n```yml\nInvoked by: {ctx.author}\nServer: {ctx.guild.name}\nCommand: {ctx.command.name}```\n__**TRACEBACK**__\n',
                    file=discord.File(io.StringIO(traceback_string), filename='traceback.py')
                )




def setup(client):
    client.add_cog(events(client))
