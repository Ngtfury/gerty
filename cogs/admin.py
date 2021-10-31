import discord
from discord.ext import commands 
import os
import sys
import importlib
import asyncio
import subprocess
import re


class Admin(commands.Cog):
    def __init__(self, client):
        self.client=client



    @commands.command(aliases=["delm"])
    @commands.is_owner()
    async def delete_message(self, ctx, mid=None):
        if mid == None:
            if ctx.message.reference:
                mid = ctx.message.reference.resolved.id
            else:
                await ctx.send("Please specify a message to delete")
        d = ctx.channel.get_partial_message(mid)
        try:
            await d.delete()
            await ctx.message.add_reaction("<:success:893501515107557466>")
        except:
            await ctx.message.add_reaction("<:error:867269410644557834>")


    @commands.group(aliases=["reboot", "reloadall", "rall", "fuckoff"], invoke_without_command=True)
    @commands.is_owner()
    async def restart(self, ctx):
        def restart_program():
            python = sys.executable
            os.execl(python, python, * sys.argv)
        em = discord.Embed(description="<:success:893501515107557466> Restarting... Allow up to 20 seconds", color=0x2F3136)
        message = await ctx.send(embed=em)

        restart_program()


    @commands.command()
    @commands.is_owner()
    async def cleanup(self, ctx, limit:int=10):
        try:
            deleted=await ctx.channel.purge(limit=limit, check=lambda i: i.author==self.client.user)
        except:
            deleted=await ctx.channel.purge(limit=limit, check=lambda i: i.author==self.client.user, bulk=False)
        await ctx.send(f"<:success:893501515107557466> Deleted **{len(deleted)}** messages", delete_after=5)


    async def run_process(self, command):
        try:
            process = await asyncio.create_subprocess_shell(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result = await process.communicate()
        except NotImplementedError:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result = await self.bot.loop.run_in_executor(None, process.communicate)

        return [output.decode() for output in result]

    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx):
        runner=await self.run_process('git pull')
        runner_next_line='\n'.join(runner)
        await ctx.send(f'```{runner_next_line}```')

def setup(client):
    client.add_cog(Admin(client))