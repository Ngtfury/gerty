from random import random
import re
import discord
from discord import emoji
from discord import guild
from discord import integrations
from discord.errors import HTTPException, InvalidArgument
from discord.ext.commands.cooldowns import BucketType
from cogs.utils import Utils
from discord.ext import commands
import datetime
import io
import time
import asyncio
from math import *
import random
import typing
import aiohttp
from io import BytesIO


class WaifuView(discord.ui.View):
    def __init__(self, ctx, image_url):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.image_url = image_url

    async def create_if_not(self, user):
        _is_already = await self.ctx.bot.db.fetch('SELECT * FROM waifu WHERE user_id = $1', user.id)
        if not _is_already:
            await self.ctx.bot.db.execute('INSERT INTO waifu (user_id,url) VALUES ($1,$2)', user.id, [])
        return


    async def on_timeout(self):
        for children in self.children:
            children.disabled = True

        await self.message.edit(view = self)

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message('Only the one who use this command can interact with these buttons.', ephemeral=True)
            return False
        return True


    @discord.ui.button(
        style = discord.ButtonStyle.gray,
        emoji = '❤️'
    )
    async def add_to_gallery(self, button, interaction: discord.Interaction):
        await self.create_if_not(self.ctx.author)
        _waifus_rec = await self.ctx.bot.db.fetchrow('SELECT url FROM waifu WHERE user_id = $1', self.ctx.author.id)
        _waifus = _waifus_rec[0]
        if not self.image_url in _waifus:
            _waifus.append(self.image_url)
            await self.ctx.bot.db.execute('UPDATE waifu SET url = $1 WHERE user_id = $2', _waifus, self.ctx.author.id)
        button.disabled = True
        embed = discord.Embed(
            description=f"""I've added [**this image**]({self.image_url}) to your favorites (gallery) successfully ❤️, Use command `{Utils.clean_prefix(ctx=self.ctx)}waifu gallery` to see all your favorite images.""",
            color = Utils.BotColors.invis()
        ) #
        await interaction.response.send_message(embed = embed, ephemeral=True)
        await self.message.edit(view = self)

    @discord.ui.button(
        style = discord.ButtonStyle.red,
        emoji = '<:trashcan:890938576563503114>'
    )
    async def delete_message(self, button, interaction: discord.Interaction):
        await interaction.response.defer()
        await self.message.delete()
        await self.ctx.message.add_reaction(Utils.BotEmojis.success())
        self.stop()


class WaifuPagesView(discord.ui.View):
    def __init__(self, embeds, ctx):
        super().__init__(timeout=60)
        self.embeds = embeds
        self.ctx = ctx
        self.current = 0
        self._number_pages_awaiting = False

    async def on_timeout(self):
        for children in self.children:
            children.disabled = True

        await self.message.edit(view = self)

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message('Only the one who use this command can interact with these buttons.', ephemeral=True)
            return False
        return True

    @discord.ui.button(
        style = discord.ButtonStyle.gray,
        label = '<',
        row = 1
    )
    async def left_arrow(self, button, interaction: discord.Interaction):
        self.current -= 1
        if self.current ==  len(self.embeds):
            self.current = 0
        elif self.current < 0:
            self.current = len(self.embeds) - 1
        _embed = self.embeds[self.current]
        _embed.set_footer(text=f'Showing image {self.current+1} of {len(self.embeds)}')
        await interaction.response.edit_message(embed = _embed, view=self)


    @discord.ui.button(
        style = discord.ButtonStyle.blurple,
        emoji = '💔',
        row = 1
    )
    async def del_from_list(self, button, interaction: discord.Interaction):
        _current_embed: discord.Embed = self.embeds[self.current]
        _url = str(_current_embed.image.url)
        _waifu_row = await self.ctx.bot.db.fetchrow('SELECT url FROM waifu WHERE user_id = $1', self.ctx.author.id)
        _waifu_list = _waifu_row[0]
        _waifu_list.remove(_url)
        await self.ctx.bot.db.execute('UPDATE waifu SET url = $1 WHERE user_id = $2', _waifu_list, self.ctx.author.id)
        self.embeds.remove(_current_embed)
        em = discord.Embed(
            color = Utils.BotColors.invis(),
            description=f"""Alright, I've removed [**this image**]({_url}) from your favorites, Use command `{Utils.clean_prefix(ctx=self.ctx)}waifu gallery` to see all your favorite images."""
        )
        if self.current ==  len(self.embeds):
            self.current = 0
        elif self.current < 0:
            self.current = len(self.embeds) - 1
        await interaction.response.send_message(embed = em, ephemeral=True)
        if not self.embeds:
            await self.message.delete()
            self.stop()
            return
        _embed = self.embeds[self.current]
        _embed.set_footer(text=f'Showing image {self.current+1} of {len(self.embeds)}')
        await self.message.edit(embed = _embed)

    @discord.ui.button(
        style = discord.ButtonStyle.gray,
        label = '>',
        row = 1
    )
    async def right_arrow(self, button, interaction: discord.Interaction):
        self.current += 1
        if self.current ==  len(self.embeds):
            self.current = 0
        elif self.current < 0:
            self.current = len(self.embeds) - 1
        _embed = self.embeds[self.current]
        _embed.set_footer(text=f'Showing image {self.current+1} of {len(self.embeds)}')
        await interaction.response.edit_message(embed = _embed, view=self)


    @discord.ui.button(
        style = discord.ButtonStyle.red,
        emoji = '<:trashcan:890938576563503114>',
        row = 1
    )
    async def quit_pages(self, button, interaction: discord.Interaction):
        await interaction.response.defer()
        await self.message.delete()
        await self.ctx.message.add_reaction(Utils.BotEmojis.success())
        self.stop()

    @discord.ui.button(
        style = discord.ButtonStyle.green,
        label = 'Skip to page...',
        row = 2
    )
    async def skip_to_page(self, button, interaction: discord.Interaction):
        if self._number_pages_awaiting:
            await interaction.response.send_message('Already awaiting for your response...', ephemeral=True)
            return
    
        await interaction.response.send_message('What page do you want to go to?', ephemeral=True)
        try:
            self._number_pages_awaiting = True
            resMessage = await self.ctx.bot.wait_for('message', check = lambda i: i.author.id == interaction.user.id and i.channel.id == interaction.channel.id and i.content.isdigit(), timeout = 20)
            self._number_pages_awaiting = False
        except asyncio.TimeoutError:
            self._number_pages_awaiting = False
            await interaction.followup.send('You didn\'t respond on time...', ephemeral=True)
            return


        _content = int(resMessage.content)
        if _content <= 0:
            await interaction.followup.send(f'Pages start from 1 not {_content}.', ephemeral=True)
            return
        if _content > len(self.embeds):
            await interaction.followup.send(f'Sorry, there are only {len(self.embeds)} pages, not {_content}.', ephemeral=True)
            return

        try:
            await resMessage.delete()
        except:
            pass

        self.current = _content - 1
        _embed = self.embeds[self.current]
        _embed.set_footer(text=f'Showing image {self.current+1} of {len(self.embeds)}')
        await interaction.followup.edit_message(embed = _embed, message_id=self.message.id)


class NitroView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.ctx = ctx

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            await interaction.response.send_message('You cannot claim your gift yourself...', ephemeral=True)
            return False
        return True

    async def on_timeout(self):
        for children in self.children:
            children.disabled = True
            children.style = discord.ButtonStyle.gray
            children.label = '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ACCEPT⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀'

        embi=discord.Embed(color=Utils.BotColors.invis(), title='Nitro', description='The gift link has either expired\n or has been revoked.')
        embi.set_author(name="You recived a gift, but...")
        embi.set_thumbnail(url='https://external-preview.redd.it/9HZBYcvaOEnh4tOp5EqgcCr_vKH7cjFJwkvw-45Dfjs.png?auto=webp&s=ade9b43592942905a45d04dbc5065badb5aa3483')

        await self.message.edit(embed = embi, view=self)
        await self.ctx.author.send('No one fall for your nitro <:Sad_cat:900825746841411604>')


    @discord.ui.button(
        style = discord.ButtonStyle.green,
        label = '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ACCEPT⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀'
    )
    async def accept_nitro(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message(content='https://tenor.com/view/rick-roll-nitro-gif-21997352', ephemeral=True)
        button.style = discord.ButtonStyle.gray
        button.label = '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀CLAIMED⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀'
        for children in self.children:
            children.disabled = True
        await self.message.edit(view = self)
        self.stop()


class CalcuViewOne(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.ctx = ctx

    async def on_timeout(self):
        for children in self.children:
            children.disabled = True
        await self.message.edit(view = self)

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message('Sorry, you cannot use this calculator', ephemeral=True)
            return False
        return True

class UploadEmojiView(discord.ui.View):
    def __init__(self, ctx, emoji_url, emoji_name):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.emoji_url = emoji_url
        self.emoji_name = emoji_name

    async def on_timeout(self):
        for children in self.children:
            children.disabled = True
        
        await self.message.edit(view = self)

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message('Sorry, you cannot interact with these buttons.', ephemeral=True)
            return False
        return True

    @discord.ui.button(
        style=discord.ButtonStyle.green,
        label = 'Yes'
    )
    async def _upload_emoji_yes(self, button, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as sess:
            async with sess.get(self.emoji_url) as rep:
                raw = io.BytesIO(await rep.read())
                buf = raw.getvalue()

            try:
                _uploaded_emoji = await self.ctx.guild.create_custom_emoji(name=self.emoji_name, image=buf, reason=f'Uploaded by {self.ctx.author.name}')
            except HTTPException:
                return await interaction.response.send_message(embed = Utils.BotEmbed.error(f'Uh oh!, Maximum number of emojis reached **({self.ctx.guild.emoji_limit})**'), ephemeral=False)
            except InvalidArgument:
                return await interaction.response.send_message(embed = Utils.BotEmbed.error('Uh oh!. Unsupported image type given'), ephemeral=False)
            await interaction.response.send_message(f'{self.ctx.author} uploaded {_uploaded_emoji}', ephemeral=False)
            for children in self.children:
                children.disabled = True
            await self.message.edit(view = self)
            self.stop()

    @discord.ui.button(
        style = discord.ButtonStyle.gray,
        label = 'No'
    )
    async def _upload_emoji_cancel(self, button, interaction: discord.Interaction):
        await interaction.response.defer()
        await self.message.delete()
        await self.ctx.send(f'Cancelled uploading emoji.')
        self.stop()

class Misc(commands.Cog):
    def __init__(self, client):
        self.client=client
        self.bot=client

        #self.buttons_one = [
        #    [
        #        Button(style=ButtonStyle.grey, label='1', id='1'),
        #        Button(style=ButtonStyle.grey, label='2', id='2'),
        #        Button(style=ButtonStyle.grey, label='3', id='3'),
        #        Button(style=ButtonStyle.blue, label='×', id='×'),
        #        Button(style=ButtonStyle.red, label='Exit', id='Exit')
        #    ],
        #    [
        #        Button(style=ButtonStyle.grey, label='4', id='4'),
        #        Button(style=ButtonStyle.grey, label='5', id='5'),
        #        Button(style=ButtonStyle.grey, label='6', id='6'),
        #        Button(style=ButtonStyle.blue, label='÷', id='÷'),
        #        Button(style=ButtonStyle.red, label='⌫', id='⌫')
        #    ],
        #    [
        #        Button(style=ButtonStyle.grey, label='7', id='7'),
        #        Button(style=ButtonStyle.grey, label='8', id='8'),
        #        Button(style=ButtonStyle.grey, label='9', id='9'),
        #        Button(style=ButtonStyle.blue, label='+', id='+'),
        #        Button(style=ButtonStyle.red, label='Clear', id='Clear')
        #    ],
        #    [
        #        Button(style=ButtonStyle.grey, label='00', id='00'),
        #        Button(style=ButtonStyle.grey, label='0', id='0'),
        #        Button(style=ButtonStyle.grey, label='.', id='.'),
        #        Button(style=ButtonStyle.blue, label='-', id='-'),
        #        Button(style=ButtonStyle.green, label='=', id='=')
        #    ],
        #    [
        #        Button(style=ButtonStyle.green, label='❮', id='❮'),
        #        Button(style=ButtonStyle.green, label='❯', id='❯'),
        #        Button(style=ButtonStyle.grey, label='Change to scientific mode', emoji='\U0001f9d1\u200D\U0001f52c', id='400')
        #    ],
        #]
        #self.buttons_two = [
        #    [
        #        Button(style=ButtonStyle.grey, label='(', id='('),
        #        Button(style=ButtonStyle.grey, label=')', id=')'),
        #        Button(style=ButtonStyle.grey, label='π', id='π'),
        #        Button(style=ButtonStyle.blue, label='×', id='×'),
        #        Button(style=ButtonStyle.red, label='Exit', id='Exit')
        #    ],
        #    [
        #        Button(style=ButtonStyle.grey, label='X²', disabled=True),
        #        Button(style=ButtonStyle.grey, label='X³', disabled=True),
        #        Button(style=ButtonStyle.grey, label='Xˣ', disabled=True),
        #        Button(style=ButtonStyle.blue, label='÷', id='÷'),
        #        Button(style=ButtonStyle.red, label='⌫', id='⌫')
        #    ],
        #    [
        #        Button(style=ButtonStyle.grey, label='e', id='e'),
        #        Button(style=ButtonStyle.grey, label='τ', id='τ'),
        #        Button(style=ButtonStyle.grey, label='000', id='000'),
        #        Button(style=ButtonStyle.blue, label='+', id='+'),
        #        Button(style=ButtonStyle.red, label='Clear', id='Clear')
        #    ],
        #    [
        #        Button(style=ButtonStyle.grey, label='√', id='√'),
        #        Button(style=ButtonStyle.grey, label=' ', disabled=True),
        #        Button(style=ButtonStyle.grey, label=' ', disabled=True),
        #        Button(style=ButtonStyle.blue, label='-', id='-'),
        #        Button(style=ButtonStyle.green, label='=', id='=')
        #    ],
        #    [
        #        Button(style=ButtonStyle.green, label='❮', id='❮'),
        #        Button(style=ButtonStyle.green, label='❯', id='❯'),
        #        Button(style=ButtonStyle.grey, label='Change to normal modeㅤ', emoji='\U0001f468\u200D\U0001f3eb', id='401')
        #    ],
        #]




    @commands.command(brief='meta', description='Gets the latency of the bot', aliases=['ms', 'latency'])
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
        em.add_field(name="<a:typing:856668509705863169> | Typing", value=f"```{time_delta} ms```", inline=False)
        em.add_field(name="<a:discord:886308080260894751> | Api latency", value=f"```{round(self.client.latency * 1000)} ms```", inline=False)
        em.add_field(name="<:postgres:892392238825488514> | Database", value=f"```{dbtime_delta} ms```", inline=False)
        em.add_field(name="📝 | Message", value=f"```{mtime_delta} ms```", inline=False)
        await mainmessage.edit('\u200b', embed=em)


    def calculate(self, exp:str):
        result=''
        o=exp
        o=o.replace('π', str(pi))
        o=o.replace('τ', str(tau))
        o=o.replace('e', str(e))
        o=o.replace('×', '*')
        o=o.replace('÷', '/')
        o=o.replace('^2', '**2')
        o=o.replace('^3', '**3')
        o=o.replace('^', '**')
        o=o.replace('√', 'sqrt')
        try:
            result = eval(o, {'sqrt': sqrt})
        except:
            result=f"Syntax Error!\nDon't forget the sign(s) ('×', '÷', ...).\nnot: 3(9+1) but 3×(9+1)"
        return result

    def input_formatter(self, original:str, new:str):
        if 'Syntax Error!' in original:
            original='|'
        lst=list(original)
        try:
            index=lst.index('|')
            lst.remove('|')
        except:
            index=0
        if new == '1':
            lst.insert(index, '1')
        elif new == '2':
            lst.insert(index, '2')
        elif new == '3':
            lst.insert(index, '3')
        elif new == '4':
            lst.insert(index, '4')
        elif new == '5':
            lst.insert(index, '5')
        elif new == '6':
            lst.insert(index, '6')
        elif new == '7':
            lst.insert(index, '7')
        elif new == '8':
            lst.insert(index, '8')
        elif new == '9':
            lst.insert(index, '9')
        elif new == '10':
            lst.insert(index, '10')
        elif new == '0':
            lst.insert(index, '0')
        elif new == '00':
            lst.insert(index, '00')
        elif new == '+':
            lst.insert(index, '+')
        elif new == '÷':
            lst.insert(index, '÷')
        elif new == '-':
            lst.insert(index, '-')
        elif new == '×':
            i=index-1
            try:
                if lst[i]=='×':
                    lst.insert(index+1, '|')
                    original=''.join(lst)
                    return original
            except:
                lst.insert(index+1, '|')
                original=''.join(lst)
                return original
            try:
                if lst[index]=='×':
                    lst.insert(index, '|')
                    original=''.join(lst)
                    return original
                else:
                    lst.insert(index, '×')
            except:
                lst.insert(index, '×')
        elif new == '.':
            lst.insert(index, '.')
        elif new == '(':
            lst.insert(index, '(')
        elif new == ')':
            lst.insert(index, ')')
        elif new == 'π':
            lst.insert(index, 'π')
        elif new == 'X²':
            if '^' in lst:
                pass
            else:
                lst.insert(index, '^2')
        elif new == 'X³':
            if '^' in lst:
                pass
            else:
                lst.insert(index, '^3')
        elif new == 'Xˣ':
            if '^' in lst:
                pass
            else:
                lst.insert(index, '^')
        elif new == 'e':
            lst.insert(index, 'e')
        elif new == 'τ':
            lst.insert(index, 'τ')
        elif new == '000':
            lst.insert(index, '000')
        elif new == '√':
            lst.insert(index, '√()')
        lst.insert(index+1, '|')
        original=''.join(lst)
        return original
    
    @commands.command(brief='fun', description='An interactive calculator with buttons', aliases=['calc', 'calculator'])
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def calcu(self,ctx):
        affichage='|'
        id=1
        e = discord.Embed(title=f'{ctx.author}\'s calculator', description=f'```{affichage}```', color=int("2f3136", 16))
        expression=''
        m = await ctx.send(components=self.buttons_one, embed=e)
        
        def checkUp(res):
            return res.user.id == ctx.author.id and res.channel.id == ctx.channel.id and res.message.id==m.id
    
        while True:
            try:
                res = await self.client.wait_for('button_click', check=checkUp, timeout=60) 
            except asyncio.TimeoutError:
                a = discord.Embed(title=f'{ctx.author}\'s calculator', description=f'```{affichage}```', color=int("2f3136", 16))
                return await m.edit(embed=a)
            else:
                if str(res.author) == str(res.message.embeds[0].title.split("'s calculator")[0]):
                    if res.component.id == 'Exit':
                        q = discord.Embed(title=f'{ctx.author}\'s calculator', description=f'{res.message.embeds[0].description}', color=int("2f3136", 16))
                        await res.respond(embed=q, type=7)
                        disableMessage=await m.channel.fetch_message(m.id)
                        return await disableMessage.disable_components()
                    elif res.component.id == '⌫':
                        lst=list(res.message.embeds[0].description.replace('`',''))
                        if len(lst)>1:
                            try:
                                index=lst.index('|')
                                x=index-2
                                y=index+1
                                if lst[x]=='×' and lst[y]=='×':
                                    lst.pop(index-1)
                                    lst.pop(index-2)
                                else:
                                    lst.pop(index-1)
                            except:
                                lst=['|']
                        affichage=''.join(lst)
                        expression=affichage
                    elif res.component.id == 'Clear':
                        expression=''
                        affichage='|'
                    elif res.component.id == '=':
                        if 'Syntax Error!' in affichage or affichage=='|':
                            expression=''
                            affichage='|'
                        else:
                            expression=expression.replace('|','')
                            expression = self.calculate(expression)
                            affichage=f"{affichage.replace('|','')}={expression}"
                            expression=''
                    elif res.component.id == '❮':
                        lst=list(res.message.embeds[0].description.replace('`',''))
                        if len(lst)>1:
                            try:
                                index=lst.index('|')
                                lst.remove('|')
                                lst.insert(index-1, '|')
                            except:
                                lst=['|']
                        affichage=''.join(lst)
                    elif res.component.id == '❯':
                        lst=list(res.message.embeds[0].description.replace('`',''))
                        if len(lst)>1:
                            try:
                                index=lst.index('|')
                                lst.remove('|')
                                lst.insert(index+1, '|')
                            except:
                                lst=['|']
                        affichage=''.join(lst)
                    elif res.component.id == '400':
                        id=2
                        e = discord.Embed(title=f'{ctx.author}\'s calculator', description=f'```{affichage}```', color=int("2f3136", 16))
                        await res.respond(embed=e, components=self.buttons_two, type=7)
                    elif res.component.id == '401':
                        id=1
                        e = discord.Embed(title=f'{ctx.author}\'s calculator', description=f'```{affichage}```', color=int("2f3136", 16))
                        await res.respond(embed=e, components=self.buttons_one, type=7)
                    else:
                        if '=' in affichage:
                            affichage=''
                        expression = self.input_formatter(original=affichage, new=res.component.label)
                        affichage=expression
                    if res.component.id != '400' and res.component.id!='401':
                        e = discord.Embed(title=f'{ctx.author}\'s calculator', description=f'```{affichage}```', color=int("2f3136", 16))
                        if id==1:
                            await res.respond(embed=e, components=self.buttons_one, type=7)
                        else:
                            await res.respond(embed=e, components=self.buttons_two, type=7)



    @commands.command(brief='fun', description='Look into a user\'s spotify activity', usage='(user)')
    async def spotify(self, ctx, *, member:discord.Member=None):
        await ctx.trigger_typing()
        if member==None:
            member=ctx.author

        spotify_result=next((activity for activity in member.activities if isinstance(activity, discord.Spotify)),None)

        if spotify_result is None:
            if member==ctx.author:
                NoResultEmbed='You are'
            else:
                NoResultEmbed=f'{member.name} is'
            em=Utils.BotEmbed.error(f'{NoResultEmbed} not listening to spotify or the bot can\'t detect it')
            return await ctx.reply(embed=em, mention_author=False)

        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                style = discord.ButtonStyle.url,
                label='Listen on spotify\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800',
                url = f'https://open.spotify.com/track/{spotify_result.track_id}',
                emoji = self.client.get_emoji(902569759323848715)
            )
        )
        view.add_item(
            discord.ui.Button(
                style = discord.ButtonStyle.gray,
                label='\u2630',
                disabled=True
            )
        )


        params = {
            'title': spotify_result.title,
            'cover_url': spotify_result.album_cover_url,
            'duration_seconds': spotify_result.duration.seconds,
            'start_timestamp': spotify_result.start.timestamp(),
            'artists': spotify_result.artists
            }

        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.jeyy.xyz/discord/spotify', params=params) as r:
                buf=BytesIO(await r.read())

        await ctx.reply(f'Listening to **{spotify_result.title}** | {member.name}', file=discord.File(buf, 'spotify.png'), view=view, mention_author=False)



    @commands.Cog.listener('on_message_delete')
    async def snipe_messages(self, message):
        if not message.channel.permissions_for(message.guild.me).send_messages:
            return

        try:
            self.bot.sniped_messages[message.channel.id]
        except KeyError:
            self.bot.sniped_messages[message.channel.id] = []

        author=message.author
        embed=message.embeds[0] if message.embeds else None
        attachments=message.attachments[0].url if message.attachments else None
        content=message.content if message.content else '*Message does not contain any content*'
        timestamp=int(datetime.datetime.now().timestamp())

        if len(self.bot.sniped_messages[message.channel.id]) >= 10:
            self.bot.sniped_messages[message.channel.id] = []

        self.bot.sniped_messages[message.channel.id].append({'content': content, 'author': author, 'embed': embed, 'attachments': attachments, 'timestamp': timestamp})


    @commands.command(brief='meta', usage='(channel) (index)', description='Snipe latest 10 deleted messages of a channel')
    @commands.cooldown(3, 1, BucketType.channel)
    async def snipe(self, ctx, channel:typing.Optional[discord.TextChannel]=None, index: typing.Union[int, str]=1):
        
        channel=channel or ctx.channel

        try:
            _object=self.bot.sniped_messages[channel.id]
        except KeyError:
            await ctx.send('There are no messages to snipe now.')
            return

        if not _object:
            await ctx.send('There are no messages to snipe now.')
            return

        if isinstance(index, str):
            if index.lower() == 'all':
                await ctx.trigger_typing()
                embed=discord.Embed(color=Utils.BotColors.invis(), timestamp=datetime.datetime.now())


                count=0
                emojis=[]
                for x in _object:
                    count=count+1

                    content=x['content']
                    author=x['author']
                    timestamp=x['timestamp']

                    _emoji=await Utils.create_emoji(bot=self.bot, user=author)
                    emojis.append(_emoji)
                    
                    embed.add_field(name=f'{count}. {_emoji} `{author.name}` - [<t:{timestamp}:R>]', value=content, inline=False)
                    embed.set_footer(text=f'Invoked by {ctx.author.name}', icon_url=f'{ctx.author.avatar.url}')
                    embed.set_author(name=f'Sniped messages in #{channel.name}', icon_url=ctx.guild.icon.url)

                    
                await ctx.send(embed=embed)
                for x in emojis:
                    await x.delete()
                return
            else:
                await ctx.send('Index must be integers or "all".')


        if isinstance(index, int):
            if index <= 0:
                await ctx.send('Index must be greater than or equal to 1.')
                return

            try:
                _message=_object[-index]
            except IndexError:
                await ctx.send(f'Now, there are only {len(_object)}/10 sniped messages in this channel not {index}.')
                return

        _content=_message['content']
        _author=_message['author']
        _embed=_message['embed']
        _attachments=_message['attachments']
        _timestamp=_message['timestamp']

        MainMessageEmbeds = []

        em=discord.Embed(color=Utils.BotColors.invis(), timestamp=datetime.datetime.now())
        em.set_author(name=f'{_author}', icon_url=f'{_author.avatar.url}')
        em.add_field(name=f'[<t:{_timestamp}:R>]', value=_content)
        em.set_footer(text=f'Invoked by {ctx.author}', icon_url=ctx.author.avatar.url)
        if _attachments:
            em.set_image(url=_attachments)
        

        MainMessageEmbeds.append(em)

        if _embed:
            MainMessageEmbeds.append(_embed)

        await ctx.send(embeds=MainMessageEmbeds)
        

    @commands.command(brief='mod', description='Upload an emoji to your server', usage='[emoji or url] (name)')
    @commands.bot_has_guild_permissions(manage_emojis=True)
    async def upload_emoji(self, ctx, emoji_: typing.Union[discord.Emoji, discord.PartialEmoji, str], name='emote'):
        if isinstance(emoji_, str):
            emoji_url = emoji_
            
        else:
            emoji_url = str(emoji_.url)

        if not emoji_url.startswith('https://'):
            await ctx.send(
                embed = Utils.BotEmbed.error('URLs must be a rendered Discord emoji or an emoji URL')
            )
            return

        view = UploadEmojiView(ctx, emoji_url, name)
        em = discord.Embed(color=Utils.BotColors.invis())
        em.set_image(url=emoji_url)
        view.message = await ctx.send(
            'Is this alright?',
            embed = em,
            view = view
        )
        return


    @commands.group(brief='fun', description='Waifu images... you can add your favorites to gallery', invoke_without_command = True)
    async def waifu(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://waifu.pics/api/sfw/waifu') as r:
                res = await r.json()  # returns dict
            embed = discord.Embed(color=0x2F3136)
            embed.set_image(url=f"{res['url']}")
            embed.set_footer(text=f"Invoked by {ctx.author.name}", icon_url=f"{ctx.author.avatar.url}")
            if random.randint(1,3) == 2:
                embed.description = '> Hey, check out this new feature `g!waifu gallery`'
            elif random.randint(1,3) == 3:
                embed.description = 'Loving me? consider joining our [**Support Server**](https://discord.gg/UZ7WCpQQ)'

            view = WaifuView(ctx, res['url'])

            view.message = await ctx.send(embed=embed, view=view)

    @waifu.command(description='Shows your waifu-favorites gallery')
    async def gallery(self, ctx):
        _is_already = await self.bot.db.fetchrow('SELECT url FROM waifu WHERE user_id = $1', ctx.author.id)
        if not _is_already:
            await ctx.send(
                embed = Utils.BotEmbed.error('You don\'t have any images on your gallery')
            )
            return
        _waifu_list = _is_already['url']
        if not _waifu_list:
            await ctx.send(
                embed = Utils.BotEmbed.error('You don\'t have any images on your gallery')
            )
            return
        embeds = []
        count = 0
        for waifu in _waifu_list:
            count+=1
            embed = discord.Embed(color=0x2F3136)
            embed.set_image(url=waifu)
            embeds.append(embed)

        view = WaifuPagesView(embeds, ctx)
        _embed = embeds[0]
        _embed.set_footer(text=f'Showing image 1 of {len(embeds)}')
        view.message = await ctx.send(embed = _embed, view = view)



    async def check_rick_roll(self, url:str):
        async with aiohttp.ClientSession() as sess:
            async with sess.get(url) as rep:
                return str(rep.url) == 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'


        #if message.content.lower() == 'hello':
            #return await message.reply('https://nohello.net/', mention_author=False)

#    def isNoHello(self, content):
#        _lower = content.lower()
#
#        _hello_list = [
#            'hello',
#            'hi',
#            'hey',
#            'bonjour',
#            'yo',
#            'hola',
#            'hallo',
#            'ciao',
#            '👋',
#            'namaste',
#            'hoi',
#            'hiya'
#        ]
#
#        return _lower in _hello_list


    @commands.Cog.listener('on_message')
    async def fun_replies(self, message):
        if not message.guild:
            return
        if message.author.bot:
            return

        if message.content == f'<@!{self.bot.user.id}>' or message.content == f'<@{self.bot.user.id}>':
            try:
                self.bot.bot_mention[message.author.id]
            except:
                self.bot.bot_mention[message.author.id] = 0

            if self.bot.bot_mention[message.author.id] == 0:
                await message.reply(
                    """Hello, I'm **Gerty**, My prefixes are `g!`, `G!` and `@Gerty`
For a list of commands do `g!help`, `G!help` or `@Gerty help`

If you continue to have problems, consider asking for help on our **Support Server**
https://discord.gg/GdftdzWKqv""",
                    mention_author=False
                )
                self.bot.bot_mention[message.author.id] += 1
                await asyncio.sleep(20)
                self.bot.bot_mention[message.author.id] = 0
                return

            else:
                _reply_list = [
                    'https://tenor.com/view/lils-silly-duck-lilsduck-ducky-duck-duck-riri-the-duck-gif-19719423',
                    'https://tenor.com/view/bruh-moai-moyai-zemby7-big_funky-gif-23796913',
                    'https://media.discordapp.net/attachments/922154070565879808/922477855991033896/unknown.png',
                    'STOP IT!!!',
                    '<a:therock:922460890270425149>',
                    'Hmmm <a:therock:922460890270425149>',
                    'Why are you pinging me all time!?1',
                    '<a:pingg:922457162079420427>',
                    "Don't ping me all time I have **OTHER WORKS** to do",
                    '<a:shutthefuckup:922457614636417045>',
                    '<:bruh:922459628569231380>'
                ]
                _reply = random.choice(_reply_list)


                return await message.reply(_reply, mention_author=False)

#        if self.isNoHello(message.content):
#            return await message.reply('https://nohello.net/', mention_author=False)

        if 'looser' in message.content.lower().split(' '):
            return await message.reply('You are the real **loser** here', mention_author=False)

        if 'imagine' in message.content.lower().split(' '):
            return await message.reply(f'**{message.author.name}** is trying really hard to imagine', mention_author=False)


        brick_cont = message.content.replace('<', '')
        rickroll_content = brick_cont.replace('>', '')
        _islink_ = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', rickroll_content)
        if _islink_:
            for link in _islink_:
                if await self.check_rick_roll(link):
                    await message.reply('⚠️ Woah, nice **RickRoll** my guy', mention_author=False)
                    return
        return

    @commands.command(brief='fun', description='Prank your friends with a fake nitro')
    async def nitro(self, ctx):
        em=discord.Embed(title="Nitro", description="Expires in 48 hours", color=0x2F3136)
        em.set_author(name="A WILD GIFT APPEARS!")
        em.set_thumbnail(url="https://media.discordapp.net/attachments/884423056934711326/888057999875244072/2Q.png")

        view = NitroView(ctx)
        view.message = await ctx.send(embed = em, view = view)



def setup(client):
    client.add_cog(Misc(client))
    client.remove_command('calcu')
