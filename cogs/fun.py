import discord
import typing
from discord.ext import commands
import re
import aiohttp
from cogs.utils import Utils



#brief='fun', usage='[text]', description='Make the bot say whatever you want with emojis!'
def setup(bot):
    bot.add_cog(FunCommands(bot))


class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot=bot



    @commands.command()
    async def emojify(self, ctx, object: typing.Union[discord.User, discord.Emoji, discord.Message, str]=None):
        await ctx.trigger_typing()
        if object==None:
            if ctx.message.reference:
                object=ctx.message.reference.resolved
            else:
                return await ctx.send(embed=Utils.BotEmbed.error('You must provide a url, emoji or a member to emojify'))
        if isinstance(object, discord.Emoji):
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
                    _emoji=self.bot.get_emoji(EmojiId)
                    _url=str(_emoji.url)
                else:
                    return await ctx.send(embed=Utils.BotEmbed.error('You must provide a url, emoji or a member to emojify'))

        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.jeyy.xyz/text/emojify?image_url={_url}') as resp:
                json=await resp.json()


        _text=json['text']

        await ctx.reply(f'```{_text}```', mention_author=False)

