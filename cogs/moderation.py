import typing
import discord
from discord.ext import commands
import asyncio
import json
from cogs.utils import Utils

class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client



#addrole command
    @commands.command(brief='mod', description='Add roles to a user', usage='[role] [user]')
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx, role: discord.Role, user: discord.Member):
        if user.top_role >= role and not ctx.author == ctx.guild.owner:
            em = Utils.BotEmbed.error('You are not high enough in the role hierarchy to add role for that member')
            await ctx.send(embed=em)
        else:
            await user.add_roles(role)
            await ctx.send(embed=Utils.BotEmbed.success(f'I\'ve added {role.mention} to {user.mention}'))



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
    @commands.bot_has_guild_permissions(kick_members=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        if member.top_role >= ctx.author.top_role and not ctx.author == ctx.guild.owner:
            await ctx.send(embed=Utils.BotEmbed.error('You are not high enough in the role hierarchy to kick that member'))
        else:
            await member.kick(reason=reason)
            await ctx.send(
                embed = Utils.BotEmbed.success(f'_**Kicked {member} successfully**_')
            )


#ban command
    @commands.command(brief='mod', description='Bans a member from the server', usage='[member] (reason)')
    @commands.cooldown(1,10,commands.BucketType.guild)
    @commands.bot_has_guild_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        if member.top_role >= ctx.author.top_role and not ctx.author == ctx.guild.owner:
            await ctx.send(
                embed = Utils.BotEmbed.error('You are not high enough in the role hierarchy to ban that member')
            )
        else:
            await member.ban(reason=reason)
            await ctx.send(
                embed = Utils.BotEmbed.success(f'_**Banned {member} successfully**_')
            )


#unban command
    @commands.command(brief='mod', description='Unbans a user', usage='[user] (reason)')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member: typing.Union[discord.User, discord.Member], reason=None):
        await member.unban(reason=reason)
        await ctx.send(
            embed = Utils.BotEmbed.success(f'_**Unbanned {member} successfully**_')
        )




def setup(client):
    client.add_cog(moderation(client))
