import aiohttp
import discord
from discord import integrations
from discord.embeds import Embed
from discord.ext import commands
from akinator.async_aki import Akinator
import akinator
from cogs.utils import Utils
from multibar import ProgressBar, ProgressTemplates, DiscordTemplates
import datetime
import time
import asyncio
from math import *

class AkinatorComponents:

    class AkinatorStartView(discord.ui.View):
        def __init__(self, ctx):
            super().__init__(timeout=60)
            self.ctx = ctx

        async def on_timeout(self):
            for children in self.children:
                children.disabled = True

            await self.message.edit(view = self)

        async def interaction_check(self, interaction: discord.Interaction):
            if interaction.user.id != self.ctx.author.id:
                await interaction.response.send_message('Sorry, this is not your game and you cannot interact with these buttons.', ephemeral=True)
                return False
            return True

        @discord.ui.button(
            style = discord.ButtonStyle.gray,
            label = 'Characters',
        )
        async def aki_char(self, button: discord.ui.Button, interaction: discord.Interaction):
            self._lang = None
            button.style = discord.ButtonStyle.green
            for children in self.children:
                children.disabled = True
            await interaction.response.edit_message(view = self)
            self.stop()

        @discord.ui.button(
            style = discord.ButtonStyle.gray,
            label = 'Animals'
        )
        async def aki_animal(self, button: discord.ui.Button, interaction: discord.Interaction):
            self._lang = 'en_animals'
            button.style = discord.ButtonStyle.green
            for children in self.children:
                children.disabled = True
            await interaction.response.edit_message(view = self)
            self.stop()

        @discord.ui.button(
            style = discord.ButtonStyle.gray,
            label = 'Objects'
        )
        async def aki_obj(self, button: discord.ui.Button, interaction: discord.Interaction):
            self._lang = 'en_objects'
            button.style = discord.ButtonStyle.green
            for children in self.children:
                children.disabled = True
            await interaction.response.edit_message(view = self)
            self.stop()

    class AkinatorView(discord.ui.View):
        def __init__(self, ctx, aki):
            super().__init__(timeout=60)
            self.ctx = ctx
            self.aki = aki

        async def on_timeout(self):
            for children in self.children:
                children.disabled = True

            await self.message.edit(view = self)

        async def interaction_check(self, interaction: discord.Interaction):
            if interaction.user.id != self.ctx.author.id:
                await interaction.response.send_message('Sorry, this is not your game and you cannot interact with these buttons.', ephemeral=True)
                return False
            return True

        @discord.ui.button(
            style = discord.ButtonStyle.green,
            label = 'Yes'
        )
        async def aki_yes(self, button, interaction: discord.Interaction):
            q = await self.aki.answer('yes')
            self._q = q
            self._interaction = interaction
            self.stop()

        @discord.ui.button(
            style = discord.ButtonStyle.gray,
            label = 'No'
        )
        async def aki_no(self, button, interaction: discord.Interaction):
            q = await self.aki.answer('no')
            self._q = q
            self._interaction = interaction
            self.stop()

        @discord.ui.button(
            style = discord.ButtonStyle.blurple,
            label = 'Don\'t know'
        )
        async def aki_idk(self, button, interaction: discord.Interaction):
            q = await self.aki.answer('idk')
            self._q = q
            self._interaction = interaction
            self.stop()

        @discord.ui.button(
            style = discord.ButtonStyle.green,
            label = 'Probably'
        )
        async def aki_prolly(self, button, interaction: discord.Interaction):
            q = await self.aki.answer('probably')
            self._q = q
            self._interaction = interaction
            self.stop()

        @discord.ui.button(
            style = discord.ButtonStyle.gray,
            label = 'Probably not'
        )
        async def aki_prolly_not(self, button, interaction: discord.Interaction):
            q = await self.aki.answer('probably not')
            self._q = q
            self._interaction = interaction
            self.stop()


def setup(bot):
    bot.add_cog(AkinatorCog(bot))

class AkinatorCog(commands.Cog):
    def __init__(self, bot):
        self.client=bot



    @commands.command(name='akinator', brief='fun', description='Attempts to determine what character  you is thinking of by asking a series of questions', aliases=['aki'])
    @commands.max_concurrency(1, per=commands.BucketType.channel)
    @commands.is_owner()
    async def _akinator(self,ctx):

        aki=Akinator()


        StartGame=discord.Embed(description='Please select an option what you are guessing.', color=Utils.BotColors.invis())
        StartGame.set_thumbnail(url='https://en.akinator.com/bundles/elokencesite/images/akinator.png?v94')
        StartGame.set_author(name='Akinator', icon_url='https://play-lh.googleusercontent.com/rjX8LZCV-MaY3o927R59GkEwDOIRLGCXFphaOTeFFzNiYY6SQ4a-B_5t7eUPlGANrcw')

        Startview = AkinatorComponents.AkinatorStartView(ctx)
        Startview.message = MainMessage = await ctx.reply(embed=StartGame, view=Startview, mention_author=False)
        _startwait = await Startview.wait()
        if _startwait:
            return

        _lang = Startview._lang
        em=discord.Embed(description=f'{Utils.BotEmojis.loading()} Loading akinator... Please wait', color=Utils.BotColors.invis())
        await MainMessage.edit(embed = em)
        q = await aki.start_game(language = _lang, child_mode = True)


        bar=ProgressBar(
            aki.progression,
            80
        )

        Mainview = AkinatorComponents.AkinatorView(ctx, aki)

        ohk=bar.write_progress(**DiscordTemplates.DEFAULT)
        em=discord.Embed(color=Utils.BotColors.invis())
        em.set_author(name='Akinator', icon_url='https://play-lh.googleusercontent.com/rjX8LZCV-MaY3o927R59GkEwDOIRLGCXFphaOTeFFzNiYY6SQ4a-B_5t7eUPlGANrcw')
        em.set_thumbnail(url='https://pbs.twimg.com/profile_images/1206579384762679299/hbixlO64_400x400.jpg')
        em.add_field(name='Question', value=f'{q}', inline=False)
        em.add_field(name='Progress', value=f'{ohk}', inline=False)
        await MainMessage.edit(embed=em, view=Mainview)

        _main_wait = await Mainview.wait()
        if _main_wait:
            return

        while aki.progression <= 80:
            bar=ProgressBar(
                aki.progression,
                100
            )

            progress=bar.write_progress(**DiscordTemplates.DEFAULT)

            LastView = AkinatorComponents.AkinatorView(ctx, aki)
            _last_wait = await LastView.wait()
            if _last_wait:
                return
            q = LastView._q
            interaction: discord.Interaction = LastView._interaction

            em=discord.Embed(color=Utils.BotColors.invis())
            em.set_author(name='Akinator', icon_url='https://play-lh.googleusercontent.com/rjX8LZCV-MaY3o927R59GkEwDOIRLGCXFphaOTeFFzNiYY6SQ4a-B_5t7eUPlGANrcw')
            em.set_thumbnail(url='https://pbs.twimg.com/profile_images/1206579384762679299/hbixlO64_400x400.jpg')
            em.add_field(name='Question', value=f'{q}', inline=False)
            em.add_field(name='Progress', value=f'{progress}', inline=False)
            await interaction.response.edit_message(embed = em, view = LastView)

        await aki.win()
        _des=aki.first_guess['description']
        _title=aki.first_guess['name']
        _img=aki.first_guess['absolute_picture_path']


        NSFWDESC=['Porn actress']


        if _des in NSFWDESC:
            _img='https://i.pinimg.com/564x/ea/06/78/ea0678165c05e77cc6d0c91f81e7bd0c.jpg'

        if not _img:
            _img='https://i.pinimg.com/564x/ea/06/78/ea0678165c05e77cc6d0c91f81e7bd0c.jpg'

        YesOrNoCompo=[[
            Button(label='Yes', id='AkiCorrect', emoji=self.client.get_emoji(910490899883126804)),
            Button(label='No', id='AkiWrong', emoji=self.client.get_emoji(910491193174028308))
        ]]
        YesCompo=[[
            Button(label='Yes', id='AkiCorrect', style=ButtonStyle.green, disabled=True, emoji=self.client.get_emoji(910490899883126804)),
            Button(label='No', id='AkiWrong', disabled=True, emoji=self.client.get_emoji(910491193174028308))
        ]]
        NoCompo=[[
            Button(label='Yes', id='AkiCorrect', disabled=True, emoji=self.client.get_emoji(910490899883126804)),
            Button(label='No', id='AkiWrong', style=ButtonStyle.red, disabled=True, emoji=self.client.get_emoji(910491193174028308))
        ]]

        em=discord.Embed(title=f'{_title}', description=f'{_des}', color=Utils.BotColors.invis())
        em.set_image(url=f'{_img}')
        em.set_thumbnail(url='https://en.akinator.com/bundles/elokencesite/images/akinator.png?v94')
        em.set_author(name='Akinator', icon_url='https://play-lh.googleusercontent.com/rjX8LZCV-MaY3o927R59GkEwDOIRLGCXFphaOTeFFzNiYY6SQ4a-B_5t7eUPlGANrcw')
        await MainMessage.edit(embed=em, components=YesOrNoCompo)
        while True:
            try:
                YesOrNoEvent=await self.client.wait_for('button_click', check=lambda i: i.channel==ctx.channel and i.message==MainMessage, timeout=10)
                if YesOrNoEvent.author != ctx.author:
                    await event.respond(type=4, content='Sorry, this is not your game and you cannot interact with these buttons.')
                    continue
                elif YesOrNoEvent.component.id=='AkiCorrect':
                    await YesOrNoEvent.respond(type=4, ephemeral=False, content='🎉 Great, guessed right one more time! It was fun to play with you!')
                    await MainMessage.edit(components=YesCompo)
                    break
                elif YesOrNoEvent.component.id=='AkiWrong':
                    await YesOrNoEvent.respond(type=4, ephemeral=False, content='Bravo, you have defeated me! Play again?')
                    await MainMessage.edit(components=NoCompo)
                    break
            except:
                DisableMessage=await MainMessage.channel.fetch_message(MainMessage.id)
                await DisableMessage.disable_components()
                break

        await aki.close()