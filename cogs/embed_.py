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


    async def wait_for_res(self, ctx, timeout=10):
        try:
            resMessage=await self.bot.wait_for('message', check=lambda i: i.author==ctx.author and i.channel==ctx.channel, timeout=timeout)
            try:
                await resMessage.delete()
            except:
                pass
            return resMessage.content
        except asyncio.TimeoutError:
            await ctx.send('You did\'nt respond on time. You can try again.')
            return False


    async def set_title(self, message: discord.Message, content, url:bool=False):


        FetchedMessage=await message.channel.fetch_message(message.id)
        Embed=FetchedMessage.embeds[0]
        if url==True:
            if not content.startswith('http'):
                return False
            Embed.url=content
            return await message.edit(embed=Embed)
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
        oauth=discord.utils.oauth_url(self.bot.user.id)
        MainEmbed=discord.Embed(title='Title', description='Description', url=f'{oauth}')
        MainEmbed.set_thumbnail(url='https://media.discordapp.net/attachments/914819940798853181/914820437538635806/oie_ZSzciFNKnAq8.png')
        MainEmbed.set_image(url='https://media.discordapp.net/attachments/914819940798853181/914820437358297109/oie_HjDdrGBbmZwR.png')
        MainEmbed.set_author(name='Author name (can point to url)', icon_url='https://cdn.logojoy.com/wp-content/uploads/20210422095037/discord-mascot.png', url=f'{oauth}')
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
                        resMessage=await self.wait_for_res(ctx=ctx, timeout=10)
                        if not resMessage:
                            continue
                        await self.set_title(message=MainMessage, content=resMessage)
                    
                    elif value=='SetDesc':
                        await interaction.respond(type=4, content=f'What description you want to be in the embed?\n{note}')
                        resMessage=await self.wait_for_res(ctx=ctx)
                        if not resMessage:
                            continue
                        await self.set_description(message=MainMessage, content=resMessage)

                    elif value=='SetTitleUrl':
                        await interaction.respond(type=4, content=f'What title url you want to be in the embed?\n{note}')
                        try:
                            resMessage=await self.bot.wait_for('message', check=lambda i: i.author==ctx.author and i.channel==ctx.channel)
                        except asyncio.TimeoutError:
                            await ctx.send('You did\'nt respond on time. You can try again.')
                            continue
                        else:
                            check=await self.set_title(message=MainMessage, content=resMessage.content, url=True)
                            if not check:
                                await ctx.send('Scheme must be one of http or https')
                                continue
                            try:
                                await resMessage.delete()
                            except:
                                pass                        


            except asyncio.TimeoutError:
                await MainMessage.disable_components()
                break