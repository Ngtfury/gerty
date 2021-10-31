import discord 
from discord.ext import commands 
import datetime
import time


class Misc(commands.Cog):
    def __init__(self, client):
        self.client=client


    @commands.command()
    async def uptime(self, ctx):
        uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
        em = discord.Embed(description=f"⏱️ {uptime}, Last restart <t:{int(lastrestart)}:R>", color=0x2F3136)
        await ctx.send(embed=em)

    @commands.command(aliases=['ms', 'latency'])
    async def ping(self, ctx):
        t_1 = time.perf_counter()
        await ctx.trigger_typing()
        t_2 = time.perf_counter()
        m_1 = time.perf_counter()
        mainmessage = await ctx.send("> Pinging <a:cursor:893391878614056991>")
        m_2 = time.perf_counter()
        mtime_delta = round((m_2-m_1)*1000)
        time_delta = round((t_2-t_1)*1000)
        dbt_1 = time.perf_counter()
        await self.client.db.execute("SELECT 1")
        dbt_2 = time.perf_counter()
        dbtime_delta = round((dbt_2-dbt_1)*1000)
        em = discord.Embed(color=0x2F3136)
        em.add_field(name="<a:typing:597589448607399949> | Typing", value=f"```{time_delta} ms```", inline=False)
        em.add_field(name="<a:discord:886308080260894751> | Api latency", value=f"```{round(self.client.latency * 1000)} ms```", inline=False)
        em.add_field(name="<:postgres:892392238825488514> | Database", value=f"```{dbtime_delta} ms```", inline=False)
        em.add_field(name="📝 | Message", value=f"```{mtime_delta} ms```", inline=False)
        await mainmessage.edit(embed=em)




def setup(client):
    client.add_cog(Misc(client))