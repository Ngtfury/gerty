import discord
import asyncio
from discord.ext import commands



class members(commands.Cog):
    def __init__(self, bot):
        self.client = bot


    @commands.command()
    async def members(self, ctx):

        embed = discord.Embed(title=f"There are {len(ctx.guild.members)} members in {ctx.guild.name}!", colour=0xffff00, timestamp=ctx.message.created_at)
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(members(client))