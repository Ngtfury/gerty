from random import random
import re
import discord
from discord import emoji
from discord import guild
from discord.errors import HTTPException
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
import discord_components
import aiohttp
from io import BytesIO
from discord_components import *



class Misc(commands.Cog):
    def __init__(self, client):
        self.client=client
        self.bot=client
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
            
        components=[[Button(style=ButtonStyle.URL, label='Listen on spotify\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800', url=f'https://open.spotify.com/track/{spotify_result.track_id}', emoji=self.client.get_emoji(902569759323848715)), Button(style=ButtonStyle.gray, label='\u2630', disabled=True)]]


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

        await ctx.reply(f'Listening to **{spotify_result.title}** | {member.name}', file=discord.File(buf, 'spotify.png'), components=components, mention_author=False)



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
                    embed.set_footer(text=f'Invoked by {ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
                    embed.set_author(name=f'Sniped messages in #{channel.name}', icon_url=ctx.guild.icon_url)

                    
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
        em.set_author(name=f'{_author}', icon_url=f'{_author.avatar_url}')
        em.add_field(name=f'[<t:{_timestamp}:R>]', value=_content)
        em.set_footer(text=f'Invoked by {ctx.author}', icon_url=ctx.author.avatar_url)
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

        if not emoji_url.startswith('https://cdn.discordapp.com/emojis/'):
            await ctx.send(
                embed = Utils.BotEmbed.error('URLs must be a rendered Discord emoji or an emoji URL')
            )
            return

        components = [[
            Button(style=ButtonStyle.green, label='Yes', id='EmojiUploadYes'),
            Button(label='No', id='EmojiUploadNo')
        ]]
        em = discord.Embed(color=Utils.BotColors.invis())
        em.set_image(url=emoji_url)
        MainMessage = await ctx.send(
            'Is this alright?',
            embed = em,
            components = components
        )
        while True:
            event = await self.bot.wait_for('button_click', check = lambda i: i.author == ctx.author and i.message.id == MainMessage.id)
            if event.component.id == 'EmojiUploadYes':
                await MainMessage.disable_components()

                async with aiohttp.ClientSession() as sess:
                    async with sess.get(emoji_url) as rep:
                        raw = io.BytesIO(await rep.read())
                        buf = raw.getvalue()

                    try:
                        _uploaded_emoji = await ctx.guild.create_custom_emoji(name=name, image=buf, reason=f'Uploaded by {ctx.author.name}')
                    except HTTPException:
                        return await event.respond(type=4, embed = Utils.BotEmbed.error(f'Uh oh!, Maximum number of emojis reached **({ctx.guild.emoji_limit})**'), ephemeral=False)
                    await event.respond(type=4, content=f'{ctx.author.display_name} uploaded {_uploaded_emoji}', ephemeral=False)
                return
            elif event.component.id == 'EmojiUploadNo':
                await event.respond(type=6)
                await MainMessage.delete()
                await ctx.send('Cancelled uploading emoji.')
                return
            

                



    async def check_rick_roll(self, url:str):
        async with aiohttp.ClientSession() as sess:
            async with sess.get(url) as rep:
                return str(rep.url) == 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'


        #if message.content.lower() == 'hello':
            #return await message.reply('https://nohello.net/', mention_author=False)

    def isNoHello(self, content):
        _lower = content.lower()

        _hello_list = [
            'hello',
            'hi',
            'hey',
            'bonjour',
            'yo',
            'hola',
            'hallo',
            'ciao',
            '👋',
            'namaste',
            'hoi',
            'hiya'
        ]

        return _lower in _hello_list


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
                    """Hello, I'm **Gerty**, My prefixes are `g!` and `@Gerty`
For a list of commands do `g!help` or `@Gerty help`

If you continue to have problems, consider asking for help on our **Support Server**
https://discord.gg/gERnjRdF""",
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

        if self.isNoHello(message.content):
            return await message.reply('https://nohello.net/', mention_author=False)

        if message.content == '...' or message.content == '..' or message.content == '.':
            return await message.reply('???', mention_author=False)

        if 'looser' in message.content.lower().split(' '):
            return await message.reply('You are the real **loser** here', mention_author=False)

        if 'mad' in message.content.lower().split(' '):
            return await message.reply(embed = discord.Embed(description='Why you heff to be [mad](https://www.youtube.com/watch?v=xzpndHtdl9A)??', color=Utils.BotColors.invis()), mention_author=False)

        if 'imagine' in message.content.lower().split(' '):
            return await message.reply(f'**{message.author.name}** is trying really had to imagine', mention_author=False)

        _islink_ = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.content)
        if _islink_:
            for link in _islink_:
                if await self.check_rick_roll(link):
                    await message.reply('⚠️ Woah, nice **RickRoll** my guy', mention_author=False)
                    return
        return

def setup(client):
    client.add_cog(Misc(client))
