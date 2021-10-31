import discord
import asyncio
import json
from discord.ext import commands



class events(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content != after.content:
            await self.client.process_commands(after)


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.id != self.client.user.id and str(payload.emoji) == u"\U0001F3AB":
                msg_id, channel_id, category_id = self.client.ticket_configs[payload.guild_id]

                if payload.message_id == msg_id:
                    guild = self.client.get_guild(payload.guild_id)

                    for category in guild.categories:
                        if category.id == category_id:
                            break

                    channel = guild.get_channel(channel_id)

                    ticket_channel = await category.create_text_channel(f"ticket-{payload.member.display_name}", topic=f"A ticket for {payload.member.display_name}.", permission_synced=True)
                    
                    await ticket_channel.set_permissions(payload.member, read_messages=True, send_messages=True)

                    message = await channel.fetch_message(msg_id)
                    await message.remove_reaction(payload.emoji, payload.member)

                    await ticket_channel.send(f"{payload.member.mention} Thank you for creating a ticket! Use **'-close'** to close your ticket.")

                    try:
                        await self.client.wait_for("message", check=lambda m: m.channel == ticket_channel and m.author == payload.member and m.content == "-close", timeout=3600)

                    except asyncio.TimeoutError:
                        await ticket_channel.delete()

                    else:
                        await ticket_channel.delete()

        if payload.member.bot:
            pass

        else:

            with open('data/reactrole.json') as react_file:
                data = json.load(react_file)
                for x in data:
                    if x['emoji'] == payload.emoji.name and x['message_id'] == payload.message_id:
                        role = discord.utils.get(self.client.get_guild(payload.guild_id).roles, id=x['role_id'])
                        await payload.member.add_roles(role)


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):

        with open('data/reactrole.json') as react_file:
            data = json.load(react_file)
        for x in data:
            if x['emoji'] == payload.emoji.name and x['message_id'] == payload.message_id:
                role = discord.utils.get(self.client.get_guild(payload.guild_id).roles, id=x['role_id'])

            await self.client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)


def setup(client):
    client.add_cog(events(client))