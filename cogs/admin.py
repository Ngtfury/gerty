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


def setup(client):
    client.add_cog(Admin(client))