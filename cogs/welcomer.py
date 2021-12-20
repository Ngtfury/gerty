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

    async def isChannelAlready(self, channel):
        _is_already = await self.bot.db.fetchrow('SELECT * FROM welcomer WHERE channel_id = $1', channel.id)
        if _is_already:
            return True
        return False

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

    @commands.group(aliases=['welcome'], invoke_without_command=True, usage='[sub command]')
    @commands.is_owner()
    async def welcomer(self, ctx):
        if not await self.isGuildAlready(ctx.guild):
            await ctx.send(
                embed = Utils.BotEmbed.error("This server does not have welcomer setup")
            )
            return

        row = await self.bot.db.fetchrow('SELECT * FROM welcomer WHERE guild_id = $1', ctx.guild.id)
        channel_obj = self.bot.get_channel(row[1])

        em = discord.Embed(color=Utils.BotColors.invis())
        em.add_field(name='Channel', value=f'{channel_obj.mention}')
        em.set_author(name=ctx.guild.name, icon_url=str(ctx.guild.icon_url))
        em.add_field(name='Message', value=row[2], inline=False)
        em.set_footer(name=f'Invoked by {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)



    @welcomer.command(aliases=['channel', 'channelset', 'setchannel'], usage='(channel)')
    async def set_channel(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel

        if not channel.permissions_for(ctx.guild.me).send_messages:
            await ctx.send(
                embed = Utils.BotEmbed.error("I don't have permissions to send messages in that channel")
            )
            return

        await self.set_welcomer_channel(ctx, channel)
        return


    @welcomer.command(aliases=['setmessage', 'message', 'messageset'], usage='[message]')
    async def set_message(self, ctx, message:str):
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
