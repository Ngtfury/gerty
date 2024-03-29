import discord
from discord.ext import commands
import datetime
import asyncio
import random

def setup(client):
    client.add_cog(Giveaways(client))





class Giveaways(commands.Cog):
    def __init__(self, bot):
        self.bot=bot


    def convert(self, time):
        pos = ["s","m","h","d"]

        time_dict = {"s" : 1, "m" : 60, "h" : 3600, "d" : 3600*24}

        unit = time[-1]

        if unit not in pos:
            return -1
        try:
            val = int(time[:-1])
        except:
            return -2


        return val * time_dict[unit]



    @commands.command(brief='mod', description='Starts a giveaway event', usage='[time] [winners] [prize]')
    @commands.has_permissions(manage_channels=True)
    async def gstart(self, ctx, time, winners:int, *, prize):
        if winners <= 0:
            return await ctx.send('There must be at least 1 winner')
        if winners > 5:
            return await ctx.send('5 winners is maximum for this giveaway') 
        timenow=int(datetime.datetime.now().timestamp())

        time=self.convert(time)
        if time == -1:
            return await ctx.send("You didn't answer the proper unit. Use (s|m|h|d) next time!")
        elif time==-2:
            return await ctx.send('The time must be an integer. Please enter an integer next time')

        try:
            await ctx.message.delete()
        except:
            pass

        firstembed=discord.Embed(description='<a:timer:905859476257656872> **Loading giveaway** <a:timer:905859476257656872>', color=0x2F3136)
        main_message=await ctx.send(embed=firstembed)
        await asyncio.sleep(1)
        
        em=discord.Embed(description=f'<:prize:905859038317776926> **Prize: {prize}**\n<a:timer:905859476257656872> Timer: <t:{timenow+time}:R> <t:{timenow+time}:T>\n<:winner:905859555852967946> Winners: {winners}\nHost: {ctx.author.mention}\n\nReact with 🎉 to participate!\nTo reroll the giveaway, type:\n`g!greroll {main_message.id}`', color=0x2F3136)
        em.set_author(name=f'{ctx.guild.name} Giveaways!', icon_url=ctx.guild.icon.url)
        em.set_image(url='https://i.imgur.com/USGQsyz.png')
        await main_message.edit('🎉 **GIVEAWAY** 🎉', embed=em)
        await main_message.add_reaction('🎉')

        await asyncio.sleep(time)
        ok_message=await ctx.channel.fetch_message(main_message.id)
        entries=await ok_message.reactions[0].users().flatten()
        entries.pop(entries.index(self.bot.user))

        if len(entries) < winners:
            noentries=discord.Embed(description=f'<:prize:905859038317776926> **Prize: {prize}**\n<:winner:905859555852967946> Host: {ctx.author.mention}\n\nGiveaway cancelled, no valid participations.\nMust be at least **{winners}** participation(s)', color=0x2F3136)
            noentries.set_author(name=f'{ctx.guild.name} Giveaways!', icon_url=ctx.guild.icon.url)
            noentries.set_image(url='https://i.imgur.com/USGQsyz.png')
            return await main_message.edit('🎉 **GIVEAWAY CANCELLED** 🎉', embed=noentries)

        win2=[]
        for x in range(winners):
            winner=random.choice(entries)
            win2.append(winner.mention)
            entries.pop(entries.index(winner))

            lastembed=discord.Embed(description=f'**🎉 [Link to giveaway]({main_message.jump_url}) | [Invite me!]({discord.utils.oauth_url(self.bot.user.id)})**', color=0x2F3136)
            await ctx.send(f'Congratulations 🎉 {winner.mention}! You won **{prize}**!', embed=lastembed)
            await asyncio.sleep(0.5)
        winners2=' '.join(win2)
        lwjgbw=discord.Embed(description=f'<:prize:905859038317776926> **Prize: {prize}**\n<a:timer:905859476257656872> Ended: <t:{timenow+time}:R> <t:{timenow+time}:T>\n<:winner:905859555852967946> Winners: {winners2}\nHost: {ctx.author.mention}\n\n\nTo reroll the giveaway, type:\n`g!greroll {main_message.id}`', color=0x2F3136)
        lwjgbw.set_author(name=f'{ctx.guild.name} Giveaways!', icon_url=ctx.guild.icon.url)
        lwjgbw.set_image(url='https://i.imgur.com/USGQsyz.png')
        await main_message.edit('🎉 **GIVEAWAY ENDED** 🎉', embed=lwjgbw)


    @commands.command(brief='mod', description='Rerolls a giveaway that ended', usage='[message ID]')
    @commands.has_permissions(manage_channels=True)
    async def greroll(self, ctx, message_id:discord.Message):
        if message_id.author != self.bot.user:
            return await ctx.send('That is not a message sent by me!')

        if not message_id.content.startswith('🎉 **GIVEAWAY ENDED** 🎉'):
            return await ctx.send('This is not a giveaway message or this giveaway must end first to reroll')

        message=await message_id.channel.fetch_message(message_id.id)
        entries=await message.reactions[0].users().flatten()
        entries.pop(entries.index(self.bot.user))

        winner=random.choice(entries)

        lastembed=discord.Embed(description=f'**🎉 [Link to giveaway]({message.jump_url}) | [Invite me!]({discord.utils.oauth_url(self.bot.user.id)})**', color=0x2F3136)
        await ctx.send(f'Congratulations the new winner is 🎉 {winner.mention}!', embed=lastembed)
