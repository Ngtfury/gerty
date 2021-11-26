import asyncio
import datetime
import discord
from discord.ext import commands
import discord_components
from discord_components import *
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
import subprocess

class Utils:

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
        em.set_footer(text=f'Invoked by {ctx.author.name}', icon_url=ctx.author.avatar_url)
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
        em.set_author(name=f'Help - {_command.qualified_name}', icon_url=self.bot.user.avatar_url)
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
        return util, misc, fun, mod, tags, admin, rtfm, image

    async def get_commands_without_description(self):
        util=[]
        misc=[]
        fun=[]
        mod=[]
        tags=[]
        admin=[]
        rtfm=[]
        image=[]
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
        return util, misc, fun, mod, tags, admin, rtfm, image


class UtilsCog(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.command(brief='util', description='Stop it get some help!', usage='(command)')
    async def help(self, ctx, *, command:str=None):
        if command:
            return await GertyHelpCommand(self.bot).send_command_help(ctx=ctx, command=command)
        
        commands=await GertyHelpCommand(self.bot).get_commands_according_brief()
        options=[
            SelectOption(label='Utility commands', description='Commands that are useful for everyone and mods', value='UtilOption', emoji=self.bot.get_emoji(891223848970747916)),
            SelectOption(label='Misc commands', description='Some other stuffs', value='MiscOption', emoji='🧩'),
            SelectOption(label='Fun commands', description='Commands that everyone can use', value='FunOption', emoji='🎪'),
            SelectOption(label='Mod commands', description='Commands that only server mods can use', value='ModOption', emoji=self.bot.get_emoji(885156113656479784)),
            SelectOption(label='Tag commands', description='Commands of the tag module', value='TagOption', emoji=self.bot.get_emoji(880100337745264680)),
            SelectOption(label='Rtfm commands', description='Searches for something in documentations', value='RtfmOption', emoji='📘'),
            SelectOption(label='Image commands', description='Very cool image edit stuffs', value='ImageOption', emoji=self.bot.get_emoji(873933502435962880)),
            SelectOption(label='Admin commands', description='Commands that only bot owner can use!', value='AdminOption', emoji=self.bot.get_emoji(908275726199963698))
        ]
        compo=[[Button(label='Home', emoji='🏘️', disabled=True, id='GoHome'), Button(label='Command list', emoji=self.bot.get_emoji(908288038101209100), id='Links'), Button(label='Quit', emoji=self.bot.get_emoji(890938576563503114), id='QuitDel')], Select(placeholder='Hover through modules!', options=options)]
        compo2=[[Button(label='Home', emoji='🏘️', id='GoHome'), Button(label='Command list', emoji=self.bot.get_emoji(908288038101209100), id='Links'), Button(label='Quit', emoji=self.bot.get_emoji(890938576563503114), id='QuitDel')], Select(placeholder='Hover through modules!', options=options)]
        compo3=[[Button(label='Home', emoji='🏘️', id='GoHome'), Button(label='Command list', emoji=self.bot.get_emoji(908288038101209100), id='Links', disabled=True), Button(label='Quit', emoji=self.bot.get_emoji(890938576563503114), id='QuitDel')], Select(placeholder='Hover through modules!', options=options)]

        MainEmbed=discord.Embed(description='`g!help [command]` - View help for specific command\nHover below categories for more help.\nReports bug if any via `g!report`\n```ml\n[] - Required Argument | () - Optional Argument```', color=Utils.BotColors.invis())
        MainEmbed.set_author(name=f'{self.bot.user.name} HelpDesk', icon_url=self.bot.user.avatar_url, url=discord.utils.oauth_url(self.bot.user.id))
        MainEmbed.add_field(name='<:modules:884784557822459985> Modules:', value='> **<:settingssssss:891223848970747916> Utilities**\n> **🧩 Miscellaneous**\n> **🎪 Fun**\n> **<:moderation:885156113656479784> Moderation**\n> **<:tag:880100337745264680> Tags**\n> **📘 Rtfm (docs)**\n> **<:image:873933502435962880> Image**\n> **<:dev:908275726199963698> Admin**')
        MainEmbed.add_field(name='<:news:885177157138145280> News', value=f'> {self.bot.news}', inline=True)
        MainEmbed.add_field(name='<:links:885161311456071750> Links', value=f'> [Invite me]({discord.utils.oauth_url(self.bot.user.id)}) | [About owner](https://discord.com/users/770646750804312105)', inline=False)
        MainEmbed.set_footer(text=f'Invoked by {ctx.author}', icon_url=ctx.author.avatar_url)


        MainMessage=await ctx.send(embed=MainEmbed, components=compo)

        _UtilNextLine='\n'.join(commands[0])
        UtilEmbed=discord.Embed(description=f'`g!help [command]` - View help for specific command\nHover below categories for more help.\nReports bug if any via `g!report`\n```ml\n[] - Required Argument | () - Optional Argument```\n{_UtilNextLine}', color=Utils.BotColors.invis())
        UtilEmbed.set_author(name='Gerty HelpDesk - Utility commands', icon_url=self.bot.user.avatar_url)
        UtilEmbed.set_footer(text=f'Invoked by {ctx.author}', icon_url=ctx.author.avatar_url)

        _Misc='\n'.join(commands[1])
        MiscEmbed=discord.Embed(description=f'`g!help [command]` - View help for specific command\nHover below categories for more help.\nReports bug if any via `g!report`\n```ml\n[] - Required Argument | () - Optional Argument```\n{_Misc}', color=Utils.BotColors.invis())
        MiscEmbed.set_author(name='Gerty HelpDesk - Misc commands', icon_url=self.bot.user.avatar_url)
        MiscEmbed.set_footer(text=f'Invoked by {ctx.author}', icon_url=ctx.author.avatar_url)

        _Fun='\n'.join(commands[2])
        FunEmbed=discord.Embed(description=f'`g!help [command]` - View help for specific command\nHover below categories for more help.\nReports bug if any via `g!report`\n```ml\n[] - Required Argument | () - Optional Argument```\n{_Fun}', color=Utils.BotColors.invis())
        FunEmbed.set_author(name='Gerty HelpDesk - Fun commands', icon_url=self.bot.user.avatar_url)
        FunEmbed.set_footer(text=f'Invoked by {ctx.author}', icon_url=ctx.author.avatar_url)

        _Mod='\n'.join(commands[3])
        ModEmbed=discord.Embed(description=f'`g!help [command]` - View help for specific command\nHover below categories for more help.\nReports bug if any via `g!report`\n```ml\n[] - Required Argument | () - Optional Argument```\n{_Mod}', color=Utils.BotColors.invis())
        ModEmbed.set_author(name='Gerty HelpDesk - Moderator commands', icon_url=self.bot.user.avatar_url)
        ModEmbed.set_footer(text=f'Invoked by {ctx.author}', icon_url=ctx.author.avatar_url)

        _Tags='\n'.join(commands[4])
        TagEmbed=discord.Embed(description=f'`g!help [command]` - View help for specific command\nHover below categories for more help.\nReports bug if any via `g!report`\n```ml\n[] - Required Argument | () - Optional Argument```\n{_Tags}', color=Utils.BotColors.invis())
        TagEmbed.set_author(name='Gerty HelpDesk - Tag commands', icon_url=self.bot.user.avatar_url)
        TagEmbed.set_footer(text=f'Invoked by {ctx.author}', icon_url=ctx.author.avatar_url)

        _Admin='\n'.join(commands[5])
        AdminEmbed=discord.Embed(description=f'`g!help [command]` - View help for specific command\nHover below categories for more help.\nReports bug if any via `g!report`\n```ml\n[] - Required Argument | () - Optional Argument```\n{_Admin}', color=Utils.BotColors.invis())
        AdminEmbed.set_author(name='Gerty HelpDesk - Admin commands', icon_url=self.bot.user.avatar_url)
        AdminEmbed.set_footer(text=f'Invoked by {ctx.author}', icon_url=ctx.author.avatar_url)

        _Rtfm='\n'.join(commands[6])
        RtfmEmbed=discord.Embed(description=f'`g!help [command]` - View help for specific command\nHover below categories for more help.\nReports bug if any via `g!report`\n```ml\n[] - Required Argument | () - Optional Argument```\n{_Rtfm}', color=Utils.BotColors.invis())
        RtfmEmbed.set_author(name='Gerty HelpDesk - Rtfm commands', icon_url=self.bot.user.avatar_url)
        RtfmEmbed.set_footer(text=f'Invoked by {ctx.author}', icon_url=ctx.author.avatar_url)


        _Image='\n'.join(commands[7])
        ImageEmbed=discord.Embed(description=f'`g!help [command]` - View help for specific command\nHover below categories for more help.\nReports bug if any via `g!report`\n```ml\n[] - Required Argument | () - Optional Argument```\n{_Image}', color=Utils.BotColors.invis())
        ImageEmbed.set_author(name='Gerty HelpDesk - Image commands', icon_url=self.bot.user.avatar_url)
        ImageEmbed.set_footer(text=f'Invoked by {ctx.author}', icon_url=ctx.author.avatar_url)

        commandlist=await GertyHelpCommand(self.bot).get_commands_without_description()

        CommandListEmbed=discord.Embed(description="""`g!help [command]` - View help for specific command
Hover below categories for more help.
Reports bug if any via `g!report`\n```ml\n[] - Required Argument | () - Optional Argument```""", color=Utils.BotColors.invis())
        CommandListEmbed.set_author(name='Gerty HelpDesk - Commands', icon_url=self.bot.user.avatar_url)
        CommandListEmbed.add_field(name='<:settingssssss:891223848970747916> Utility commands', value=', '.join(commandlist[0]), inline=False)
        CommandListEmbed.add_field(name='🧩 Misc commands', value=', '.join(commandlist[1]), inline=False)
        CommandListEmbed.add_field(name='🎪 Fun commands', value=', '.join(commandlist[2]), inline=False)
        CommandListEmbed.add_field(name='<:moderation:885156113656479784> Mod commands', value=', '.join(commandlist[3]), inline=False)
        CommandListEmbed.add_field(name='<:tag:880100337745264680> Tag commands', value=', '.join(commandlist[4]), inline=False)
        CommandListEmbed.add_field(name='📘 Rtfm commands', value=', '.join(commandlist[6]), inline=False)
        CommandListEmbed.add_field(name='<:image:873933502435962880> Image commands', value=', '.join(commandlist[7]))
        CommandListEmbed.add_field(name='<:dev:908275726199963698> Admin commands', value=', '.join(commandlist[5]), inline=False)
        CommandListEmbed.set_footer(text=f'Invoked by {ctx.author}', icon_url=ctx.author.avatar_url)



        #loaded embeds

        while True:
            try:
                event=await self.bot.wait_for('interaction', check=lambda i: i.channel==ctx.channel and i.message==MainMessage, timeout=40)
                if event.author != ctx.author:
                    await event.respond(type=4, content='Sorry, this menu cannot be controlled by you')
                else:
                    if isinstance(event.component, Select):
                        if event.values[0]:
                            value=event.values[0]
                            if value=='UtilOption':
                                await event.respond(type=7, embed=UtilEmbed, components=compo2)
                            elif value=='MiscOption':
                                await event.respond(type=7, embed=MiscEmbed, components=compo2)
                            elif value=='FunOption':
                                await event.respond(type=7, embed=FunEmbed, components=compo2)
                            elif value=='ModOption':
                                await event.respond(type=7, embed=ModEmbed, components=compo2)
                            elif value=='TagOption':
                                await event.respond(type=7, embed=TagEmbed, components=compo2)
                            elif value=='AdminOption':
                                await event.respond(type=7, embed=AdminEmbed, components=compo2)
                            elif value=='RtfmOption':
                                await event.respond(type=7, embed=RtfmEmbed, components=compo2)
                            elif value=='ImageOption':
                                await event.respond(type=7, embed=ImageEmbed, components=compo2)
                    elif isinstance(event.component, Button):
                        if event.component.id=='GoHome':
                            await event.respond(type=7, embed=MainEmbed, components=compo)
                        elif event.component.id=='QuitDel':
                            await event.respond(type=6)
                            await MainMessage.delete()
                            await ctx.message.add_reaction('<:success:893501515107557466>')
                            break
                        elif event.component.id=='Links':
                            await event.respond(type=7, embed=CommandListEmbed, components=compo3)
            except asyncio.TimeoutError:
                await MainMessage.disable_components()
                break


        

    @commands.Cog.listener()
    async def on_command(self, ctx):
        if ctx.author.id in self.bot.owner_ids:
            return
        if not ctx.guild:
            return
        em=discord.Embed(description=f'Command “**{ctx.command.qualified_name}**“ used by **{ctx.author}** ({ctx.author.mention})\nIn server **{ctx.guild.name}**\nIn channel {ctx.channel.name} ({ctx.channel.mention})\n\n[Jump to message]({ctx.message.jump_url})', timestamp=datetime.datetime.now(), color=Utils.BotColors.invis())
        em.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        em.set_footer(text='Used command at')
        em.set_thumbnail(url=ctx.guild.icon_url)
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url('https://discord.com/api/webhooks/907593512856477717/OSHPK46rXV_jJCPIn_W9K71kRb_GqTeLzR2EXOs0Uzmf4FaVmVlrJdiJPkOsw8cXevYx', adapter=AsyncWebhookAdapter(session))
            await webhook.send(embed=em, username='Gerty command logs', avatar_url=self.bot.user.avatar_url)


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        em=discord.Embed(description=f'**Guild owner**: **{guild.owner.name}** ({guild.owner.mention})\n**Channels**: {len(guild.channels)}\n**Members**: {guild.member_count}', color=Utils.BotColors.invis(), timestamp=datetime.datetime.now())
        em.set_author(name=guild.name, icon_url=guild.icon_url)
        em.set_thumbnail(url=guild.icon_url)
        em.set_footer(text='Joined server at')
        async with aiohttp.ClientSession() as session:
            web=Webhook.from_url(url='https://discord.com/api/webhooks/907593485224386560/T6k31rtY8Yf_WsSjH77OW27bteM7Gnl7ve7q6rcRXfyQj6s5bLXsoYO97kHqo70MOtdH', adapter=AsyncWebhookAdapter(session))
            await web.send(embed=em, username='Gerty guild logs', avatar_url=self.bot.user.avatar_url)


    @commands.Cog.listener()
    async def on_shard_connect(self, shard_id):
        async with aiohttp.ClientSession() as session:
            web=Webhook.from_url(url='https://discord.com/api/webhooks/907681269452800061/-uEovWEWLcEXKNecuYe_1OlfkSAlCpv_fR8TcH2TsBJ9wab52GdB6QarlHaa3WqUotqR', adapter=AsyncWebhookAdapter(session))
            await web.send(content=f'🟢 Ready', username=f'Shard {shard_id}', avatar_url='https://singlecolorimage.com/get/2bff00/400x100')

    @commands.Cog.listener()
    async def on_shard_disconnect(self, shard_id):
        async with aiohttp.ClientSession() as session:
            web=Webhook.from_url(url='https://discord.com/api/webhooks/907681269452800061/-uEovWEWLcEXKNecuYe_1OlfkSAlCpv_fR8TcH2TsBJ9wab52GdB6QarlHaa3WqUotqR', adapter=AsyncWebhookAdapter(session))
            await web.send(content=f'🟡 Disconnected', username=f'Shard {shard_id}', avatar_url='https://singlecolorimage.com/get/ffdd00/400x100')


    @commands.Cog.listener()
    async def on_shard_resumed(self, shard_id):
        async with aiohttp.ClientSession() as session:
            web=Webhook.from_url(url='https://discord.com/api/webhooks/907681269452800061/-uEovWEWLcEXKNecuYe_1OlfkSAlCpv_fR8TcH2TsBJ9wab52GdB6QarlHaa3WqUotqR', adapter=AsyncWebhookAdapter(session))
            await web.send(content=f'🟢 Resumed', username=f'Shard {shard_id}', avatar_url='https://singlecolorimage.com/get/2bff00/400x100')



def setup(bot):
    bot.add_cog(UtilsCog(bot))