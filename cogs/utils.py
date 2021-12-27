import asyncio
import datetime
import discord
from discord import embeds
from discord.ext import commands
from discord.interactions import Interaction
from discord.types.components import ButtonStyle
from discord.ui import view
import numpy as np
import functools
from PIL import Image, ImageDraw
import psutil
import io
import discord_webhook
from discord_webhook import DiscordWebhook, DiscordEmbed
import aiohttp
import subprocess
import sys
import random
from random import *
import pathlib
import shutil
import os
import pkg_resources
import datetime
import pygit2
import itertools
import time


class ConfirmView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

    async def on_timeout(self):
        for children in self.children:
            children.disabled = True

        await self.message.edit(view = self)



class Utils:

    class Paginator(discord.ui.View):
        def __init__(self, embeds, ctx):
            super().__init__(timeout=60)
            self.embeds = embeds
            self.ctx = ctx
            self.current = 0
            self._number_pages_awaiting = False

        async def on_timeout(self):
            for children in self.children:
                children.disabled = True

            await self.message.edit(view = self)

        async def interaction_check(self, interaction: discord.Interaction):
            if interaction.user.id != self.ctx.author.id:
                await interaction.response.send_message('Sorry, you cannot interact with this menu', ephemeral=True)
                return False
            return True

        @discord.ui.button(
            style = discord.ButtonStyle.gray,
            label = '<<'
        )
        async def double_left_arrow(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.current = 0
            await interaction.response.edit_message(embed = self.embeds[self.current])

        @discord.ui.button(
            style = discord.ButtonStyle.gray,
            label = '<'
        )
        async def left_arrow(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.current -= 1
            if self.current ==  len(self.embeds):
                self.current = 0
            elif self.current < 0:
                self.current = len(self.embeds) - 1
            await interaction.response.edit_message(embed = self.embeds[self.current])

        @discord.ui.button(
            style = discord.ButtonStyle.red,
            emoji = '<:trashcan:890938576563503114>'
        )
        async def quit_button(self, button, interaction: discord.Interaction):
            await interaction.response.defer()
            await self.message.delete()
            await self.ctx.message.add_reaction(Utils.BotEmojis.success())
            self.stop()

        @discord.ui.button(
            style = discord.ButtonStyle.gray,
            label = '>'
        )
        async def right_arrow(self, button, interaction: discord.Interaction):
            self.current += 1
            if self.current ==  len(self.embeds):
                self.current = 0
            elif self.current < 0:
                self.current = len(self.embeds) - 1

            await interaction.response.edit_message(embed = self.embeds[self.current])

        @discord.ui.button(
            style = discord.ButtonStyle.gray,
            label = '>>'
        )
        async def double_right_arrow(self, button, interaction: discord.Interaction):
            self.current = len(self.embeds) - 1
            await interaction.response.edit_message(embed = self.embeds[self.current])

        @discord.ui.button(
            style = discord.ButtonStyle.blurple,
            label = 'Skip to page...'
        )
        async def skip_to_page(self, button, interaction: discord.Interaction):
            if self._number_pages_awaiting:
                await interaction.response.send_message('Already awaiting for your response...', ephemeral=True)
                return
    
            await interaction.response.send_message('What page do you want to go to?', ephemeral=True)
            try:
                self._number_pages_awaiting = True
                resMessage = await self.ctx.bot.wait_for('message', check = lambda i: i.author.id == interaction.user.id and i.channel.id == interaction.channel.id and i.content.isdigit(), timeout = 20)
                self._number_pages_awaiting = False
            except asyncio.TimeoutError:
                self._number_pages_awaiting = False
                await interaction.followup.send('You didn\'t respond on time...', ephemeral=True)
                return


            _content = int(resMessage.content)
            if _content <= 0:
                await interaction.followup.send(f'Pages start from 1 not {_content}.', ephemeral=True)
                return
            if _content > len(self.embeds):
                await interaction.followup.send(f'Sorry, there are only {len(self.embeds)} pages, not {_content}.', ephemeral=True)
                return

            try:
                await resMessage.delete()
            except:
                pass

            self.current = _content - 1
            await interaction.followup.edit_message(embed = self.embeds[self.current], message_id=self.message.id)
            

 


    class Member:
        def __init__(self, bot, id):
            self.bot=bot
            self.member_id=id

        @property
        async def banner(self):
            _user_obj = await self.bot.http.get_user(self.member_id)
            _banner_obj = _user_obj['banner']

            if not _banner_obj:
                return None

            _banner_hash_ = 'gif' if _banner_obj.startswith('a_') else 'png'

            return f'https://cdn.discordapp.com/banners/{self.member_id}/{_banner_obj}.{_banner_hash_}?size=1024'


    async def create_emoji(bot, user: discord.User):

        guild_ids=[917315359126745088, 917310572180168735, 917316291059134474]


        guild=bot.get_guild(random.choice(guild_ids))
        async with aiohttp.ClientSession() as sess:
            async with sess.get(str(user.avatar.url)) as rep:
                buf=await rep.read()
                
        img=Image.open(io.BytesIO(buf))
        height,width = img.size
        lum_img = Image.new('L', [height,width] , 0)
        draw = ImageDraw.Draw(lum_img)
        draw.pieslice([(0,0), (height,width)], 0, 360, fill = 255, outline = "white")
        img_arr =np.array(img)
        lum_img_arr =np.array(lum_img)
        final_img_arr = np.dstack((img_arr,lum_img_arr))
        arr_img = Image.fromarray(final_img_arr)
        arr_img = arr_img.resize((128,128),Image.ANTIALIAS)
        arr_img.save('asset.png', quality=95)
        with open('asset.png', 'rb') as f:
            d=f.read()
        final=await guild.create_custom_emoji(name='custom', image=d)
        return final


    async def confirm(bot, description, interaction=None, ctx=None):
        if not interaction:
            if not ctx:
                raise RuntimeError('ctx or interaction should be specified')


        ConfirmCompo=[[
            Button(style=ButtonStyle.green, id='ConfirmOk', emoji=bot.get_emoji(910490899883126804)),
            Button(id='ConfirmAbort', emoji=bot.get_emoji(910491193174028308))
        ]]

        em=discord.Embed(description=f'<:pokerquestion:913801385739423744> {description}', color=Utils.BotColors.invis())
        if interaction:
            MainMessage=await interaction.send(embed=em, components=ConfirmCompo, ephemeral=False)
        else:
            MainMessage=await ctx.send(embed=em, components=ConfirmCompo)
        while True:
            try:
                if ctx:
                    _check=lambda i: i.author==ctx.author and i.channel==ctx.channel
                else:
                    _check=lambda i: i.message==MainMessage
                ConfirmEvent=await bot.wait_for('button_click', check=_check, timeout=60)
                if ConfirmEvent.component.id=='ConfirmOk':
                    await ConfirmEvent.respond(type=6)
                    try:
                        await MainMessage.delete()
                    except:
                        pass
                    return True
                elif ConfirmEvent.component.id=='ConfirmAbort':
                    await ConfirmEvent.respond(type=6)
                    try:
                        await MainMessage.delete()
                    except:
                        pass
                    return False
            except asyncio.TimeoutError:
                await MainMessage.disable_components()



    def clean_prefix(ctx):
        if ctx.prefix==f'<@!{ctx.bot.user.id}> ':
            _prefix=f'@{ctx.bot.user.name} '
        else:
            _prefix=ctx.prefix
        return _prefix

    class Exe:
        def __init__(self,bot):
            self.client=bot

        async def run(self, command):
            try:
                process = await asyncio.create_subprocess_shell(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                result = await process.communicate()
            except NotImplementedError:
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                result = await self.client.loop.run_in_executor(None, process.communicate)

            notReadable=[output.decode() for output in result]
            Readable='\n'.join(notReadable)
            return f'$ {command}\n{Readable}'

    class BotEmbed:
        def error(description:str):
            embed=discord.Embed(description=f'<:error:893501396161290320> {description}', color=0x2F3136)
            return embed
        def success(description:str):
            embed=discord.Embed(description=f'<:success:893501515107557466> {description}', color=0x2F3136)
            return embed

    class BotEmojis:
        def error():
            return '<:error:893501396161290320>'
        def success():
            return '<:success:893501515107557466>'
        def loading():
            return '<a:z_loading:878684429789306920>'

    class BotColors:
        def invis():
            return 0x2F3136


class GertyHelpCommand:
    def __init__(self, bot):
        self.bot=bot
    async def send_command_help(self, ctx, command:str, embed:bool=False):
        _command=self.bot.get_command(f'{command}')
        if not _command:
            return await ctx.send(embed=Utils.BotEmbed.error(f'There is no command called “{command}“'))
        t='`'
        em=discord.Embed(description=f'{t}{t}{t}ml\n[] - Required Argument | () - Optional Argument\n{t}{t}{t}', color=0x2F3136)
        em.set_footer(text=f'Invoked by {ctx.author.name}', icon_url=ctx.author.avatar.url)
        if _command.description:
            _des=_command.description
        else:
            _des='No description provided for this command'
        em.add_field(name='Description', value=f'{_des}', inline=False)
        if f'{ctx.prefix}' == f'<@!{self.bot.user.id}> ':
            _prefix=f'@{self.bot.user.name} '
        else:
            _prefix=ctx.prefix
        if _command.usage:
            _usage=f'{t}{t}{t}{_prefix}{_command.qualified_name} {_command.usage}{t}{t}{t}'
        else:
            _usage=f'```{_prefix}{_command.qualified_name}```'
        em.add_field(name='Usage', value=_usage)
        em.set_author(name=f'Help - {_command.qualified_name}', icon_url=self.bot.user.avatar.url)
        if _command.aliases:
            aliases=[]
            for x in _command.aliases:
                aliases.append(f'`{x}`')
            em.add_field(name='Aliases', value=', '.join(aliases))
        try:
            subcommands=[]
            for cmd in _command.commands:
                subcommands.append(f'{cmd.name}')
            _subcommands=[]
            for sub in subcommands:
                _subcommands.append(f'`{sub}`')
            em.add_field(name='Subcommands', value=', '.join(_subcommands), inline=False)
        except AttributeError:
            pass
        if _command.checks:
            checks=_command.checks[0]
            try:
                do_or_not=checks(ctx)
                if do_or_not:
                    pass
            except Exception as check_err:
                em.add_field(name='Missing permissions', value=str(check_err), inline=False)
        if embed==True:
            return em
        else:
            return await ctx.send(embed=em)

    async def get_commands_according_brief(self):
        util=[]
        misc=[]
        fun=[]
        mod=[]
        tags=[]
        admin=[]
        rtfm=[]
        image=[]
        selfrole = []
        welcomer = []
        for command in self.bot.commands:
            if command.brief:
                if command.description:
                    _des=command.description
                else:
                    _des='No description provided'
                if command.brief=='util':
                    util.append(f'<:arrow:885193320068968508> `{command.qualified_name}` - {_des}')
                    try:
                        for sub in command.commands:
                            if sub.description:
                                _des=sub.description
                            else:
                                _des='No description provided'
                            util.append(f'<:arrow:885193320068968508> `{sub.qualified_name}` - {_des}')
                    except:
                        pass
                elif command.brief=='meta':
                    misc.append(f'<:arrow:885193320068968508> `{command.qualified_name}` - {_des}')
                    try:
                        for sub in command.commands:
                            if sub.description:
                                _des=sub.description
                            else:
                                _des='No description provided'
                            misc.append(f'<:arrow:885193320068968508> `{sub.qualified_name}` - {_des}')
                    except:
                        pass
                elif command.brief=='fun':
                    fun.append(f'<:arrow:885193320068968508> `{command.qualified_name}` - {_des}')
                    try:
                        for sub in command.commands:
                            if sub.description:
                                _des=sub.description
                            else:
                                _des='No description provided'
                            fun.append(f'<:arrow:885193320068968508> `{sub.qualified_name}` - {_des}')
                    except:
                        pass #
                elif command.brief=='mod':
                    mod.append(f'<:arrow:885193320068968508> `{command.qualified_name}` - {_des}')
                    try:
                        for sub in command.commands:
                            if sub.description:
                                _des=sub.description
                            else:
                                _des='No description provided'
                            mod.append(f'<:arrow:885193320068968508> `{sub.qualified_name}` - {_des}')
                    except:
                        pass
                elif command.brief=='tags':
                    tags.append(f'<:arrow:885193320068968508> `{command.qualified_name}` - {_des}')
                    try:
                        for sub in command.commands:
                            if sub.description:
                                _des=sub.description
                            else:
                                _des='No description provided'
                            tags.append(f'<:arrow:885193320068968508> `{sub.qualified_name}` - {_des}')
                    except:
                        pass
                elif command.brief=='admin':
                    admin.append(f'<:arrow:885193320068968508> `{command.qualified_name}` - {_des}')
                    try:
                        for sub in command.commands:
                            if sub.description:
                                _des=sub.description
                            else:
                                _des='No description provided'
                            admin.append(f'<:arrow:885193320068968508> `{sub.qualified_name}` - {_des}')
                    except:
                        pass
                elif command.brief=='rtfm':
                    rtfm.append(f'<:arrow:885193320068968508> `{command.qualified_name}` - {_des}')
                    try:
                        for sub in command.commands:
                            if sub.description:
                                _des=sub.description
                            else:
                                _des='No description provided'
                            rtfm.append(f'<:arrow:885193320068968508> `{sub.qualified_name}` - {_des}')
                    except:
                        pass
                elif command.brief=='image':
                    image.append(f'<:arrow:885193320068968508> `{command.qualified_name}` - {_des}')
                    try:
                        for sub in command.commands:
                            if sub.description:
                                _des=sub.description
                            else:
                                _des='No description provided'
                            image.append(f'<:arrow:885193320068968508> `{sub.qualified_name}` - {_des}')
                    except:
                        pass
                elif command.brief=='selfrole':
                    selfrole.append(f'<:arrow:885193320068968508> `{command.qualified_name}` - {_des}')
                    try:
                        for sub in command.commands:
                            if sub.description:
                                _des=sub.description
                            else:
                                _des='No description provided'
                            selfrole.append(f'<:arrow:885193320068968508> `{sub.qualified_name}` - {_des}')
                    except:
                        pass
                elif command.brief=='welcomer':
                    welcomer.append(f'<:arrow:885193320068968508> `{command.qualified_name}` - {_des}')
                    try:
                        for sub in command.commands:
                            if sub.description:
                                _des=sub.description
                            else:
                                _des='No description provided'
                            welcomer.append(f'<:arrow:885193320068968508> `{sub.qualified_name}` - {_des}')
                    except:
                        pass
        return util, misc, fun, mod, tags, admin, rtfm, image, selfrole, welcomer

    async def get_commands_without_description(self):
        util=[]
        misc=[]
        fun=[]
        mod=[]
        tags=[]
        admin=[]
        rtfm=[]
        image=[]
        selfrole=[]
        welcomer = []
        for command in self.bot.commands:
            if command.brief:
                if command.brief=='util':
                    util.append(f'`{command.name}`')
                    try:
                        for sub in command.commands:
                            util.append(f'`{sub.qualified_name}`')
                    except:
                        pass
                elif command.brief=='meta':
                    misc.append(f'`{command.name}`')
                    try:
                        for sub in command.commands:
                            misc.append(f'`{sub.qualified_name}`')
                    except:
                        pass
                elif command.brief=='fun':
                    fun.append(f'`{command.name}`')
                    try:
                        for sub in command.commands:
                            fun.append(f'`{sub.qualified_name}`')
                    except:
                        pass
                elif command.brief=='mod':
                    mod.append(f'`{command.name}`')
                    try:
                        for sub in command.commands:
                            mod.append(f'`{sub.qualified_name}`')
                    except:
                        pass
                elif command.brief=='tags':
                    tags.append(f'`{command.name}`')
                    try:
                        for sub in command.commands:
                            tags.append(f'`{sub.qualified_name}`')
                    except:
                        pass
                elif command.brief=='admin':
                    admin.append(f'`{command.name}`')
                    try:
                        for sub in command.commands:
                            admin.append(f'`{sub.qualified_name}`')
                    except:
                        pass
                elif command.brief=='rtfm':
                    rtfm.append(f'`{command.name}`')
                    try:
                        for sub in command.commands:
                            rtfm.append(f'`{sub.qualified_name}`')
                    except:
                        pass
                elif command.brief=='image':
                    image.append(f'`{command.name}`')
                    try:
                        for sub in command.commands:
                            image.append(f'`{sub.qualified_name}`')
                    except:
                        pass
                elif command.brief=='selfrole':
                    selfrole.append(f'`{command.name}`')
                    try:
                        for sub in command.commands:
                            selfrole.append(f'`{sub.qualified_name}`')
                    except:
                        pass
                elif command.brief=='welcomer':
                    welcomer.append(f'`{command.name}`')
                    try:
                        for sub in command.commands:
                            welcomer.append(f'`{sub.qualified_name}`')
                    except:
                        pass
        return util, misc, fun, mod, tags, admin, rtfm, image, selfrole, welcomer

class HelpHomeButton(discord.ui.Button):
    def __init__(self, HomeEmbed, ctx):
        super().__init__(
            style=discord.ButtonStyle.gray,
            label='Home',
            emoji='🏘️',
        )
        self.homeembed = HomeEmbed
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(embed=self.homeembed)

class HelpCommandlistButton(discord.ui.Button):
    def __init__(self, commandlistembed, ctx):
        super().__init__(
            style = discord.ButtonStyle.gray,
            label='Command list',
            emoji=ctx.bot.get_emoji(908288038101209100),
        )
        self.embed = commandlistembed
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):

        await interaction.response.edit_message(embed=self.embed)


class HelpQuitButton(discord.ui.Button):
    def __init__(self, ctx):
        super().__init__(
            emoji=ctx.bot.get_emoji(890938576563503114),
            label='Quit',
            style=discord.ButtonStyle.gray
        )
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):

        await interaction.response.defer()
        await interaction.message.delete()
        await self.ctx.message.add_reaction('<:success:893501515107557466>')

class HelpSelect(discord.ui.Select):
    def __init__(
        self,
        options,
        UtilEmbed,
        MiscEmbed,
        FunEmbed,
        ModEmbed,
        TagEmbed,
        AdminEmbed,
        RtfmEmbed,
        ImageEmbed,
        SelfRoleEmbed,
        WelcomerEmbed,
    ):
        super().__init__(placeholder='Hover through modules!', options=options)
        self.UtilEmbed = UtilEmbed
        self.MiscEmbed = MiscEmbed
        self.FunEmbed = FunEmbed
        self.ModEmbed = ModEmbed
        self.TagEmbed = TagEmbed
        self.AdminEmbed = AdminEmbed
        self.RtfmEmbed = RtfmEmbed
        self.ImageEmbed = ImageEmbed
        self.SelfRoleEmbed = SelfRoleEmbed
        self.WelcomerEmbed = WelcomerEmbed

    async def callback(self, interaction: discord.Interaction):
        value = interaction.data['values'][0]
        if value == 'UtilOption':
            await interaction.response.edit_message(embed = self.UtilEmbed)
        elif value == 'MiscOption':
            await interaction.response.edit_message(embed = self.MiscEmbed)
        elif value == 'FunOption':
            await interaction.response.edit_message(embed = self.FunEmbed)
        elif value == 'ModOption':
            await interaction.response.edit_message(embed = self.ModEmbed)
        elif value == 'TagOption':
            await interaction.response.edit_message(embed = self.TagEmbed)
        elif value == 'AdminOption':
            await interaction.response.edit_message(embed = self.AdminEmbed)
        elif value == 'RtfmOption':
            await interaction.response.edit_message(embed = self.RtfmEmbed)
        elif value == 'ImageOption':
            await interaction.response.edit_message(embed = self.ImageEmbed)
        elif value == 'SelfRoleOption':
            await interaction.response.edit_message(embed = self.SelfRoleEmbed)
        elif value == 'WelcomerOption':
            await interaction.response.edit_message(embed = self.WelcomerEmbed)

class HelpCommandView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.ctx = ctx

    async def on_timeout(self):
        for children in self.children:
            children.disabled = True

        await self.message.edit(view = self)

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(ephemeral=True, content='Sorry, you cannot interact with this help menu.')
            return False
        return True

class UtilsCog(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.command(brief='util', description='Stop it get some help!', usage='(command)')
    async def help(self, ctx, *, command:str=None):
        if command:
            return await GertyHelpCommand(self.bot).send_command_help(ctx=ctx, command=command)
        
        commands=await GertyHelpCommand(self.bot).get_commands_according_brief()
        options=[
            discord.SelectOption(label='Utility commands', description='Commands that are useful for everyone and mods', value='UtilOption', emoji=self.bot.get_emoji(891223848970747916)),
            discord.SelectOption(label='Misc commands', description='Some other stuffs', value='MiscOption', emoji='🧩'),
            discord.SelectOption(label='Fun commands', description='Commands that everyone can use', value='FunOption', emoji='🎪'),
            discord.SelectOption(label='Mod commands', description='Commands that only server mods can use', value='ModOption', emoji=self.bot.get_emoji(885156113656479784)),
            discord.SelectOption(label='Tag commands', description='Commands of the tag module', value='TagOption', emoji=self.bot.get_emoji(880100337745264680)),
            discord.SelectOption(label='Rtfm commands', description='Searches for something in documentations', value='RtfmOption', emoji='📘'),
            discord.SelectOption(label='Image commands', description='Very cool image edit stuffs', value='ImageOption', emoji=self.bot.get_emoji(873933502435962880)),
            discord.SelectOption(label='Self-role commands', description='Dynamic self-role menu commands', value='SelfRoleOption', emoji=self.bot.get_emoji(919180776896073768)),
            discord.SelectOption(label='Welcomer commands', description='Greet new users with autoroles and messages',value='WelcomerOption', emoji='🧭'),
            discord.SelectOption(label='Admin commands', description='Commands that only bot owner can use!', value='AdminOption', emoji=self.bot.get_emoji(908275726199963698))
        ]

        MainEmbed=discord.Embed(description='`g!help [command]` - View help for specific command\nHover below categories for more help.\nReports bug if any via `g!report`\n```ml\n[] - Required Argument | () - Optional Argument```', color=Utils.BotColors.invis())
        MainEmbed.set_author(name=f'{self.bot.user.name} HelpDesk', icon_url=self.bot.user.avatar.url, url=discord.utils.oauth_url(self.bot.user.id))
        MainEmbed.add_field(name='<:modules:884784557822459985> Modules:', value='> **<:settingssssss:891223848970747916> Utilities**\n> **🧩 Miscellaneous**\n> **🎪 Fun**\n> **<:moderation:885156113656479784> Moderation**\n> **<:tag:880100337745264680> Tags**\n> **📘 Rtfm (docs)**\n> **<:image:873933502435962880> Image**\n> **<:menu:919180776896073768> Self-role**\n> **🧭 Welcomer**\n> **<:dev:908275726199963698> Admin**')
        MainEmbed.add_field(name='<:news:885177157138145280> News', value=f'> {self.bot.news}', inline=True)
        MainEmbed.add_field(name='<:links:885161311456071750> Links', value=f'> [Invite me]({discord.utils.oauth_url(self.bot.user.id)}) | [About owner](https://discord.com/users/770646750804312105) | [Support Server]({self.bot.support_server_link})', inline=False)
        MainEmbed.set_footer(text=f'Invoked by {ctx.author}', icon_url=ctx.author.avatar.url)


        _UtilNextLine='\n'.join(commands[0])
        UtilEmbed=discord.Embed(description=f'`g!help [command]` - View help for specific command\nHover below categories for more help.\nReports bug if any via `g!report`\n```ml\n[] - Required Argument | () - Optional Argument```\n{_UtilNextLine}', color=Utils.BotColors.invis())
        UtilEmbed.set_author(name='Gerty HelpDesk - Utility commands', icon_url=self.bot.user.avatar.url)
        UtilEmbed.set_footer(text=f'Invoked by {ctx.author}', icon_url=ctx.author.avatar.url)

        _Misc='\n'.join(commands[1])
        MiscEmbed=discord.Embed(description=f'`g!help [command]` - View help for specific command\nHover below categories for more help.\nReports bug if any via `g!report`\n```ml\n[] - Required Argument | () - Optional Argument```\n{_Misc}', color=Utils.BotColors.invis())
        MiscEmbed.set_author(name='Gerty HelpDesk - Misc commands', icon_url=self.bot.user.avatar.url)
        MiscEmbed.set_footer(text=f'Invoked by {ctx.author}', icon_url=ctx.author.avatar.url)

        _Fun='\n'.join(commands[2])
        FunEmbed=discord.Embed(description=f'`g!help [command]` - View help for specific command\nHover below categories for more help.\nReports bug if any via `g!report`\n```ml\n[] - Required Argument | () - Optional Argument```\n{_Fun}', color=Utils.BotColors.invis())
        FunEmbed.set_author(name='Gerty HelpDesk - Fun commands', icon_url=self.bot.user.avatar.url)
        FunEmbed.set_footer(text=f'Invoked by {ctx.author}', icon_url=ctx.author.avatar.url)

        _Mod='\n'.join(commands[3])
        ModEmbed=discord.Embed(description=f'`g!help [command]` - View help for specific command\nHover below categories for more help.\nReports bug if any via `g!report`\n```ml\n[] - Required Argument | () - Optional Argument```\n{_Mod}', color=Utils.BotColors.invis())
        ModEmbed.set_author(name='Gerty HelpDesk - Moderator commands', icon_url=self.bot.user.avatar.url)
        ModEmbed.set_footer(text=f'Invoked by {ctx.author}', icon_url=ctx.author.avatar.url)

        _Tags='\n'.join(commands[4])
        TagEmbed=discord.Embed(description=f'`g!help [command]` - View help for specific command\nHover below categories for more help.\nReports bug if any via `g!report`\n```ml\n[] - Required Argument | () - Optional Argument```\n{_Tags}', color=Utils.BotColors.invis())
        TagEmbed.set_author(name='Gerty HelpDesk - Tag commands', icon_url=self.bot.user.avatar.url)
        TagEmbed.set_footer(text=f'Invoked by {ctx.author}', icon_url=ctx.author.avatar.url)

        _Admin='\n'.join(commands[5])
        AdminEmbed=discord.Embed(description=f'`g!help [command]` - View help for specific command\nHover below categories for more help.\nReports bug if any via `g!report`\n```ml\n[] - Required Argument | () - Optional Argument```\n{_Admin}', color=Utils.BotColors.invis())
        AdminEmbed.set_author(name='Gerty HelpDesk - Admin commands', icon_url=self.bot.user.avatar.url)
        AdminEmbed.set_footer(text=f'Invoked by {ctx.author}', icon_url=ctx.author.avatar.url)

        _Rtfm='\n'.join(commands[6])
        RtfmEmbed=discord.Embed(description=f'`g!help [command]` - View help for specific command\nHover below categories for more help.\nReports bug if any via `g!report`\n```ml\n[] - Required Argument | () - Optional Argument```\n{_Rtfm}', color=Utils.BotColors.invis())
        RtfmEmbed.set_author(name='Gerty HelpDesk - Rtfm commands', icon_url=self.bot.user.avatar.url)
        RtfmEmbed.set_footer(text=f'Invoked by {ctx.author}', icon_url=ctx.author.avatar.url)


        _Image='\n'.join(commands[7])
        ImageEmbed=discord.Embed(description=f'`g!help [command]` - View help for specific command\nHover below categories for more help.\nReports bug if any via `g!report`\n```ml\n[] - Required Argument | () - Optional Argument```\n{_Image}', color=Utils.BotColors.invis())
        ImageEmbed.set_author(name='Gerty HelpDesk - Image commands', icon_url=self.bot.user.avatar.url)
        ImageEmbed.set_footer(text=f'Invoked by {ctx.author}', icon_url=ctx.author.avatar.url)

        SelfRole='\n'.join(commands[8])
        SelfRoleEmbed=discord.Embed(description=f'`g!help [command]` - View help for specific command\nHover below categories for more help.\nReports bug if any via `g!report`\n```ml\n[] - Required Argument | () - Optional Argument```\n{SelfRole}', color=Utils.BotColors.invis())
        SelfRoleEmbed.set_author(name='Gerty HelpDesk - Selfrole commands', icon_url=self.bot.user.avatar.url)
        SelfRoleEmbed.set_footer(text=f'Invoked by {ctx.author}', icon_url=ctx.author.avatar.url)

        Welcomer='\n'.join(commands[9])
        WelcomerEmbed=discord.Embed(description=f'`g!help [command]` - View help for specific command\nHover below categories for more help.\nReports bug if any via `g!report`\n```ml\n[] - Required Argument | () - Optional Argument```\n{Welcomer}', color=Utils.BotColors.invis())
        WelcomerEmbed.set_author(name='Gerty HelpDesk - Welcomer commands', icon_url=self.bot.user.avatar.url)
        WelcomerEmbed.set_footer(text=f'Invoked by {ctx.author}', icon_url=ctx.author.avatar.url)

        commandlist=await GertyHelpCommand(self.bot).get_commands_without_description()

        CommandListEmbed=discord.Embed(description="""`g!help [command]` - View help for specific command
Hover below categories for more help.
Reports bug if any via `g!report`\n```ml\n[] - Required Argument | () - Optional Argument```""", color=Utils.BotColors.invis())
        CommandListEmbed.set_author(name='Gerty HelpDesk - Commands', icon_url=self.bot.user.avatar.url)
        CommandListEmbed.add_field(name='<:settingssssss:891223848970747916> Utility commands', value=', '.join(commandlist[0]), inline=False)
        CommandListEmbed.add_field(name='🧩 Misc commands', value=', '.join(commandlist[1]), inline=False)
        CommandListEmbed.add_field(name='🎪 Fun commands', value=', '.join(commandlist[2]), inline=False)
        CommandListEmbed.add_field(name='<:moderation:885156113656479784> Mod commands', value=', '.join(commandlist[3]), inline=False)
        CommandListEmbed.add_field(name='<:tag:880100337745264680> Tag commands', value=', '.join(commandlist[4]), inline=False)
        CommandListEmbed.add_field(name='📘 Rtfm commands', value=', '.join(commandlist[6]), inline=False)
        CommandListEmbed.add_field(name='<:image:873933502435962880> Image commands', value=', '.join(commandlist[7]), inline=False)
        CommandListEmbed.add_field(name='<:menu:919180776896073768> Self-role commands', value=', '.join(commandlist[8]), inline=False)
        CommandListEmbed.add_field(name='🧭 Welcomer commands', value=', '.join(commandlist[9]), inline=False)
        CommandListEmbed.add_field(name='<:dev:908275726199963698> Admin commands', value=', '.join(commandlist[5]), inline=False)
        CommandListEmbed.set_footer(text=f'Invoked by {ctx.author}', icon_url=ctx.author.avatar.url)

        view = HelpCommandView(ctx)
        view.add_item(HelpHomeButton(MainEmbed, ctx))
        view.add_item(HelpCommandlistButton(CommandListEmbed, ctx))
        view.add_item(HelpQuitButton(ctx))
        view.add_item(
            HelpSelect(
                options,
                UtilEmbed,
                MiscEmbed,
                FunEmbed,
                ModEmbed,
                TagEmbed,
                AdminEmbed,
                RtfmEmbed,
                ImageEmbed,
                SelfRoleEmbed,
                WelcomerEmbed
            )
        )

        view.message = await ctx.reply(
            embed = MainEmbed,
            mention_author = False,
            view = view
        )


    def get_ram_usage(self):
        return int(psutil.virtual_memory().total - psutil.virtual_memory().available)

    def get_ram_total(self):
        return int(psutil.virtual_memory().total)


    def sync_get_class_def_etc(self):
        p = pathlib.Path('./')
        cm = cr = fn = cl = ls = fc = 0
        for f in p.rglob('*.py'):
            if str(f).startswith("venv"):
                continue
            fc += 1
            with f.open() as of:
                for l in of.readlines():
                    l = l.strip()
                    if l.startswith('class'):
                        cl += 1
                    if l.startswith('def'):
                        fn += 1
                    if l.startswith('async def'):
                        cr += 1
                    if '#' in l:
                        cm += 1
                    ls += 1
        return fc, ls, cl, fn, cr, cm

    async def async_get_class_def_etc(self):
        thing=functools.partial(self.sync_get_class_def_etc)
        some_stuff=await self.bot.loop.run_in_executor(None, thing)
        return some_stuff


    def format_commit(self, commit):
        short, _, _ = commit.message.partition('\n')
        short_sha2 = commit.hex[0:6]
        commit_tz = datetime.timezone(datetime.timedelta(minutes=commit.commit_time_offset))
        commit_time = datetime.datetime.fromtimestamp(commit.commit_time).astimezone(commit_tz)

        # [`hash`](url) message (offset)
        offset = f'<t:{int(commit_time.astimezone(datetime.timezone.utc).timestamp())}:R>'
        return f'[`{short_sha2}`](https://github.com/Ngtfury/Gerty/commit/{commit.hex}) {short} ({offset})'



    def get_last_commits(self, count=5):
            repo = pygit2.Repository('.git')
            commits = list(itertools.islice(repo.walk(repo.head.target, pygit2.GIT_SORT_TOPOLOGICAL), count))
            return '\n'.join(self.format_commit(c) for c in commits if not c.message.replace('\n', '') == 'a')

    @commands.command(name='botinfo', brief='util', aliases=['bot-info', 'invite', 'about', 'botabout', 'info'])
    async def _bot_info(self, ctx):
        await ctx.trigger_typing()

        files = await self.async_get_class_def_etc()

        total, used, free = shutil.disk_usage("/")

        _uptime = f'<t:{int(self.bot.uptime)}:T> (<t:{int(self.bot.uptime)}:R>)'
        _fury = self.bot.get_user(770646750804312105)
        _created_at = f'<t:{int(self.bot.user.created_at.timestamp())}:D> (<t:{int(self.bot.user.created_at.timestamp())}:R>)'

        em = discord.Embed(
            title='About me!',
            color=Utils.BotColors.invis(),
            description=f"""Hello, I'm a discord bot made by [`{_fury}`](https://discord.com/users/{_fury.id})
            I've lots of fun and moderation commands
            I've been on discord since {_created_at}
            I've been online since {_uptime}
            
            [**Invite me to your server!**]({discord.utils.oauth_url(self.bot.user.id)})| [**Join our Support Server!**]({self.bot.support_server_link})"""
        )
        em.set_author(name=str(self.bot.user), icon_url=self.bot.user.avatar.url)

        total_channels = sum(len(x.channels) for x in self.bot.guilds)

        em.add_field(
            name='<:robot:919852515737104395> __**General Info**__',
            value = f"""Total servers: `{len(self.bot.guilds)}`
            Total users: `{len(self.bot.users)}`
            Total channels: `{total_channels}`
            Total commands: `{len(self.bot.commands)}`
            Command usage: `{self.bot.command_usage}`
            Messages seen: `{self.bot.messages_seen}`"""
        , inline=True)

        em.add_field(
            name = '<:cogs:919851429613682688> __**System**__',
            value = f"""PID: `{os.getpid()}`
            CPU: `{round(psutil.cpu_percent())}%`/`100%`
            RAM: `{int(self.get_ram_usage() / 1024 / 1024)}MB`/`{int(self.get_ram_total() / 1024 / 1024)}MB`
            Disk: `{used // (2 ** 30)}GB`/`{total // (2 ** 30)}GB`
            Discord.py: `{pkg_resources.get_distribution('discord.py').version}`
            Python: `{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}`"""
        , inline=True)

        em.add_field(
            name = '<:folder:919852062668390410> __**Files**__',
            value = f"""Files: `{files[0]}`
            Lines: `{files[1]}`
            Classes: `{files[2]}`
            Functions: `{files[3]}`
            Coroutines: `{files[4]}`
            Comments: `{files[5]}`
            """
        , inline=True)

        em.add_field(
            name = '<:github:917691688984670240> **__Latest changes__**',
            value = self.get_last_commits(),
            inline = False
        )

        em.set_footer(text=f'Invoked by {ctx.author}', icon_url=ctx.author.avatar.url)

        for shard in self.bot.shards.items():
            shard_id = shard[0]
            shard_obj = shard[1]
            guilds_ = [x for x in self.bot.guilds if x.shard_id==shard_id]
            guild_count = len(guilds_)
            member_count = sum(len(g.members) for g in guilds_)
            _location = '<:YOU_ARE_HERE:919205918120497194>' if ctx.guild.shard_id == shard_id else ''

            em.add_field(
                name=f'**__Shard #{shard_id}__{_location}**',
                value=f"""Latency: `{round(shard_obj.latency*1000)}`ms
                Guilds: `{guild_count}`
                Users: `{member_count}`"""
            )

        await ctx.send(embed=em)

    @commands.Cog.listener('on_message')
    async def update_messages_seen(self, message):
        self.bot.messages_seen += 1

    @commands.Cog.listener()
    async def on_command(self, ctx):
        self.bot.command_usage += 1
        if ctx.author.id == 770646750804312105:
            return
        if not ctx.guild:
            return
        em = DiscordEmbed(description=f'Command “**{ctx.command.qualified_name}**“ used by **{ctx.author}** ({ctx.author.mention})\nIn server **{ctx.guild.name}**\nIn channel {ctx.channel.name} ({ctx.channel.mention})\n\n[Jump to message]({ctx.message.jump_url})', color=Utils.BotColors.invis())
        em.set_timestamp()
        em.set_author(name=str(ctx.author), icon_url=str(ctx.author.avatar.url))
        em.set_footer(text=f'Guild ID: {ctx.guild.id}')
        em.set_thumbnail(url=str(ctx.guild.icon.url))
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/907593512856477717/OSHPK46rXV_jJCPIn_W9K71kRb_GqTeLzR2EXOs0Uzmf4FaVmVlrJdiJPkOsw8cXevYx', username='Gerty command logs', avatar_url=str(self.bot.user.avatar.url))
        webhook.add_embed(em)
        webhook.execute()
        return




    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        em=DiscordEmbed(description=f'**Guild owner**: **{guild.owner.name}** ({guild.owner.mention})\n**Channels**: {len(guild.channels)}\n**Members**: {guild.member_count}', color=Utils.BotColors.invis())
        em.set_timestamp()
        em.set_author(name=guild.name, icon_url=str(guild.icon.url))
        em.set_thumbnail(url=str(guild.icon.url))
        em.set_footer(text='Joined server at')
        webhook = DiscordWebhook(
            url='https://discord.com/api/webhooks/907593485224386560/T6k31rtY8Yf_WsSjH77OW27bteM7Gnl7ve7q6rcRXfyQj6s5bLXsoYO97kHqo70MOtdH',
            username='Gerty guild logs',
            avatar_url=str(self.bot.user.avatar.url)
        )
        webhook.add_embed(em)
        webhook.execute()


    @commands.Cog.listener()
    async def on_shard_connect(self, shard_id):
        webhook = DiscordWebhook(
            url='https://discord.com/api/webhooks/907681269452800061/-uEovWEWLcEXKNecuYe_1OlfkSAlCpv_fR8TcH2TsBJ9wab52GdB6QarlHaa3WqUotqR',
            content = f'<a:GreenCircle:905843069549695026> Ready',
            username=f'Shard {shard_id}', 
            avatar_url='https://singlecolorimage.com/get/2bff00/400x100'
        )
        webhook.execute()

    @commands.Cog.listener()
    async def on_shard_disconnect(self, shard_id):
        webhook = DiscordWebhook(
            url='https://discord.com/api/webhooks/907681269452800061/-uEovWEWLcEXKNecuYe_1OlfkSAlCpv_fR8TcH2TsBJ9wab52GdB6QarlHaa3WqUotqR',
            content=f'<a:Redcircle:905396170925424651> Disconnected', 
            username=f'Shard {shard_id}', 
            avatar_url='https://singlecolorimage.com/get/ffdd00/400x100'
        )
        webhook.execute()

    @commands.Cog.listener()
    async def on_shard_resumed(self, shard_id):
        webhook = DiscordWebhook(
            url='https://discord.com/api/webhooks/907681269452800061/-uEovWEWLcEXKNecuYe_1OlfkSAlCpv_fR8TcH2TsBJ9wab52GdB6QarlHaa3WqUotqR',
            content=f'<a:GreenCircle:905843069549695026> Resumed', 
            username=f'Shard {shard_id}', 
            avatar_url='https://singlecolorimage.com/get/2bff00/400x100'
        )
        webhook.execute()



def setup(bot):
    bot.add_cog(UtilsCog(bot))