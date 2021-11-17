import discord
from cogs.utils import Utils
from discord.ext import commands
import datetime
import time
import asyncio
from math import *
import discord_components
import aiohttp
from io import BytesIO
from discord_components import *



class Misc(commands.Cog):
    def __init__(self, client):
        self.client=client
        self.buttons_one = [
            [
                Button(style=ButtonStyle.grey, label='1', id='1'),
                Button(style=ButtonStyle.grey, label='2', id='2'),
                Button(style=ButtonStyle.grey, label='3', id='3'),
                Button(style=ButtonStyle.blue, label='×', id='×'),
                Button(style=ButtonStyle.red, label='Exit', id='Exit')
            ],
            [
                Button(style=ButtonStyle.grey, label='4', id='4'),
                Button(style=ButtonStyle.grey, label='5', id='5'),
                Button(style=ButtonStyle.grey, label='6', id='6'),
                Button(style=ButtonStyle.blue, label='÷', id='÷'),
                Button(style=ButtonStyle.red, label='⌫', id='⌫')
            ],
            [
                Button(style=ButtonStyle.grey, label='7', id='7'),
                Button(style=ButtonStyle.grey, label='8', id='8'),
                Button(style=ButtonStyle.grey, label='9', id='9'),
                Button(style=ButtonStyle.blue, label='+', id='+'),
                Button(style=ButtonStyle.red, label='Clear', id='Clear')
            ],
            [
                Button(style=ButtonStyle.grey, label='00', id='00'),
                Button(style=ButtonStyle.grey, label='0', id='0'),
                Button(style=ButtonStyle.grey, label='.', id='.'),
                Button(style=ButtonStyle.blue, label='-', id='-'),
                Button(style=ButtonStyle.green, label='=', id='=')
            ],
            [
                Button(style=ButtonStyle.green, label='❮', id='❮'),
                Button(style=ButtonStyle.green, label='❯', id='❯'),
                Button(style=ButtonStyle.grey, label='Change to scientific mode', emoji='\U0001f9d1\u200D\U0001f52c', id='400')
            ],
        ]
        self.buttons_two = [
            [
                Button(style=ButtonStyle.grey, label='(', id='('),
                Button(style=ButtonStyle.grey, label=')', id=')'),
                Button(style=ButtonStyle.grey, label='π', id='π'),
                Button(style=ButtonStyle.blue, label='×', id='×'),
                Button(style=ButtonStyle.red, label='Exit', id='Exit')
            ],
            [
                Button(style=ButtonStyle.grey, label='X²', disabled=True),
                Button(style=ButtonStyle.grey, label='X³', disabled=True),
                Button(style=ButtonStyle.grey, label='Xˣ', disabled=True),
                Button(style=ButtonStyle.blue, label='÷', id='÷'),
                Button(style=ButtonStyle.red, label='⌫', id='⌫')
            ],
            [
                Button(style=ButtonStyle.grey, label='e', id='e'),
                Button(style=ButtonStyle.grey, label='τ', id='τ'),
                Button(style=ButtonStyle.grey, label='000', id='000'),
                Button(style=ButtonStyle.blue, label='+', id='+'),
                Button(style=ButtonStyle.red, label='Clear', id='Clear')
            ],
            [
                Button(style=ButtonStyle.grey, label='√', id='√'),
                Button(style=ButtonStyle.grey, label=' ', disabled=True),
                Button(style=ButtonStyle.grey, label=' ', disabled=True),
                Button(style=ButtonStyle.blue, label='-', id='-'),
                Button(style=ButtonStyle.green, label='=', id='=')
            ],
            [
                Button(style=ButtonStyle.green, label='❮', id='❮'),
                Button(style=ButtonStyle.green, label='❯', id='❯'),
                Button(style=ButtonStyle.grey, label='Change to normal modeㅤ', emoji='\U0001f468\u200D\U0001f3eb', id='401')
            ],
        ]




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
    async def spotify(self, ctx, member:discord.Member=None):
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
            
        components=[[Button(style=ButtonStyle.URL, label='Listen on spotify\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800', url=f'https://open.spotify.com/track/{spotify_result.track_id}', emoji=self.client.get_emoji(902569759323848715)), Button(style=ButtonStyle.gray, label='\u2630', disabled=True)]]


        params = {
            'title': spotify_result.title,
            'cover_url': spotify_result.album_cover_url,
            'duration_seconds': spotify_result.duration.seconds,
            'start_timestamp': spotify_result.start.timestamp(),
            'artists': spotify_result.artists
            }

        r = await aiohttp.ClientSession().get('https://api.jeyy.xyz/discord/spotify', params=params)
        buf = BytesIO(await r.read())

        await ctx.reply(f'Listening to **{spotify_result.title}** by **{spotify_result.artist}**', file=discord.File(buf, 'spotify.png'), components=components, mention_author=False)

def setup(client):
    client.add_cog(Misc(client))