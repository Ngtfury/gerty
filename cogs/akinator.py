import discord
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
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def _akinator(self,ctx):
        em=discord.Embed(description=f'{Utils.BotEmojis.loading()} Loading akinator... Please wait', color=Utils.BotColors.invis())
        MainMessage=await ctx.send(embed=em)

        components=[[
            Button(style=ButtonStyle.green, label='Yes', id='AkiYes'),
            Button(label='No', id='AkiNo'),
            Button(label='I Don\'t know', id='AkiIdk'),
            Button(style=ButtonStyle.green, label='Probably', id='AkiProbably'),
            Button(label='Probably not', id='AkiProbablyNot')
        ], Button(style=ButtonStyle.red, label='Quit', id='AkiQuit')]

        aki=Akinator()

        q=await aki.start_game()

        bar=ProgressBar(
            aki.progression,
            100
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
                event=await self.client.wait_for('button_click', check=lambda i: i.channel==ctx.channel and i.author==ctx.author and i.message==MainMessage, timeout=40)
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
        em=discord.Embed(title=f'{_title}', description=f'{_des}', color=Utils.BotColors.invis())
        em.set_image(url=f'{_img}')
        em.set_thumbnail(url='https://pbs.twimg.com/profile_images/1206579384762679299/hbixlO64_400x400.jpg')
        em.set_author(name='Akinator', icon_url='https://play-lh.googleusercontent.com/rjX8LZCV-MaY3o927R59GkEwDOIRLGCXFphaOTeFFzNiYY6SQ4a-B_5t7eUPlGANrcw')
        await MainMessage.edit(embed=em)
        await MainMessage.disable_components()
        await aki.close()