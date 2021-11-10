import discord
from discord import client
from discord.ext import commands
import random
import json
import time
import asyncio


class AFK(commands.Cog):

    def __init__(self, client):
        self.client = client
    #*
    async def update_data(self, afk, user):
        if not f'{user.id}' in afk:
            afk[f'{user.id}'] = {}
            afk[f'{user.id}']['AFK'] = 'False'
            afk[f'{user.id}']['reason'] = 'None'
            afk[f'{user.id}']['guild'] = 'None'
    
    async def time_formatter(self, seconds: float):

        minutes, seconds = divmod(int(seconds), 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        tmp = ((str(days) + "d, ") if days else "") + \
            ((str(hours) + "h, ") if hours else "") + \
            ((str(minutes) + "m, ") if minutes else "") + \
            ((str(seconds) + "s, ") if seconds else "")
        return tmp[:-2]
    
    @commands.Cog.listener()
    async def on_message(self, message):
        with open('data/afk.json', 'r') as f:
            afk = json.load(f)
        try:
            for user_mention in message.mentions:
                if afk[f'{user_mention.id}']['AFK'] == 'True' and afk[f'{user_mention.id}']['guild'] == f'{message.guild.id}':
                    if message.author.bot:
                        return
                    
                    reason = afk[f'{user_mention.id}']['reason']
                    meth = int(time.time()) - int(afk[f'{user_mention.id}']['time'])
                    been_afk_for = await self.time_formatter(meth)

                    embed=discord.Embed(description=f"{reason}", color=0x2F3136)
                    await message.channel.send(f'{message.author.mention}, **{user_mention.name}** went AFK <a:afk:890119774015717406> `{been_afk_for}` ago:', embed=embed)
                    
                    meeeth = int(afk[f'{user_mention.id}']['mentions']) + 1
                    afk[f'{user_mention.id}']['mentions'] = meeeth
                    with open('data/afk.json', 'w') as f:
                        json.dump(afk, f)
        except:
            pass
        
        if not message.author.bot:
            try:
                await self.update_data(afk, message.author)

                if afk[f'{message.author.id}']['AFK'] == 'True' and afk[f'{message.author.id}']['guild'] == f'{message.guild.id}':
                    
                    meth = int(time.time()) - int(afk[f'{message.author.id}']['time'])
                    been_afk_for = await self.time_formatter(meth)
                    mentionz = afk[f'{message.author.id}']['mentions']

                
                    emb = discord.Embed(description=f"<a:afk:890119774015717406> You've been AFK for: `{been_afk_for}`. And you were pinged **{mentionz}** time(s)", color=0x2F3136)
                    await message.channel.send(f'{message.author.mention} Welcome Back!', embed=emb)
                    
                    afk[f'{message.author.id}']['AFK'] = 'False'
                    afk[f'{message.author.id}']['reason'] = 'None'
                    afk[f'{message.author.id}']['time'] = '0'
                    afk[f'{message.author.id}']['mentions'] = 0
                    afk[f'{message.author.id}']['guild'] = 'None'
                    
                    with open('data/afk.json', 'w') as f:
                        json.dump(afk, f)
            except:
                pass
                
                try:
                    await message.author.edit(nick=f'{message.author.display_name[5:]}')
                except:
                    pass
        
        with open('data/afk.json', 'w') as f:
            json.dump(afk, f)
    

    @commands.command(brief='meta', description='Sets user stats as afk', usage='(reason)', aliases=["afkset"])
    async def afk(self, ctx, *, reason=None):
        if reason == None:
            reason = "AFK"
        with open('data/afk.json', 'r') as f:
            afk = json.load(f)
        
        await self.update_data(afk, ctx.message.author)
        afk[f'{ctx.author.id}']['AFK'] = 'True'
        afk[f'{ctx.author.id}']['reason'] = f'{reason}'
        afk[f'{ctx.author.id}']['time'] = int(time.time())
        afk[f'{ctx.author.id}']['mentions'] = 0
        afk[f'{ctx.author.id}']['guild'] = f'{ctx.guild.id}'

        em = discord.Embed(description=f"{reason}", color=0x2F3136)
        await ctx.send(f"{ctx.author.mention} I've set you as AFK <a:afk:890119774015717406>:", embed=em)

        await asyncio.sleep(5)
        with open('data/afk.json', 'w') as f:
            json.dump(afk, f)
        try:
            await ctx.author.edit(nick=f'[AFK] {ctx.author.display_name}')
        except:
            pass
        
def setup(client):
    client.add_cog(AFK(client))
