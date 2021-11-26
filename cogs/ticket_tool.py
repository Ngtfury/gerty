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

        TicketComponents=[[
            Button(emoji='📩', id=f'ticket-{ctx.guild.id}')
        ]]

        self.bot.ticket_tool_guild_ids.append(ctx.guild.id)

        TicketToolEmbed=discord.Embed(description='**Open a ticket to contact server moderators**\nTo create a ticket click the 📩 button', color=Utils.BotColors.invis())
        TicketToolEmbed.set_footer(text='Gerty - Ticketing without clutter', icon_url=self.bot.user.avatar_url)
        TicketToolEmbed.set_author(name='Ticket Tool', icon_url='https://tickettool.xyz/images/footer.png')
        MainMessage=await channel.send(embed=TicketToolEmbed, components=TicketComponents)
        await self.bot.db.execute('INSERT INTO ticket_tool (guild_id,message_id,channel_id) VALUES ($1,$2,$3)', ctx.guild.id, MainMessage.id, channel.id)



    @ticket.command(name='delete', description='Deletes a ticket system', usage='(channel)')
    async def ticket_delete(self, ctx):
        if not ctx.guild.id in self.bot.ticket_tool_guild_ids:
            await ctx.send('There is no ticket system configured in this server to delete. Did you mean create?')
            return

        MessageID=await self.bot.db.fetchrow('SELECT * FROM ticket_tool WHERE guild_id=$1', ctx.guild.id)

        await self.bot.db.execute('DELETE FROM ticket_tool WHERE guild_id=$1', ctx.guild.id)
        self.bot.ticket_tool_guild_ids.remove(ctx.guild.id)

        try:
            delchannel=self.bot.get_channel(MessageID[2])
            delmsg=await delchannel.fetch_message(MessageID[1])
            await delmsg.delete()
        except:
            pass

        await self.bot.db.execute('DELETE FROM running_tickets WHERE guild_id=$1', ctx.guild.id)
        del self.bot.running_tickets[ctx.guild.id]
        self.bot.running_tickets[ctx.guild.id]=[]
        await ctx.send(embed=Utils.BotEmbed.success('Deleted ticket tool system for this server.'))


    @commands.Cog.listener('on_button_click')
    async def ticket_button_click(self, interaction):
        if interaction.guild.id in self.bot.ticket_tool_guild_ids:
            if interaction.component.id==f'ticket-{interaction.guild.id}':
                if interaction.author.id in self.bot.running_tickets[interaction.guild.id]:
                    return await interaction.respond(type=4, content='You already have a running ticket.')

                overwrites={
                    interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                    interaction.guild.me: discord.PermissionOverwrite(view_channel=True),
                    interaction.author: discord.PermissionOverwrite(view_channel=True)
                }

                TicketChannel=await interaction.guild.create_text_channel(name=f'ticket-{interaction.author.name}', topic=f'Ticket support for {interaction.author.name}', overwrites=overwrites, reason=f'Ticket for {interaction.author.name}')

                TicketEmbedDone=discord.Embed(title=f'{interaction.author.name}\'s ticket', description='Support will be there for you shortly', color=Utils.BotColors.invis())
                TicketEmbedDone.set_author(name='Ticket Tool', icon_url='https://tickettool.xyz/images/footer.png')
                TicketEmbedDone.set_footer(text='Gerty - Ticketing without clutter', icon_url=self.bot.user.avatar_url)
                await interaction.respond(type=4, content=f'Ticket created at channel {TicketChannel.mention}.')
                await TicketChannel.send(f'{interaction.author.mention}', embed=TicketEmbedDone)

                await self.bot.db.execute('INSERT INTO running_tickets (guild_id,channel_id,author_id) VALUES ($1,$2,$3)', interaction.guild.id, TicketChannel.id, interaction.author.id)
                self.bot.running_tickets[interaction.guild.id].append(interaction.author.id)
    
