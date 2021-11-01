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


def setup(client):
    client.add_cog(events(client))