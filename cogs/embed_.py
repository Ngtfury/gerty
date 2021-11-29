import discord
from discord.ext import commands
import discord_components
from discord_components import *
import asyncio
import random


def setup(client):
    client.add_cog(EmbedEditor(client))

class EmbedEditor(commands.Cog):
    def __init__(self, bot):
        self.bot=bot


    async def set_title(self, message: discord.Message, content):
        FetchedMessage=await message.channel.fetch_message(message.id)
        Embed=FetchedMessage.embeds[0]
        if content=='None':
            _content=None
        else:
            _content=content
        Embed.title=_content

        return await message.edit(embed=Embed)


    async def set_description(self, message: discord.Message, content):
        FetchedMessage=await message.channel.fetch_message(message.id)
        Embed=FetchedMessage.embeds[0]
        if content=='None':
            _content=None
        else:
            _content=content
        Embed.description=_content

        return await message.edit(embed=Embed)


    @commands.command(brief='fun', description='Dynamic embed editor')
    async def embed(self, ctx):

        SelOptions=[
            SelectOption(label='Set Title', value='SetTitle'),
            SelectOption(label='Set Description', value='SetDesc'),
            SelectOption(label='Set title URL', value='SetTitleUrl'),
            SelectOption(label='Set footer', value='SetFooter')
        ]

        MainEmbed=discord.Embed(title='Title', description='Description', url='https://cdn.discordapp.com/attachments/914698141004079135/914810488225955920/embed.png')
        MainEmbed.set_thumbnail(url='https://cdn.logojoy.com/wp-content/uploads/20210422095037/discord-mascot.png')
        MainEmbed.set_image(url='https://cdn.logojoy.com/wp-content/uploads/20210422095037/discord-mascot.png')
        MainEmbed.add_field(name='Field name', value='Color sets\n< that', inline=True)
        MainEmbed.add_field(name='Field name', value='Color is an int/hex not string', inline=True)
        MainEmbed.add_field(name='Field name', value='Field value', inline=True)
        MainEmbed.add_field(name='Non-inline field name', value='The number of inline fields that can shown on the same row is limited to 3', inline=True)
        MainEmbed.set_footer(icon_url='https://cdn.logojoy.com/wp-content/uploads/20210422095037/discord-mascot.png', text='Footer text • timestamp')

        MainMessage=await ctx.send(embed=MainEmbed, components=[Select(placeholder='Dynamic embed editor', options=SelOptions)])

        note='**Note**: you can respond `None` if you dont want.'
        while True:
            try:

                interaction=await self.bot.wait_for('interaction', check=lambda i: i.author==ctx.author and i.channel==ctx.channel, timeout=60)
                if isinstance(interaction.component, Select):
                    value=interaction.values[0]
                
                    if value=='SetTitle':
                        await interaction.respond(type=4, content=f'What title you want to be in the embed?\n{note}')
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
                        await interaction.respond(type=4, content=f'What description you want to be in the embed?\n{note}')
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