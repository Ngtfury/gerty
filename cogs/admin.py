import discord
from discord.ext import commands 
import os
import sys
import importlib
import discord_components
import io
import textwrap
import traceback
import io
import os
import re
import sys
import copy
import time
import subprocess
from discord_components import *
import asyncio
import subprocess
import re
import datetime
from contextlib import redirect_stdout


class Admin(commands.Cog):
    def __init__(self, client):
        self.client=client
        self._last_result = None

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
            result = await self.client.loop.run_in_executor(None, process.communicate)

        return [output.decode() for output in result]


    def restart_program(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)

    def load_or_reload(self, ext):
        try:
            self.client.reload_extension(ext)
        except commands.ExtensionNotLoaded:
            self.client.load_extension(ext)
            

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
        if runner_next_line.startswith('Already up to date.'):
            return
        else:
            options=[]
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    options.append(SelectOption(label=f'{filename[:-3]}', value=f'{filename[:-3]}'))
            compo=[Select(placeholder='Reload extentions one by one', options=options), Button(style=ButtonStyle.gray, label='Restart', id='rall')]
            await asyncio.sleep(1)
            em3=discord.Embed(title='Git sync', description=f'```shell\n$ git pull\n\n{runner_next_line}\n[status] Return code 0```', color=0x2F3136, timestamp=datetime.datetime.now())
            em3.set_footer(text='Sync done at')
            await main_message.edit(embed=em3, components=compo)
            while True:
                try:
                    event=await self.client.wait_for('interaction', check=lambda i: i.channel==ctx.channel and i.author==ctx.author, timeout=10)
                    if isinstance(event.component, Select):
                        if event.values[0]:
                            try:
                                self.load_or_reload(f'cogs.{str(event.values[0])}')
                                loaded_or_not=f'<:success:893501515107557466> Reloaded {str(event.values[0])} successfully'
                            except:
                                loaded_or_not=f'<:error:893501396161290320> Coudn\'t load {str(event.values[0])}'
                            nicmbed=discord.Embed(description=loaded_or_not, color=0x2F3136)
                            await event.respond(type=4, embed=nicmbed, ephemeral=False)
                    elif isinstance(event.component, Button):
                        if event.component.id=='rall':
                            await event.respond(type=7, components=[Select(placeholder='Reload extentions one by one', disabled=True, options=[SelectOption(label='ok', value='ok')]), Button(style=ButtonStyle.green, label='Restart', id='rall', disabled=True)])
                            self.restart_program()
                            break
                except asyncio.TimeoutError:
                    #
                    #kwbgkwrkgrb
                    await main_message.edit(components=[Select(placeholder='Reload extentions one by one', disabled=True, options=[SelectOption(label='ok', value='ok')]), Button(style=ButtonStyle.gray, label='Restart', id='rall', disabled=True)])
                    break

    @commands.command()
    @commands.is_owner()
    async def blacklist(self, ctx, user: discord.Member, *, reason):
        if user==ctx.author:
            return await ctx.send('You cannot blacklist yourself')
    
        already=await self.client.db.fetch('SELECT * FROM blacklisted WHERE user_id=$1', user.id)
        if already:
            return await ctx.send('That user is already blacklisted')

        await self.client.db.execute('INSERT INTO blacklisted (user_id,reason) VALUES ($1,$2)', user.id, reason)
        em=discord.Embed(description=f'<:success:893501515107557466> **Blacklisted {user.name} for {reason}**', color=0x2F3136)
        await ctx.send(embed=em)

    @commands.command()
    async def unblacklist(self, ctx, user: discord.Member):
        results=await self.client.db.fetch('SELECT * FROM blacklisted WHERE user_id=$1', user.id)
        if not results:
            return await ctx.send('That user is not blacklisted')

        await self.client.db.execute('DELETE FROM blacklisted WHERE user_id=$1', user.id)
        em=discord.Embed(description=f'<:success:893501515107557466> **Unblacklisted {user.name}**', color=0x2F3136)
        await ctx.send(embed=em)

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')


    @commands.command(pass_context=True, hidden=True, name='eval')
    @commands.is_owner()
    async def _eval(self, ctx, *, body: str):
        """Evaluates a code"""

        env = {
            'bot': self.client,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')


def setup(client):
    client.add_cog(Admin(client))