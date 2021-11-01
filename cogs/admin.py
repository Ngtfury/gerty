import discord
from discord.ext import commands 
import os
import sys
import importlib
import discord_components
from discord_components import *
import asyncio
import subprocess
import re
import datetime

from discord_components import component


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


    def restart_program(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)

    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx):
        em=discord.Embed(title='Git sync', description='```shell\n$ git pull```', color=0x2F3136)
        main_message=await ctx.send(embed=em)
        await ctx.message.add_reaction('<:arrow:885193320068968508>')
        await asyncio.sleep(0.5)
        runner=await self.run_process('git pull')
        runner_next_line='\n'.join(runner)
        em2=discord.Embed(title='Git sync', description=f'```shell\n$ git pull\n\n{runner_next_line}```', color=0x2F3136)
        await main_message.edit(embed=em2)
        await ctx.message.add_reaction('<:success:893501515107557466>')

        compo=[Button(style=ButtonStyle.gray, label='Restart', id='rall')]

        if runner_next_line.startswith('Already up to date.'):
            return
        else:
            await asyncio.sleep(1)
            em3=discord.Embed(title='Git sync', description=f'```shell\n$ git pull\n\n{runner_next_line}\n[status] Return code 0```', color=0x2F3136, timestamp=datetime.datetime.now())
            em3.set_footer(text='Sync done at')
            to_disable=await main_message.edit(embed=em3, components=compo)
            while True:
                event=await self.client.wait_for('button_click', check=lambda i: i.component.id in ['rall'] and i.channel==ctx.channel and i.author==ctx.author)
                if event.component.id=='rall':
                    await to_disable.disable_components()
                    self.restart_program()
                    break


def setup(client):
    client.add_cog(Admin(client))