import discord
import typing
from discord.ext import commands
import re
import time
import aiohttp
from io import BytesIO
from cogs.utils import Utils




def setup(bot):
    bot.add_cog(ImageCommands(bot))


class ImageCommands(commands.Cog):
    def __init__(self, bot):
        self.bot=bot


    async def api_error(self, ctx):
        em=Utils.BotEmbed.error(f'You must provide a url, custom emoji or a member to `{ctx.command.qualified_name}`. You can also reply to a message and use command bot will automatically find emoji or url if any')
        return await ctx.send(embed=em)



    @commands.command(brief='image', usage='[user or custom emoji or url]', description='Changes an emoji image or user avatar or an image to emoji form')
    async def emojify(self, ctx, object: typing.Union[discord.User, discord.PartialEmoji, discord.Message, str]=None):
        await ctx.trigger_typing()
        if object==None:
            if ctx.message.reference:
                object=ctx.message.reference.resolved
            else:
                object=ctx.author
        if isinstance(object, discord.PartialEmoji):
            _url=str(object.url)
        elif isinstance(object, discord.User):
            _url=str(object.avatar_url)
        elif isinstance(object, discord.Message):
            _urllist=re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', object.content)
            if _urllist:
                _url=''.join(_urllist)
            else:
                _urllist=re.findall(r'<(?P<animated>a?):(?P<name>[a-zA-Z0-9_]{2,32}):(?P<id>[0-9]{18,22})>', object.content)
                if _urllist:
                    _urllisttuple=_urllist[0]
                    EmojiId=_urllisttuple[2]
                    _emoji=self.bot.get_emoji(int(EmojiId))
                    _url=str(_emoji.url)
                else:
                    return await ctx.send(embed=Utils.BotEmbed.error('You must provide a url, custom emoji or a member to emojify. You can also reply to a message and use command bot will automatically find emoji or url if any'))
        elif isinstance(object, str):
            _urllist=re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(object))
            if not _urllist:
                return await ctx.send(embed=Utils.BotEmbed.error('You must provide a url, custom emoji or a member to emojify. You can also reply to a message and use command bot will automatically find emoji or url if any'))
            else:
                _url=str(object)
        else:
            return await ctx.send(embed=Utils.BotEmbed.error('You must provide a url, custom emoji or a member to emojify. You can also reply to a message and use command bot will automatically find emoji or url if any'))

        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.jeyy.xyz/text/emojify?image_url={_url}') as resp:
                json=await resp.json()

        try:
            _text=json['text']
        except KeyError:
            return await ctx.send(embed=Utils.BotEmbed.error('You must provide a only url, custom emoji or a member to emojify\nYou can also reply to a message and use command bot will automatically find emoji or url if any'))


        em=discord.Embed(description=f'```{_text}```', color=Utils.BotColors.invis())
        await ctx.reply(embed=em, mention_author=False)


    
    @commands.command(brief='image', usage='[user or custom emoji or url]', description='Adds some heart effects to the image')
    async def hearts(self,ctx, object: typing.Union[discord.User, discord.PartialEmoji, discord.Message, str]=None):
        await ctx.trigger_typing()
        time1=time.perf_counter()
        if object==None:
            if ctx.message.reference:
                object=ctx.message.reference.resolved
            else:
                object=ctx.author

        if isinstance(object, discord.PartialEmoji):
            _url=str(object.url)
        elif isinstance(object, discord.User):
            _url=str(object.avatar_url)
        elif isinstance(object, discord.Message):
            _urllist=re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', object.content)
            if _urllist:
                _url=''.join(_urllist)
            else:
                _urllist=re.findall(r'<(?P<animated>a?):(?P<name>[a-zA-Z0-9_]{2,32}):(?P<id>[0-9]{18,22})>', object.content)
                if _urllist:
                    _urllisttuple=_urllist[0]
                    EmojiId=_urllisttuple[2]
                    _emoji=self.bot.get_emoji(int(EmojiId))
                    _url=str(_emoji.url)
                else:
                    return await ctx.send(embed=Utils.BotEmbed.error('You must provide a url, custom emoji or a member to hearts. You can also reply to a message and use command bot will automatically find emoji or url if any'))
        elif isinstance(object, str):
            _urllist=re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(object))
            if not _urllist:
                return await ctx.send(embed=Utils.BotEmbed.error('You must provide a url, custom emoji or a member to hearts. You can also reply to a message and use command bot will automatically find emoji or url if any'))
            else:
                _url=str(object)
        else:
            return await ctx.send(embed=Utils.BotEmbed.error('You must provide a url, custom emoji or a member to hearts. You can also reply to a message and use command bot will automatically find emoji or url if any'))

        
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.jeyy.xyz/image/hearts?image_url={_url}&rainbow=True') as r:
                if r.status != 200:
                    return await ctx.send(embed=Utils.BotEmbed.error(f'Sorry there was an error, {r.reason}'))
                buf=BytesIO(await r.read())
        time2=time.perf_counter()
        timedelta=time2-time1
        await ctx.reply(f'Process took `{timedelta}` seconds', file=discord.File(buf, 'hearts.gif'), mention_author=False)


    @commands.command(brief='image', usage='[user or custom emoji or url]', description='Creates a maths equation meme with an image', aliases=['math'])
    async def equation(self, ctx, object: typing.Union[discord.User, discord.PartialEmoji, discord.Message, str]=None):
        await ctx.trigger_typing()
        time1=time.perf_counter()
        if object==None:
            if ctx.message.reference:
                object=ctx.message.reference.resolved
            else:
                object=ctx.author

        if isinstance(object, discord.PartialEmoji):
            _url=str(object.url)
        elif isinstance(object, discord.User):
            _url=str(object.avatar_url)
        elif isinstance(object, discord.Message):
            _urllist=re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', object.content)
            if _urllist:
                _url=''.join(_urllist)
            else:
                _urllist=re.findall(r'<(?P<animated>a?):(?P<name>[a-zA-Z0-9_]{2,32}):(?P<id>[0-9]{18,22})>', object.content)
                if _urllist:
                    _urllisttuple=_urllist[0]
                    EmojiId=_urllisttuple[2]
                    _emoji=self.bot.get_emoji(int(EmojiId))
                    _url=str(_emoji.url)
                else:
                    return await self.api_error(ctx)
        elif isinstance(object, str):
            _urllist=re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(object))
            if not _urllist:
                return await self.api_error(ctx)
            else:
                _url=str(object)
        else:
            return await self.api_error(ctx)

        
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.jeyy.xyz/image/equations?image_url={_url}') as r:
                if r.status != 200:
                    return await ctx.send(embed=Utils.BotEmbed.error(f'Sorry there was an error, {r.reason}'))
                buf=BytesIO(await r.read())
        time2=time.perf_counter()
        timedelta=time2-time1
        await ctx.reply(f'Process took `{timedelta}` seconds', file=discord.File(buf, 'equations.gif'), mention_author=False)


    @commands.command(brief='image', description='Gives boil effect to an image', usage='[user or custom emoji or url]')
    async def boil(self, ctx, object: typing.Union[discord.User, discord.PartialEmoji, discord.Message, str]=None):
        await ctx.trigger_typing()
        time1=time.perf_counter()
        if object==None:
            if ctx.message.reference:
                object=ctx.message.reference.resolved
            else:
                object=ctx.author

        if isinstance(object, discord.PartialEmoji):
            _url=str(object.url)
        elif isinstance(object, discord.User):
            _url=str(object.avatar_url)
        elif isinstance(object, discord.Message):
            _urllist=re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', object.content)
            if _urllist:
                _url=''.join(_urllist)
            else:
                _urllist=re.findall(r'<(?P<animated>a?):(?P<name>[a-zA-Z0-9_]{2,32}):(?P<id>[0-9]{18,22})>', object.content)
                if _urllist:
                    _urllisttuple=_urllist[0]
                    EmojiId=_urllisttuple[2]
                    _emoji=self.bot.get_emoji(int(EmojiId))
                    _url=str(_emoji.url)
                else:
                    return await self.api_error(ctx)
        elif isinstance(object, str):
            _urllist=re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(object))
            if not _urllist:
                return await self.api_error(ctx)
            else:
                _url=str(object)
        else:
            return await self.api_error(ctx)

 
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.jeyy.xyz/image/boil?image_url={_url}') as r:
                if r.status != 200:
                    return await ctx.send(embed=Utils.BotEmbed.error(f'Sorry there was an error, {r.reason}'))
                buf=BytesIO(await r.read())
        time2=time.perf_counter()
        timedelta=time2-time1
        await ctx.reply(f'Process took `{timedelta}` seconds', file=discord.File(buf, 'boiled.gif'), mention_author=False)


    @commands.command(brief='image', description='Adds a layer of sob meme to an image', usage='[user or custom emoji or url]')
    async def sob(self, ctx, object: typing.Union[discord.Member, discord.PartialEmoji, discord.Message, str]=None):
        await ctx.trigger_typing()
        time1=time.perf_counter()
        if object==None:
            if ctx.message.reference:
                object=ctx.message.reference.resolved
            else:
                object=ctx.author

        if isinstance(object, discord.PartialEmoji):
            _url=str(object.url)
        elif isinstance(object, discord.Member):
            _url=str(object.avatar_url)
        elif isinstance(object, discord.Message):
            _urllist=re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', object.content)
            if _urllist:
                _url=''.join(_urllist)
            else:
                _urllist=re.findall(r'<(?P<animated>a?):(?P<name>[a-zA-Z0-9_]{2,32}):(?P<id>[0-9]{18,22})>', object.content)
                if _urllist:
                    _urllisttuple=_urllist[0]
                    EmojiId=_urllisttuple[2]
                    _emoji=self.bot.get_emoji(int(EmojiId))
                    _url=str(_emoji.url)
                else:
                    return await self.api_error(ctx)
        elif isinstance(object, str):
            _urllist=re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(object))
            if not _urllist:
                return await self.api_error(ctx)
            else:
                _url=str(object)
        else:
            return await self.api_error(ctx)

 
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.jeyy.xyz/image/sob?image_url={_url}') as r:
                if r.status != 200:
                    return await ctx.send(embed=Utils.BotEmbed.error(f'Sorry there was an error, {r.reason}'))
                buf=BytesIO(await r.read())
        time2=time.perf_counter()
        timedelta=time2-time1
        await ctx.reply(f'Process took `{timedelta}` seconds', file=discord.File(buf, 'boiled.gif'), mention_author=False)