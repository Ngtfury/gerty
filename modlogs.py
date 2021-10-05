from datetime import datetime
import discord
from discord.ext import commands
import time
import asyncpg


def setup(client):
    client.add_cog(modlogs(client))

class modlogs(commands.Cog):
    def __init__(self, client):
        self.client = client

    
    @commands.command()
    async def modping(self, ctx):
        dbt_1 = time.perf_counter()
        await self.client.db.execute("SELECT 1")
        dbt_2 = time.perf_counter()
        dbtime_delta = round((dbt_2-dbt_1)*1000)
        await ctx.send(f"Done in {dbtime_delta} ms")


    @commands.group(invoke_without_command=True)
    async def modlog(self, ctx):
        await ctx.send("Hm")

    @modlog.command()
    async def channel(self, ctx, channel: discord.TextChannel):
        try:
            g = await channel.send(".")
            await g.delete()
        except:
            await ctx.send(f"I cannot send message to {channel.mention}")
        else:
            result = await self.client.db.fetchrow("SELECT channel_id FROM mod_logs WHERE guild_id = $1", ctx.guild.id)
            if not result:
                await self.client.db.execute("INSERT INTO mod_logs (guild_id, channel_id) VALUES ($1,$2)", ctx.guild.id, channel.id)
                em = discord.Embed(description=f"<:success:893501515107557466> Mod logs channel **set** to {channel.mention}", color=0x2F3136)
                await ctx.send(embed=em)
            else:
                await self.client.db.execute("UPDATE mod_logs SET channel_id = $1 WHERE guild_id = $2", channel.id, ctx.guild.id)
                em = discord.Embed(description=f"<:success:893501515107557466> Mod logs channel **updated** to {channel.mention}", color=0x2F3136)
                await ctx.send(embed=em)
    
    @modlog.command()
    async def delete(self, ctx):
        result = await self.client.db.fetchrow("SELECT channel_id FROM mod_logs WHERE guild_id = $1", ctx.guild.id)
        if result:
            await self.db.execute("DELETE FROM mod_logs WHERE guild_id = $1", ctx.guild.id)
            em = discord.Embed(description=f"<:success:893501515107557466> Successfully **deleted** mod logs data for this server", color=0x2F3136)
            await ctx.send(embed=em)
        else:
            em = discord.Embed(description=f"<:success:893501515107557466> There is no mod logs channel for this server in my database to delete", color=0x2F3136)
            await ctx.send(embed=em)


    @commands.Cog.listener()
    async def on_message_delete(self, message):
        result = await self.client.db.fetchrow("SELECT channel_id FROM mod_logs WHERE guild_id = $1", message.guild.id)
        if result:
            em = discord.Embed(color=0x2F3136)
            em.set_author(name=f"{message.author}", icon_url=f"{message.author.avatar_url}")
            em.add_field(name=f"Message deleted in #{message.channel.name}", value=f"{message.content}")
            channel = self.client.get_channel(result[0])
            await channel.send(embed=em)

        

