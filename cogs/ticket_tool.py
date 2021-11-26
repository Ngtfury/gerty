import discord
import discord_components
from discord_components import *
from cogs.utils import GertyHelpCommand, Utils
from discord.ext import commands
import asyncio


def setup(client):
    client.add_cog(TicketTool(client))

class TicketTool(commands.Cog):
    def __init__(self, bot):
        self.bot=bot



    @commands.group(brief='mod', description='A ticket system', usage='[sub command]', invoke_without_command=True)
    async def ticket(self, ctx):
        return await GertyHelpCommand(self.bot).send_command_help(ctx, command='ticket')


    @ticket.command(name='create', description='Creates ticket system in a channel', usage='(channel)')
    async def ticket_create(self, ctx, channel: discord.TextChannel=None):
        if channel==None:
            channel=ctx.channel


        if ctx.guild.id in self.bot.ticket_tool_guild_ids:
            return await ctx.send(f'This server already has a ticket system configured. To delete or to re setup do `g!ticket delete`.')

        em=discord.Embed(description=f'{Utils.BotEmojis.loading()} Loading... Ticket tool system', color=Utils.BotColors.invis())
        MainMessage=await channel.send(embed=em)

        TicketComponents=[[
            Button(label='Create Ticket', emoji='📩', id=f'ticket-{ctx.guild.id}')
        ]]

        await self.bot.db.execute('INSERT INTO ticket_tool (guild_id,message_id,channel_id) VALUES ($1,$2,$3)', ctx.guild.id, MainMessage.id, channel.id)
        self.bot.ticket_tool_guild_ids.append(ctx.guild.id)

        TicketToolEmbed=discord.Embed(title='Ticket', description='To create a ticket click the 📩 button', color=Utils.BotColors.invis())
        TicketToolEmbed.set_footer(text='Gerty - Ticketing without clutter', icon_url=self.bot.user.avatar_url)
        await asyncio.sleep(0.5)
        await MainMessage.edit(embed=TicketToolEmbed, components=TicketComponents)


    @ticket.command(name='delete', description='Deletes a ticket system', usage='(channel)')
    async def ticket_delete(self, ctx):
        if not ctx.guild.id in self.bot.ticket_tool_guild_ids:
            await ctx.send('There is no ticket system configured in this server to delete. Did you mean create?')
            return

        MessageID=await self.bot.db.fetchrow('SELECT (message_id,channel_id) FROM ticket_tool WHERE guild_id=$1', ctx.guild.id)

        await self.bot.db.execute('DELETE FROM ticket_tool WHERE guild_id=$1', ctx.guild.id)
        self.bot.ticket_tool_guild_ids.remove(ctx.guild.id)

        delchannel=self.bot.get_channel(MessageID[0][1])
        delmsg=await delchannel.fetch_message(MessageID[0][0])
        await delmsg.delete()

        await ctx.send(embed=Utils.BotEmbed.success('Deleted ticket tool system for this server.'))
