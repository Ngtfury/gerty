import discord
from discord.ext import commands
import time


class modlogs(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def modping(self, ctx):
        dbt_1 = time.perf_counter()
        await self.db.execute("SELECT 1")
        dbt_2 = time.perf_counter()
        dbtime_delta = round((dbt_2-dbt_1)*1000)
        await ctx.send(f"Done in {dbtime_delta} ms")





def setup(client):
    client.add_cog(modlogs(client))