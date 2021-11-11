import discord
from discord.ext import commands
import asyncio
import json

class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client



#addrole command
    @commands.command(brief='mod', description='Add roles to a user', usage='[role] [user]')
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx, role: discord.Role, user: discord.Member):
        if user.top_role >= role and not ctx.author == ctx.guild.owner:
            em = discord.Embed(description="<:error:867269410644557834> You are not high enough in the role hierarchy to add role for that member", color=0x2F3136)
            await ctx.send(embed=em)
        else:
            await user.add_roles(role)
            await ctx.send(f"I have given {role} role to {user}")



#removerole command
    @commands.command(brief='mod', description='Removes roles from a user', usage='[role] [user]')
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.has_permissions(manage_roles=True)
    async def removerole(self, ctx, role: discord.Role, user: discord.Member):
        if user.top_role >= role and not ctx.author == ctx.guild.owner:
            em = discord.Embed(description="<:error:867269410644557834> You are not high enough in the role hierarchy to remove role for that member", color=0x2F3136)
            await ctx.send(embed=em)
        else:
            await user.remove_roles(role)
            await ctx.send(f"I have removed {role} role from {user}")



#clear command
    @commands.command(brief='mod', description='Purges messages in channel', usage='[amount]', aliases=["purge"])
    @commands.cooldown(1,10,commands.BucketType.user)
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



#kick command
    @commands.command(brief='mod', description='Kicks a user from the server', usage='[member] (reason)')
    @commands.cooldown(1,10,commands.BucketType.guild)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        if member.top_role >= ctx.author.top_role and not ctx.author == ctx.guild.owner:
            em = discord.Embed(description="<:error:867269410644557834> You are not high enough in the role hierarchy to kick that member", color=0x2F3136)
            await ctx.send(embed=em)
        else:
            await member.kick(reason=reason)
            if reason == None:
                em = discord.Embed(description=f"<:succes:867385889059504128> **_{member.name} is kicked from {ctx.guild.name}_**", color=0x2F3136)
            else:
                em = discord.Embed(description=f"<:succes:867385889059504128> **_{member.name} is kicked from {ctx.guild.name} for reason: {reason}_**", color=0x2F3136)
            await ctx.send(embed=em)


#ban command
    @commands.command(brief='mod', description='Bans a member from the server', usage='[member] (reason)')
    @commands.cooldown(1,10,commands.BucketType.guild)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        if member.top_role >= ctx.author.top_role and not ctx.author == ctx.guild.owner:
            em = discord.Embed(description="<:error:867269410644557834> You are not high enough in the role hierarchy to ban that member", color=0x2F3136)
            await ctx.send(embed=em)
        else:
            await member.ban(reason=reason)
            if reason == None:
                em = discord.Embed(description=f"<:succes:867385889059504128> **_{member.name} is banned from {ctx.guild.name}_**", color=0x2F3136)
            else:
                em = discord.Embed(description=f"<:succes:867385889059504128> **_{member.name} is banned from {ctx.guild.name} for reason: {reason}_**", color=0x2F3136)
            await ctx.send(embed=em)


#unban command
    @commands.command(brief='mod', description='Unbans a user', usage='[user]')
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


#announcement command
    @commands.command(brief='mod', description='Announces something to a channel', usage='[channel] [message]')
    @commands.has_permissions(manage_channels=True)
    async def announce(self, ctx, channel: discord.TextChannel, *, msg):
      embed=discord.Embed(description=f"This is an announcement from moderator {ctx.author.name}", color=ctx.author.color)
      embed.set_author(name=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon_url}")
      embed.add_field(name="Announcement:", value=f"{msg}", inline=False)
      m = await channel.send(embed=embed)
      await ctx.message.add_reaction('✅')
      embed=discord.Embed(description=f"Announcement sent in [{channel.mention}] [Jump to announcement]({m.jump_url})", color=ctx.author.color)
      await ctx.send(embed=embed)



def setup(client):
    client.add_cog(moderation(client))
