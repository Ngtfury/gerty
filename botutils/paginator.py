import discord
from discord import *
from discord.ext import commands
import discord_components
from discord_components import *
import asyncio


class Paginator:
    def __init__(self, ctx:commands.Context, embeds:list, content=None, timeout:int=20):
        self.embeds=embeds
        self.timeout=timeout
        self.content=content
        self.ctx=ctx
        self.bot=commands.AutoShardedBot
        self.current=1


    async def disable_check(self) -> None:
        if self.current==1 and len(self.embeds)==1:
            right_disable=True
            left_disable=True
        elif self.current==1 and not len(self.embeds)==1:
            right_disable=False
            left_disable=True
        elif self.current==len(self.embeds):
            right_disable=True
            left_disable=False
        else:
            right_disable=False
            left_disable=False
        return right_disable, left_disable


    async def start(self):
        right_disable, left_disable=await self.disable_check()
        current=self.current
        embed=self.embeds[current]
        MainMessage=await self.ctx.send(
            content=self.content,
            embed=embed,
            components=[[Button(style=ButtonStyle.green, label='<', id='ButtonLeft', disabled=left_disable), Button(style=ButtonStyle.gray, label=f'{int(self.embeds.index(self.embeds[current])) + 1}/{len(self.embeds)}', disabled=True), Button(style=ButtonStyle.green, label='>', id='ButtonRight', disabled=right_disable)]]
        )
        while True:
            right_disable2, left_disable2=await self.disable_check()
            try:
                event=asyncio.ensure_future(self.bot.wait_for(self, event="button_click", check=lambda i: i.channel==self.ctx.channel and i.component.id in ['ButtonLeft', 'ButtonRight']))
                if event.component.id=='ButtonLeft':
                    current-=1
                elif event.component.id=='ButtonRight':
                    current+=1

                await event.respond(
                    type=7,
                    embed=self.embeds[current],
                    components=[[Button(style=ButtonStyle.green, label='<', id='ButtonLeft', disabled=left_disable2), Button(style=ButtonStyle.gray, label=f'{int(self.embeds.index(self.embeds[current])) + 1}/{len(self.embeds)}', disabled=True), Button(style=ButtonStyle.green, label='>', id='ButtonRight', disabled=right_disable2)]]
                )
            except asyncio.TimeoutError:
                await MainMessage.disable_components()
                break
                
