import discord
from discord.ext import commands
import asyncio

class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

#addrole command
    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx, role: discord.Role, user: discord.Member):
      await user.add_roles(role)
      await ctx.send(f"I have given {role} role to {user}")

    @addrole.error
    async def addrole_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.MissingPermissions):
          m = await ctx.send(f"{ctx.author.mention} looks like You don't have permissions to use this command. Please contact {ctx.guild.name} administrators")
          await asyncio.sleep(4)
          await m.delete()
        if isinstance(error, commands.MissingRequiredArgument):
          await ctx.send(f"{ctx.author.mention} please fill all the required arguments for this command. g!addrole [role][member]")

#removerole command
    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.has_permissions(manage_roles=True)
    async def removerole(self, ctx, role: discord.Role, user: discord.Member):
      await user.remove_roles(role)
      await ctx.send(f"I have removed {role} role from {user}")

    @removerole.error
    async def removerole_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.MissingPermissions):
          m = await ctx.send(f"{ctx.author.mention} looks like You don't have permissions to use this command. Please contact {ctx.guild.name} administrators")
          await asyncio.sleep(3)
          await m.delete()
        if isinstance(error, commands.MissingRequiredArgument):
          await ctx.send(f"{ctx.author.mention} please fill all the required arguments for this command. g!removerole [role] [member]")

#clear command
    @commands.command(aliases=["purge"])
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=20):
        if amount > 1000:
            em = discord.Embed(description="<:error:867269410644557834> You are being rate limited. Maximum limit is `1000`.", color=ctx.author.color)
            await ctx.send(embed=em)
        else:
            await ctx.channel.purge(limit=amount)
            m = await ctx.send(f'Deleted `{amount}` messages in {ctx.channel.mention}')
            await asyncio.sleep(3)
            await m.delete()

    @clear.error
    async def clear_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.MissingPermissions):
          m = await ctx.send(f"{ctx.author.mention} looks like You don't have permission to use this command. Please contact {ctx.guild.name} administrators")
          await asyncio.sleep(4)
          await m.delete()

#kick command
    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.guild)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
      await member.kick(reason=reason)
      await ctx.send(f'Member {member.name} has been kicked form {ctx.guild.name}')

    @kick.error
    async def kick_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.MissingPermissions):
          m = await ctx.send(f"{ctx.author.mention} You need kick members permission to use this command. Please contact {ctx.guild.name} administrators")
          await asyncio.sleep(4)
          await m.delete() 
        if isinstance(error, commands.MissingRequiredArgument):
          await ctx.send(f"{ctx.author.mention} Please specify the user you want to kick")


#ban command
    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.guild)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
      await member.ban(reason=reason)
      await ctx.reply(f'{member.mention} has been banned from {ctx.guild.name}')

    @ban.error
    async def ban_error(self, ctx, error):
      print(error)
      if isinstance(error, commands.MissingPermissions):
        m = await ctx.send(f"{ctx.author.mention} You need ban members permission to use this command. Please contact {ctx.guild.name} administrators")
        await asyncio.sleep(4)
        await m.delete()
      if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"{ctx.author.mention} Please specify the user you want to ban")

#unban command
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')


        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Successfully unbanned {user.mention}')
                return
    @unban.error
    async def unban_error(self, ctx, error):
      print(error)
      if isinstance(error, commands.MissingPermissions):
        m = await ctx.send(f"{ctx.author.mention} you do not have permission to use this command. Please contact {ctx.guild.name} administrators")
        await asyncio.sleep(4)
        await m.delete()
      if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"{ctx.author.mention} please specify the user you want to unban")

#announcement command
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def announce(self, ctx, channel: discord.TextChannel, *, msg):
      embed=discord.Embed(description=f"This is an announcement from moderator {ctx.author.name}", color=ctx.author.color)
      embed.set_author(name=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon_url}")
      embed.add_field(name="Announcement:", value=f"{msg}", inline=False)
      m = await channel.send(embed=embed)
      await ctx.message.add_reaction('✅')
      embed=discord.Embed(description=f"Announcement sent in [{channel.mention}] [Jump to announcement]({m.jump_url})", color=ctx.author.color)
      await ctx.send(embed=embed)

    @announce.error
    async def announce_error(self, ctx, error):
      if isinstance(error, commands.MissingPermissions):
        m = await ctx.send(f"{ctx.author.mention} you do not have permission to use this command. Please contact {ctx.guild.name} administrators")
        await asyncio.sleep(4)
        await m.delete()
      if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"{ctx.author.mention} please fill the required arguments for this command. g!announce [channel] [message]")




def setup(client):
    client.add_cog(moderation(client))
