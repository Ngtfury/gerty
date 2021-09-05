import discord
from discord.ext import commands


class dyayoutube(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def hell(self, ctx):
        await ctx.send("Hello vero")



def setup(client):
    client.add_cog(dyayoutube(client))