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
                await resMessage.add_reaction('<a:error:918118195376816128>')
                continue

            await resMessage.delete()
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
                await resMessage.add_reaction('<a:error:918118195376816128>')
                continue

            await resMessage.delete()
            return [title_, _desc]


    def isDiscordEmoji(emoji):
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

            if resMessage.lower() == 'done':
                await resMessage.delete()
                return role__


            splited_ = resMessage.split('|')
            if not len(splited_) == 3:
                await resMessage.add_reaction('<a:error:918118195376816128>')
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
                await resMessage.add_reaction('<a:error:918118195376816128>')
                continue

            role__.append({'role': role_be, 'emoji': emoji_, 'desc': description_})
            count += 1
            await resMessage.delete()


        return role__

            




    @commands.group(name='selfrole', invoke_without_command=True)
    @commands.is_owner()
    @commands.bot_has_permissions(manage_channels=True, manage_messages=True, manage_roles=True)
    @commands.has_permissions(manage_channels=True, manage_messages=True, manage_roles=True)
    async def self_role(self, ctx):
        pass


    @self_role.command(name='create')
    async def self_role_create(self, ctx):
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
        TitleDescEmbed.set_author(name=self.bot.user.name, icon_url=self.bot.avatar_url)
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
        RoleEmbed.set_author(name=self.bot.user.name, icon_url=self.bot.avatar_url)
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
            role[role_name].append({'id': role_id, 'emoji': role_emoji, 'desc': role_desc})

        em=discord.Embed(description='<a:timer:905859476257656872> Loading Dynamic self-role menu <a:timer:905859476257656872>')
        _final_channel = channel_[0]
        FinalMessage = await _final_channel.send(embed=em)

        options = []
        for final_role in role_.items():
            _role_name_final = final_role[0]
            _role_dict = final_role[1]
            if isinstance(_role_dict['emoji'], str):
                _emoji_final = _role_dict['emoji']
            elif isinstance(_role_dict['emoji'], int):
                _emoji_final = self.bot.get_emoji(_role_dict['emoji'])

            options.append(
                SelectOption(
                    label=_role_name_final,
                    value=str(_role_dict['id']),
                    description=str(_role_dict['desc']),
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




