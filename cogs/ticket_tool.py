from asyncio.locks import Event
import discord
from cogs.utils import GertyHelpCommand, Utils
from discord.ext import commands
import asyncio


def setup(client):
    client.add_cog(TicketTool(client))

class TicketTool(commands.Cog):
    def __init__(self, bot):
        self.bot=bot



    @commands.group(brief='mod', description='A ticket system', usage='[sub command]', invoke_without_command=True)
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def ticket(self, ctx):
        if not ctx.guild.id in self.bot.ticket_tool_guild_ids:
            return await GertyHelpCommand(self.bot).send_command_help(ctx, command='ticket')
        

        _id=await self.bot.db.fetchrow('SELECT channel_id FROM ticket_tool WHERE guild_id=$1', ctx.guild.id)

        channel=ctx.guild.get_channel(_id[0])

        await ctx.send(embed=Utils.BotEmbed.success(f'Ticket system is already configured in {channel.mention} for this server.'))


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
        self.bot.running_tickets[ctx.guild.id]=[]

        TicketToolEmbed=discord.Embed(description='**Open a ticket to contact server moderators**\nTo create a ticket click the 📩 button', color=Utils.BotColors.invis())
        TicketToolEmbed.set_footer(text='Gerty - Ticketing without clutter', icon_url=self.bot.user.avatar.url)
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
                    interaction.guild.me: discord.PermissionOverwrite(embed_links=True),
                    interaction.author: discord.PermissionOverwrite(view_channel=True)
                }

                TicketChannel=await interaction.guild.create_text_channel(name=f'ticket-{interaction.author.name}', topic=f'Ticket support for {interaction.author.name}', overwrites=overwrites, reason=f'Ticket for {interaction.author.name}')


                TicketDoneCompo=[[
                    Button(emoji='🔒', id=f'ticketclose-{interaction.author.id}')
                ]]

                TicketEmbedDone=discord.Embed(description='**Support will be there for you shortly**\nTo close this ticket click 🔒 button', color=Utils.BotColors.invis())
                TicketEmbedDone.set_author(name=f'{interaction.author.name}\'s ticket', icon_url='https://tickettool.xyz/images/footer.png')
                TicketEmbedDone.set_footer(text=f'Invoked by {interaction.author}', icon_url=interaction.author.avatar.url)
                await interaction.respond(type=4, content=f'Ticket created at channel {TicketChannel.mention}.')
                await TicketChannel.send(f'{interaction.author.mention} Welcome', embed=TicketEmbedDone, components=TicketDoneCompo)

                await self.bot.db.execute('INSERT INTO running_tickets (guild_id,channel_id,author_id) VALUES ($1,$2,$3)', interaction.guild.id, TicketChannel.id, interaction.author.id)
                self.bot.running_tickets[interaction.guild.id].append(interaction.author.id)


#
    @commands.Cog.listener('on_button_click')
    async def ticket_delete_button_click(self, interaction):
        if interaction.guild.id in self.bot.ticket_tool_guild_ids:
            if interaction.component.id==f'ticketclose-{interaction.author.id}':
                confirm=await Utils.confirm(self.bot, description='Are you sure you want to close this ticket?', interaction=interaction)
                if not confirm:
                    return
                await self.bot.db.execute('DELETE FROM running_tickets WHERE author_id=$1', interaction.author.id)
                self.bot.running_tickets[interaction.guild.id].remove(interaction.author.id)
                await interaction.channel.delete()
            elif interaction.component.id.startswith('ticketclose'):
                runner_id=await self.bot.db.fetchrow('SELECT author_id FROM running_tickets WHERE channel_id=$1', interaction.channel.id)
                await self.bot.db.execute('DELETE FROM running_tickets WHERE channel_id=$1', interaction.channel.id)
                self.bot.running_tickets[interaction.guild.id].remove(runner_id[0])
                await interaction.channel.delete()



    @commands.Cog.listener('on_guild_remove')
    async def ticket_list_clear_guild_remove(self, guild):
        if guild.id in self.bot.ticket_tool_guild_ids:
            await self.bot.db.execute('DELETE FROM running_tickets WHERE guild_id=$1', guild.id)
            await self.bot.db.execute('DELETE FROM ticket_tool WHERE guild_id=$1', guild.id)
            del self.bot.running_tickets[guild.id]
            self.bot.ticket_tool_guild_ids.remove(guild.id)



    
