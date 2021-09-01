import discord
from discord import client
from discord.ext import commands
import random
import json
import time
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_choice, create_option


class AFK(commands.Cog):

    def __init__(self, client):
        self.client = client
    #*
    async def update_data(self, afk, user):
        if not f'{user.id}' in afk:
            afk[f'{user.id}'] = {}
            afk[f'{user.id}']['AFK'] = 'False'
            afk[f'{user.id}']['reason'] = 'None'
    
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
        with open('afk.json', 'r') as f:
            afk = json.load(f)
        
        for user_mention in message.mentions:
            if afk[f'{user_mention.id}']['AFK'] == 'True':
                if message.author.bot: 
                    return
                
                reason = afk[f'{user_mention.id}']['reason']
                meth = int(time.time()) - int(afk[f'{user_mention.id}']['time'])
                been_afk_for = await self.time_formatter(meth)
                
                await message.channel.send(f'{message.author.mention} {user_mention.name} Is currently AFK: {reason} | For: {been_afk_for}')
                
                meeeth = int(afk[f'{user_mention.id}']['mentions']) + 1
                afk[f'{user_mention.id}']['mentions'] = meeeth
                with open('afk.json', 'w') as f:
                    json.dump(afk, f)
        
        if not message.author.bot:
            await self.update_data(afk, message.author)

            if afk[f'{message.author.id}']['AFK'] == 'True':
                
                meth = int(time.time()) - int(afk[f'{message.author.id}']['time'])
                been_afk_for = await self.time_formatter(meth)
                mentionz = afk[f'{message.author.id}']['mentions']

              

                await message.channel.send(f'Welcome Back {message.author.name}! | You\'ve been AFK for: {been_afk_for} | No. of mentions: {mentionz}')
                
                afk[f'{message.author.id}']['AFK'] = 'False'
                afk[f'{message.author.id}']['reason'] = 'None'
                afk[f'{message.author.id}']['time'] = '0'
                afk[f'{message.author.id}']['mentions'] = 0
                
                with open('afk.json', 'w') as f:
                    json.dump(afk, f)
                
                try:
                    await message.author.edit(nick=f'{message.author.display_name[5:]}')
                except:
                    print(f'I wasnt able to edit [{message.author}].')
        
        with open('afk.json', 'w') as f:
            json.dump(afk, f)
    

    @commands.command(aliases=["afkset"])
    async def afk(self, ctx, *, reason=None):
        with open('afk.json', 'r') as f:
            afk = json.load(f)

        if not reason:
            reason = 'None'
        
        await self.update_data(afk, ctx.message.author)
        afk[f'{ctx.author.id}']['AFK'] = 'True'
        afk[f'{ctx.author.id}']['reason'] = f'{reason}'
        afk[f'{ctx.author.id}']['time'] = int(time.time())
        afk[f'{ctx.author.id}']['mentions'] = 0

        
        await ctx.send(f"I've set your AFK {ctx.message.author.name}!: {reason}")

        with open('afk.json', 'w') as f:
            json.dump(afk, f)
        try:
            await ctx.author.edit(nick=f'[AFK] {ctx.author.display_name}')
        except:
            print(f'I wasnt able to edit [{ctx.message.author}].')

def setup(client):
    client.add_cog(AFK(client))
