import discord
from discord.ext import commands
import discord_components
from discord_components import *
import asyncio


def setup(client):
    client.add_cog(EmbedEditor(client))

class EmbedEditor(commands.Cog):
    def __init__(self, bot):
        self.bot=bot


    async def set_title(message: discord.Message, content):
        FetchedMessage=await message.channel.fetch_message(message.id)
        Embed=FetchedMessage.embeds[0]
        Embed.title=content

        return await message.edit(embed=Embed)


    async def set_description(message: discord.Message, content):
        FetchedMessage=await message.channel.fetch_message(message.id)
        Embed=FetchedMessage.embeds[0]
        Embed.description=content

        return await message.edit(embed=Embed)


    @commands.command(brief='fun', description='Dynamic embed editor')
    async def embed(self, ctx):

        SelectOptions=[
            SelectOption(label='Set Title', value='SetTitle'),
            SelectOption(label='Set Description', value='SetDesc')
        ]

        MainMessage=await ctx.send(embed=discord.Embed(title='Title', description='Description'), components=[Select(placeholder='Dynamic embed editor', options=SelectOptions)])

        while True:
            try:

                interaction=await self.bot.wait_for('interaction', check=lambda i: i.author==ctx.author and i.channel==ctx.channel, timeout=60)
                if isinstance(interaction, Select):
                    value=interaction.values[0]
                
                    if value=='SetTitle':
                        await interaction.respond(type=4, content='What title you want to be in the embed?')
                        try:
                            resMessage=await self.bot.wait_for('message', check=lambda i: i.author==ctx.author and i.channel==ctx.channel)
                        except asyncio.TimeoutError:
                            await ctx.send('You did\'nt respond on time. You can try again.')
                            continue
                        else:
                            await self.set_title(message=MainMessage, content=resMessage.content)
                            try:
                                await resMessage.delete()
                            except:
                                pass
                    
                    elif value=='SetDesc':
                        await interaction.respond(type=4, content='What description you want to be in the embed?')
                        try:
                            resMessage=await self.bot.wait_for('message', check=lambda i: i.author==ctx.author and i.channel==ctx.channel)
                        except asyncio.TimeoutError:
                            await ctx.send('You did\'nt respond on time. You can try again.')
                            continue
                        else:
                            await self.set_description(message=MainMessage, content=resMessage.content)
                            try:
                                await resMessage.delete()
                            except:
                                pass



            except asyncio.TimeoutError:
                await MainMessage.disable_components()
                break