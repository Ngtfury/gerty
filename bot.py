import discord
from discord import webhook
from discord.enums import try_enum
from discord.ext import commands
import asyncpg
import os
import aiohttp
import time
import discord_webhook
from discord_webhook import DiscordWebhook, DiscordEmbed
from cogs.utils import Utils



class GertyBot(commands.AutoShardedBot):
    """A top-tier multi-purpose alternative for discord bots"""

    def __init__(self):
        print('__init__ called. Loading bot...')
        super().__init__(
            command_prefix = commands.when_mentioned_or('g!', 'G!'),
            intents=discord.Intents.all(),
            strip_after_prefix=True,
            case_insensitive=True
        )
        self.maintenance_mode = False
        self.maintenance_timestamp = 1640277000

        self.news=f'<:updates:911239861225279488> **UPDATE**\n> New command `welcomer`\n> Welcome new members with a message\n> and autoroles..'
        self.db = self.loop.run_until_complete(asyncpg.create_pool(host="ec2-54-162-119-125.compute-1.amazonaws.com", port="5432", user="fejnxxnhwryzfy", password="5c956634680e4137ff4baede1a09b0f27e98f045eeb779b50d6729b0f5a2abae", database="dcph9t30tehh6l"))
        print('Connected to database.')
        self.remove_command("help")
        self.token = "ODU1NDQzMjc1NjU4MTY2Mjgy.YMyjog.PbT8noERy_xLFxNVK16iLvNdU-s"
        os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
        os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 
        os.environ["JISHAKU_HIDE"] = "True"

    async def load_cache(self):
        self.ticket_tool_guild_ids = []
        self.running_tickets = {}
        self.sniped_messages = {}
        self.self_roles = []
        self.messages_seen = 0
        self.command_usage = 0
        self.bot_mention = {}
        self.afk = {}
        self.reminder = {}
        self.INITIAL_EXTENSIONS = [
            'jishaku',
        ]
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                self.INITIAL_EXTENSIONS.append(f'cogs.{filename[:-3]}')
        self.INITIAL_EXTENSIONS.remove('cogs.reminder')
        

        message_ids=await self.db.fetch('SELECT guild_id FROM ticket_tool')
        for id in message_ids:
            self.ticket_tool_guild_ids.append(id[0])

        running_ids=await self.db.fetch('SELECT guild_id,author_id FROM running_tickets')
        for guild in self.ticket_tool_guild_ids:
            self.running_tickets[guild]=[]

        for rid in running_ids:
            try:
                self.running_tickets[rid[0]].append(rid[1])
            except KeyError:
                pass


        self_role_message = await self.db.fetch('SELECT * FROM self_role')
        for message_id in self_role_message:
            self.self_roles.append(message_id[0])


        afk_users = await self.db.fetch('SELECT * FROM afk')
        for afk_user in afk_users:
            self.afk[afk_user['user_id']] = {}
            self.afk[afk_user['user_id']]['reason'] = afk_user['reason']
            self.afk[afk_user['user_id']]['time'] = afk_user['time']
            self.afk[afk_user['user_id']]['global'] = afk_user['global']
            self.afk[afk_user['user_id']]['guild_id'] = afk_user['guild_id'] if afk_user['guild_id'] else None


        print('Loaded cache successfully.')

    def load_or_reload(self, ext):
        try:
            self.reload_extension(ext)
        except commands.ExtensionNotFound:
            self.load_extension(ext)



    async def load_extensions(self):

        loaded_or_not = []

        for ext in self.INITIAL_EXTENSIONS:
            try:
                #self.load_or_reload(ext)
                self.load_extension(ext)
                loaded_or_not.append(f'<a:GreenCircle:905843069549695026> Loaded extension `{ext}` succesfully.')
            except:
                loaded_or_not.append(f'<a:Redcircle:905396170925424651> Extension `{ext}` didn\'t load properly.')
                continue
                

        em = DiscordEmbed(color=Utils.BotColors.invis(), description='\n'.join(loaded_or_not))

        webhook = DiscordWebhook(
            url='https://discord.com/api/webhooks/913841289198452767/QCan64ApWA4aP0-rSR664hq-HH3FUoEZ5dmFLZmT6lFNMPXVawJzpyAmDn6Nl9wpLItg',
            avatar_url='https://singlecolorimage.com/get/2bff00/400x100', 
            username='Ext Logs'
        )
        webhook.add_embed(em)
        webhook.execute()
        print('Loaded extensions successfully.')
        return


    @property
    async def status_invis(self):
        await self.change_presence(status=discord.Status.invisible, activity=self.activity)

    @property
    async def status_idle(self):
        await self.change_presence(status=discord.Status.idle, activity=self.activity)

    @property
    async def status_dnd(self):
        await self.change_presence(status=discord.Status.dnd, activity=self.activity)

    @property
    async def status_online(self):
        await self.change_presence(status=discord.Status.online, activity=self.activity)

    async def on_ready(self):

        await self.load_cache()
        await self.load_extensions()
        for shard in self.shards:
            if not self.maintenance_mode:
                activity=discord.Activity(
                    type = discord.ActivityType.watching,
                    name = f'@Gerty | g!help | {len(self.guilds)} servers | Shard {shard}'
                )
                await self.change_presence(status=discord.Status.online, activity=activity, shard_id=shard)
            else:
                await self.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.competing, name='Maintenance'), shard_id=shard)

        self.uptime = time.time()

        webhook = DiscordWebhook(
            url='https://discord.com/api/webhooks/907681269452800061/-uEovWEWLcEXKNecuYe_1OlfkSAlCpv_fR8TcH2TsBJ9wab52GdB6QarlHaa3WqUotqR',
            content = '<:yes:910490899883126804> Connected to Gerty successfully.', 
            avatar_url='https://singlecolorimage.com/get/2bff00/400x100', username='Status'
        )
        webhook.execute()

        print(f"Connected to {self.user}.")

    def run(self):
        super().run(self.token, reconnect=True)

