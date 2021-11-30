import discord
from discord import embeds
from discord.ext import commands
import discord_components
from discord_components import *
import asyncio
import random
from cogs.utils import Utils


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
            await ctx.send('You didn\'t respond on time. You can try again.', delete_after=3)
            return False


    async def set_title(self, message: discord.Message, content, url:bool=False):


        FetchedMessage=await message.channel.fetch_message(message.id)
        Embed=FetchedMessage.embeds[0]
        if url==True:
            if not content.startswith('http'):
                return False
            Embed.url=content
            return await message.edit(embed=Embed)
        if content in ['None', 'none']:
            _content=None
        else:
            _content=content
        Embed.title=_content

        return await message.edit(embed=Embed)


    async def set_description(self, message: discord.Message, content):
        FetchedMessage=await message.channel.fetch_message(message.id)
        Embed=FetchedMessage.embeds[0]
        if content in ['None', 'none']:
            _content=None
        else:
            _content=content
        Embed.description=_content

        return await message.edit(embed=Embed)

#    async def set_footer(self, message: discord.Message, content:str, icon:bool=False):
#        FetchedMessage=await message.channel.fetch_message(message.id)
#        Embed=FetchedMessage.embeds[0]
#        if icon:
#            if not content.startswith('http'):
#                return False
#            else:
#                Embed.set_footer(icon_url=content)
#            try:
#                await message.edit(embed=Embed)
#                return
#            except Exception as e:
#                if str(e) in ['Invalid Form Body', 'Not a well formed URL.']:
#                    return 'URLERR'
#        if content in ['None', 'none']:
#            Embed.set_footer(text='')
#        else:
#            Embed.set_footer(text=content)

#        return await message.edit(embed=Embed)


    async def set_author(self, ctx, message:discord.Message, interaction):

        compo=[[
            Button(label='Edit author name', id='SetAuthorName'),
            Button(label='Edit author icon', id='SetAuthorIcon'),
            Button(label='Edit author URL', id='SetAuthorURL'),
            Button(style=ButtonStyle.green, label='Confirm', id='ConfirmAuthor')
        ], Button(style=ButtonStyle.red, label='Quit', id='AuthorCancel')]

        firstEmbed=discord.Embed(color=Utils.BotColors.invis())

        Author_=message.embeds[0].author
        if not Author_:
            firstEmbed.set_author(name='<Author name here>', url=discord.utils.oauth_url(self.bot.user.id), icon_url='https://cdn.logojoy.com/wp-content/uploads/20210422095037/discord-mascot.png')
        else:
            if Author_.icon_url:
                icon_=Author_.icon_url
            else:
                icon_=discord.Embed.Empty

            firstEmbed.set_author(name=Author_.name, icon_url=icon_)
        MainMessage=await interaction.send(embed=firstEmbed, components=compo, ephemeral=False)

        while True:
            try:
                event=await ctx.bot.wait_for('button_click', check=lambda i: i.author==ctx.author and i.channel==ctx.channel, timeout=20)
                if event.component.id=='SetAuthorName':
                    await event.respond(type=4, content='What name do you want to be for author?')
                    resMessage=await self.wait_for_res(ctx)
                    if not resMessage:
                        continue
                    if len(resMessage) > 256:
                        await ctx.send('Author name must be 256 or fewer in length.', delete_after=3)
                        continue


                    FetchedMessage=await MainMessage.channel.fetch_message(MainMessage.id)
                    Embed=FetchedMessage.embeds[0]

                    Embed.set_author(name=resMessage, icon_url=Embed.author.icon_url, url=Embed.author.url)
                    await MainMessage.edit(embed=Embed)

                elif event.component.id=='SetAuthorIcon':
                    await event.respond(type=4, content='What icon do you want to be for author? (Only URL allowed)')
                    resMessage=await self.wait_for_res(ctx)
                    if not resMessage:
                        continue

                    if resMessage in ['None', 'none']:
                        _icon=discord.Embed.Empty
                    else:
                        if not resMessage.startswith('http'):
                            await ctx.send(f'Scheme "{resMessage}" is not supported. Scheme must be one of `http`, `https`.', delete_after=3)
                            continue
                        _icon=resMessage

                    FetchedMessage=await MainMessage.channel.fetch_message(MainMessage.id)
                    Embed=FetchedMessage.embeds[0]

                    Embed.set_author(name=Embed.author.name, icon_url=_icon, url=Embed.author.url)
                    try:
                        await MainMessage.edit(embed=Embed)
                    except Exception as e:
                        if str(e) in ['Invalid Form Body', 'Not a well formed URL.']:
                            await ctx.send('Not a well formed image URL provided in footer icon.', delete_after=3)
                            continue
                        else:
                            await ctx.send(str(e), delete_after=3)
                            continue

                elif event.component.id=='SetAuthorURL':
                    await event.respond(type=4, content='What URL do you want to be for author? (Only URL allowed)')
                    resMessage=await self.wait_for_res(ctx)
                    if not resMessage:
                        continue

                    if resMessage in ['None', 'none']:
                        _URL=discord.Embed.Empty
                    else:
                        if not resMessage.startswith('http'):
                            await ctx.send(f'Scheme "{resMessage}" is not supported. Scheme must be one of `http`, `https`.', delete_after=3)
                            continue
                        _URL=resMessage
                    FetchedMessage=await MainMessage.channel.fetch_message(MainMessage.id)
                    Embed=FetchedMessage.embeds[0]

                    Embed.set_author(name=Embed.author.name, icon_url=Embed.author.icon_url, url=_URL)
                    await MainMessage.edit(embed=Embed)

                elif event.component.id=='ConfirmAuthor':
                    await event.respond(type=6)

                    FetchedMessageJR=await MainMessage.channel.fetch_message(MainMessage.id)
                    EmbedJR=FetchedMessageJR.embeds[0]

                    await MainMessage.delete()

                    _author_name=EmbedJR.author.name
                    _author_icon=EmbedJR.author.icon_url
                    _author_url=EmbedJR.author.url

                    FetchedMain=await message.channel.fetch_message(message.id)
                    EmbedMain=FetchedMain.embeds[0]

                    EmbedMain.set_author(name=_author_name, icon_url=_author_icon, url=_author_url)
                    
                    await message.edit(embed=EmbedMain)
                    return

                elif event.component.id=='AuthorCancel':
                    await event.respond(type=6)
                    try:
                        await MainMessage.delete()
                    except:
                        pass
                    return


            except asyncio.TimeoutError:
                try:
                    await MainMessage.delete()
                    return
                except:
                    return

    async def set_footer(self, ctx, message: discord.Message, interaction):

        compo=[[
            Button(label='Edit footer text', id='SetText'),
            Button(label='Edit footer icon', id='SetIcon'),
            Button(label='Confirm', style=ButtonStyle.green, id='ConfirmFooter'),
        ], Button(style=ButtonStyle.red, label='Quit', id='FooterCancel')]

        em=discord.Embed(color=Utils.BotColors.invis())

        Footer_=message.embeds[0].footer
        if not Footer_:
            em.set_footer(text='<Footer text here>', icon_url='https://cdn.logojoy.com/wp-content/uploads/20210422095037/discord-mascot.png')
        else:
            if Footer_.icon_url:
                icon_=Footer_.icon_url
            else:
                icon_=discord.Embed.Empty
            em.set_footer(text=Footer_.text, icon_url=icon_)
        MainMessage=await interaction.send(embed=em, components=compo, ephemeral=False)

        while True:
            try:
                event=await ctx.bot.wait_for('button_click', check=lambda i: i.author==ctx.author and i.channel==ctx.channel, timeout=10)
                if event.component.id=='SetText':
                    await event.respond(type=4, content='What text do you want to be in footer?')
                    resMessage=await self.wait_for_res(ctx)
                    if not resMessage:
                        continue


                    FetchedMessage=await MainMessage.channel.fetch_message(MainMessage.id)
                    Embed=FetchedMessage.embeds[0]

                    if resMessage in ['None', 'none']:
                        _text=None
                    else:
                        _text=resMessage

                    Embed.set_footer(text=_text, icon_url=Embed.footer.icon_url)
                    await MainMessage.edit(embed=Embed)

                elif event.component.id=='SetIcon':
                    await event.respond(type=4, content='What icon do you want to be in footer? (only url allowed)')
                    resMessage=await self.wait_for_res(ctx)
                    if not resMessage:
                        continue

                    FetchedMessage=await MainMessage.channel.fetch_message(MainMessage.id)
                    Embed=FetchedMessage.embeds[0]

                    if resMessage in ['None', 'none']:
                        _icon=discord.Embed.Empty
                    else:
                        if not resMessage.startswith('http'):
                            await ctx.send(f'Scheme "{resMessage}" is not supported. Scheme must be one of `http`, `https`.', delete_after=3)
                            continue
                        _icon=resMessage


                    Embed.set_footer(icon_url=_icon, text=Embed.footer.text)
                    try:
                        await MainMessage.edit(embed=Embed)
                    except Exception as e:
                        if str(e) in ['Invalid Form Body', 'Not a well formed URL.']:
                            await ctx.send('Not a well formed image URL provided in footer icon.', delete_after=3)
                            continue

                elif event.component.id=='ConfirmFooter':
                    await event.respond(type=6)

                    FetchedMessageJR=await MainMessage.channel.fetch_message(MainMessage.id)
                    EmbedJR=FetchedMessageJR.embeds[0]

                    await MainMessage.delete()

                    _footer=EmbedJR.footer.text
                    _icon=EmbedJR.footer.icon_url

                    FetchedMain=await message.channel.fetch_message(message.id)
                    EmbedMain=FetchedMain.embeds[0]

                    EmbedMain.set_footer(text=_footer, icon_url=_icon)
                    
                    return await message.edit(embed=EmbedMain)

                elif event.component.id=='FooterCancel':
                    try:
                        await MainMessage.delete()
                    except:
                        pass
                    return
                    
            except asyncio.TimeoutError:
                try:
                    await MainMessage.delete()
                    return
                except:
                    return


    async def set_color(self, ctx, message: discord.Message, interaction):
        
        ColorOptions=[
            SelectOption(label='Blue', value='ColorBlue', emoji='🟦'),
            SelectOption(label='White', value='ColorWhite', emoji='⬜'),
            SelectOption(label='Yellow', value='ColorYellow', emoji='🟨'),
            SelectOption(label='Red', value='ColorRed', emoji='🟥'),
            SelectOption(label='Brown', value='ColorBrown', emoji='🟫'),
            SelectOption(label='Green', value='ColorGreen', emoji='🟩'),
            SelectOption(label='Violet', value='ColorViolet', emoji='🟪'),
            SelectOption(label='Orange', value='ColorOrange', emoji='🟧'),
            SelectOption(label='Black', value='ColorBlack', emoji='⬛'),
            SelectOption(label='Invisible', value='ColorInvis')
        ]

        ColorComponents=[[
            Select(placeholder='Select colors you want', options=ColorOptions),
        ], Button(style=ButtonStyle.green, label='Custom color', id='ColorCustom'), Button(style=ButtonStyle.red, label='Quit', id='ColorQuit')]

        MainMessage=await interaction.send(content='⠀', components=ColorComponents, ephemeral=False)

        while True:
            inter=await ctx.bot.wait_for('interaction', check=lambda i: i.author==ctx.author and i.channel==ctx.channel)

            FetchedMessage=await message.channel.fetch_message(message.id)
            Embed=FetchedMessage.embeds[0]

            if isinstance(inter.component, Select):
                value=inter.values[0]
                await inter.respond(type=6)

                if value=='ColorBlue':
                    Embed.color=0x2580f7
                elif value=='ColorWhite':
                    Embed.color=0xffffff
                elif value=='ColorYellow':
                    Embed.color=0xccff00
                elif value=='ColorRed':
                    Embed.color=0xff0000
                elif value=='ColorBrown':
                    Embed.color=0x964B00
                elif value=='ColorGreen':
                    Embed.color=0x2bed3e
                elif value=='ColorViolet':
                    Embed.color=0x881c9c
                elif value=='ColorOrange':
                    Embed.color=0xff6200
                elif value=='ColorBlack':
                    Embed.color=0x000000
                elif value=='ColorInvis':
                    Embed.color=Utils.BotColors.invis()

                await message.edit(embed=Embed)
            elif isinstance(inter.component, Button):
                if inter.component.id=='ColorQuit':
                    try:
                        await MainMessage.delete()
                    except:
                        pass
                    return
                elif inter.component.id=='ColorCustom':
                    await inter.respond(type=4, content='What color you want to be in embed? (Only hex or numbers allowed)')
                    resMessage=await self.wait_for_res(ctx)
                    if not resMessage:
                        continue

                    try:
                        _hexa=int(resMessage)
                    except ValueError:
                        try:
                            _hexiof=hex(resMessage)
                        except TypeError:
                            pass
                        else:
                            orghex_=_hexiof
                    else:
                        if _hexa:
                            _hex=hex(_hexa)
                        elif orghex_:
                            _hex=orghex_
                        else:
                            await ctx.send('Invalid color only hex or numbers allowed')
                            return
                        Embed.color=_hex
                        await message.edit(embed=Embed)
                    



    @commands.command(brief='fun', description='Dynamic embed editor')
    @commands.is_owner()
    async def embed(self, ctx):

        SelOptions=[
            SelectOption(label='Edit Title', value='SetTitle'),
            SelectOption(label='Edit Description', value='SetDesc'),
            SelectOption(label='Edit title URL', value='SetTitleUrl'),
            SelectOption(label='Edit author', value='SetAuthor'),
            SelectOption(label='Edit Color', value='SetColor'),
            SelectOption(label='Edit footer', value='SetFooter'),
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

    
        while True:
            if random.randint(1,2)==2:
                note='**Note**: you can respond `None` if you dont want.'
            else:
                note=''
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
                        resMessage=await self.wait_for_res(ctx)
                        if not resMessage:
                            continue
                        check=await self.set_title(message=MainMessage, content=resMessage, url=True)
                        if check==False:
                            await ctx.send('Scheme must be one of `http` or `https`', delete_after=3)
                            continue

                    elif value=='SetFooter':
                        Fetched=await MainMessage.channel.fetch_message(MainMessage.id)
                        await self.set_footer(ctx, message=Fetched, interaction=interaction)
                    
                    elif value=='SetAuthor':
                        Fetched=await MainMessage.channel.fetch_message(MainMessage.id)
                        await self.set_author(ctx, Fetched, interaction=interaction)
                    
                    elif value=='SetColor':
                        Fetched=await MainMessage.channel.fetch_message(MainMessage.id)
                        await self.set_color(ctx, message=Fetched, interaction=interaction)

#                    elif value=='SetFooterIcon':
#                        await interaction.respond(type=4, content=f'What footer icon you want to be in the embed?\n{note}')
#                        resMessage=await self.wait_for_res(ctx)
#                        if not resMessage:
#                            continue
#                        check=await self.set_footer(message=MainMessage, icon=True, content=resMessage)
#                        if check==False:
#                            await ctx.send('Scheme must be one of `http` or `https`', delete_after=3)
#                            continue
#                        elif check=='URLERR':
#                            await ctx.send('Not a well formed image URL.')
#                            continue


            except asyncio.TimeoutError:
                await MainMessage.disable_components()
                break