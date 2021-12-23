from asyncio.tasks import wait
import discord
from discord.ext import commands
import datetime

from discord.ui import view
from cogs.utils import Utils
import humanize


def setup(bot):
    bot.add_cog(AfkCommandCog(bot))

class AfkView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.ctx = ctx

    async def on_timeout(self):
        for children in self.children:
            children.disabled = True

        await self.message.edit(view = self)

    async def interaction_check(self, interation: discord.Interaction):
        if interation.user.id != self.ctx.author.id:
            await interation.response.send_message(ephemeral=True, content='Sorry, you cannot interact with these buttons')
            return False
        return True

    @discord.ui.button(
        style = discord.ButtonStyle.green,
        label = 'Global'
    )
    async def set_global(self, button, interation: discord.Interaction):
        await interation.response.defer()
        await interation.message.delete()
        self._global = True
        self.stop()

    @discord.ui.button(
        style = discord.ButtonStyle.gray,
        label = 'Local'
    )
    async def set_local(self, button, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.message.delete()
        self._global = False
        self.stop()



class AfkCommandCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(brief='meta', description='Sets your status as AFK', usage='(reason)')
    async def afk(self, ctx, *, reason: str = 'I\'m AFK :)'):
        if ctx.author.id in self.bot.afk:
            isglobal = self.bot.afk[ctx.author.id]['global']
            if isglobal:
                return
            guild_id = self.bot.afk[ctx.author.id]['guild_id']
            guild_name = 'some other server' if not self.bot.get_guild(guild_id) else self.bot.get_guild(guild_id).name

            await ctx.send(
                f'Sorry, you are already AFK in {guild_name}, I cant set your AFK now.'
            )
            return

        if len(reason) > 40:
            await ctx.send('Sorry, only upto 40 characters for reason please.')
            return

        view = AfkView(ctx)

        view.message = MainMessage = await ctx.send(
            embed = discord.Embed(color=Utils.BotColors.invis(), description='<a:afk:890119774015717406> Choose your afk style from the buttons below.'),
            view = view
        )

        _wait = await view.wait()
        if _wait == True:
            return


        _global = view._global

        text = 'globally' if _global else 'locally'
        em = discord.Embed(
            color = Utils.BotColors.invis(),
            description=f'<a:afk:890119774015717406> `{ctx.author.name}` I\'ve set your AFK {text}, {reason}'
        )
        await ctx.send(embed = em)


        if _global:
            await self.bot.db.execute(
                """INSERT INTO afk (user_id,reason,time,global) VALUES ($1,$2,$3,$4)""",
                ctx.author.id,
                reason,
                int(datetime.datetime.now().timestamp()),
                _global,
            )
        else:
            await self.bot.db.execute(
                """INSERT INTO afk (user_id,reason,time,global,guild_id) VALUES ($1,$2,$3,$4,$5)""",
                ctx.author.id,
                reason,
                int(datetime.datetime.now().timestamp()),
                _global,
                ctx.guild.id
            )

        self.bot.afk[ctx.author.id] = {}
        self.bot.afk[ctx.author.id]['reason'] = reason
        self.bot.afk[ctx.author.id]['time'] = int(datetime.datetime.now().timestamp())
        self.bot.afk[ctx.author.id]['global'] = _global
        self.bot.afk[ctx.author.id]['guild_id'] = ctx.guild.id if not _global else None




    @commands.Cog.listener('on_message')
    async def delete_afk(self, message):
        if message.author.bot:
            return

        if not message.author.id in self.bot.afk:
            return

        time = self.bot.afk[message.author.id]['time']
        isglobal = self.bot.afk[message.author.id]['global']
        guild_id = self.bot.afk[message.author.id]['guild_id']
        if not isglobal:
            if not guild_id == message.guild.id:
                return

        _text = 'globally' if isglobal else 'locally'

        del self.bot.afk[message.author.id]

        dt_object = datetime.datetime.fromtimestamp(time)
        hum_delta = humanize.naturaldelta(dt_object)

        embed = discord.Embed(
            color = Utils.BotColors.invis(),
            description=f'<a:afk:890119774015717406> Welcome back `{message.author.name}`, You were AFK {_text} for {hum_delta}'
        )
        await message.reply(embed = embed, mention_author=False)

        await self.bot.db.execute(
            """DELETE FROM afk WHERE user_id = $1""",
            message.author.id
        )


    @commands.Cog.listener('on_message')
    async def log_afk(self, message):
        if message.author.bot:
            return

        if not message.mentions:
            return

        for user in message.mentions:
            if not user.id in self.bot.afk:
                return

            isglobal = self.bot.afk[user.id]['global']
            guild_id = self.bot.afk[user.id]['guild_id']
            if not isglobal:
                if not guild_id == message.guild.id:
                    return

            _text = 'globally' if isglobal else 'locally'

            reason = self.bot.afk[user.id]['reason']
            time = self.bot.afk[user.id]['time']

            em = discord.Embed(color=Utils.BotColors.invis(), description=f'<a:afk:890119774015717406> `{user.name}` went {_text} AFK <t:{time}:R>, {reason}')
            await message.reply(embed = em, mention_author = False)

        return





