import discord
from discord.ext import commands
import datetime

from discord_components.button import Button, ButtonStyle
from cogs.utils import Utils


def setup(bot):
    bot.add_cog(AfkCommandCog(bot))


class AfkCommandCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(brief='meta', description='Sets your status as AFK', usage='(reason)')
    async def afk(self, ctx, reason: str = 'I\'m AFK :)'):
        if ctx.author.id in self.bot.afk:
            await ctx.send(
                f"""**I set your afk {ctx.author.display_name}!**
                wait what?!! you can be afk twice??"""
            )
            return


        MainMessage = await ctx.send(
            'Choose your afk style from the buttons below.',
            components = [[
                Button(style=ButtonStyle.green, label='Global', id='AfkSetGlobal'),
                Button(label='Local', id='AfkSetLocal')
            ]]
        )
        while True:
            event = await self.bot.wait_for('button_click', check=lambda i: i.author==ctx.author and i.message.id == MainMessage.id)
            await event.respond(type=6)
            if event.component.id == 'AfkSetGlobal':
                _global = True
                break
            elif event.component.id == 'AfkSetLocal':
                _global = False
                break
        
        await MainMessage.delete()
        text = 'globally' if _global else 'locally'
        em = discord.Embed(
            color = Utils.BotColors.invis(),
            description=f'<a:afk:890119774015717406> **{ctx.author.name}** I\'ve set your AFK {text}, {reason}'
        )
        await ctx.send(embed = em)

        self.bot.afk[ctx.author.id] = {}
        self.bot.afk[ctx.author.id]['reason'] = reason
        self.bot.afk[ctx.author.id]['time'] = int(datetime.datetime.now().timestamp())
        self.bot.afk[ctx.author.id]['gobal'] = _global
        self.bot.afk[ctx.author.id]['guild_id'] = ctx.guild.id if not _global else None


        await self.bot.db.execute(
            """INSERT INTO afk (user_id,reason,time,global,guild_id) VALUES ($1,$2,$3,$4,$5)""",
            reason,
            int(datetime.datetime.now().timestamp()),
            _global,
            ctx.guild.id if not _global else None
        )



