import math
from re import match
import discord
import asyncio
import traceback
import json
from __main__ import UserBlacklisted, DisabledCommand, NoDmCommands, MaintenanceMode
from discord import message
from discord.ext import commands
from cogs.utils import Utils
from difflib import get_close_matches
import io
import os
import copy
import sys

class ErrorMatchExecute(discord.ui.Button):
    def __init__(self, ctx, match):
        super().__init__(
            style = discord.ButtonStyle.gray,
            label=f'Execute {match}',
            emoji = '<:icons_correct:922161718610776105>'
        )
        self._message = ctx.message
        self.ctx = ctx
        self.match = match

    async def callback(self, interaction: discord.Interaction):
        copied = copy.copy(self._message)
        copied._edited_timestamp = discord.utils.utcnow()
        copied.content = copied.content.replace(str(self.ctx.invoked_with), self.match)
        await interaction.response.defer()
        await self.message.delete()
        await self.ctx.bot.process_commands(copied)
    

class ErrorMatchesView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.ctx = ctx


    async def on_timeout(self):
        await self.message.delete()

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message('Sorry, you cannot interact with these buttons', ephemeral=True)
            return False
        return True





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
            command_names = []
            for command in ctx.bot.commands:
                command_names.append(command.name)
                for alias in command.aliases:
                    command_names.append(alias)
                try:
                    for subcommand in command.commands:
                        command_names.append(subcommand.name)
                        for subaliases in subcommand.aliases:
                            command_names.append(subaliases)
                except:
                    pass        
            matches = get_close_matches(ctx.invoked_with, command_names)


            if matches:
                view = ErrorMatchesView(ctx)
                _button = ErrorMatchExecute(ctx, str(matches[0]))
                view.add_item(_button)
                view.message = _button.message = await ctx.send(
                    f"""Sorry, but the command **{ctx.invoked_with}** was not found
did you mean **`{matches[0]}`**?""",
                    view = view
                )
        else:
            errview = discord.ui.View()
            errview.add_item(discord.ui.Button(style = discord.ButtonStyle.url, label = 'Support Server', url = 'https://discord.gg/7DJwH6rh', emoji='<:supportserver:923960355842031646>'))
            await ctx.reply(
                embed = discord.Embed(
                    color = Utils.BotColors.invis(),
                    title='<:exclamation:922393359941771304> An unexpected error occured',
                    description=f'{str(error)}'
                ).set_footer(text='Error has been reported to our devs, will be fixed soon...'),
                view = errview,
                mention_author=False
            )
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
