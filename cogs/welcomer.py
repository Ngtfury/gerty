from re import A
import discord
from discord.ext import commands
from cogs.utils import Utils



def setup(bot):
    bot.add_cog(WelcomerCog(bot))

class WelcomerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def isGuildAlready(self, guild):
        _is_already = await self.bot.db.fetchrow('SELECT * FROM welcomer WHERE guild_id = $1', guild.id)
        if _is_already:
            return True
        return False

    async def isAutoRoles(self, guild):
        row = await self.bot.db.fetchrow('SELECT auto_roles FROM welcomer WHERE guild_id = $1', guild.id)
        _is_already = row[0]
        if _is_already:
            return True
        return False


    async def isChannelAlready(self, channel):
        _is_already = await self.bot.db.fetchrow('SELECT * FROM welcomer WHERE channel_id = $1', channel.id)
        if _is_already:
            return True
        return False

    async def GetAutoRoles(self, guild):
        row = await self.bot.db.fetchrow('SELECT auto_roles FROM welcomer WHERE guild_id = $1', guild.id)
        _is_already = row[0]
        if not _is_already:
            return []
        return _is_already

    async def set_welcomer_channel(self, ctx, channel):
        if await self.isChannelAlready(channel):
            await self.bot.db.execute(
                """UPDATE welcomer SET channel_id = $1 WHERE guild_id = $2""",
                channel.id,
                ctx.guild.id
            )

            await ctx.send(
                embed = Utils.BotEmbed.success(f'Successfully updated welcomer channel to {channel.mention}')
            )
            return
        
        await self.bot.db.execute(
            """INSERT INTO welcomer (channel_id,guild_id,message) VALUES ($1,$2,$3)""",
            channel.id,
            ctx.guild.id,
            "Hello, welcome {user_mention} to {server_name} you are {member_count}th member of our server."
        )

        await ctx.send(
            embed = Utils.BotEmbed.success(f'Successfully set {channel.mention} as welcomer channel')
        )
        return

    @commands.group(brief='welcomer', aliases=['welcome'], invoke_without_command=True, usage='[sub command]', description='Welcomer module, welcome new users')
    @commands.has_permissions(manage_channels=True)
    async def welcomer(self, ctx):
        if not await self.isGuildAlready(ctx.guild):
            await ctx.send(
                embed = Utils.BotEmbed.error("This server does not have welcomer setup")
            )
            return

        row = await self.bot.db.fetchrow('SELECT * FROM welcomer WHERE guild_id = $1', ctx.guild.id)
        channel_obj = self.bot.get_channel(row[1])

        welcomer_roles = await self.GetAutoRoles(ctx.guild)

        em = discord.Embed(color=Utils.BotColors.invis())
        em.add_field(name='Channel', value=f'{channel_obj.mention}')
        em.set_author(name=ctx.guild.name, icon_url=str(ctx.guild.icon.url))
        em.add_field(name='Message', value=row[2], inline=False)
        if welcomer_roles:
            role_objs = []
            for role_id in welcomer_roles:
                role_objs.append(ctx.guild.get_role(role_id))
            em.add_field(name='Autoroles', value=', '.join([role.mention for role in role_objs]), inline=False)
        em.set_footer(text=f'Invoked by {ctx.author}', icon_url=ctx.author.avatar.url)
        await ctx.send(embed=em)



    @welcomer.command(aliases=['channel', 'channelset', 'setchannel'], usage='(channel)', name='set-channel', description='Set welcomer channel')
    async def set_channel(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel

        if not channel.permissions_for(ctx.guild.me).send_messages:
            await ctx.send(
                embed = Utils.BotEmbed.error("I don't have permissions to send messages in that channel")
            )
            return

        await self.set_welcomer_channel(ctx, channel)
        return

    @welcomer.command(aliases = ['autorole', 'auto-role', 'role', 'autoroles', 'ar', 'ar-add'], usage='[role]', description='Set welcomer autoroles, welcome new users with a role')
    async def auto_role(self, ctx, role: discord.Role):
        if not await self.isGuildAlready(ctx.guild):
            await ctx.send(
                embed = Utils.BotEmbed.error("This server does not have welcomer setup")
            )
            return

        role_list = await self.GetAutoRoles(ctx.guild)
        if len(role_list) >= 5:
            await ctx.send(
                embed = Utils.BotEmbed.error('Sorry, but maximum autoroles for this server is 5')
            )
            return

        role_list.append(role.id)
        await self.bot.db.execute(
            """UPDATE welcomer SET auto_roles = $1 WHERE guild_id = $2""",
            role_list,
            ctx.guild.id
        )

        await ctx.send(
            embed = Utils.BotEmbed.success(f"Successfully added {role.mention} in welcomer autoroles")
        )
        return

    @welcomer.command(aliases=['autorole-remove', 'ar-remove', 'autorolesremove'], description='Remove a role form autorole list', usage='[role]')
    async def auto_role_remove(self, ctx, role: discord.Role):
        if not await self.isGuildAlready(ctx.guild):
            await ctx.send(
                embed = Utils.BotEmbed.error("This server does not have welcomer setup")
            )
            return

        role_list = await self.GetAutoRoles(ctx.guild)
        if not role_list:
            await ctx.send(
                embed = Utils.BotEmbed.error('There is no welcomer autoroles setup for this server')
            )
            return

        if not role.id in role_list:
            await ctx.send(
                embed = Utils.BotEmbed.error(f'{role.mention} is not in the welcomer autorole list')
            )
            return

        role_list.remove(role.id)
        await self.bot.db.execute(
            """UPDATE welcomer SET auto_roles = $1 WHERE guild_id = $2""",
            role_list,
            ctx.guild.id
        )
        await ctx.send(
            embed = Utils.BotEmbed.success(f'Removed {role.mention} from welcomer autorole list')
        )
        return

        

    @welcomer.command(aliases=['setmessage', 'message', 'messageset'], usage='[message]', name='set-message', description='Set welcomer message, welcome new users with a message')
    async def set_message(self, ctx, *, message:str):
        if not await self.isGuildAlready(ctx.guild):
            await ctx.send(
                embed = Utils.BotEmbed.error("This server does not have welcomer setup")
            )
            return

        await self.bot.db.execute(
            """UPDATE welcomer SET message = $1 WHERE guild_id = $2""",
            message,
            ctx.guild.id
        )

        await ctx.send(
            embed = Utils.BotEmbed.success("Successfully updated welcomer message for this server")
        )
        return

    @welcomer.command(aliases=['del', 'deldata', 'deletedata'], name='delete', description='Delete all welcomer data')
    async def delete_data(self, ctx):
        if not await self.isGuildAlready(ctx.guild):
            await ctx.send(
                embed = Utils.BotEmbed.error("This server does not have welcomer setup")
            )
            return

        await self.bot.db.execute(
            """DELETE FROM welcomer WHERE guild_id = $1""",
            ctx.guild.id
        )

        await ctx.send(
            embed = Utils.BotEmbed.success("Successfully deleted welcomer data of this server")
        )
        return

    @welcomer.command(aliases=['var'], description='See welcomer message variables')
    async def variables(self, ctx):
        em = discord.Embed(
            color=Utils.BotColors.invis(),
            title='Variables',
            description=f"""**These are the variables of `welcomer` module in Gerty**
            <:arrow:885193320068968508> `user_mention` - {ctx.author.mention}
            <:arrow:885193320068968508> `user_name` - {ctx.author.name}
            <:arrow:885193320068968508> `user_full_name` - {ctx.author}
            <:arrow:885193320068968508> `user_id` - {ctx.author.id}
            <:arrow:885193320068968508> `user_discrim` - {ctx.author.discriminator}
            <:arrow:885193320068968508> `server_name` - {ctx.guild.name}
            <:arrow:885193320068968508> `member_count` - {ctx.guild.member_count}"""
        )

        await ctx.send(embed=em)


    @commands.Cog.listener('on_guild_channel_delete')
    async def update_welcomer_on_channel_delete(self, channel):
        if await self.isChannelAlready(channel):
            await self.bot.db.execute(
                """DELETE FROM welcomer WHERE channel_id = $1""",
                channel.id
            )

    @commands.Cog.listener('on_guild_role_delete')
    async def update_welcomer_role_on_delete(self, role):
        if await self.isAutoRoles(role.guild):
            role_list = await self.GetAutoRoles(role.guild)

            if not role.id in role_list:
                return

            role_list.remove(role.id)
            await self.bot.db.execute(
                """UPDATE welcomer SET auto_roles = $1 WHERE guild_id = $2""",
                role_list,
                role.guild.id
            )


    @commands.Cog.listener('on_member_join')
    async def welcome_member(self, member):
        if await self.isGuildAlready(member.guild):
            row = await self.bot.db.fetchrow('SELECT * FROM welcomer WHERE guild_id = $1', member.guild.id)
            channel_obj = self.bot.get_channel(row[1])

            user_mention = member.mention
            user_name = member.name
            user_full_name = str(member)
            user_id = member.id
            user_discrim = member.discriminator

            server_name = member.guild.name
            member_count = member.guild.member_count


            await channel_obj.send(
                str(row[2]).format(
                    user_mention = user_mention,
                    user_name = user_name,
                    user_full_name = user_full_name,
                    user_id = user_id,
                    user_discrim = user_discrim,
                    server_name = server_name,
                    member_count = member_count
                )
            )

            if member.bot:
                return

            if await self.isAutoRoles(member.guild):
                role_list = await self.GetAutoRoles(member.guild)
                for role in role_list:
                    role_obj = member.guild.get_role(int(role))
                    try:
                        await member.add_roles(role_obj, reason='Auto roles')
                    except:
                        pass

