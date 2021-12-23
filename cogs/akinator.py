import discord
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

    class AkinatorView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=60)

        async def on_timeout(self):
            for children in self.children:
                children.disabled = True

            await self.message.edit(view = self)

        async def interaction_check(self, interaction: discord.Interaction):
            if interaction.author.id != self.ctx.author.id:
                await interaction.response.send_message('Sorry, this is not your game and you cannot interact with these buttons.', ephemeral=True)
                return False
            return True

    class AkiCharButton(discord.ui.Button):
        def __init__(self, aki):
            super().__init__(
                style = discord.ButtonStyle.gray,
                label = 'Character',
            )
            self.aki = aki

        async def callback(self, interaction: discord.Interaction):
            q=await self.aki.start_game(language=None, child_mode=True)
            em=discord.Embed(description=f'{Utils.BotEmojis.loading()} Loading akinator... Please wait', color=Utils.BotColors.invis())
            await interaction.response.edit_message(embed = em)
            return q

    class AkiAnimalButton(discord.ui.Button):
        def __init__(self, aki):
            super().__init__(
                style=discord.ButtonStyle.gray,
                label = 'Animal'
            )
            self.aki = aki

        async def callback(self, interaction: discord.Interaction):
            q=await self.aki.start_game(language='en_animals', child_mode=True)
            em=discord.Embed(description=f'{Utils.BotEmojis.loading()} Loading akinator... Please wait', color=Utils.BotColors.invis())
            compos = interaction.message.components
            for compo in compos:
                for children in compo.children:
                    children.disabled = True
            await interaction.response.edit_message(embed = em, view = compos)
            return q

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

        StartComponents=[[
            Button(label='Character', id='AkiCharacter'),
            Button(label='Animal', id='AkiAnimal'),
            Button(label='Object', id='AkiObject')
        ]]
        CharecterCompo=[[
            Button(label='Character', id='AkiCharacter', style=ButtonStyle.green, disabled=True),
            Button(label='Animal', id='AkiAnimal', disabled=True),
            Button(label='Object', id='AkiObject', disabled=True)
        ]]
        AnimalCompo=[[
            Button(label='Character', id='AkiCharacter', disabled=True),
            Button(label='Animal', id='AkiAnimal', disabled=True, style=ButtonStyle.green),
            Button(label='Object', id='AkiObject', disabled=True)
        ]]
        ObjCompo=[[
            Button(label='Character', id='AkiCharacter', disabled=True),
            Button(label='Animal', id='AkiAnimal', disabled=True),
            Button(label='Object', id='AkiObject', disabled=True, style=ButtonStyle.green)
        ]]


        StartGame=discord.Embed(description='Please select an option what you are guessing.', color=Utils.BotColors.invis())
        StartGame.set_thumbnail(url='https://en.akinator.com/bundles/elokencesite/images/akinator.png?v94')
        StartGame.set_author(name='Akinator', icon_url='https://play-lh.googleusercontent.com/rjX8LZCV-MaY3o927R59GkEwDOIRLGCXFphaOTeFFzNiYY6SQ4a-B_5t7eUPlGANrcw')
        MainMessage=await ctx.reply(embed=StartGame, components=StartComponents, mention_author=False)


        while True:
            try:
                AkiStartEvent=await self.client.wait_for('button_click', check=lambda i: i.channel==ctx.channel and i.message==MainMessage, timeout=20)
                if AkiStartEvent.author != ctx.author:
                    await AkiStartEvent.respond(type=4, content='Sorry, this is not your game and you cannot interact with these buttons.')
                    continue
                if AkiStartEvent.component.id=='AkiCharacter':
                    em=discord.Embed(description=f'{Utils.BotEmojis.loading()} Loading akinator... Please wait', color=Utils.BotColors.invis())
                    await AkiStartEvent.respond(type=7, embed=em, components=CharecterCompo)
                    q=await aki.start_game(language=None, child_mode=True)
                    break
                elif AkiStartEvent.component.id=='AkiAnimal':
                    em=discord.Embed(description=f'{Utils.BotEmojis.loading()} Loading akinator... Please wait', color=Utils.BotColors.invis())
                    await AkiStartEvent.respond(type=7, embed=em, components=AnimalCompo)
                    q=await aki.start_game(language='en_animals', child_mode=True)
                    break
                elif AkiStartEvent.component.id=='AkiObject':
                    em=discord.Embed(description=f'{Utils.BotEmojis.loading()} Loading akinator... Please wait', color=Utils.BotColors.invis())
                    await AkiStartEvent.respond(type=7, embed=em, components=ObjCompo)
                    q=await aki.start_game(language='en_objects', child_mode=True)
                    break
            except:
                await MainMessage.disable_components()
                return


        FirstCompoNents=[[
            Button(style=ButtonStyle.green, label='Yes', id='AkiYes'),
            Button(label='No', id='AkiNo'),
            Button(label='Don\'t know', id='AkiIdk', style=ButtonStyle.blue),
            Button(style=ButtonStyle.green, label='Probably', id='AkiProbably'),
            Button(label='Probably not', id='AkiProbablyNot')
        ], [Button(label='Back', disabled=True, id='AkiBack'), Button(style=ButtonStyle.red, label='Quit', id='AkiQuit')]]


        components=[[
            Button(style=ButtonStyle.green, label='Yes', id='AkiYes'),
            Button(label='No', id='AkiNo'),
            Button(label='Don\'t know', id='AkiIdk', style=ButtonStyle.blue),
            Button(style=ButtonStyle.green, label='Probably', id='AkiProbably'),
            Button(label='Probably not', id='AkiProbablyNot')
        ], [Button(label='Back', id='AkiBack', style=ButtonStyle.blue), Button(style=ButtonStyle.red, label='Quit', id='AkiQuit')]]


        bar=ProgressBar(
            aki.progression,
            80
        )

        ohk=bar.write_progress(**DiscordTemplates.DEFAULT)
        em=discord.Embed(color=Utils.BotColors.invis())
        em.set_author(name='Akinator', icon_url='https://play-lh.googleusercontent.com/rjX8LZCV-MaY3o927R59GkEwDOIRLGCXFphaOTeFFzNiYY6SQ4a-B_5t7eUPlGANrcw')
        em.set_thumbnail(url='https://pbs.twimg.com/profile_images/1206579384762679299/hbixlO64_400x400.jpg')
        em.add_field(name='Question', value=f'{q}', inline=False)
        em.add_field(name='Progress', value=f'{ohk}', inline=False)
        await MainMessage.edit(embed=em, components=FirstCompoNents)

        while aki.progression <= 80:
            bar=ProgressBar(
                aki.progression,
                100
            )

            progress=bar.write_progress(**DiscordTemplates.DEFAULT)

            try:
                event=await self.client.wait_for('button_click', check=lambda i: i.channel==ctx.channel and i.message==MainMessage, timeout=40)
                if event.author != ctx.author:
                    await event.respond(type=4, content='Sorry, this is not your game and you cannot interact with these buttons.')
                    continue
                if event.component.id=='AkiYes':
                    await event.respond(type=6)
                    q=await aki.answer('yes')
                    em=discord.Embed(color=Utils.BotColors.invis())
                    em.set_author(name='Akinator', icon_url='https://play-lh.googleusercontent.com/rjX8LZCV-MaY3o927R59GkEwDOIRLGCXFphaOTeFFzNiYY6SQ4a-B_5t7eUPlGANrcw')
                    em.set_thumbnail(url='https://pbs.twimg.com/profile_images/1206579384762679299/hbixlO64_400x400.jpg')
                    em.add_field(name='Question', value=f'{q}', inline=False)
                    em.add_field(name='Progress', value=f'{progress}', inline=False)
                    await event.respond(type=7, embed=em, components=components)
                    continue
                elif event.component.id=='AkiNo':
                    await event.respond(type=6)
                    q=await aki.answer('no')
                    em=discord.Embed(color=Utils.BotColors.invis())
                    em.set_author(name='Akinator', icon_url='https://play-lh.googleusercontent.com/rjX8LZCV-MaY3o927R59GkEwDOIRLGCXFphaOTeFFzNiYY6SQ4a-B_5t7eUPlGANrcw')
                    em.set_thumbnail(url='https://pbs.twimg.com/profile_images/1206579384762679299/hbixlO64_400x400.jpg')
                    em.add_field(name='Question', value=f'{q}', inline=False)
                    em.add_field(name='Progress', value=f'{progress}', inline=False)
                    await event.respond(type=7, embed=em, components=components)
                    continue
                elif event.component.id=='AkiProbably':
                    await event.respond(type=6)
                    q=await aki.answer('Probably')
                    em=discord.Embed(color=Utils.BotColors.invis())
                    em.set_author(name='Akinator', icon_url='https://play-lh.googleusercontent.com/rjX8LZCV-MaY3o927R59GkEwDOIRLGCXFphaOTeFFzNiYY6SQ4a-B_5t7eUPlGANrcw')
                    em.set_thumbnail(url='https://pbs.twimg.com/profile_images/1206579384762679299/hbixlO64_400x400.jpg')
                    em.add_field(name='Question', value=f'{q}', inline=False)
                    em.add_field(name='Progress', value=f'{progress}', inline=False)
                    await event.respond(type=7, embed=em, components=components)
                    continue
                elif event.component.id=='AkiProbablyNot':
                    await event.respond(type=6)
                    q=await aki.answer('Probably not')
                    em=discord.Embed(color=Utils.BotColors.invis())
                    em.set_author(name='Akinator', icon_url='https://play-lh.googleusercontent.com/rjX8LZCV-MaY3o927R59GkEwDOIRLGCXFphaOTeFFzNiYY6SQ4a-B_5t7eUPlGANrcw')
                    em.set_thumbnail(url='https://pbs.twimg.com/profile_images/1206579384762679299/hbixlO64_400x400.jpg')
                    em.add_field(name='Question', value=f'{q}', inline=False)
                    em.add_field(name='Progress', value=f'{progress}', inline=False)
                    await event.respond(type=7, embed=em, components=components)
                    continue
                elif event.component.id=='AkiIdk':
                    await event.respond(type=6)
                    q=await aki.answer('idk')
                    em=discord.Embed(color=Utils.BotColors.invis())
                    em.set_author(name='Akinator', icon_url='https://play-lh.googleusercontent.com/rjX8LZCV-MaY3o927R59GkEwDOIRLGCXFphaOTeFFzNiYY6SQ4a-B_5t7eUPlGANrcw')
                    em.set_thumbnail(url='https://pbs.twimg.com/profile_images/1206579384762679299/hbixlO64_400x400.jpg')
                    em.add_field(name='Question', value=f'{q}', inline=False)
                    em.add_field(name='Progress', value=f'{progress}', inline=False)
                    await event.respond(type=7, embed=em, components=components)
                    continue
                elif event.component.id=='AkiBack':
                    await event.respond(type=6)
                    try:
                        q = await aki.back()
                        em=discord.Embed(color=Utils.BotColors.invis())
                        em.set_author(name='Akinator', icon_url='https://play-lh.googleusercontent.com/rjX8LZCV-MaY3o927R59GkEwDOIRLGCXFphaOTeFFzNiYY6SQ4a-B_5t7eUPlGANrcw')
                        em.set_thumbnail(url='https://pbs.twimg.com/profile_images/1206579384762679299/hbixlO64_400x400.jpg')
                        em.add_field(name='Question', value=f'{q}', inline=False)
                        em.add_field(name='Progress', value=f'{progress}', inline=False)
                        await event.respond(type=7, embed=em, components=components)
                        continue
                    except akinator.CantGoBackAnyFurther:
                        em=discord.Embed(color=Utils.BotColors.invis())
                        em.set_author(name='Akinator', icon_url='https://play-lh.googleusercontent.com/rjX8LZCV-MaY3o927R59GkEwDOIRLGCXFphaOTeFFzNiYY6SQ4a-B_5t7eUPlGANrcw')
                        em.set_thumbnail(url='https://pbs.twimg.com/profile_images/1206579384762679299/hbixlO64_400x400.jpg')
                        em.add_field(name='Question', value=f'{q}', inline=False)
                        em.add_field(name='Progress', value=f'{progress}', inline=False)
                        await event.respond(type=7, embed=em, components=FirstCompoNents)
                        continue     
                elif event.component.id=='AkiQuit':
                    await event.respond(type=6)
                    break
            except asyncio.TimeoutError:
                break
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