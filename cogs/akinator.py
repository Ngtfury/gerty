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
import discord_components
from discord_components import *


def setup(bot):
    bot.add_cog(AkinatorCog(bot))

class AkinatorCog(commands.Cog):
    def __init__(self, bot):
        self.client=bot



    @commands.command(name='akinator', brief='fun', description='Attempts to determine what character  you is thinking of by asking a series of questions', aliases=['aki'])
    @commands.max_concurrency(1, per=commands.BucketType.channel)
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
        MainMessage=await ctx.send(embed=StartGame, components=StartComponents)


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



        components=[[
            Button(style=ButtonStyle.green, label='Yes', id='AkiYes'),
            Button(label='No', id='AkiNo'),
            Button(label='I don\'t know', id='AkiIdk', style=ButtonStyle.blue),
            Button(style=ButtonStyle.green, label='Probably', id='AkiProbably'),
            Button(label='Probably not', id='AkiProbablyNot')
        ], Button(style=ButtonStyle.red, label='Quit', id='AkiQuit')]


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
        await MainMessage.edit(embed=em, components=components)

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
                    await event.respond(type=7, embed=em)
                    continue
                elif event.component.id=='AkiNo':
                    await event.respond(type=6)
                    q=await aki.answer('no')
                    em=discord.Embed(color=Utils.BotColors.invis())
                    em.set_author(name='Akinator', icon_url='https://play-lh.googleusercontent.com/rjX8LZCV-MaY3o927R59GkEwDOIRLGCXFphaOTeFFzNiYY6SQ4a-B_5t7eUPlGANrcw')
                    em.set_thumbnail(url='https://pbs.twimg.com/profile_images/1206579384762679299/hbixlO64_400x400.jpg')
                    em.add_field(name='Question', value=f'{q}', inline=False)
                    em.add_field(name='Progress', value=f'{progress}', inline=False)
                    await event.respond(type=7, embed=em)
                    continue
                elif event.component.id=='AkiProbably':
                    await event.respond(type=6)
                    q=await aki.answer('Probably')
                    em=discord.Embed(color=Utils.BotColors.invis())
                    em.set_author(name='Akinator', icon_url='https://play-lh.googleusercontent.com/rjX8LZCV-MaY3o927R59GkEwDOIRLGCXFphaOTeFFzNiYY6SQ4a-B_5t7eUPlGANrcw')
                    em.set_thumbnail(url='https://pbs.twimg.com/profile_images/1206579384762679299/hbixlO64_400x400.jpg')
                    em.add_field(name='Question', value=f'{q}', inline=False)
                    em.add_field(name='Progress', value=f'{progress}', inline=False)
                    await event.respond(type=7, embed=em)
                    continue
                elif event.component.id=='AkiProbablyNot':
                    await event.respond(type=6)
                    q=await aki.answer('Probably not')
                    em=discord.Embed(color=Utils.BotColors.invis())
                    em.set_author(name='Akinator', icon_url='https://play-lh.googleusercontent.com/rjX8LZCV-MaY3o927R59GkEwDOIRLGCXFphaOTeFFzNiYY6SQ4a-B_5t7eUPlGANrcw')
                    em.set_thumbnail(url='https://pbs.twimg.com/profile_images/1206579384762679299/hbixlO64_400x400.jpg')
                    em.add_field(name='Question', value=f'{q}', inline=False)
                    em.add_field(name='Progress', value=f'{progress}', inline=False)
                    await event.respond(type=7, embed=em)
                    continue
                elif event.component.id=='AkiIdk':
                    await event.respond(type=6)
                    q=await aki.answer('idk')
                    em=discord.Embed(color=Utils.BotColors.invis())
                    em.set_author(name='Akinator', icon_url='https://play-lh.googleusercontent.com/rjX8LZCV-MaY3o927R59GkEwDOIRLGCXFphaOTeFFzNiYY6SQ4a-B_5t7eUPlGANrcw')
                    em.set_thumbnail(url='https://pbs.twimg.com/profile_images/1206579384762679299/hbixlO64_400x400.jpg')
                    em.add_field(name='Question', value=f'{q}', inline=False)
                    em.add_field(name='Progress', value=f'{progress}', inline=False)
                    await event.respond(type=7, embed=em)
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

        NSFW=['Mia Khalifa']

        if _title in NSFW:
            _img='https://c.tenor.com/x8v1oNUOmg4AAAAM/rickroll-roll.gif'

        YesOrNoCompo=[[
            Button(style=ButtonStyle.green, label='Yes', id='AkiCorrect'),
            Button(style=ButtonStyle.red, label='No', id='AkiWrong')
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
                    await YesOrNoEvent.respond(type=4, ephemeral=False, content='🎉 Great, guessed right one more time !. It was fun to play with you!')
                    DisableMessage=await MainMessage.channel.fetch_message(MainMessage.id)
                    await DisableMessage.disable_components()
                    break
                elif YesOrNoEvent.component.id=='AkiWrong':
                    await YesOrNoEvent.respond(type=4, ephemeral=False, content='Bravo, you have defeated me !')
                    DisableMessage=await MainMessage.channel.fetch_message(MainMessage.id)
                    await DisableMessage.disable_components()
                    break
            except:
                DisableMessage=await MainMessage.channel.fetch_message(MainMessage.id)
                await DisableMessage.disable_components()
                break

        await aki.close()