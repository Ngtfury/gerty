import discord
from discord.ext import commands 
import os
import sys
import importlib
from discord.ext.commands import bot
import io
import typing
import textwrap
import traceback
import io
import os
import re
import sys
import copy
import time
import subprocess
import asyncio
import subprocess
import re
import datetime
from contextlib import redirect_stdout

from cogs.utils import Utils


class Admin(commands.Cog):
    def __init__(self, client):
        self.client=client
        self.bot = client
        self._last_result = None

    @commands.command(brief='admin', description='Deletes a message sent by the bot', usage='[message]', aliases=["delm"])
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


    @commands.command(brief='admin', description='Restarts the bot', aliases=["reboot", "reloadall", "rall", "fuckoff"])
    @commands.is_owner()
    async def restart(self, ctx):
        def restart_program():
            python = sys.executable
            os.execl(python, python, * sys.argv)
        em = discord.Embed(description="<:success:893501515107557466> Restarting... Allow up to 20 seconds", color=0x2F3136)
        message = await ctx.send(embed=em)

        restart_program()


    @commands.command(brief='admin', description='Cleans message sent by the bot', usage='(limit)')
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
            

    @commands.command(brief='admin', description='Syncs code from github')
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
                                embed=Utils.BotEmbed.success(f'Reloaded {str(event.values[0])} successfully')
                                await event.respond(type=4, embed=embed, ephemeral=False)
                            except Exception as error:
                                traceback_string = "".join(traceback.format_exception(exc=None, value=error, tb=error.__traceback__))
                                await event.respond(type=4, ephemeral=False, file=discord.File(io.StringIO(traceback_string), filename='traceback.py'))

                    elif isinstance(event.component, Button):
                        if event.component.id=='rall':
                            await event.respond(type=6)
                            disableMessage=await main_message.channel.fetch_message(main_message.id)
                            await disableMessage.disable_components()
                            self.restart_program()
                            break
                except asyncio.TimeoutError:
                    disableMessage=await main_message.channel.fetch_message(main_message.id)
                    await disableMessage.disable_components()
                    break

    @commands.command(brief='admin', description='Blacklists/Bot bans a user', usage='[user] [reason]', aliases=['bl', 'botban'])
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

    @commands.command(brief='admin', description='Unblacklists/Bot unbans a user', usage='[user]', aliases=['unbl', 'botunban'])
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


    @commands.command(brief='admin', description='Evals the code given', usage='[code]', pass_context=True, hidden=True, name='eval')
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

    @commands.command(brief='admin', description='Add your bot to support server!! (only works on support server)', usage='[Bot ID] [Reason]', name='addbot')
    async def add_bot(self, ctx, bot: discord.User, *, reason:str):
        if not ctx.guild.id == 902948871267815454:
            return

        if not bot.bot:
            await ctx.send(
                embed = Utils.BotEmbed.error('That is a user not a bot, Invite them to this server lmao')
            )
            return

        MainMessage = await ctx.send(
            """By adding your bot to this server, you confirm that you **agree** to the rules of this server""",
            components = [[
                Button(style=ButtonStyle.green, label='I agree', id='AgreeAddBot'),
                Button(label='Cancel', id='CancelAddBot')
            ]]
        )
        while True:
            event = await self.bot.wait_for('button_click', check=lambda i: i.author == ctx.author and i.channel == ctx.channel and i.message.id == MainMessage.id)
            if event.component.id == 'AgreeAddBot':
                await event.respond(type=6)
                await MainMessage.delete()
                await ctx.send('Your bot has been requested to the moderators, I will send you a DM when it gets added.')
                break
            elif event.component.id == 'CancelAddBot':
                await event.respond(type=6)
                await MainMessage.delete()
                await ctx.send('You cancelled adding your bot to this server.')
                return

        em = discord.Embed(
            color = Utils.BotColors.invis(),
            description= f"""**Bot ID**: {bot.id}
            **Bot**: {bot}/{bot.mention}
            **Owner**: {ctx.author}/{ctx.author.mention}
            **Case ID**: {ctx.author.id}
            
            [*Jump to request*]({ctx.message.jump_url})
            [*Invite this bot here!*]({discord.utils.oauth_url(bot.id)})""",
            title='New bot submission',
            timestamp=datetime.datetime.now()
        )
        em.add_field(name='Reason', inline=False, value=reason)
        em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        em.set_footer(text='Requested')

        channel_ = self.bot.get_channel(922736416956506153)
        await channel_.send('<@&922150348871856158>', embed=em)

    @commands.command(brief='admin', description='Accepts bot submittions (admin only)', usage = '[Case ID]', name='acceptbot')
    @commands.has_any_role(922151186386288671, 922150348871856158, 922150939702493204)
    async def accept_bot(self, ctx, owner: typing.Union[discord.User, discord.Member], bot: typing.Union[discord.User, discord.Member]):
        if not ctx.guild.id == 902948871267815454:
            return

        await owner.send(
            f"""Your bot, {bot.mention}, has been added to Gerty HQ"""
        )
        await ctx.message.add_reaction(Utils.BotEmojis.success())
        return





def setup(client):
    client.add_cog(Admin(client))