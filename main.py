import discord
import random
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from discord.ext.commands.errors import MaxConcurrencyReached
import praw
import urllib.parse, urllib.request, re
import os
import requests
import aiohttp
import math
#
import urllib.request
import urllib.parse
import hashlib
import requests
import re
import traceback
import aiofiles
import datetime
import asyncio
import json
import jishaku
import DiscordUtils
import asyncpg
import PIL.ImageOps
import googletrans
import mal
import itertools
import io
import datetime
import base64
import sys
import functools
import typing
import datetime, time
import dateutil.parser
from difflib import get_close_matches
from gtts import gTTS
from thispersondoesnotexist import get_online_person
from mal import *
from thispersondoesnotexist import save_picture
from googletrans import Translator
from PIL import Image
from discord import Webhook, AsyncWebhookAdapter
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
from discord import asset
from discord_components import *
from discord import channel
from discord import embeds, DMChannel
from random import choice
from asyncio import TimeoutError
from discord.colour import Color
from PIL import Image, ImageEnhance
from cogs.utils import GertyHelpCommand, Utils
from googleapiclient.discovery import build
from discord_together import DiscordTogether
from PIL import ImageFilter
from PIL import Image
from collections import namedtuple
from cogs.events import DisabledCommand, UserBlacklisted
import async_cse
import asyncpg
import ast
import inspect


INITIAL_EXTENSIONS = [
  'jishaku',
  'cogs.admin',
  'cogs.AFK',
  'cogs.covid',
  'cogs.dropdown_role',
  'cogs.embed_',
  'cogs.events',
  'cogs.github_api',
  'cogs.giveaways',
  'cogs.image',
  'cogs.misc',
  'cogs.moderation',
  'cogs.modlogs',
  'cogs.rtfm',
  'cogs.tags',
  'cogs.ticket_tool',
  'cogs.utils'
]


class GertyBot(commands.AutoShardedBot):
  def __init__(self, *args, **kwargs):
    print('__init__ called. Loading bot...')
    super().__init__(*args, **kwargs)

    self.news=f'<:updates:911239861225279488> **UPDATE**\n> New command `botinfo`\n> Shows information about me'
    self.db = self.loop.run_until_complete(asyncpg.create_pool(host="ec2-54-162-119-125.compute-1.amazonaws.com", port="5432", user="fejnxxnhwryzfy", password="5c956634680e4137ff4baede1a09b0f27e98f045eeb779b50d6729b0f5a2abae", database="dcph9t30tehh6l"))
    self.remove_command("help")

  async def load_cache(self):
    self.ticket_tool_guild_ids = []
    self.running_tickets = {}
    self.sniped_messages = {}
    self.self_roles = []
    self.messages_seen = 0
    self.command_usage = 0
    
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

  async def load_extensions(self):

    loaded_or_not = []

    for ext in INITIAL_EXTENSIONS:
      try:
        self.load_extension(ext)
      except commands.ExtensionAlreadyLoaded:
        try:
          self.reload_extension(ext)
        except Exception as error:
          loaded_or_not.append(f'<a:Redcircle:905396170925424651> Extension `{ext}` didn\'t load properly.')
          continue
      else:
        loaded_or_not.append(f'<a:GreenCircle:905843069549695026> Loaded extension `{ext}` succesfully.')

    em = discord.Embed(color=Utils.BotColors.invis, description='\n'.join(loaded_or_not))

    async with aiohttp.ClientSession() as session:
      web=Webhook.from_url(url='https://discord.com/api/webhooks/913841289198452767/QCan64ApWA4aP0-rSR664hq-HH3FUoEZ5dmFLZmT6lFNMPXVawJzpyAmDn6Nl9wpLItg', adapter=AsyncWebhookAdapter(session))
      await web.send(avatar_url='https://singlecolorimage.com/get/2bff00/400x100', username='Ext Logs', embeds = [em])
    return
 


  async def on_ready(self):
    DiscordComponents(self)

    print(f"Connected to {self.user}.")
    await self.load_cache()
    await self.load_extensions()
    self.uptime = time.time()

    async with aiohttp.ClientSession() as session:
      web=Webhook.from_url(url='https://discord.com/api/webhooks/907681269452800061/-uEovWEWLcEXKNecuYe_1OlfkSAlCpv_fR8TcH2TsBJ9wab52GdB6QarlHaa3WqUotqR', adapter=AsyncWebhookAdapter(session))
      await web.send('<:yes:910490899883126804> Connected to Gerty successfully.', avatar_url='https://singlecolorimage.com/get/2bff00/400x100', username='Status')



client = GertyBot(
  command_prefix = commands.when_mentioned_or('g!'),
  intents=discord.Intents.all(),
  activity=discord.Activity(type=discord.ActivityType.watching, name="My mobile"),
  status=discord.Status.online,
  strip_after_prefix=True,
  case_insensitive=True
)





def source(o):
  s = inspect.getsource(o).split("\n")
  indent = len(s[0]) - len(s[0].lstrip())
  return "\n".join(i[indent:] for i in s)

source_=source(discord.gateway.DiscordWebSocket.identify)
patched=re.sub(r'([\'"]\$browser[\'"]:\s?[\'"]).+([\'"])', r"\1Discord Android\2", source_)
loc = {}
exec(compile(ast.parse(patched), "<string>", "exec"),discord.gateway.__dict__, loc)
discord.gateway.DiscordWebSocket.identify = loc["identify"]







ch1 = ["Rock", "Scissors", "Paper"]
api_key = "AIzaSyDNgIRLXv0XcvFw_gJ_dpG2Cx-pkoN4Cio"


os.environ["JISHAKU_NO_UNDERSCORE"] = "True"

# also 
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 
os.environ["JISHAKU_HIDE"] = "True"









async def time_formatter(seconds: float):

  minutes, seconds = divmod(int(seconds), 60)
  hours, minutes = divmod(minutes, 60)
  days, hours = divmod(hours, 24)
  tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "")
  return tmp[:-2]



@client.check
async def check_blacklist(ctx):
  is_blacklisted=await client.db.fetchrow('SELECT * FROM blacklisted WHERE user_id=$1', ctx.author.id)
  if is_blacklisted:
    raise UserBlacklisted(ctx.author, reason=is_blacklisted['reason'])
    return False
  else:
    return True



@client.check
async def disabled_command(ctx):
  if ctx.author.id == 770646750804312105:
    return True
  is_disabled=await client.db.fetchrow('SELECT * FROM disabled WHERE channel_id=$1', ctx.channel.id)
  if is_disabled and ctx.command.name != 'toggle_commands':
      raise DisabledCommand
      return False
  else:
    return True


@client.command(brief='meta', description='Gets the bot uptime')
async def uptime(ctx):
  uptime = str(datetime.timedelta(seconds=int(round(time.time()-client.uptime))))
  em = discord.Embed(description=f"⏱️ {uptime}, Last restart <t:{int(client.uptime)}:R>", color=0x2F3136)
  main=await ctx.send(embed=em)
  for x in range(7):
    up2 = str(datetime.timedelta(seconds=int(round(time.time()-client.uptime))))
    em2 = discord.Embed(description=f"⏱️ {up2}, Last restart <t:{int(client.uptime)}:R>", color=0x2F3136)
    await main.edit(embed=em2)
    await asyncio.sleep(1)




@client.command(brief='mod', description='Toggle disable/enable commands per channel', usage='(channel)', aliases=['toggle', 'toggle-commands', 'toggle-all'])
@commands.has_permissions(manage_messages=True)
async def toggle_commands(ctx, channel:discord.TextChannel=None):
  if channel==None:
    channel=ctx.channel
  is_already_disabled=await client.db.fetch('SELECT * FROM disabled WHERE channel_id=$1', channel.id)
  if is_already_disabled:
    await client.db.execute('DELETE FROM disabled WHERE channel_id=$1', channel.id)
    disembed=discord.Embed(description=f'<:success:893501515107557466> Enabled commands in {channel.mention}', color=0x2F3136)
    return await ctx.send(embed=disembed)
  await client.db.execute("INSERT INTO disabled (channel_id) VALUES ($1)", channel.id)
  em=discord.Embed(description=f'<:success:893501515107557466> Disabled commands in {channel.mention}', color=0x2F3136)
  await ctx.send(embed=em)




@client.command(brief='fun', usage='[question]', description='Ask the magic 8ball a question!', aliases=['8ball'])
async def _8ball(ctx, *, question):
  responses = ["It is certain.",
"It is decidedly so.",
"Without a doubt.",
"Yes - definitely.",
"You may rely on it.",
"As I see it, yes.",
"Most likely.",
"Outlook good.",
"Yes.",
"Signs point to yes.",
"Reply hazy, try again.",
"Ask again later.",
"Better not tell you now.",
"Cannot predict now.",
"Concentrate and ask again.",
"Don't count on it.",
"My reply is no.",
"My sources say no.",
"Outlook not so good.",
"Very doubtful.",
"I didn't understand please repeat"]
  em = discord.Embed(description=f"**Question**: {question}\n **Reply**: {random.choice(responses)}")
  await ctx.send(embed=em)


@client.command(brief='util', usage='(member)', description='Get a user\'s avatar', aliases=["av"])
async def avatar(ctx, user: discord.Member=None):
    if user == None:
      if ctx.message.reference:
        user = ctx.message.reference.resolved.author
      else:
        user = ctx.author
    em = discord.Embed(title=f"{user.name}'s Avatar", description=f"[WEBP]({user.avatar_url_as(static_format='webp')}) | [JPEG]({user.avatar_url_as(static_format='jpeg')}) | [PNG]({user.avatar_url_as(static_format='png')})", color=0x2F3136)
    em.set_image(url=f"{user.avatar_url}")
    em.set_footer(text=f"Invoked by {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
    await ctx.send(embed=em)


#emojify command

#say command
@client.command(brief='util', usage='[text]', description='Make the bot say whatever you want', aliases=["s"])
async def say(ctx, *, content):
  try:
    await ctx.message.delete()
  except:
    pass
  if ctx.message.reference:
    await ctx.message.reference.resolved.reply(f"{content}", allowed_mentions=discord.AllowedMentions(everyone=False, roles=False))
  else:
    await ctx.send(f"{content}", allowed_mentions=discord.AllowedMentions(everyone=False, roles=False))



@client.command(brief='util', usage='[member] (reason)', description='Mutes a member so that they cannot talk or add reactions')
@commands.has_permissions(manage_channels=True)
async def mute(ctx, member: discord.Member, *, reason=None):
  if member.top_role >= ctx.author.top_role and not ctx.author == ctx.guild.owner:
    em = discord.Embed(description="<:error:867269410644557834> You are not high enough in the role hierarchy to mute that member", color=0x2F3136)
    await ctx.send(embed=em)
  else:
    guild= ctx.guild
    mutedRole = discord.utils.get(guild.roles, name='Muted')

    if not mutedRole:
      mutedRole = await guild.create_role(name="Muted")

      for channel in guild.channels:
        await channel.set_permissions(mutedRole, speak=False, send_messages=False)

    await member.add_roles(mutedRole, reason=reason)
    if reason == None:
      embed = discord.Embed(description=f"<:success:893501515107557466> Muted {member.name}#{member.discriminator}", color=0x2bff00)
      await ctx.send(embed=embed)
      await member.send(f'You were muted in the server **{guild.name}**')
    else:
      embed2 = discord.Embed(description=f"<:success:893501515107557466> Muted {member.name}#{member.discriminator} for reason **{reason}**", color=0x2bff00)
      await ctx.send(embed=embed2)
      await member.send(f'You were muted in the server **{guild.name}** for reason: __{reason}__')




@client.command(brief='util', usage='[member]', description='Unmutes a member from mute')
@commands.has_permissions(manage_channels=True)
async def unmute(ctx, member: discord.Member):
  mutedRole = discord.utils.get(ctx.guild.roles, name='Muted')

  await member.remove_roles(mutedRole)
  em = discord.Embed(description=f"<:success:893501515107557466> Unmuted {member.name}#{member.discriminator}", color=0x2bff00)
  await ctx.send(embed=em)
  await member.send(f'You are now unmuted in the server **{ctx.guild.name}**')



def convert(time):
  pos = ["s","m","h","d"]

  time_dict = {"s" : 1, "m" : 60, "h" : 3600, "d" : 3600*24}

  unit = time[-1]

  if unit not in pos:
    return -1
  try:
    val = int(time[:-1])
  except:
    return -2


  return val * time_dict[unit]


#tic tac toe command
player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]


@client.command(brief='fun', usage='[player1] [player2]', description='Start to play a tic tac toe game with  your friend!', aliases=['ttt'])
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("> **It is <@" + str(player1.id) + ">'s turn.**")
        elif num == 2:
            turn = player2
            await ctx.send("> **It is <@" + str(player2.id) + ">'s turn.**")
    else:
        await ctx.send("> **A game is already in progress! Finish it before starting a new one.**")


@client.command(brief='fun', usage='[tile number]', description='Place tic tac toe tile')
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " **wins!**")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("> ** It's a tie!**")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("> **Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.**")
        else:
            await ctx.send("> **It is not your turn.**")
    else:
        await ctx.send("> **Please start a new game using the g!ttt command.**")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("> **Please mention 2 players for this command.**")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("> **Please make sure to mention/ping players (ie. <@855443275658166282>).**")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("> **Please enter a position you would like to mark.**")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("> **Please make sure to enter an integer**.")


@client.command(brief='fun', usage='[search]', description='Search for anything in google', aliases=["show", "search", "img", "googlesearch"])
@commands.cooldown(1,5,commands.BucketType.user)
async def google(ctx, *, search):
  try:
    googleclient = async_cse.Search("AIzaSyDNgIRLXv0XcvFw_gJ_dpG2Cx-pkoN4Cio")
    results = await googleclient.search(f"{search}", safesearch=True, image_search=True)
  except:
    return await ctx.send("No results, try including more keywords")
    await googleclient.close()

    #embeds 
    #em1
  em1 = discord.Embed(title=f"{results[0].title}", description=f"{results[0].description}", url=f"{results[0].url}", color=0x2F3136)
  em1.set_image(url=f"{results[0].image_url}")
    #em2
  em2 = discord.Embed(title=f"{results[1].title}", description=f"{results[1].description}", url=f"{results[1].url}", color=0x2F3136)
  em2.set_image(url=f"{results[1].image_url}")
    #em3
  em3 = discord.Embed(title=f"{results[2].title}", description=f"{results[2].description}", url=f"{results[2].url}", color=0x2F3136)
  em3.set_image(url=f"{results[2].image_url}")

  em4 = discord.Embed(title=f"{results[3].title}", description=f"{results[3].description}", url=f"{results[3].url}", color=0x2F3136)
  em4.set_image(url=f"{results[3].image_url}")

  em5 = discord.Embed(title=f"{results[4].title}", description=f"{results[4].description}", url=f"{results[4].url}", color=0x2F3136)
  em5.set_image(url=f"{results[4].image_url}")

  em6 = discord.Embed(title=f"{results[5].title}", description=f"{results[5].description}", url=f"{results[5].url}", color=0x2F3136)
  em6.set_image(url=f"{results[5].image_url}")

  em7 = discord.Embed(title=f"{results[6].title}", description=f"{results[6].description}", url=f"{results[6].url}", color=0x2F3136)
  em7.set_image(url=f"{results[6].image_url}")

  em8 = discord.Embed(title=f"{results[7].title}", description=f"{results[7].description}", url=f"{results[7].url}", color=0x2F3136)
  em8.set_image(url=f"{results[7].image_url}")

  em9 = discord.Embed(title=f"{results[8].title}", description=f"{results[8].description}", url=f"{results[8].url}", color=0x2F3136)
  em9.set_image(url=f"{results[8].image_url}")

  em10 = discord.Embed(title=f"{results[9].title}", description=f"{results[9].description}", url=f"{results[9].url}", color=0x2F3136)
  em10.set_image(url=f"{results[9].image_url}")

    #pagination
  paginationList = [em1, em2, em3, em4, em5, em6, em7, em8, em9, em10]
  current = 0


  mainmessage = await ctx.send(embed=paginationList[current], components=[[Button(style=ButtonStyle.grey, id = "back", label='<'), Button(style=ButtonStyle.grey, label=f'{int(paginationList.index(paginationList[current])) + 1}/{len(paginationList)}', disabled=True), Button(style=ButtonStyle.grey, id = "front", label='>'), Button(style=ButtonStyle.red, id = "delete", emoji=client.get_emoji(890938576563503114))]])

  await googleclient.close()
  while True:
    try:
      event = await client.wait_for("button_click", check = lambda i: i.component.id in ["back", "front", "delete"], timeout=60.0)

      if event.author != ctx.author:
        await event.respond(
          type=4,
          content="Sorry, this buttons cannot be controlled by you"
        )
      else:
        if event.component.id == "back":
          current -= 1
        elif event.component.id == "front":
          current += 1
        elif event.component.id == "delete":
          try:
            await mainmessage.delete()
          except:
            pass
          break

        if current == len(paginationList):
          current = 0
        elif current < 0:
          current = len(paginationList) - 1
            
        await event.respond(
          type=7,
          embed=paginationList[current],
          components=[[Button(style=ButtonStyle.grey, id = "back", label='<'), Button(style=ButtonStyle.grey, label=f'{int(paginationList.index(paginationList[current])) + 1}/{len(paginationList)}', disabled=True), Button(style=ButtonStyle.grey, id = "front", label='>'), Button(style=ButtonStyle.red, id = "delete", emoji=client.get_emoji(890938576563503114))]]
        )
    except asyncio.TimeoutError:
      try:
        await mainmessage.edit(
          components=[[Button(style=ButtonStyle.grey, id = "back", label='<', disabled=True), Button(style=ButtonStyle.grey, label=f'{int(paginationList.index(paginationList[current])) + 1}/{len(paginationList)}', disabled=True), Button(style=ButtonStyle.grey, id = "front", label='>', disabled=True), Button(style=ButtonStyle.red, id = "delete", emoji=client.get_emoji(890938576563503114), disabled=True)]]
        )
        break
      except:
        break



#help command


#memes


#rps try :sob:
@client.command(brief='fun', description='Stars a rock paper scissors game!')
@commands.cooldown(1,5,commands.BucketType.user)
async def rps(ctx):

  comp = choice(ch1)
  yet = discord.Embed(title=f"{ctx.author.display_name}'s Rock Paper Scissors Game!", description="> Status: **You haven't clicked on any button yet!**", color=0xa600ff)
  win = discord.Embed(title=f"{ctx.author.display_name} You won!", description=f"> Status: **You Have Won** Bot had chosen {comp}", color=0x00ff08)
  out = discord.Embed(title=f"{ctx.author.display_name} You didn't click on time!", description="> Status: **Timed out**", color=0xff0000)
  lost = discord.Embed(title=f"{ctx.author.display_name} You Lost!", description=f"> Status: You have lost bot had chosen {comp}", color=0xff0000)
  tie = discord.Embed(title=f"{ctx.author.display_name} It's Tie", description=f"> Status: **It's a tie** bot had chosen {comp}", color=0xd4ff00)

  m = await ctx.send(
    embed=yet,
    components=[[Button(style=1, label="Rock",), Button(style=3, label="Paper"), Button(style=ButtonStyle.red, label="Scissors")]]
  )

  def check(res):
    return ctx.author == res.user and res.channel == ctx.channel

  try:
    res = await client.wait_for("button_click", check=check, timeout=15)
    player = res.component.label

    if player==comp:
      await m.edit(embed=tie, components=[])

    if player=="Rock" and comp=="Paper":
      await m.edit(embed=lost, components=[])

    if player=="Rock" and comp=="Scissors":
      await m.edit(embed=win, components=[])

    if player=="Paper" and comp=="Rock":
      await m.edit(embed=win, components=[])
    
    if player=="Paper" and comp=="Scissors":
      await m.edit(embed=lost, components=[])
    
    if player=="Scissors" and comp=="Rock":
      await m.edit(embed=lost, components=[])

    if player=="Scissors" and comp=="Paper":
      await m.edit(embed=win, components=[])

  except TimeoutError:
    await m.edit(
      embed=out,
      components=[[Button(label="Oops", disabled=True)]],
    )


  
#userinfo

@client.command(brief='util', usage='(member)', description='Get all info of a user', aliases=["userinfo", "ui"])
async def whois(ctx, member: discord.Member=None):
  if member == None:
    if ctx.message.reference:
      member = ctx.message.reference.resolved.author
    else:
      member = ctx.author
  roles = [role for role in member.roles]
  #general
  embed=discord.Embed(color=0x2F3136)
  embed.add_field(name="General Info", value=f"> **<:personadd:880087005520863263> User name**: {member.name}\n> **<:gtextchannel:856095565632765972> Discriminator**: #{member.discriminator}\n> **<:pencil:880087936043974716> Display name**: {member.display_name}\n> **<:graypin:880087574490808370> User ID**: {member.id}\n> <:image:873933502435962880> **Avatar URL**: [:link:]({member.avatar_url})", inline=False)

  #other info
  cdate = int(member.created_at.timestamp())
  jdate = int(member.joined_at.timestamp())
  if member.bot is True:
    bot = "<:success:893501515107557466>"
  else:
    bot = "<:error:867269410644557834>"

  if member.public_flags.hypesquad_balance is True:
    hypesquad="Balance <:balance:866614979214049290>"
  elif member.public_flags.hypesquad_bravery is True:
    hypesquad="Bravery <:bravery:866614978864873523>"
  elif member.public_flags.hypesquad_brilliance is True:
    hypesquad="Brilliance <:brilliance:866614979250487316>"
  else:
    hypesquad="<:error:867269410644557834>No hypesquad"
  try:
    if member.activities[0].name == None:
      activ = f"{member.activities[0].emoji}"
    elif {member.activities[0].emoji} == None:
      activ = f"{member.activities[0].name}"
    elif {member.activities[0].emoji} and {member.activities[0].name} != None:
      activ = f"{member.activities[0].emoji} {member.activities[0].name}"
  except:
    activ = "<:error:867269410644557834>No Activity/Status"
  sts = f"{member.status}"
  if sts == "dnd":
    status = "Do not disturb <a:dnd:880119895872897044>"
  elif sts == "idle":
    status = "Idle/AFK <a:idle:880119894593650698>"
  elif sts == "online":
    status = "Online <a:online:880119894702690375>"
  elif sts == "offline":
    status = "Offline <:offline:880120737162231828>"
  try:
    mob = f"{member.mobile_status}"
    des = f"{member.desktop_status}"
    web = f"{member.web_status}"
    if f"{member.status}" == "offline":
      stsresult = "<:error:867269410644557834>User is offline cannot retrieve info"
    elif not mob == "offline":
      stsresult = "Mobile :mobile_phone:"
    elif not des == "offline":
      stsresult = "Desktop <:desktop:880130561400766514>"
    elif not web == "offline":
      stsresult = "Web browser <:browser:880130561493069834>"
  except:
    stsresult = "Error retrieving info"
  #embed
  embed.add_field(name="Other info", value=f"> **<:plus:880083147893649468> Account created on**: <t:{cdate}:D>(<t:{cdate}:R>)\n> **<:plus:880083147893649468> Joined this server at**: <t:{jdate}:D>(<t:{jdate}:R>)\n> **:robot: Bot?**: {bot}\n> **<a:hypesquad:880084715690922074> hypesquad house**: {hypesquad}\n> **<:activity:880089919018659960> Activity/Custom status**: {activ}\n> **<:statusup:880122823719395348> User status**: {status}\n> **<:discordclient:880131587478528010> User client**: {stsresult}")

  if member.joined_at is None:
    pos = "<:error:867269410644557834>Could not locate position"
  else:
    pos = sum(m.joined_at < member.joined_at for m in ctx.guild.members if m.joined_at is not None)

  #Info in server
  r = " ".join([role.mention for role in roles if role != ctx.guild.default_role])
  embed.add_field(name="Info regarding this server", value=f"> **<:greactionrole:856129896106688522> Top role**: {member.top_role.mention}\n> **<:greactionrole:856129896106688522> Roles ({len(roles)})**: {r}\n> **<:join:880111799314284634> Join position**: {pos}", inline=False)
  embed.set_author(name=f"User info - {member}", icon_url=member.avatar_url)
  embed.set_thumbnail(url=member.avatar_url)
  embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
  await ctx.send(embed=embed)



@client.command(brief='mod', usage='(channel)', description='Locks a channel for @everyone role')
@commands.has_permissions(manage_channels = True)
async def lock(ctx, channel: discord.TextChannel = None):
  if channel == None:
    channel = ctx.channel
  await channel.set_permissions(ctx.guild.default_role, send_messages=False)
  embed = discord.Embed(description=f"<:success:893501515107557466> {channel.mention} is now locked", color=0x2bff00)
  await ctx.send(embed=embed)

  


@client.command(brief='mod', usage='(channel)', description='Unlocks a locked channel')
@commands.has_permissions(manage_channels = True)
async def unlock(ctx, channel: discord.TextChannel = None):
  if channel == None:
    channel = ctx.channel
    
  await channel.set_permissions(ctx.guild.default_role, send_messages=True)
  embed = discord.Embed(description=f"<:success:893501515107557466> {channel.mention} is now unlocked", color=0x2bff00)
  await ctx.send(embed=embed)



@client.command(brief='mod', usage='[seconds]', description='Sets slowmode in current channel')
@commands.has_permissions(manage_channels = True)
async def slowmode(ctx, seconds: int):
  await ctx.channel.edit(slowmode_delay=seconds)
  em = discord.Embed(description=f"<:success:893501515107557466> Set the slowmode delay in {ctx.channel.mention} to {seconds} seconds! <:slowmode:861261195621040138>", color=0x2bff00)
  await ctx.send(embed=em)




@client.command(brief='util', usage='[member] (new nick)', description='Sets new nickname to a member', pass_content=True)
@commands.cooldown(1,5,commands.BucketType.user)
async def nick(ctx, member: discord.Member, *, arg):
  await member.edit(nick=arg)
  await ctx.send(f'Nickname was changed for {member.mention} to {arg}')

@client.command(brief='util', usage='[member]', description='Resets nickname of a member'
, pass_content=True)
@commands.cooldown(1,5,commands.BucketType.user)
async def resetnick(ctx, member: discord.Member):
  await member.edit(nick=f"{member.name}")
  await ctx.send(f"Nickname reset to {member.name}")


    
@client.command(brief='fun', usage='[member]', description='Please don\'t do this!!!')
async def hack(ctx, user: discord.Member):
  m = await ctx.send(f"Hacking {user.name} for {ctx.author.name} now!")
  await asyncio.sleep(1)
  await m.edit("[▖] Finding id and pass (2fa bypassed)")
  await asyncio.sleep(1)
  await m.edit("[▖] Finding id and pass (2fa bypassed) - 10%")
  await asyncio.sleep(1)
  await m.edit("[▖] Finding id and pass (2fa bypassed) - 49%")
  await asyncio.sleep(1)
  await m.edit("[▖] Finding id and pass (2fa bypassed) - 100%")
  await asyncio.sleep(1)
  await m.edit(f"[▘] Found id and pass\n **ID:** {user.name}@gmail.com\n **PASS:** `XXXXXXXXX` (password can only be visible to {ctx.author.name})")
  await asyncio.sleep(1)
  await m.edit(f"[▝] Selling ID and PASS of {user.name} to **Dark web**")
  await asyncio.sleep(1)
  await m.edit(f"[▗]Finding ip address of {user.name}")
  await asyncio.sleep(1)
  await m.edit(f"[▗]Finding ip address of {user.name} - 16%")
  await asyncio.sleep(1)
  await m.edit(f"[▗]Finding ip address of {user.name} - 82%")
  await asyncio.sleep(1)
  await m.edit(f"[▗]Finding ip address of {user.name} - 100%")
  await asyncio.sleep(1)
  await m.edit("[▖]**IP:** 127.00.1")
  await asyncio.sleep(1)
  await m.edit(f"[▘] Injecting Trojan virus to discriminator #{user.discriminator} - 27%")
  await asyncio.sleep(1)
  await m.edit(f"[▘] Injecting Trojan virus to discriminator #{user.discriminator} - 88%")
  await asyncio.sleep(1)
  await m.edit(f"[▘] Injecting Trojan virus to discriminator #{user.discriminator} - 100%")
  await asyncio.sleep(1)
  await m.edit(f"[▝]Reporting discord for breaking TOS of account {user.name}")
  await asyncio.sleep(1)
  await m.edit(f"Completed hacking {user.name} for {ctx.author.name}")
  await ctx.send(f"{user.mention} you will be logged out from your account within 3 days enjoy your last days in discord <a:evil_peepo:862347454980947998>")


@client.command(brief='meta', usage='[your report]', description='Reports something to bot devs')
async def report(ctx, *, report=None):
  report_channel = client.get_channel(906874684119859230)
  time_when_report = datetime.datetime.now()
  timestamp_when_report = time_when_report.timestamp()
  try:
    invite = await ctx.channel.create_invite(max_age = 0, max_uses = 0)
  except:
    invite = "none"
  if report is None:
    return await ctx.send(f"{ctx.author.mention} Please include information about the report.")
  if len(ctx.message.content) < 20:
    await ctx.send("Your report must be at least 20 characters in length")
  else:
    em = discord.Embed(title="Gerty report logs", description=f"Report by {ctx.author} ({ctx.author.mention})\nOn server **[{ctx.guild.name}]({invite})**\nReported on <t:{int(timestamp_when_report)}:D> (<t:{int(timestamp_when_report)}:R>)", color=0x2F3136)
    em.set_thumbnail(url=f"{ctx.author.avatar_url}")
    em.set_author(name=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon_url}")
    em.add_field(name="Report 📥", value=f"{report}")
    em.set_footer(text=f"Invoker ID: {ctx.author.id}", icon_url=f"{ctx.author.avatar_url}")
    await ctx.send(":incoming_envelope: | _Your report has been sent to staff team!_")
    report_message = await report_channel.send(embed=em)
    ownerembed=discord.Embed(description=f"{ctx.author.name} has reported a bug!!! [Jump to report]({report_message.jump_url})", color=0x2F3136)
    fury = client.get_user(770646750804312105)
    await fury.send(embed=ownerembed)
    await report_message.add_reaction('✅')

    try:
      def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["✅"]

      reaction, user = await client.wait_for("reaction_add", timeout=604800, check=check)

      if str(reaction.emoji) == "✅":
        await ctx.author.send(":envelope_with_arrow: | Your report has been looked into and dealt with. Thanks for your report")
    except Exception as e:
      print(e)

#new music




@client.command(brief='meta', usage='[channel] (member)', description='Moves a member or you to another channel')
async def move(ctx , channel: discord.VoiceChannel, member:discord.Member=None):
  if member == None:
    member = ctx.author
  await member.move_to(channel)
  em = discord.Embed(description=f"<:success:893501515107557466> {member.mention} has been moved to {channel.mention}", color=ctx.author.color)
  await ctx.send(embed=em)            
           
 
#wanted
@client.command(brief='fun', usage='(member)', description='WANTED!!!')
async def wanted(ctx, user: discord.Member = None):
  if user == None:
    user = ctx.author

  wanted = Image.open("images/wanted.jpg")
  asset  = user.avatar_url_as(size = 128)
  data = BytesIO(await asset.read())
  pfp = Image.open(data)

  pfp = pfp.resize((177,177))
  wanted.paste(pfp, (136,245))

  wanted.save("profile.jpg")
  await ctx.send(file = discord.File("profile.jpg"))


@client.command(brief='fun', usage='(member 1) (member2)', description='Generates a drake meme')
async def drake(ctx, user: discord.Member = None, user2: discord.Member = None):
  if user2 == None:
    user2 = ctx.author

  drake = Image.open("images/drake.jpg")
  asset1  = user.avatar_url_as(size = 128)
  data = BytesIO(await asset1.read())
  pfp = Image.open(data)

  pfp = pfp.resize((272,255))
  drake.paste(pfp, (340,305))


  asset2  = user2.avatar_url_as(size = 128)
  data2 = BytesIO(await asset2.read())
  pfp2 = Image.open(data2)

  pfp2 = pfp2.resize((272,255))
  drake.paste(pfp2, (343,17))

  drake.save("drake2.jpg")
  await ctx.send(file = discord.File("drake2.jpg"))

@client.command(brief='fun', usage='(member)', description='Generates a spongebob meme', aliases=["spongebob"])
async def sponge(ctx, user: discord.Member = None):
  if user == None:
    user = ctx.author

  sponge = Image.open("images/spongebob.jpg")
  asset  = user.avatar_url_as(size = 128)
  data = BytesIO(await asset.read())
  pfp = Image.open(data)

  pfp = pfp.resize((186,244))
  sponge.paste(pfp, (75,123))

  sponge.save("spongebob2.jpg")
  await ctx.send(file = discord.File("spongebob2.jpg"))


@client.command(brief='util', usage='(channel)', description='Deletes a channel and create a clone of it')
@commands.has_permissions(manage_channels=True)
async def nuke(ctx, channel: discord.TextChannel=None):
  if channel==None:
    channel=ctx.channel
  await channel.delete(reason=f'Nuked by {ctx.author}')
  clone_channel=await channel.clone(reason=f'Nuked by {ctx.author}')
  await clone_channel.edit(position=channel.position)
  await clone_channel.send(f'Channel nuked by `{ctx.author.name}`')
  


@client.command(brief='meta', usage='[to language] [text]', description='Translates given text to given language')
async def translate(ctx, lang, *, args=None):
  if args == None:
    if ctx.message.reference:
      args = f"{ctx.message.reference.resolved.content}"
    else:
      args = "Please specify something to translate!!"
  t = Translator()
  a = t.translate(args, dest=lang)
  em = discord.Embed(description=f"<:replyingto:888432748065353749> **Translation**: {a.text}", color=0x2F3136)
  await ctx.send(embed=em)


def sync_anime(search):
  animeresult=AnimeSearch(search)
  anime=Anime(f"{animeresult.results[0].mal_id}")
  return anime

async def async_anime(search):
  thing=functools.partial(sync_anime, f'{search}')
  some_stuff=await client.loop.run_in_executor(None, thing)
  return some_stuff

@client.command(brief='fun', usage='[search]', description='Shows details of an anime')
async def anime(ctx, *, search):
  embed = discord.Embed(description=f"> {Utils.BotEmojis.loading()} Fetching anime details..", color=Utils.BotColors.invis())
  s = await ctx.send(embed=embed)
  anime=await async_anime(search)
  if anime==None:
    return await s.edit(embed=Utils.BotEmbed.errors(f'Sorry, there are no results for `{search}` in the database'))
  

  if not anime.type:
    _type='N/A'
  else:
    _type=anime.type
  if not anime.status:
    _status='N/A'
  else:
    _status=anime.status
  if not anime.score:
    _score='N/A'
  else:
    _score=anime.score
  if not anime.rank:
    _rank='N/A'
  else:
    _rank=f'Top {anime.rank}'
  if not anime.duration:
    _duration='N/A'
  else:
    _duration=anime.duration
  if not anime.rating:
    _rating='N/A'
  else:
    _rating=anime.rating
  if not anime.episodes:
    _episodes='N/A'
  else:
    _episodes=anime.episodes
  if not anime.aired:
    _aired='N/A'
  else:
    _aired=anime.aired
  if not anime.genres:
    _genres='N/A'
  else:
    _genres=', '.join(anime.genres)

  em = discord.Embed(title=f"{anime.title}", description=f"{str(anime.synopsis)}\n **Source**: {str(anime.source)}", url=anime.url, color=Utils.BotColors.invis())
  em.add_field(name="🗂️ Type", value=_type)
  em.add_field(name="⏳ Status", value=_status)
  em.add_field(name="⭐ Rating/10", value=_score)
  em.add_field(name=f"🏆 Rank", value=f"{_rank}")
  em.add_field(name="⏱️ Duration", value=_duration)
  em.add_field(name="⚠️ Rated to", value=_rating)
  em.add_field(name="💽 Episodes", value=_episodes)
  em.add_field(name="🗓️ Aired", value=_aired)
  em.add_field(name="➡️ Genres", value=_genres)
  em.set_thumbnail(url=anime.image_url)
  await s.edit(embed=em)


@client.command(brief='meta', usage='[channel]', description='Starts a youtube together activity')
async def ytt(ctx, channel: discord.VoiceChannel=None):
  if channel == None:
    await ctx.send("Please mention a voice channel to start the activity")
  else:
    link = await togetherControl.create_link(channel.id, 'youtube')
    em = discord.Embed(description=f"<:youtube:865883178904059924> [Click here to start Youtube Together activity]({link})", color=0xfd1212)
    s = await ctx.send(embed=em)
    await asyncio.sleep(60)
    embed = discord.Embed(description=f"This activity ended. Don't worry `/`ytt can help you out! <:wumpyyy:873171096176848967>", color=ctx.author.color)
    await s.edit(embed=embed)

@client.command(brief='meta', usage='[channel]', description='Starts a poker night activity')
async def poker(ctx, channel: discord.VoiceChannel=None):
  if channel == None:
    await ctx.send("Please mention a voice channel to start the activity")
  else:
    link = await togetherControl.create_link(channel.id, 'poker')
    em = discord.Embed(description=f"♠️ [Click here to start Poker night activity]({link})", color=0xfd1212)
    await ctx.send(embed=em)


@client.command(brief='meta', usage='[channel]', description='Starts a chess-in-the-park activity')
async def chess(ctx, channel: discord.VoiceChannel=None):
  if channel == None:
    await ctx.send("Please mention a voice channel to start the activity")
  else:
    link = await togetherControl.create_link(channel.id, 'chess')
    em = discord.Embed(description=f"♟️ [Click here to start Chess in the park activity]({link})", color=0xfd1212)
    await ctx.send(embed=em)


@client.command(brief='meta', usage='[channel]', description='Starts a betrayal activity')
async def betrayal(ctx, channel: discord.VoiceChannel=None):
  if channel == None:
    await ctx.send("Please mention a voice channel to start the activity")
  else:
    link = await togetherControl.create_link(channel.id, 'betrayal')
    em = discord.Embed(description=f"<:games:873121470308569168> [Click here to start betrayal.io activity]({link})", color=0xfd1212)
    await ctx.send(embed=em)

@client.command(brief='meta', description='Starts a fishington.io activity')
async def fishing(ctx, channel: discord.VoiceChannel=None):
  if channel == None:
    await ctx.send("Please mention a voice channel to start the activity")
  else:
    link = await togetherControl.create_link(channel.id, 'fishing')
    em = discord.Embed(description=f"<:games:873121470308569168> [Click here to start fishington.io activity]({link})", color=0xfd1212)
    await ctx.send(embed=em)
    

@client.command(brief='meta', usage='(member) [content]', description='Sends content from a webhook as the member')
async def webhook(ctx, member: typing.Optional[discord.Member] = None, *, content:str):
  if member==None:
    member=ctx.author

  if not await ctx.channel.webhooks():
    try:
      await ctx.channel.create_webhook(name='Gerty')
    except:
      return await ctx.send(embed=Utils.BotEmbed.error('There is no webhooks in this channel or bot does\'t have permission to access'))
  
  hooks=await ctx.channel.webhooks()
  data={
    'content': content,
    'avatar_url': str(member.avatar_url),
    'username': f'{member.display_name}'
  }
  try:
    await ctx.message.delete()
  except:
    pass
  async with aiohttp.ClientSession() as ses:
    async with ses.post(url=hooks[0].url, json=data) as rep:
      return
  
  
@client.command(brief='fun', usage='(member)', description='Are you sure to delete this trash?', aliases=["delete"])
async def trash(ctx, user: discord.Member = None):
  if user == None:
    user = ctx.author

  trash = Image.open("images/delete.png")
  asset  = user.avatar_url_as(size = 128)
  data = BytesIO(await asset.read())
  pfp = Image.open(data)

  pfp = pfp.resize((218,209))
  trash.paste(pfp, (109,129))

  trash.save("delete2.png")
  await ctx.send(file = discord.File("delete2.png"))
  
  
@client.command(brief='fun', usage='[member]', description='ewwww!!!', aliases=["affect"])
async def child(ctx, user: discord.Member = None):
  if user == None:
    user = ctx.author

  affect = Image.open("images/affect.png")
  asset  = user.avatar_url_as(size = 128)
  data = BytesIO(await asset.read())
  pfp = Image.open(data)

  pfp = pfp.resize((192,151))
  affect.paste(pfp, (166,355))

  affect.save("affect2.png")
  await ctx.send(file = discord.File("affect2.png"))
  
@client.command(brief='fun', usage='[user]', description='He is a sussy baka!!', aliases=["sus"])
async def amongus(ctx, user: discord.Member = None):
  if user == None:
    user = ctx.author

  sus = Image.open("images/sus.png")
  asset  = user.avatar_url_as(size = 128)
  data = BytesIO(await asset.read())
  pfp = Image.open(data)

  pfp = pfp.resize((204,171))
  sus.paste(pfp, (221,50))

  sus.save("sus2.png")
  await ctx.send(file = discord.File("sus2.png"))
  
  
#buttons array
buttons = [
    [
        Button(style=ButtonStyle.grey, label='1'),
        Button(style=ButtonStyle.grey, label='2'),
        Button(style=ButtonStyle.grey, label='3'),
        Button(style=ButtonStyle.blue, label='×'),
        Button(style=ButtonStyle.red, label='Exit')
    ],
    [
        Button(style=ButtonStyle.grey, label='4'),
        Button(style=ButtonStyle.grey, label='5'),
        Button(style=ButtonStyle.grey, label='6'),
        Button(style=ButtonStyle.blue, label='÷'),
        Button(style=ButtonStyle.red, label='←')
    ],
    [
        Button(style=ButtonStyle.grey, label='7'),
        Button(style=ButtonStyle.grey, label='8'),
        Button(style=ButtonStyle.grey, label='9'),
        Button(style=ButtonStyle.blue, label='+'),
        Button(style=ButtonStyle.red, label='Clear')
    ],
    [
        Button(style=ButtonStyle.grey, label='00'),
        Button(style=ButtonStyle.grey, label='0'),
        Button(style=ButtonStyle.grey, label='.'),
        Button(style=ButtonStyle.blue, label='-'),
        Button(style=ButtonStyle.green, label='=')
    ],
]
 
 
#brief='fun', usage='', description=''
@client.command(brief='fun', usage='[user]', description='Grayscales a users avatar')
async def grayscale(ctx, user: discord.Member=None):
    if user == None:
      user = ctx.author
    filename = "avatar1.jpg"
    await user.avatar_url.save(filename)
    img = Image.open('avatar1.jpg').convert('L')
    img.save('greyscale.jpg')
    f = discord.File("greyscale.jpg", filename="greyscale.jpg")
    em = discord.Embed(title=f"Image to gray", description=f"<:image:873933502435962880> Converted {user.name}'s [avatar]({user.avatar_url}) to gray", color=0x2F3136)
    em.set_image(url="attachment://greyscale.jpg")
    em.set_footer(text=f"Invoked by {ctx.author.name}", icon_url=ctx.author.avatar_url)
    await ctx.send(file=f, embed=em)

@client.command(brief='fun', usage='[user]', description='Inverts a users avatar')
async def invert(ctx, user: discord.Member=None):
  if user == None:
    user = ctx.author
  filename = "avatar1.jpg"
  await user.avatar_url.save(filename)
  image = Image.open('avatar1.jpg')
  inverted_image = PIL.ImageOps.invert(image)
  inverted_image.save('inverted.jpg')
  f = discord.File("inverted.jpg", filename="inverted.jpg")
  em = discord.Embed(title=f"Inverted image", description=f"<:image:873933502435962880> Inverted {user.name}'s [avatar]({user.avatar_url})", color=0x2F3136)
  em.set_image(url="attachment://inverted.jpg")
  em.set_footer(text=f"Invoked by {ctx.author.name}", icon_url=ctx.author.avatar_url)
  await ctx.send(file=f, embed=em)

 
@client.group(brief='image', description='Enhances a users avatar', usage='[sub command]', invoke_without_command=True)
async def enhance(ctx):
    em = discord.Embed(title="Image enhancement commands", description="**<a:dot:860177926851002418> g!enhance [option]**\n > <:image:873933502435962880> options:\n`color`, `contrast`, `brightness`, `sharpness`, `rgb`", color=0x2F3136)
    await ctx.send(embed=em)


@enhance.command(brief='image', usage='(user)', description='Enhances color of the users avatar')
async def color(ctx, user: discord.Member=None):
  if user == None:
    if ctx.message.reference:
      user = ctx.message.reference.resolved.author
    else:
      user = ctx.author
    filename = "avatar1.jpg"
    await user.avatar_url.save(filename)
    image = Image.open('avatar1.jpg')
    color = ImageEnhance.Color(image)
    color.enhance(1.5).save('color.jpg')
    f = discord.File("color.jpg", filename="color.jpg")
    em2 = discord.Embed(title=f"Image enhancements", description=f"<:image:873933502435962880> Enhanced color of {user.name}'s [avatar]({user.avatar_url})", color=0x2F3136)
    em2.set_image(url="attachment://color.jpg")
    em2.set_footer(text=f"Invoked by {ctx.author.name}", icon_url=ctx.author.avatar_url)
    await ctx.send(file=f, embed=em2)

@enhance.command(description='Enhances contrast of a user\'s avatar', usage='(user)')
async def contrast(ctx, user: discord.Member=None):
  if user == None:
    if ctx.message.reference:
      user = ctx.message.reference.resolved.author
    else:
      user = ctx.author
    filename = "avatar1.jpg"
    await user.avatar_url.save(filename)
    image = Image.open('avatar1.jpg')
    contrast = ImageEnhance.Contrast(image)
    contrast.enhance(1.5).save('contrast.jpg')
    f = discord.File("contrast.jpg", filename="contrast.jpg")
    em = discord.Embed(title=f"Image enhancements", description=f"<:image:873933502435962880> Enhanced contrast of {user.name}'s [avatar]({user.avatar_url})", color=0x2F3136)
    em.set_image(url="attachment://contrast.jpg")
    em.set_footer(text=f"Invoked by {ctx.author.name}", icon_url=ctx.author.avatar_url)
    await ctx.send(file=f, embed=em)

@enhance.command(description='Enhances brightness of a user\'s avatar', usage='(user)')
async def brightness(ctx, user:discord.Member=None):
  if user == None:
    if ctx.message.reference:
      user = ctx.message.reference.resolved.author
    else:
      user = ctx.author
    filename = "avatar1.jpg"
    await user.avatar_url.save(filename)
    image = Image.open('avatar1.jpg')
    brightness = ImageEnhance.Brightness(image)
    brightness.enhance(1.5).save('brightness.jpg')
    f = discord.File("brightness.jpg", filename="brightness.jpg")
    em = discord.Embed(title=f"Image enhancements", description=f"<:image:873933502435962880> Enhanced brightness of {user.name}'s [avatar]({user.avatar_url})", color=0x2F3136)
    em.set_image(url="attachment://brightness.jpg")
    em.set_footer(text=f"Invoked by {ctx.author.name}", icon_url=ctx.author.avatar_url)
    await ctx.send(file=f, embed=em)


@enhance.command(description='Enhances sharpness of a user\'s avatar', usage='(user)')
async def sharpness(ctx, user:discord.Member=None):
  if user == None:
    if ctx.message.reference:
      user = ctx.message.reference.resolved.author
    else:
      user = ctx.author
    filename = "avatar1.jpg"
    await user.avatar_url.save(filename)
    image = Image.open('avatar1.jpg')
    sharpness = ImageEnhance.Sharpness(image)
    sharpness.enhance(1.5).save('sharpness.jpg')
    f = discord.File("sharpness.jpg", filename="sharpness.jpg")
    em = discord.Embed(title=f"Image enhancements", description=f"<:image:873933502435962880> Enhanced sharpness of {user.name}'s [avatar]({user.avatar_url})", color=0x2F3136)
    em.set_image(url="attachment://sharpness.jpg")
    em.set_footer(text=f"Invoked by {ctx.author.name}", icon_url=ctx.author.avatar_url)
    await ctx.send(file=f, embed=em)

@enhance.command(description='Enhances rgb of a user\'s avatar', usage='(user)')
async def rgb(ctx, user:discord.Member=None):
  if user == None:
    if ctx.message.reference:
      user = ctx.message.reference.resolved.author
    else:
      user = ctx.author
    filename = "avatar1.jpg"
    await user.avatar_url.save(filename)
    image = Image.open('avatar1.jpg')
    red, green, blue = image.split()
    new_image = Image.merge("RGB", (green, red, blue))
    new_image.save('rbg.jpg')
    f = discord.File("rbg.jpg", filename="rbg.jpg")
    em = discord.Embed(title=f"Image enhancements", description=f"<:image:873933502435962880> Enhanced RGB of {user.name}'s [avatar]({user.avatar_url})", color=0x2F3136)
    em.set_image(url="attachment://rbg.jpg")
    em.set_footer(text=f"Invoked by {ctx.author.name}", icon_url=ctx.author.avatar_url)
    await ctx.send(file=f, embed=em)
  
  
@client.command(brief='fun', description='This person does not exist??', aliases=["doesnotexist", "thispersondoesnotexist"])
async def persondoesnotexist(ctx):
  
  picture = await get_online_person()
  
  await save_picture(picture, "doesnotexist.jpeg")
  f = discord.File("doesnotexist.jpeg", filename="doesnotexist.jpeg")
  em = discord.Embed(title='This person does not exist', color=0x2F3136)
  em.set_image(url="attachment://doesnotexist.jpeg")
  em.set_footer(text='Generative adversarial network')
  await ctx.send(file=f, embed=em)



  
@client.command(brief='util', description='Know all about current server', aliases=["si"])
async def serverinfo(ctx):
  if ctx.guild.description is not None:
    desc = f"> **<:tag:880100337745264680> Server Description**: {ctx.guild.description}"
  else:
    desc = ""
  em = discord.Embed(description=f"{desc}", color=0x2F3136)
  em.set_author(name=f"Server info - {ctx.guild.name}", icon_url=f"{ctx.guild.icon_url}")
  #fields
  #general info
  em.add_field(name="General Info", value=f"> **<:gsupportserver:855714629606703124> Server name**: {ctx.guild.name}\n> **<:graypin:880087574490808370> Server ID**: {ctx.guild.id}\n> **<:image:873933502435962880> Icon URL**: [:link:]({ctx.guild.icon_url})\n> **<:serverowner:880438839783600158> Server owner**: {ctx.guild.owner}({ctx.guild.owner.mention})", inline=False)
  #other info
  try:
    if ctx.guild.afk_channel is not None:
      afkch = f"{ctx.guild.afk_channel.mention}"
      afkti = f"\n> **<:slowmode:861261195621040138> Afk timeout**: {int(ctx.guild.afk_timeout/60)} minutes"
    else:
      afkch = "<:error:867269410644557834> No afk channel"
      afkti = ""
  except:
    afkch = "<:error:867269410644557834> cannot fetch info"
    afkti = ""
  c = f"{int(ctx.guild.created_at.timestamp())}"
  em.add_field(name="Other info", value=f"> **:zzz: Afk channel**: {afkch}{afkti}\n> **:earth_africa:  Server regi-**: {ctx.guild.region}\n> **<:discord_member:860138883165061120> Server members**: {len(ctx.guild.members)}\n> **<:cancel:872394940779474985> Max members**: {ctx.guild.max_members}\n> **:video_camera:  Max video channel users**: {ctx.guild.max_video_channel_users}\n> **<:boost:880459171991003146> Boost level**: {ctx.guild.premium_tier}\n> **<:boost:880459171991003146> Total boosts**: {ctx.guild.premium_subscription_count}\n> **<:plus:880083147893649468> Created at**: <t:{c}:D>(<t:{c}:R>)", inline=False)
  em.set_thumbnail(url=f"{ctx.guild.icon_url}")
  #moderation
  if f"{ctx.guild.mfa_level}" == "0":
    mfa = "Does not require 2FA for moderation"
  elif f"{ctx.guild.mfa_level}" == "1":
    mfa = "Required 2FA for moderation"
  #
  if f"{ctx.guild.explicit_content_filter}" == "all_members":
    filterf = "Scan media content from all members"
  elif f"{ctx.guild.explicit_content_filter}" == "disabled":
    filterf = "Don't scan any media content"
  elif f"{ctx.guild.explicit_content_filter}" == "no_role":
    filterf = "Scan media content from members without role"

  em.add_field(name="Security info", value=f"> **<:staff:880448969921142845> 2FA authorisation level**: {mfa}\n> **<:blurplemoderator:862212401080434698> Verification level**: {ctx.guild.verification_level}\n> **<:nsfwchannel:880452038297804850> Explicit content filter**: {filterf}", inline=False)
  await ctx.send(embed=em)
  

@client.command(brief='fun', description='Generates a fake but original discord token of a user', usage='(user)', aliases=["whattoken", "what_token"])
async def generate_token(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author
    byte_first = str(member.id).encode('ascii')
    first_encode = base64.b64encode(byte_first)
    first = first_encode.decode('ascii')
    time_rn = datetime.datetime.utcnow()
    epoch_offset = int(time_rn.timestamp())
    bytes_int = int(epoch_offset).to_bytes(10, "big")
    bytes_clean = bytes_int.lstrip(b"\x00")
    unclean_middle = base64.standard_b64encode(bytes_clean)
    middle = unclean_middle.decode('utf-8').rstrip("==")
    Pair = namedtuple("Pair", "min max")
    num = Pair(48, 57)  # 0 - 9
    cap_alp = Pair(65, 90)  # A - Z
    cap = Pair(97, 122)  # a - z
    select = (num, cap_alp, cap)
    last = ""
    for each in range(27):
        pair = random.choice(select)
        last += str(chr(random.randint(pair.min, pair.max)))

    complete = ".".join((first, middle, last))


    embed = discord.Embed(
        title=f"{member.display_name}'s token",
        description=f"**User:** `{member}`\n"
                    f"**ID:** `{member.id}`\n"
                    f"**Bot:** `{member.bot}`",
        color=0x2F3136
        )
    embed.add_field(name="Token created:", value=f"<t:{epoch_offset}> (<t:{epoch_offset}:R>)", inline=False)
    embed.add_field(name="Generated Token:", value=f"`{complete}`", inline=False)
    embed.set_footer(text="This command is not a copy")
    embed.set_thumbnail(url=member.avatar_url)
    await ctx.send(embed=embed)

@client.command(brief='fun', description='You fucking weeb')
async def waifu(ctx):
  async with aiohttp.ClientSession() as cs:
      async with cs.get('https://api.waifu.pics/sfw/waifu') as r:
          res = await r.json()  # returns dict
          embed = discord.Embed(color=0x2F3136)
          embed.set_image(url=f"{res['url']}")
          embed.set_footer(text=f"Invoked by {ctx.author.name} · SFW - enabled", icon_url=f"{ctx.author.avatar_url}")
          await ctx.send(embed=embed)


@client.command(brief='fun', description='Http cat images', usage='(http status code)', aliases=['http_cat'])
async def http(ctx, status_code):
  embed = discord.Embed(color=0x2F3136)
  embed.set_image(url=f"https://http.cat/{status_code}")
  embed.set_footer(text=f"Invoked by {ctx.author.name}", icon_url=f"{ctx.author.avatar_url}")
  await ctx.send(embed=embed)



@client.command(brief='fun', description='Make the bot say (in voice) whatever you want', usage='[text]')
async def tts(ctx, *, text:commands.clean_content):
  em = discord.Embed(description="<a:z_loading:878684429789306920> Processing your tts", color=0x2F3136)
  if len(text) >= 20:
    d = await ctx.send(embed=em)
  texttotts = f"{text}"
  language='en'
  output=gTTS(text=texttotts, lang=language, slow=False)
  output.save('tts.mp3')
  if len(text) >= 20:
    await d.delete()
  await ctx.send(f"{ctx.author.mention}",file=discord.File('tts.mp3'))



@client.command(brief='fun', description='NITRO!!! FREE NITRO!!!')
async def nitro(ctx):
  em=discord.Embed(title="Nitro", description="Expires in 48 hours", color=0x2F3136)
  em.set_author(name="A WILD GIFT APPEARS!")
  em.set_thumbnail(url="https://media.discordapp.net/attachments/884423056934711326/888057999875244072/2Q.png")


  components = [
    Button(style=ButtonStyle.green, label='⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ACCEPT⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀', id='NitroButton')
  ]

  main = await ctx.send(embed=em, components=components)

  while True:
    try:
      event = await client.wait_for('button_click', check=lambda i: i.channel==ctx.channel and i.message==main, timeout=40) #
      if event.author==ctx.author:
        await event.respond(type=4, content="You cannot claim your gift yourself!")
      elif event.component.id=='NitroButton':
        await main.edit(components=[Button(style=ButtonStyle.gray, label='⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀CLAIMED⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀', id='NitroButton', disabled=True)])
        await event.respond(type=4, content='https://tenor.com/view/rick-roll-nitro-gif-21997352')
        try:
          await ctx.author.send(f"You've rickrolled {event.author.name} :joy:")
        except:
          pass
        break

    except asyncio.TimeoutError:
      try:
        await ctx.author.send('No one fall for your nitro <:Sad_cat:900825746841411604>')
      except:
        pass
      embi=discord.Embed(color=Utils.BotColors.invis(), title='Nitro', description='The gift link has either expired\n or has been revoked.')
      embi.set_author(name="You recived a gift, but...")
      embi.set_thumbnail(url='https://external-preview.redd.it/9HZBYcvaOEnh4tOp5EqgcCr_vKH7cjFJwkvw-45Dfjs.png?auto=webp&s=ade9b43592942905a45d04dbc5065badb5aa3483')
      await main.edit(embed=embi, components=[Button(style=ButtonStyle.gray, label='⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ACCEPT⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀', id='NitroButton', disabled=True)])
      break







@client.command(brief='fun', description='Find all emoji an emoji', usage='[emoji]', aliases=['emoinfo', 'emojinfo'])
async def emojiinfo(ctx, emoji : typing.Union[discord.Emoji, discord.PartialEmoji]):
  if isinstance(emoji, discord.Emoji):
    fetchedEmoji = await ctx.guild.fetch_emoji(emoji.id)
    url = f"{emoji.url}"
    available = "No"
    managed = "No"
    animated = "No"
    user = f"{fetchedEmoji.user}"

    emoji_created_at = int(emoji.created_at.timestamp())
    compo = [Button(style=ButtonStyle.URL, label="Emoji link", emoji="🔗", url=url)]

    if fetchedEmoji.user is None:
      user = "Couldn't get user"
    if emoji.available:
      available = "Yes"
    if emoji.managed:
      managed = "Yes"
    if emoji.animated:
      animated = "Yes"
    
    em = discord.Embed(description=f"<:pencil:880087936043974716> **Name:** {emoji.name}\n<:graypin:880087574490808370> **ID:** {emoji.id}\n<:plus:880083147893649468> **Created at:** <t:{emoji_created_at}:D> (<t:{emoji_created_at}:R>)\n:link: **Link:** [Click here]({url})\n<:nitro:892417079460888596> **Animated?:** {animated}\n<:personadd:880087005520863263> **Created by**: {user}\n<:gsupportserver:855714629606703124> **Guild**: {emoji.guild}\n<:twitch:892419054818689045> **Twitch managed?**: {managed}\n<:online:891215382914953247> **Available?**: {available}", color=0x2F3136)
    em.set_thumbnail(url=emoji.url)
    await ctx.send(embed=em, components=compo)

  elif isinstance(emoji, discord.PartialEmoji):
    url = f"{emoji.url}"
    animated = "No"
    if emoji.animated:
      animated = "Yes"
    emoji_created_at = int(emoji.created_at.timestamp())
    compo = [Button(style=ButtonStyle.URL, label="Emoji link", emoji="🔗", url=url)]
    em = discord.Embed(description=f"<:pencil:880087936043974716> **Name:** {emoji.name}\n<:graypin:880087574490808370> **ID:** {emoji.id}\n<:plus:880083147893649468> **Created at:** <t:{emoji_created_at}:D> (<t:{emoji_created_at}:R>)\n:link: **Link:** [Click here]({url})\n<:nitro:892417079460888596> **Animated?:** {animated}", color=0x2F3136)
    em.set_thumbnail(url=emoji.url)
    await ctx.send(embed=em, components=compo)
  else:
    await ctx.send("wtf?? whattttttt")


@client.group(brief='fun', description='Find who is lurking in your chat with buttons',invoke_without_command=True)
async def lurking(ctx):
  compo = [Button(style=ButtonStyle.gray, emoji="👀", id="lurk")]
  mainmessage = await ctx.send(
    "👀",
    components=compo
  )
  lurkers = []
  while True:
    try:
      event = await client.wait_for("button_click", check=lambda i: i.component.id in ["lurk"], timeout=10.0)
      if event.component.id == "lurk":
        if f"{event.author.name}" in lurkers:
          await event.respond(
            content="Why are you lurking? <:Kekw:832585380183408691>",
            type=4
          )
        else:
          await event.respond(
            content=f"`{event.author.name}` is lurking 👀",
            type=4,
            ephemeral=False
          )
          lurkers.append(f"{event.author.name}")
    except:
      await mainmessage.edit(components=[Button(style=ButtonStyle.gray, emoji=client.get_emoji(759934286097809428), id="lurk", label="No one lurking", disabled=True)])
      break

@lurking.command(brief='fun', description='Find who is lurking in your chat with selects')
async def select(ctx):
  compo = [Select(placeholder="hello!", options=[
    SelectOption(
      label="select me?",
      emoji="👀",
      value="lurk2"
    ),
    SelectOption(
      label="select me too?",
      emoji="👀",
      value="lurk3"
    ),
  ])]
  lurkers = []
  mainmessage = await ctx.send("👀", components=compo)

  while True:
    try:
      event = await client.wait_for("select_option", check=None, timeout=10.0)
      value = event.values[0]

      if value == "lurk2" or "lurk3":
        if f"{event.author.name}" in lurkers:
          await event.respond(
            content="Why are you lurking? <:Kekw:832585380183408691>",
            type=4
          )
        else:
          await event.respond(
            content=f"`{event.author.name}` is lurking 👀",
            type=4,
            ephemeral=False
          )
          lurkers.append(f"{event.author.name}")
    except asyncio.TimeoutError:
      compo2 = [Select(placeholder="No one lurking :(", disabled=True, options=[
        SelectOption(
          label="select me?",
          emoji="👀",
          value="lurk2"
        )
      ])]
      await mainmessage.edit(components=compo2)
      


client.run("ODU1NDQzMjc1NjU4MTY2Mjgy.YMyjog.PbT8noERy_xLFxNVK16iLvNdU-s", reconnect=True)
