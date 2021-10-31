import discord
from discord.ext import commands 
import os
import sys
import importlib
import asyncio
import subprocess


class Admin(commands.Cog):
    def __init__(self, client):
        self.client=client



    async def run_process(self, command):
        try:
            process = await asyncio.create_subprocess_shell(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result = await process.communicate()
        except NotImplementedError:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result = await self.bot.loop.run_in_executor(None, process.communicate)

        return [output.decode() for output in result]


    @commands.command(aliases=["delm"])
    @commands.is_owner()
    async def delete_message(ctx, mid=None):
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
    async def restart(ctx):
        def restart_program():
            python = sys.executable
            os.execl(python, python, * sys.argv)
        em = discord.Embed(description="<:success:893501515107557466> Restarting... Allow up to 20 seconds", color=0x2F3136)
        message = await ctx.send(embed=em)

        restart_program()

    @restart.command(name='all')
    async def _reload_all(self, ctx):

        async with ctx.typing():
            stdout, stderr = await self.run_process('git pull')

        # progress and stuff is redirected to stderr in git pull
        # however, things like "fast forward" and files
        # along with the text "already up-to-date" are in stdout

        if stdout.startswith('Already up-to-date.'):
            return await ctx.send(stdout)

        modules = self.find_modules_from_git(stdout)
        mods_text = '\n'.join(f'{index}. `{module}`' for index, (_, module) in enumerate(modules, start=1))

        statuses = []
        for is_submodule, module in modules:
            if is_submodule:
                try:
                    actual_module = sys.modules[module]
                except KeyError:
                    statuses.append((ctx.tick(None), module))
                else:
                    try:
                        importlib.reload(actual_module)
                    except Exception as e:
                        statuses.append((ctx.tick(False), module))
                    else:
                        statuses.append((ctx.tick(True), module))
            else:
                try:
                    self.reload_or_load_extension(module)
                except commands.ExtensionError:
                    statuses.append((ctx.tick(False), module))
                else:
                    statuses.append((ctx.tick(True), module))

        await ctx.send('\n'.join(f'{status}: `{module}`' for status, module in statuses))


def setup(client):
    client.add_cog(Admin(client))