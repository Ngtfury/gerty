import asyncio
import json
import re
import discord
from discord.ext import commands
import discord_components
from cogs.utils import Utils
from discord_components import *


def setup(bot):
    bot.add_cog(DropDownRole(bot))


class DropDownRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def wait_for_channel_message(self, ctx, MainMessage):
        while True:
            try:
                resMessageBasic = await self.bot.wait_for('message', check = lambda i: i.author == ctx.author and i.channel == ctx.channel, timeout = 60)
                resMessage = resMessageBasic.content
            except asyncio.TimeoutError:
                await ctx.send(
                    embed = Utils.BotEmbed.error('You didn\'t respond on time. You can try again!')
                )
                await MainMessage.delete()
                return False

            if resMessage.lower() == 'cancel':
                await MainMessage.reply(
                    embed = discord.Embed('This proccess has been cancelled successfully.')
                )
                return False

            try:
                channel_to_send = await commands.TextChannelConverter().convert(ctx=ctx, argument=resMessage)
            except commands.ChannelNotFound:
                await resMessageBasic.add_reaction('<a:error:918118195376816128>')
                continue

            await resMessageBasic.delete()
            return channel_to_send


    async def wait_for_titledesc_message(self, ctx, MainMessage):
        while True:
            try:
                resMessageBasic = await self.bot.wait_for('message', check = lambda i: i.author == ctx.author and i.channel == ctx.channel, timeout = 60)
                resMessage = resMessageBasic.content
            except asyncio.TimeoutError:
                await ctx.send(
                    embed = Utils.BotEmbed.error('You didn\'t respond on time. You can try again!')
                )
                await MainMessage.delete()
                return False

            if resMessage.lower() == 'cancel':
                await MainMessage.reply(
                    embed = discord.Embed('This proccess has been cancelled successfully.')
                )
                return False

            splited_ = resMessage.split('|')
            title_ = splited_[0]
            try:
                _desc = splited_[1]
            except IndexError:
                await resMessageBasic.add_reaction('<a:error:918118195376816128>')
                continue

            await resMessageBasic.delete()
            return [title_, _desc]


    def isDiscordEmoji(self, emoji):
        if re.match(r'<(?P<animated>a?):(?P<name>[a-zA-Z0-9_]{2,32}):(?P<id>[0-9]{18,22})>', emoji):
            return True
        else:
            return False

    async def wait_for_role_message(self, ctx, MainMessage):

        role__ = []

        count = 0
        while True:
            if count >= 25:
                break
            try:
                resMessageBasic = await self.bot.wait_for('message', check = lambda i: i.author == ctx.author and i.channel == ctx.channel, timeout = 60)
                resMessage = resMessageBasic.content
            except asyncio.TimeoutError:
                await ctx.send(
                    embed = Utils.BotEmbed.error('You didn\'t respond on time. You can try again!')
                )
                await MainMessage.delete()
                return False

            if resMessage.lower() == 'cancel':
                await MainMessage.reply(
                    embed = discord.Embed('This proccess has been cancelled successfully.')
                )
                return False

            if resMessage.lower() == '-done':
                await resMessageBasic.delete()
                return role__


            splited_ = resMessage.split('|')
            if not len(splited_) == 3:
                await resMessageBasic.add_reaction('<a:error:918118195376816128>')
                continue

            _emoji = splited_[0].replace(' ', '')
            _role = splited_[1].replace(' ', '')
            description_ = splited_[2]

            if self.isDiscordEmoji(_emoji):
                _discord_emoji = await commands.EmojiConverter().convert(ctx=ctx, argument=_emoji)
                emoji_ = int(_discord_emoji.id)
            else:
                emoji_ = str(_emoji)

            try:
                role_be = await commands.RoleConverter().convert(ctx=ctx, argument=_role)
            except commands.RoleNotFound:
                await resMessageBasic.add_reaction('<a:error:918118195376816128>')
                continue

            if role_be > ctx.guild.me.top_role:
                await resMessageBasic.add_reaction('<a:error:918118195376816128>')
                continue

            role__.append({'role': role_be, 'emoji': emoji_, 'desc': description_})
            count += 1
            await resMessageBasic.delete()


        return role__

            




    @commands.group(name='selfrole', invoke_without_command=True, aliases=['self-role', 'dropdown-role', 'autorole'])
    @commands.is_owner()
    @commands.bot_has_guild_permissions(manage_messages=True, manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    async def self_role(self, ctx):
        panels = await self.bot.db.fetch('SELECT * FROM self_role WHERE guild_id = $1', ctx.guild.id)
        if not panels:
            await ctx.send(
                embed = Utils.BotEmbed.error(f'This server don\'t have any self-role panels setup.')
            )
            return

        _list = []

        count = 0
        for panel in panels:
            count = count+1
            channel = self.bot.get_channel(panel[1])
            message = await channel.fetch_message(panel[0])
            _list.append(f'[**Panel {count}**]({message.jump_url}) - {channel.mention}')

        em = discord.Embed(title='Dynamic self-role menu', description='\n'.join(_list), color=Utils.BotColors.invis())
        em.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=em)





    @self_role.command(name='create', aliases=['make'])
    async def self_role_create(self, ctx):
        already_3 = await self.bot.db.fetch('SELECT * FROM self_role WHERE guild_id = $1', ctx.guild.id)
        if len(already_3) >= 3:
            await ctx.send(
                embed = Utils.BotEmbed.error('You already have 3 self role panels in your server.')
            )
            return

        channel_ = []
        title_ = []
        description_ = []
        role_ = {}


        ChannelEmbed = discord.Embed(description=f'<:rightarrow1:918127433184579594> In which **channel** you\'re planning to send the menu.\n<:rightarrow1:918127433184579594> You can send ID, mention or name of the channel\n> **Example** {ctx.channel.mention}', title='Dynamic self role menu', color=Utils.BotColors.invis())
        ChannelEmbed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        ChannelEmbed.set_footer(text='You can cancel this process by sending “cancel“ as reply.')
        ChannelEmbed.set_thumbnail(url='https://media.discordapp.net/attachments/918104349148860457/918123683954978897/settings.png')

        MainMessage = await ctx.send(embed=ChannelEmbed)

        _channel_ = await self.wait_for_channel_message(ctx, MainMessage)
        if not _channel_:
            return
        
        channel_.append(_channel_)

        TitleDescEmbed = discord.Embed(
            color=Utils.BotColors.invis(),
            description=f'<:rightarrow1:918127433184579594> What should be the **title** and **description** of the embed? seperate with “|“\n> **Example**: `This is the title | This is the description`',
            title='Dynamic self role menu'
        )
        TitleDescEmbed.set_thumbnail(url='https://media.discordapp.net/attachments/918104349148860457/918123683954978897/settings.png')
        TitleDescEmbed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        TitleDescEmbed.set_footer(text='You can cancel this process by sending “cancel“ as reply.')

        await MainMessage.edit(embed=TitleDescEmbed)


        _title_desc = await self.wait_for_titledesc_message(ctx, MainMessage)
        if not _title_desc:
            return

        title_.append(_title_desc[0])
        description_.append(_title_desc[1])

        RoleEmbed = discord.Embed(
            color = Utils.BotColors.invis(),
            description=f'<:rightarrow1:918127433184579594> Enter and role along with the description\n<:rightarrow1:918127433184579594> Enter them one by one. The bot will react with a tick if your entry is valid. Emojis are not necessary.\n<:rightarrow1:918127433184579594> Enter `-done` to end/complete the setup.\n> **Example**: `💙 | @BlueColorRole | Select to get blue color role`',
            title='Dynamic self role menu'
        )
        RoleEmbed.set_thumbnail(url='https://media.discordapp.net/attachments/918104349148860457/918123683954978897/settings.png')
        RoleEmbed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        RoleEmbed.set_footer(text='You can cancel this process by sending “cancel“ as reply.')

        await MainMessage.edit(embed=RoleEmbed)

        _role_desc_emoji = await self.wait_for_role_message(ctx, MainMessage)
        if not _role_desc_emoji:
            return


        for role in _role_desc_emoji:
            role_id = role['role'].id
            role_name = role['role'].name
            role_emoji = role['emoji']
            role_desc = role['desc']

            role_[role_name] = []
            role_[role_name].append({'id': role_id, 'emoji': role_emoji, 'desc': role_desc})

        em=discord.Embed(description='<a:timer:905859476257656872> **Loading Dynamic self-role menu** <a:timer:905859476257656872>', color=Utils.BotColors.invis())
        _final_channel = channel_[0]
        FinalMessage = await _final_channel.send(embed=em)
        self.bot.self_roles.append(FinalMessage.id)
        await self.bot.db.execute('INSERT INTO self_role (message_id,channel_id,guild_id) VALUES ($1,$2,$3)', FinalMessage.id, FinalMessage.channel.id, ctx.guild.id)
        await asyncio.sleep(0.5)
        await MainMessage.delete()

        options = []
        for final_role in role_.items():
            _role_name_final = final_role[0]
            _role_dict = final_role[1]
            if isinstance(_role_dict[0]['emoji'], str):
                _emoji_final = _role_dict[0]['emoji']
            elif isinstance(_role_dict[0]['emoji'], int):
                _emoji_final = self.bot.get_emoji(_role_dict[0]['emoji'])

            options.append(
                SelectOption(
                    label=_role_name_final,
                    value=str(_role_dict[0]['id']),
                    description=str(_role_dict[0]['desc']),
                    emoji=_emoji_final
                )
            )

        options.append(
            SelectOption(
                label='None',
                value='SelfRoleNone',
                emoji='🚫',
                description='De-select all options'
            )
        )

        components = [
            Select(placeholder='Dynamic self-role menu', options=options)
        ]

        FinalEmbed = discord.Embed(
            title=''.join(title_),
            description=''.join(description_),
            color=Utils.BotColors.invis()
        )
        await FinalMessage.edit(
            embed=FinalEmbed,
            components=components
        )



        await ctx.send(
            embed = Utils.BotEmbed.success(
                f'Successfully sent the [menu]({FinalMessage.jump_url}) in {FinalMessage.channel.mention}'
            )
        )




