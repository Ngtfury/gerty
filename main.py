import discord
import random
from discord.ext import commands
import praw
import urllib.parse, urllib.request, re
import os
import requests
import aiohttp
import math
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
from googleapiclient.discovery import build
from discord_together import DiscordTogether
from PIL import ImageFilter
from PIL import Image
from collections import namedtuple
import async_cse
import asyncpg
import ast
import inspect

activity = discord.Activity(type=discord.ActivityType.watching, name="My mobile")
client = commands.AutoShardedBot(command_prefix = commands.when_mentioned_or("g!", "g! ", "!g"), intents=discord.Intents.all(), activity=activity, status=discord.Status.online, owner_ids=[770646750804312105, 343019667511574528, 293468815130492928])
togetherControl = DiscordTogether(client)
client.remove_command("help")


client.db = client.loop.run_until_complete(asyncpg.create_pool(host="ec2-54-162-119-125.compute-1.amazonaws.com", port="5432", user="fejnxxnhwryzfy", password="5c956634680e4137ff4baede1a09b0f27e98f045eeb779b50d6729b0f5a2abae", database="dcph9t30tehh6l"))



def source(o):
  s = inspect.getsource(o).split("\n")
  indent = len(s[0]) - len(s[0].lstrip())
  return "\n".join(i[indent:] for i in s)

source_=source(discord.gateway.DiscordWebSocket.identify)
patched=re.sub(r'([\'"]\$browser[\'"]:\s?[\'"]).+([\'"])', r"\1Discord Android\2", source_)
loc = {}
exec(compile(ast.parse(patched), "<string>", "exec"),discord.gateway.__dict__, loc)
discord.gateway.DiscordWebSocket.identify = loc["identify"]





for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    try:
      client.load_extension(f'cogs.{filename[:-3]}')
      print(f'Loaded module {filename[:-3]} succesfully ✅')
    except:
      print(f'Module {filename[:-3]} didn\'t load properly ❌')
client.load_extension('jishaku')
print(f'Loaded module jishaku succesfully ✅')
print('--------------------------------')
print('Connecting to bot...')


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


class UserBlacklisted(commands.CheckFailure):
  def __init__(self, user, reason, *args, **kwargs):
    self.user=user
    self.reason=reason
    super().__init__(*args, **kwargs)


@client.check
async def check_blacklist(ctx):
  is_blacklisted=await client.db.fetchrow('SELECT * FROM blacklisted WHERE user_id=$1', ctx.author.id)
  if is_blacklisted:
    raise UserBlacklisted(ctx.author, reason=is_blacklisted['reason'])
    return False
  else:
    return True


@client.event
async def on_ready():
  DiscordComponents(client)
  async with aiofiles.open("ticket_configs.txt", mode="a") as temp:
        pass

  async with aiofiles.open("ticket_configs.txt", mode="r") as file:
        lines = await file.readlines()
        for line in lines:
            data = line.split(" ")
            client.ticket_configs[int(data[0])] = [int(data[1]), int(data[2]), int(data[3])]

  print(f"Connected to {client.user.name}.")
  client.uptime = time.time()

@client.command()
async def uptime(ctx):
  uptime = str(datetime.timedelta(seconds=int(round(time.time()-client.uptime))))
  em = discord.Embed(description=f"⏱️ {uptime}, Last restart <t:{int(client.uptime)}:R>", color=0x2F3136)
  main=await ctx.send(embed=em)
  for x in range(7):
    up2 = str(datetime.timedelta(seconds=int(round(time.time()-client.uptime))))
    em2 = discord.Embed(description=f"⏱️ {up2}, Last restart <t:{int(client.uptime)}:R>", color=0x2F3136)
    await main.edit(embed=em2)
    await asyncio.sleep(1)


@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    em = discord.Embed(description="<:error:893501396161290320> Please wait **{:.2f}** seconds before using this command again".format(error.retry_after), color=0x2F3136)
    await ctx.send(embed=em)
  elif isinstance(error, commands.MissingRequiredArgument):
    em = discord.Embed(description=f"<:error:893501396161290320> You are missing a required argument `{error.param.name}`", color=0x2F3136)
    await ctx.reply(embed=em, mention_author=False)
  elif isinstance(error, commands.MissingPermissions):
    em = discord.Embed(description=f"<:error:893501396161290320> You are missing following permissions to run this command, `{', '.join(error.missing_perms)}`", color=0x2F3136)
    await ctx.reply(embed=em, mention_author=False)
  elif isinstance(error, commands.NotOwner):
    em = discord.Embed(description="<:error:893501396161290320>Lol you are not my owner :joy:", color=0x2F3136)
    await ctx.send(embed=em)
  elif isinstance(error, commands.BotMissingPermissions):
    em = discord.Embed(description=f"<:error:893501396161290320>The bot is missing following permissions to run this command, `{', '.join(error.missing_perms)}`", color=0x2F3136)
    await ctx.reply(embed=em, mention_author=False)
  elif isinstance(error, UserBlacklisted):
    em = discord.Embed(description=f"<:error:893501396161290320> You are blacklisted from using commands for reason `{error.reason}`", color=0x2F3136)
    await ctx.send(embed=em)
  elif f"{error}" == "Command raised an exception: Forbidden: 403 Forbidden (error code: 50013): Missing Permissions":
    em = discord.Embed(description=f"<:error:893501396161290320> The bot is missing permissions to run this command", color=0x2F3136)
    await ctx.reply(embed=em, mention_author=False)
  elif isinstance(error, commands.MemberNotFound):
    em = discord.Embed(description=f"<:error:893501396161290320> Member `{error.argument}` was not found in this server", color=0x2F3136)
    await ctx.reply(embed=em, mention_author=False)
  elif isinstance(error, commands.ChannelNotFound):
    em = discord.Embed(description=f"<:error:893501396161290320> Channel `{error.argument}` was not found in this server", color=0x2F3136)
    await ctx.reply(embed=em, mention_author=False)
  elif isinstance(error, commands.ChannelNotReadable):
    em = discord.Embed(description=f"<:error:893501396161290320> Bot does not have permissions to read messages in `{error.argument}`", color=0x2F3136)
    await ctx.reply(embed=em, mention_author=False)
  elif isinstance(error, commands.RoleNotFound):
    em = discord.Embed(description=f"<:error:893501396161290320> Role `{error.argument}` was not found in this server", color=0x2F3136)
    await ctx.reply(embed=em, mention_author=False)
  elif isinstance(error, commands.BadArgument):
    em = discord.Embed(description=f"<:error:893501396161290320> {error}", color=0x2F3136)
    await ctx.reply(embed=em, mention_author=False)
  elif isinstance(error, commands.CommandNotFound):
    command_names = [str(x) for x in ctx.bot.commands]
    matches = get_close_matches(ctx.invoked_with, command_names)
    if matches:
      em = discord.Embed(description=f"Did you mean **{matches[0]}** ?\n> click on <:success:893501515107557466> to run `{matches[0]}` command", color=0x2F3136)
      mainmessagecommand = await ctx.send(
        embed=em,
        components=[[Button(style=ButtonStyle.gray, emoji=client.get_emoji(893501515107557466), id = "invokecommand"), Button(style=ButtonStyle.red, emoji=client.get_emoji(890938576563503114), id = "deletecommandmessage")]]
      )
      while True:
        try:
          event = await client.wait_for(
            "button_click",
            check = lambda i: i.component.id in ["invokecommand", "deletecommandmessage"],
            timeout=10.0
          )
          if event.author != ctx.author:
            await event.respond(
              content="Sorry, this buttons cannot be controlled by you",
              type=4
            )
          else:
            if event.component.id == "invokecommand":
              await mainmessagecommand.delete()
              cmd = client.get_command(f"{matches[0]}")
              await cmd(ctx)
            elif event.component.id == "deletecommandmessage":
              await mainmessagecommand.delete()
              await ctx.message.add_reaction("<:cancel:872394940779474985>")
        except asyncio.TimeoutError:
          try:
            await mainmessagecommand.edit(
              components=[[Button(style=ButtonStyle.green, emoji=client.get_emoji(893501515107557466), custom_id = "invokecommand", disabled=True), Button(style=ButtonStyle.red, emoji=client.get_emoji(890938576563503114), custom_id = "deletecommandmessage", disabled=True)]]
            )
          except:
            pass
          break
  else:
    await ctx.reply('An unexpected error ocurred... Error has been reported to our devs, will be fixed soon...', mention_author=False, delete_after=5)
    error_log_channel=client.get_channel(905004192404504586)

    traceback_string = "".join(traceback.format_exception(etype=None, value=error, tb=error.__traceback__))

    main_message=await error_log_channel.send(f'__**AN ERROR OCCURED**__\n```yml\nInvoked by: {ctx.author}\nServer: {ctx.guild.name}\nCommand: {ctx.command.name}```\n__**TRACEBACK**__\n```py\n{traceback_string}```')
    await main_message.add_reaction('🗑️')
    def check(reaction):
      return str(reaction.emoji) in ["🗑️"]

    await client.wait_for('reaction_add', check=check, timeout=604800)
    await main_message.edit(f'{main_message.content}\n```ml\n✅ MARKED AS FIXED BY DEVELOPERS```')


@client.command(aliases=['8ball'])
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


@client.command(aliases=["av"])
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


@client.command()
@commands.has_permissions(manage_channels=True)
async def deletechannel(ctx, channel: discord.TextChannel):
      if ctx.author.guild_permissions.manage_channels:
        
        await channel.delete()
        m = discord.Embed(description=f"<:success:893501515107557466> Deleted {channel.name} [{ctx.author.mention}]", color=0x2bff00)
        await ctx.send(embed=m)


#delete voice channel command

@client.command(aliases=["deletevc", "dvc"])
@commands.has_permissions(manage_channels=True)
async def deletevoicechannel(ctx, channel: discord.VoiceChannel):
      if ctx.author.guild_permissions.manage_channels:
        
        await channel.delete()
        m = discord.Embed(description=f"<:success:893501515107557466> Deleted {channel.name} [{ctx.author.mention}]", color=0x2bff00)
        await ctx.send(embed=m)


#emojify command

@client.command()
async def emojify(ctx, *, text):
  emojis = []
  for s in text:
    if s.isdecimal():
      num2emo = {'0':'zero', '1':'one', '2':'two', '3':'three',
                 '4':'four', '5':'five', '6':'six',
                 '7': 'seven','8': 'eight','9': 'nine'}

      emojis.append(f':{num2emo.get(s)}:')
    elif s.isalpha():
      emojis.append(f':regional_indicator_{s}: ')
    else:
      emojis.append(s)
  await ctx.send(''.join(emojis))

#say command
@client.group(invoke_without_command=True, aliases=["s"])
async def say(ctx, *, content):
  try:
    await ctx.message.delete()
  except:
    pass
  if ctx.message.reference:
    await ctx.message.reference.resolved.reply(f"{content}", allowed_mentions=discord.AllowedMentions(everyone=False, roles=False))
  else:
    await ctx.send(f"{content}", allowed_mentions=discord.AllowedMentions(everyone=False, roles=False))

@say.command(aliases=["em"])
async def embed(ctx, *, reply = "without reply"):
  try:
    await ctx.message.delete()
  except:
    pass
  if ctx.message.reference.resolved.embeds[0]:
    if reply == "with reply":
      await ctx.message.reference.resolved.reply(f"{ctx.message.reference.resolved.content}", embed=ctx.message.reference.resolved.embeds[0])
    else:
      await ctx.send(embed=ctx.message.reference.resolved.embeds[0])
  else:
    await ctx.send("I cant find any message with embeds")



@client.command()
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





@client.command()
@commands.has_permissions(manage_channels=True)
async def unmute(ctx, member: discord.Member):
  mutedRole = discord.utils.get(ctx.guild.roles, name='Muted')

  await member.remove_roles(mutedRole)
  em = discord.Embed(description=f"<:success:893501515107557466> Unmuted {member.name}#{member.discriminator}", color=0x2bff00)
  await ctx.send(embed=em)
  await member.send(f'You are now unmuted in the server **{ctx.guild.name}**')


#giveaway command main
@client.command()
@commands.has_permissions(administrator=True)
async def giveaway(ctx):
  await ctx.send("**Let's start this Giveaway! answer these questions within __15 seconds__**")

  questions = ["> **Which channel should giveaway be hosted in?**",
              "> **What should be the duration of the giveaway? (s|m|h|d)**",
              "> **What is the prize of the giveaway?**"]

  answers = []

  def check(m):
      return m.author == ctx.author and m.channel == ctx.channel

  for i in questions:
    await ctx.send(i)

    try:
      msg = await client.wait_for('message', timeout=15.0, check=check)
    except asyncio.TimeoutError:
      await ctx.send('**You did\'t answer in time, Please be quicker next time!**')
      return
    else:
        answers.append(msg.content)
#<#id> this is the way id is made
  try:
      c_id = int(answers[0][2:-1])
  except:
      await ctx.send(f"**You didn't mention the channel properly. Do it like this {ctx.channel.mention} next time**")
      return

  channel = client.get_channel(c_id)

  time = convert(answers[1])
  if time == -1:
      await ctx.send(f"**You didn't answer the proper unit. Use (s|m|h|d) next time!**")
      return
  elif time == -2:
      await ctx.send(f"**The time must be an integer. Please enter an integer next time**")
      return
  prize = answers[2]

  await ctx.send(f"**The giveaway will be in {channel.mention} and will last {answers[1]}! <a:gallset:857139110976290847> **")

  embed = discord.Embed(title = "Giveaway! <a:ggiveaway:856509556632453120> ",description = f"**{prize}**<a:gprize:856516166193381376> ", color=0x00eeff, timestamp=ctx.message.created_at)

  embed.add_field(name = "Hosted by:", value = ctx.author.mention)

  embed.set_footer(text = f"Ends {answers[1]} from now!")

  my_msg = await channel.send(embed=embed)

  await my_msg.add_reaction("<a:ggiveaway:856509556632453120>")

  await asyncio.sleep(time)

  new_msg = await channel.fetch_message(my_msg.id)

  users =await new_msg.reactions[0].users().flatten()
  users.pop(users.index(client.user))

  winner = random.choice(users)



  await channel.send(f"**Congratulations!<a:ggiveaway:856509556632453120>** {winner.mention} won **__{prize}__** <:gpogpepe:856516618183376917>")


#reroll command
@client.command()
async def reroll(ctx, channel : discord.TextChannel, id_ : int):
    try:
      new_msg = await channel.fetch_message(id_)
    except:
        await ctx.send("The id was enters incorrectly.")
        return

    users =await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)


    await ctx.send(f"**__Giveaway Reroll __**Congratulations!<a:ggiveaway:856509556632453120>{winner.mention} won **__The Giveaway__**")

#gend command


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


@client.command(aliases=['ttt'])
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


@client.command()
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


@client.command(aliases=["show", "search", "img", "googlesearch"])
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


reddit = praw.Reddit(client_id = "vuwfZiZXYnPZlg",
                     client_secret = "aOLy1GQJrhCIPAe7UCeCMGvIoP0JLw",
                     username = "Gerty_1",
                     password = "82xPm!erQA$adt6",
                     user_agent = "Gerty")


@client.command()
@commands.cooldown(1,10000,commands.BucketType.channel)
async def meme(ctx):
  emm = discord.Embed(description="<a:loading:865563025586389003> _Oh wait a sec! <:fekdankmemer:859078210619965501>_", color=0xeeff00)
  v = await ctx.send(embed=emm)
  subreddit = reddit.subreddit("memes")
  all_subs = []

  top = subreddit.top(limit = 50)

  for submission in top:
    all_subs.append(submission)

  random_sub = random.choice(all_subs)

  name = random_sub.title
  url = random_sub.url

  em = discord.Embed(title = name)

  em.set_image(url = url)

  await v.edit(embed=em)




#rps try :sob:
@client.command()
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

@client.command(aliases=["userinfo", "ui"])
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



@client.command(aliases=['ci'])
@commands.cooldown(1,5,commands.BucketType.user)
async def channelinfo(ctx):
  

  embed = discord.Embed(title=f"**Info of channel __{ctx.channel.name}__**", description=f"{'Category: {}'.format(ctx.channel.category.name) if ctx.channel.category else 'This channel is not a category'}", color=0xa600ff, timestamp=ctx.message.created_at)
  embed.add_field(name="Channel Guild", value=ctx.guild.name, inline=False)
  embed.add_field(name="Channel ID", value=ctx.channel.id, inline=False)
  embed.add_field(name="Channel Topic", value=f"{channel.topic if ctx.channel.topic else 'No Topic'}", inline=False)
  embed.add_field(name="Channel Position", value=ctx.channel.position, inline=False)
  embed.add_field(name="Channel Slowmode delay", value=ctx.channel.slowmode_delay, inline=False)
  embed.add_field(name="Is channel NSFW?", value=ctx.channel.is_nsfw() , inline=False)
  embed.add_field(name="Is this an announcement channel?", value=ctx.channel.is_news(), inline=False)
  embed.add_field(name="Channel Created at", value=ctx.channel.created_at, inline=False)
  embed.add_field(name="Channel Permissions (synced)", value=ctx.channel.permissions_synced, inline=False)
  embed.add_field(name="Channel Hash", value=hash(ctx.channel), inline=False)

  await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(manage_channels = True)
async def lock(ctx, channel: discord.TextChannel = None):
  if channel == None:
    channel = ctx.channel
  await channel.set_permissions(ctx.guild.default_role, send_messages=False)
  embed = discord.Embed(description=f"<:success:893501515107557466> {channel.mention} is now locked", color=0x2bff00)
  await ctx.send(embed=embed)

  


@client.command()
@commands.has_permissions(manage_channels = True)
async def unlock(ctx, channel: discord.TextChannel = None):
  if channel == None:
    channel = ctx.channel
    
  await channel.set_permissions(ctx.guild.default_role, send_messages=True)
  embed = discord.Embed(description=f"<:success:893501515107557466> {channel.mention} is now unlocked", color=0x2bff00)
  await ctx.send(embed=embed)

@client.command(aliases=["flip"])
async def coin(ctx):
  v = await ctx.send("> **<a:flip:867032673403142144> The coin is flipping**")
  await asyncio.sleep(3)
  n = random.randint(0, 1)
  await v.edit("> It is **Heads**" if n == 1 else "> It is **Tails**")
  

@client.command()
@commands.has_permissions(manage_channels = True)
async def slowmode(ctx, seconds: int):
  await ctx.channel.edit(slowmode_delay=seconds)
  em = discord.Embed(description=f"<:success:893501515107557466> Set the slowmode delay in {ctx.channel.mention} to {seconds} seconds! <:slowmode:861261195621040138>", color=0x2bff00)
  await ctx.send(embed=em)




@client.command(pass_content=True)
@commands.cooldown(1,5,commands.BucketType.user)
async def nick(ctx, member: discord.Member, *, arg):
  await member.edit(nick=arg)
  await ctx.send(f'Nickname was changed for {member.mention} to {arg}')

@client.command(pass_content=True)
@commands.cooldown(1,5,commands.BucketType.user)
async def resetnick(ctx, member: discord.Member):
  await member.edit(nick=f"{member.name}")
  await ctx.send(f"Nickname reset to {member.name}")




@client.command()
@commands.cooldown(1,10,commands.BucketType.guild)
@commands.has_permissions(administrator = True)
async def massunban(ctx):
  m = await ctx.send('<a:gloading:855680101529944064> Mass unbanning')
  banlist = await ctx.guild.bans()
  for users in banlist:
    try:
      await ctx.guild.unban(user=users.user)
    except:
      pass
  await m.edit("Everyone unbanned")


    

@client.command()
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



@client.command()
async def help(ctx):
  components=[Select(placeholder="See commands of specific modules!",
                                    options=[
                                      SelectOption(
                                        label="Fun commands",
                                        value="fun",
                                        description="Commands that everyone can use",
                                        emoji="😄"
                                      ),
                                      SelectOption(
                                        label="Mod commands",
                                        value="mod",
                                        description="Commands for admins/mods",
                                        emoji=client.get_emoji(885156113656479784)
                                      ),
                                      SelectOption(
                                        label="Music commands",
                                        value="music",
                                        description="Music player commands",
                                        emoji=client.get_emoji(857925385726197760)
                                      ),
                                      SelectOption(
                                        label="Miscellaneous Commands",
                                        value="misc",
                                        description="Some other stuffs",
                                        emoji="🧩"
                                      ),
                                      SelectOption(
                                        label="Role-play commands",
                                        value="role",
                                        description="See some social commands",
                                        emoji=client.get_emoji(885157475354021959),
                                      ),
                                      SelectOption(
                                        label="Activity commands",
                                        value="activity",
                                        description="Games that you can play in a vc",
                                        emoji=client.get_emoji(880089919018659960),
                                      ),
                                      SelectOption(
                                        label="Back to Home",
                                        value="home",
                                        description="Go back to the main page",
                                        emoji=client.get_emoji(885166192661266452),
                                      ),
                                    ])]
  embed=discord.Embed(description="`g!help [module/category]` - View specific module.\nHover below categories for more information.\nReport bugs if any `g!report`\n```ml\n[] - Required Argument | () - Optional Argument```", color=0x2F3136)
  embed.set_author(name="Gerty Helpdesk", icon_url=f"{client.user.avatar_url}")
  embed.add_field(name="<:modules:884784557822459985> Modules:", value="> <:cate:885482994452795413>  Fun\n> <:cate:885482994452795413>  Moderation\n> <:cate:885482994452795413>  Music\n> <:cate:885482994452795413>  Miscellaneous\n> <:cate:885482994452795413>  Roleplay\n> <:cate:885482994452795413>  Activity")
  embed.add_field(name="<:news:885177157138145280> News, <t:1632316584:R>:", value="> Update in afk command!")
  embed.add_field(name="<:links:885161311456071750> Links:", value="> [Invite me](https://discord.com/api/oauth2/authorize?client_id=855443275658166282&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.gg%2Fms3PvCvQqK&scope=bot%20applications.commands) | [Support server](https://discord.gg/ZScUFjBuvQ) | [Dashboard](https://magic-scythe-cuckoo.glitch.me/)", inline=False)
  embed.set_footer(text=f"Invoked by {ctx.author.name} • Main Page", icon_url=f"{ctx.author.avatar_url}")


  e1 = discord.Embed(title="Fun commands", description="`g!help [module/category]` - View specific module.\nHover below categories for more information.\n```ml\n[] - Required Argument | () - Optional Argument```", color=0x2F3136)
  e1.set_author(name="Gerty Helpdesk", icon_url=f"{client.user.avatar_url}")
  e1.set_footer(text=f"Invoked by {ctx.author.name} • Page 1/6", icon_url=f"{ctx.author.avatar_url}")
  e1.add_field(name="Commands 1/2", value="<:arrow:885193320068968508> `emojify` - Emojifies the given text, usage: emojify [text]\n<:arrow:885193320068968508> `meme` - Sends a random meme\n<:arrow:885193320068968508> `rps` - Starts a rock paper scissors game with the bot\n<:arrow:885193320068968508> `ttt` - Stats a tic tac toe game, usage: ttt [user1] (user2)\n<:arrow:885193320068968508> `place` - Tic tac toe sub command, usage: place [tile position]\n<:arrow:885193320068968508> `hack` - A funny unreal hack command, usage: hack [user]\n<:arrow:885193320068968508> `calc` - Enhanced calculator with interactions\n<:arrow:885193320068968508> `wanted` - Generates an image, usage: wanted [user]\n<:arrow:885193320068968508> `spongebob` - Generates an image, usage: spongebob [user]")
  e1.add_field(name="Commands 2/2", value="<:arrow:885193320068968508> `coin` - Flips a coin and chooses heads or tails\n<:arrow:885193320068968508> `anime` - Get details of an anime/manga, usage: anime [name]\n<:arrow:885193320068968508> `trash` - Generates an image, usage: trash [user]\n<:arrow:885193320068968508> `affect` - Generates an image, usage: affect [user]\n<:arrow:885193320068968508> `amongus` - Generates an image, usage: amongus [user]\n<:arrow:885193320068968508> `enhance` - Enhances user's avatar, usage: enhance [sub command] [user]\n<:arrow:885193320068968508> `grayscale` - Grayscales user's avatar, usage: grayscale [user]\n<:arrow:885193320068968508> `invert` - Inverts color of the user's avatar, usage: invert [user]", inline=False)
#mod commands
  e2 = discord.Embed(title="Moderation commands", description="`g!help [module/category]` - View specific module.\nHover below categories for more information.\n```ml\n[] - Required Argument | () - Optional Argument```", color=0x2F3136)
  e2.set_author(name="Gerty Helpdesk", icon_url=f"{client.user.avatar_url}")
  e2.set_footer(text=f"Invoked by {ctx.author.name} • Page 2/6", icon_url=f"{ctx.author.avatar_url}")
  e2.add_field(name="Commands 1/3", value="<:arrow:885193320068968508> `clear` - Clears messages in the current channel, usage: clear [amount]\n<:arrow:885193320068968508> `kick` - Kicks a user from the guild, usage: kick [user] (reason)\n<:arrow:885193320068968508> `ban` - Bans a user from the guild, usage: ban [user] (reason)\n<:arrow:885193320068968508> `unban` - Unbans a user from the guild, usage: unban [user]\n<:arrow:885193320068968508> `announce` - Announce something, usage: announce [channel] [message]\n<:arrow:885193320068968508> `deletechannel` - Deletes a \"Text\" channel, usage: deletechannel [channel]\n<:arrow:885193320068968508> `deletevc` - Deletes a \"voice\" channel, usage: deletevc [channel]\n<:arrow:885193320068968508> `nuke` - Deletes a channel and creates a clone, usage: nuke [channel]\n<:arrow:885193320068968508> `clone` - Make a clone of a channel, usage: clone [channel]")
  e2.add_field(name="Commands 2/3", value="<:arrow:885193320068968508> `reactrole` - Starts a react role event, usage: reactrole [emoji] [role] [message]\n<:arrow:885193320068968508> `mute` - Mutes a member, usage: mute [user] (reason)\n<:arrow:885193320068968508> `unmute` - Unmutes a member, usage: unmute [user]\n<:arrow:885193320068968508> `giveaway` - Starts a giveaway event\n<:arrow:885193320068968508> `reroll` - rerolls the giveaway, usage: reroll [message id]\n<:arrow:885193320068968508> `channelinfo` - Shows full info of a channel, usage: channelinfo (channel)\n<:arrow:885193320068968508> `lock` - Makes a channel lockdown, usage: lock (channel)\n<:arrow:885193320068968508> `snipe` - Snipes a deleted message from current channel", inline=False)
  e2.add_field(name="Commands 3/3", value="<:arrow:885193320068968508> `unlock` - Unlocks a channel from lockdown, usage: unlock (channel)\n<:arrow:885193320068968508> `slowmode` - Sets slowmode delay, usage: slowmode [seconds]\n<:arrow:885193320068968508> `nick` - Changes nickname, usage: nick (user) [nick]\n<:arrow:885193320068968508> `resetnick` - Resets nickname, usage: resetnick [user]\n<:arrow:885193320068968508> `ticket` - Creates a ticket event, usage: nick [message id] [category id]\n<:arrow:885193320068968508> `massunban` - Unbans everyone from the guild\n<:arrow:885193320068968508> `members` - Shows how many members are in the guild\n<:arrow:885193320068968508> `addrole` - Adds role to given member, usage: addrole [role] [user]\n<:arrow:885193320068968508> `removerole` - Removes a role from the user, usage: removerole [role] [user]")

  e3 = discord.Embed(title="Music commands", description="`g!help [module/category]` - View specific module.\nHover below categories for more information.\n```ml\n[] - Required Argument | () - Optional Argument```", color=0x2F3136)
  e3.set_author(name="Gerty Helpdesk", icon_url=f"{client.user.avatar_url}")
  e3.set_footer(text=f"Invoked by {ctx.author.name} • Page 3/6", icon_url=f"{ctx.author.avatar_url}")
  e3.add_field(name="Commands 1/1", value="<:arrow:885193320068968508> `join` - The bot joines your VC\n<:arrow:885193320068968508> `play` - The player starts playing, usage: play [url/song name]\n<:arrow:885193320068968508> `pause` - The player pauses\n<:arrow:885193320068968508> `resume` - The player resumes\n<:arrow:885193320068968508> `queue` - Shows a list of queued songs\n<:arrow:885193320068968508> `loop` - Loops the current song\n<:arrow:885193320068968508> `remove` - Removes a song from the queue, usage: remove [song position]\n<:arrow:885193320068968508> `nowplaying` - Shows details of now playing song in the player\n<:arrow:885193320068968508> `volume` - Changes the volume of the player, usage: volume [percentage]\n<:arrow:885193320068968508> `skip` - Skips the current song to next in the queue\n<:arrow:885193320068968508> `dc` - The bot disconnects and player stops")

  e4 = discord.Embed(title="Misc commands", description="`g!help [module/category]` - View specific module.\nHover below categories for more information.\n```ml\n[] - Required Argument | () - Optional Argument```", color=0x2F3136)
  e4.set_author(name="Gerty Helpdesk", icon_url=f"{client.user.avatar_url}")
  e4.set_footer(text=f"Invoked by {ctx.author.name} • Page 4/6", icon_url=f"{ctx.author.avatar_url}")
  e4.add_field(name="Commands 1/2", value="<:arrow:885193320068968508> `ping` - Shows the bot latency\n<:arrow:885193320068968508> `avatar` - Shows the avatar of a user, usage: avatar [user]\n<:arrow:885193320068968508> `code` - Shows which lang bot is using\n<:arrow:885193320068968508> `mail` - Sends a mail to a user, usage: mail [user] (message)\n<:arrow:885193320068968508> `say` - The bot echo you, usage: say [message]\n<:arrow:885193320068968508> `show` - The bot shows an image from google, usage: show [keyword]\n<:arrow:885193320068968508> `covid` - See covid status of a country, usage: covid [country]")
  e4.add_field(name="Commands 2/2", value="<:arrow:885193320068968508> `spotify` - Shows the details of music user listening to, usage: spotify [user]\n<:arrow:885193320068968508> `afk` - Sets your status as afk, usage: afk (message)\n<:arrow:885193320068968508> `moveme` - Moves you from a vc to another, usage: moveme [channel]\n<:arrow:885193320068968508> `translate` - Translates, usage: translate [To language] [message]\n<:arrow:885193320068968508> `webhook` - Sends a message from webhook, usage: webhook (user) [message]\n<:arrow:885193320068968508> `screenshot` - Shows screenshot of a website, usage screenshot [url]\n<:arrow:885193320068968508> `serverinfo` - Shows everything of the server\n<:arrow:885193320068968508> `report` - Report something to bot dev, usage: report [message]", inline=False)

  e5 = discord.Embed(title="Role-play commands", description="`g!help [module/category]` - View specific module.\nHover below categories for more information.\n```ml\n[] - Required Argument | () - Optional Argument```", color=0x2F3136)
  e5.set_author(name="Gerty Helpdesk", icon_url=f"{client.user.avatar_url}")
  e5.set_footer(text=f"Invoked by {ctx.author.name} • Page 5/6", icon_url=f"{ctx.author.avatar_url}")
  e5.add_field(name="Commands 1/1", value="<:arrow:885193320068968508> `hug` - Gives a hug to the user, usage: hug [user]\n<:arrow:885193320068968508> `kiss` - Mmuuuah!, usage: kiss [user]\n<:arrow:885193320068968508> `slam` - And his name is john cena, usage: slam [user]\n<:arrow:885193320068968508> `punch` - Dishooom Dishooomm!, usage: punch [user]")

  e6 = discord.Embed(title="Activity commands", description="`g!help [module/category]` - View specific module.\nHover below categories for more information.\n```ml\n[] - Required Argument | () - Optional Argument```", color=0x2F3136)
  e6.set_author(name="Gerty Helpdesk", icon_url=f"{client.user.avatar_url}")
  e6.set_footer(text=f"Invoked by {ctx.author.name} • Page 6/6", icon_url=f"{ctx.author.avatar_url}")
  e6.add_field(name="Commands 1/1", value="<:arrow:885193320068968508> `ytt` - Youtube together activity, usage: ytt [voice channel]\n<:arrow:885193320068968508> `poker` - Poker night activity, usage: poker [voice channel]\n<:arrow:885193320068968508> `chess` - Chess in the park activity, usage: chess [voice channel]\n<:arrow:885193320068968508> `betrayal` - Betrayal.io activity, usage: betrayal [voice channel]\n<:arrow:885193320068968508> `fishing` - Fishington.io activity, usage: fishing [voice channel]")

  mainmessage = await ctx.send(embed=embed, components=components)



  while True:
    try:
      event = await client.wait_for("select_option", check=None, timeout=60.0)
      value = event.values[0]

      

      if value == "fun":
        if event.author != ctx.author:
          await event.respond(
            content=f"{event.author.mention} This is not your select menu. Type `g!help` for yours",
            type = 4,
        )
        else:
          await event.respond(
            type = 7,
            embed=e1
        )

      elif value == "mod":
        if event.author != ctx.author:
          await event.respond(
            content=f"{event.author.mention} This is not your select menu. Type `g!help` for yours",
            type = 4,
        )
        else:
          await event.respond(
            type = 7,
            embed=e2
        )

      elif value == "music":
        if event.author != ctx.author:
          await event.respond(
            content=f"{event.author.mention} This is not your select menu. Type `g!help` for yours",
            type = 4,
        )
        else:
          await event.respond(
            type = 7,
            embed=e3
        )
      elif value == "home":
        if event.author != ctx.author:
          await event.respond(
            content=f"{event.author.mention} This is not your select menu. Type `g!help` for yours",
            type = 4,
        )
        else:
          await event.respond(
            type = 7,
            embed=embed
        )
      elif value == "misc":
        if event.author != ctx.author:
          await event.respond(
            content=f"{event.author.mention} This is not your select menu. Type `g!help` for yours",
            type = 4,
        )
        else:
          await event.respond(
            type = 7,
            embed=e4
        )
      elif value == "role":
        if event.author != ctx.author:
          await event.respond(
            content=f"{event.author.mention} This is not your select menu. Type `g!help` for yours",
            type = 4,
        )
        else:
          await event.respond(
            type = 7,
            embed=e5
        )

      elif value == "activity":
        if event.author != ctx.author:
          await event.respond(
            content=f"{event.author.mention} This is not your select menu. Type `g!help` for yours",
            type = 4,
        )
        else:
          await event.respond(
            type = 7,
            embed=e6
        )

    except asyncio.TimeoutError:
      await mainmessage.edit(
        components=[Select(placeholder="This Menu expired, use command again", disabled=True,
                                    options=[
                                      SelectOption(
                                        label="Back to Home",
                                        value="home",
                                        description="Go back to where you started",
                                        emoji=client.get_emoji(885166192661266452)
                                      ),
                                      SelectOption(
                                        label="Fun commands",
                                        value="fun",
                                        description="Commands that everyone can use",
                                        emoji="😄"
                                      ),
                                      SelectOption(
                                        label="Mod commands",
                                        value="mod",
                                        description="Moderation commands for admins/mods",
                                        emoji=client.get_emoji(885156113656479784)
                                      ),
                                      SelectOption(
                                        label="Music commands",
                                        value="music",
                                        description="Music player commands",
                                        emoji=client.get_emoji(857925385726197760)
                                      ),
                                    ])]
      )
      break



#roleplay
#hug
@client.command()
async def hug(ctx, user: discord.Member):
  hugGifs = ["https://media1.tenor.com/images/1069921ddcf38ff722125c8f65401c28/tenor.gif?itemid=11074788",
  "https://media1.tenor.com/images/7db5f172665f5a64c1a5ebe0fd4cfec8/tenor.gif?itemid=9200935",
  "https://media1.tenor.com/images/daffa3b7992a08767168614178cce7d6/tenor.gif?itemid=15249774",
  "https://media.tenor.com/images/3a9d2bd1bde9ed8ea02b2222988be6da/tenor.gif",
  "https://media.tenor.com/images/7766f3d163f651b6d9d7c3b718d8e6fb/tenor.gif",
  "https://media1.tenor.com/images/552c49f523d61c01da04bb1128b42cbf/tenor.gif?itemid=13747286",
  "https://media1.tenor.com/images/c1058ebe89313d50dfc878d38630036b/tenor.gif?itemid=13976210",
  "https://media1.tenor.com/images/08de7ad3dcac4e10d27b2c203841a99f/tenor.gif?itemid=4874598",
  "https://media1.tenor.com/images/efdd8f53689b1bb3437054d608156e95/tenor.gif?itemid=4885269",
  "https://cdn.weeb.sh/images/S1DyFuQD-.gif"]
  embed = discord.Embed(color=0xff0040)
  embed.set_author(name=f"{ctx.author.name} hugs {user.name}!", icon_url=f"{ctx.author.avatar_url}")
  embed.set_image(url=random.choice(hugGifs))

  await ctx.send(embed=embed)



@client.command()
async def kiss(ctx, user: discord.Member):
  kissGifs = ["https://media1.tenor.com/images/503bb007a3c84b569153dcfaaf9df46a/tenor.gif?itemid=17382412",
  "https://media1.tenor.com/images/f5167c56b1cca2814f9eca99c4f4fab8/tenor.gif?itemid=6155657",
  "https://media1.tenor.com/images/621ceac89636fc46ecaf81824f9fee0e/tenor.gif?itemid=4958649",
  "https://media.tenor.com/images/68d59bb29d7d8f7895ce385869989852/tenor.gif",
  "https://media.tenor.com/images/5a6a04fc81d70ef353d928a87ed25f6b/tenor.gif",
  "https://media1.tenor.com/images/47cb6c6e70765343835e5b2d1955e804/tenor.gif?itemid=17747859",
  "https://media.tenor.com/images/de18124ebe36764446ee2dbf54a672bf/tenor.gif"]
  embed = discord.Embed(color=0xff0040)
  embed.set_author(name=f"{ctx.author.name} kisses {user.name}!", icon_url=f"{ctx.author.avatar_url}")
  embed.set_image(url=random.choice(kissGifs))
  await ctx.send(embed=embed)



@client.command()
async def slam(ctx, member: discord.Member):
  slamGifs = ["https://media1.tenor.com/images/89309d227081132425e5931fbbd7f59b/tenor.gif?itemid=4880762",
  "https://media.tenor.com/images/6d0c8075ea6f2f125449886099e2da4c/tenor.gif",
  "https://media.tenor.com/images/bc850e301bd742c42097c97b054b4d2f/tenor.gif",
  "https://media.tenor.com/images/8b231fc7b71e03204143c6f6a96d406b/tenor.gif"]
  embed = discord.Embed(color=0xff0040)
  embed.set_author(name=f"{ctx.author.name} slams {member.name}!", icon_url=f"{ctx.author.avatar_url}")
  embed.set_image(url=random.choice(slamGifs))
  await ctx.send(embed=embed)



@client.command()
async def punch(ctx, user: discord.Member):
  punchGifs = ["https://media1.tenor.com/images/55507aea306782b916659085fc062909/tenor.gif?itemid=8932977",
  "https://media1.tenor.com/images/c621075def6ca41785ef4aaea20cc3a2/tenor.gif?itemid=7679409",
  "https://media.tenor.com/images/04a3cf11736bfa9083b91f2d41b76774/tenor.gif",
  "https://media1.tenor.com/images/f03329d8877abfde62b1e056953724f3/tenor.gif?itemid=13785833",
  "https://media1.tenor.com/images/abb5363c1f59268e3f94521247eace30/tenor.gif?itemid=16346949",
  "https://media1.tenor.com/images/36430033b3549744ce109929cbd6694e/tenor.gif?itemid=17053376"]
  embed = discord.Embed(color=0xff0040)
  embed.set_author(name=f"{ctx.author.name} gives {user.name} a punch!", icon_url=f"{ctx.author.avatar_url}")
  embed.set_image(url=random.choice(punchGifs))
  await ctx.send(embed=embed)



#reports 
@client.command()
async def report(ctx, *, report=None):
  report_channel = client.get_channel(905007925444116520)
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


#ticket 


client.ticket_configs = {}


    


@client.command()
async def ticket(ctx, msg: discord.Message=None, category: discord.CategoryChannel=None):
    if msg is None or category is None:
        await ctx.channel.send("Failed to configure the ticket as an argument was not given or was invalid. i.e g!ticket [message id] [category id]")
        return

    client.ticket_configs[ctx.guild.id] = [msg.id, msg.channel.id, category.id] # this resets the configuration

    async with aiofiles.open("ticket_configs.txt", mode="r") as file:
        data = await file.readlines()

    async with aiofiles.open("ticket_configs.txt", mode="w") as file:
        await file.write(f"{ctx.guild.id} {msg.id} {msg.channel.id} {category.id}\n")

        for line in data:
            if int(line.split(" ")[0]) != ctx.guild.id:
                await file.write(line)
                
    await msg.add_reaction(u"\U0001F3AB")
    await ctx.channel.send("Succesfully configured the ticket system.")



#moosic
music = DiscordUtils.Music()

@client.command()
async def join(ctx):
  voicetrue = ctx.author.voice
  if voicetrue is None:
    return await ctx.send("You are not connected to a voice channel")
  em = discord.Embed(description=f"Joined {ctx.author.voice.channel.mention}", color=0x25f500)
  await ctx.send(embed=em)
  await ctx.author.voice.channel.connect()

@client.command(aliases=["disconnect"])
async def dc(ctx):
  player = music.get_player(guild_id=ctx.guild.id)
  voicetrue = ctx.author.voice
  mevoicetrue = ctx.guild.me.voice
  if voicetrue is None:
    return await ctx.send("You are not connected to a voice channel")
  if mevoicetrue is None:
    return await ctx.send("I am not currently in a voice channel")
  await ctx.voice_client.disconnect()
  await ctx.message.add_reaction('<a:bye:857642966457253898>')
  dc = discord.Embed(description=f"<:disconnect:857641894313984040> Disconnected",color=0xf5ed00)
  await ctx.send(embed=dc)
 

@client.command(aliases=["p"])
async def play(ctx, *, url):
  try:
    voicetrue = ctx.author.voice
    if voicetrue is None:
      return await ctx.send("You are not connected to a voice channel")
    em = discord.Embed(description=f"Joined {ctx.author.voice.channel.mention}", color=0x25f500)
    await ctx.author.voice.channel.connect()
    await ctx.send(embed=em)
  except:
    pass
  x = discord.Embed(description=f"<a:loading:865563025586389003>  Searching requested song", color=0xff0059)
  s = await ctx.send(embed=x)
  player = music.get_player(guild_id=ctx.guild.id)
  if not player:
    player = music.create_player(ctx, ffmpeg_error_betterfix=True)
    if not ctx.voice_client.is_playing():
      await player.queue(url, search=True)
    song = await player.play()
    m = discord.Embed(title="Started playing", description=f"> <a:music:857925385726197760> [{song.name}]({song.url}) [{ctx.author.mention}]", color=0xff0059)
    m.set_image(url=f"{song.thumbnail}")
    await s.edit(embed=m)
  else:
    song  = await player.queue(url, search=True)
    v = discord.Embed(title="Added to Queue", description=f"> <a:music:857925385726197760> [{song.name}]({song.url}) has been added to queue! [{ctx.author.mention}]", color=0xff0059)
    v.set_image(url=f"{song.thumbnail}")
    await s.edit(embed=v)


@client.command()
async def queue(ctx):
  player = music.get_player(guild_id=ctx.guild.id)
  em = discord.Embed(title="Queue", description=f"{',<:blank:862724961096695858>'.join([song.name for song in player.current_queue()])}", color=0xff0059)
  await ctx.send(embed=em)


@client.command()
async def skip(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    await player.skip(force=True)
    data = await player.skip(force=True)
    if len(data) == 2:
      if len(data) == 2:
        embed = discord.Embed(title="Skipped", description=f"[{data[0].name}]({data[0].url})", color=0xfff700)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description=f"> Stopped playing [{data[0].name}]({data[0].url}) nothing in the queue!", color=0x80ff00)
        await ctx.send(embed=embed)
    


@client.command(aliases=["vol"])
async def volume(ctx, volume):
    player = music.get_player(guild_id=ctx.guild.id)
    song, volumee = await player.change_volume(float(volume) / 100) # volume should be a float between 0 to 1
    embed = discord.Embed(description=f"Set volume to {volumee*100}%", color=0xfff700)
    await ctx.send(embed=embed)


@client.command()
async def pause(ctx):
  player = music.get_player(guild_id=ctx.guild.id)
  song = await player.pause()
  embed = discord.Embed(title="Paused playing", description=f"[{song.name}]({song.url})", color=0xfff700)
  await ctx.send(embed=embed)

@client.command()
async def resume(ctx):
  player = music.get_player(guild_id=ctx.guild.id)
  song = await player.resume()
  embed = discord.Embed(title="Resumed playing", description=f"[{song.name}]({song.url})", color=0xfff700)
  await ctx.send(embed=embed)


@client.command()
async def loop(ctx):
  player = music.get_player(guild_id=ctx.guild.id)
  song = await player.toggle_song_loop()
  if song.is_looping:
    embed = discord.Embed(title="Now looping", description=f"[{song.name}]({song.url}) [{ctx.author.mention}]", color=0xfff700)
    return await ctx.send(embed=embed)
  else:
    embed = discord.Embed(title="Stopped looping", description=f"[{song.name}]({song.url}) [{ctx.author.mention}]", color=0xfff700)
    return await ctx.send(embed=embed)
    

@client.command(aliases=["np"])
async def nowplaying(ctx):
  player = music.get_player(guild_id=ctx.guild.id)
  song = player.now_playing()
  embed = discord.Embed(title="Now playing", description=f"[{song.name}]({song.url})", color=0xfff700)
  embed.add_field(name="⏳ Duration", value=f"{round(song.duration/60)} mins [`(rounded)`](https://youtu.be/jeg_TJvkSjg)")
  embed.add_field(name="📌 Author", value=f"[{song.channel}]({song.channel_url})")
  embed.add_field(name="🪄 Views", value=f"{song.views}")
  if song.is_looping == True:
    embed.add_field(name="💽 Looping?", value="<:success:893501515107557466>")
  else:
    embed.add_field(name="💽 Looping?", value="<:error:867269410644557834>")
  embed.set_image(url=f"{song.thumbnail}")
  await ctx.send(embed=embed)
  

@client.command()
async def remove(ctx, index):
  player = music.get_player(guild_id=ctx.guild.id)
  song = await player.remove_from_queue(int(index))
  embed = discord.Embed(title="Removed from Queue", description=f"[{song.name}]({song.url}) has been removed from queue! [{ctx.author.mention}]", color=0xfff700)
  await ctx.send(embed=embed)


            

@client.command()
async def moveme(ctx , channel: discord.VoiceChannel, member:discord.Member=None):
  if member == None:
    member = ctx.author
  await member.move_to(channel)
  em = discord.Embed(description=f"<:success:893501515107557466> {member.mention} has been moved to {channel.mention}", color=ctx.author.color)
  await ctx.send(embed=em)            
           
 
#wanted
@client.command()
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


@client.command()
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

@client.command(aliases=["spongebob"])
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


@client.command()
@commands.has_permissions(manage_channels=True)
async def nuke(ctx, channel: discord.TextChannel=None):
  if channel==None:
    channel=ctx.channel
  await channel.delete(reason=f'Nuked by {ctx.author}')
  clone_channel=await channel.clone(reason=f'Nuked by {ctx.author}')
  await clone_channel.edit(position=channel.position)
  await clone_channel.send(f'Channel nuked by `{ctx.author.name}`')
  


@client.command()
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


@client.command()
async def anime(ctx, *, search):
  embed = discord.Embed(description="> <a:loading:865563025586389003> Fetching anime details..")
  s = await ctx.send(embed=embed)
  search = AnimeSearch(search)
  anime = Anime(f"{search.results[0].mal_id}")
  em = discord.Embed(title=f"{anime.title}", description=f"{str(anime.synopsis)}\n **Source**: {str(anime.source)}", url=anime.url, color=ctx.author.color)
  em.add_field(name="🗂️ Type", value=str(anime.type))
  em.add_field(name="⏳ Status", value=str(anime.status))
  em.add_field(name="⭐ Rating/10", value=float(anime.score))
  em.add_field(name=f"🏆 Rank", value=f"Top {int(anime.rank)}")
  em.add_field(name="⏱️ Duration", value=str(anime.duration))
  em.add_field(name="⚠️ Rated to", value=str(anime.rating))
  em.add_field(name="💽 Episodes", value=int(anime.episodes))
  em.add_field(name="🗓️ Aired", value=str(anime.aired))
  em.add_field(name="➡️ Genres", value=f"{', '.join(anime.genres)}")
  em.set_thumbnail(url=anime.image_url)
  await s.edit(embed=em)


@client.command()
async def timestamp(ctx, unixcode: int):
  em = discord.Embed(title="Unixcode to timestamp converter", description=f"Long Date   | <t:{unixcode}:D>\nShort Date   | <t:{unixcode}:d>\n---------------------------------------\nLong Date/Time   | <t:{unixcode}:F>\nShort Date/Time   | <t:{unixcode}:f>\n---------------------------------------\nLong Time   | <t:{unixcode}:T>\nShort Time   | <t:{unixcode}:t>\n---------------------------------------\nRelative Time   | <t:{unixcode}:R>", color=0xff00d4)
  em.set_footer(text=f"Invoked by {ctx.author.name}", icon_url=ctx.author.avatar_url)
  await ctx.send(embed=em)



@client.command()
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

@client.command()
async def poker(ctx, channel: discord.VoiceChannel=None):
  if channel == None:
    await ctx.send("Please mention a voice channel to start the activity")
  else:
    link = await togetherControl.create_link(channel.id, 'poker')
    em = discord.Embed(description=f"♠️ [Click here to start Poker night activity]({link})", color=0xfd1212)
    await ctx.send(embed=em)


@client.command()
async def chess(ctx, channel: discord.VoiceChannel=None):
  if channel == None:
    await ctx.send("Please mention a voice channel to start the activity")
  else:
    link = await togetherControl.create_link(channel.id, 'chess')
    em = discord.Embed(description=f"♟️ [Click here to start Chess in the park activity]({link})", color=0xfd1212)
    await ctx.send(embed=em)


@client.command()
async def betrayal(ctx, channel: discord.VoiceChannel=None):
  if channel == None:
    await ctx.send("Please mention a voice channel to start the activity")
  else:
    link = await togetherControl.create_link(channel.id, 'betrayal')
    em = discord.Embed(description=f"<:games:873121470308569168> [Click here to start betrayal.io activity]({link})", color=0xfd1212)
    await ctx.send(embed=em)

@client.command()
async def fishing(ctx, channel: discord.VoiceChannel=None):
  if channel == None:
    await ctx.send("Please mention a voice channel to start the activity")
  else:
    link = await togetherControl.create_link(channel.id, 'fishing')
    em = discord.Embed(description=f"<:games:873121470308569168> [Click here to start fishington.io activity]({link})", color=0xfd1212)
    await ctx.send(embed=em)
    

@client.command()
async def webhook(ctx, member: discord.Member = None, *, content):
  try:
    if member == None:
      member = ctx.author
    if await ctx.channel.webhooks():
      await ctx.message.delete()
      for w in await ctx.channel.webhooks():
        if w.name == "Gerty":
          url = f"{w.url}"
          data = {
            "content" : f"{content}",
            "username" : f"{member.display_name}",
            "avatar_url": f"{member.avatar_url}"
          }
          requests.post(url, json = data)
  except:
    em = discord.Embed(description=f'1. Try kicking the bot and [inviting](https://discord.com/api/oauth2/authorize?client_id=855443275658166282&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.gg%2Fms3PvCvQqK&scope=bot%20applications.commands) again\n2. Else create a webhook named _"Gerty"_  in {ctx.channel.name}\n> In order to use emojis from other servers, the @everyone role needs permission to "Use External Emojis" in the **Channel Settings Permissions.**', color=0xf62323)
    em.set_image(url="https://media.discordapp.net/attachments/873567363679785020/873569504167333978/unknown.png")
    em.set_author(name="Error while running this command", icon_url="https://cdn.discordapp.com/emojis/867269410644557834.png?v=1")
    await ctx.send(embed=em)
  
def generate_screenshot_api_url(customer_key, secret_phrase, options):
  api_url = 'https://api.screenshotmachine.com/?key=' + customer_key
  if secret_phrase:
    api_url = api_url + '&hash=' + hashlib.md5((options.get('url') + secret_phrase).encode('utf-8')).hexdigest()
  api_url = api_url + '&' + urllib.parse.urlencode(options)
  return api_url;


@client.command()
async def screenshot(ctx, url):
  if ctx.channel.is_nsfw():
    customer_key = '3fd3f1'
    secret_phrase = '' # leave secret phrase empty, if not needed
    options = {
      'url': f'{url}', # mandatory parameter
      # all next parameters are optional, see our website screenshot API guide for more details
      'dimension': '1366x768', # or "1366xfull" for full length screenshot
      'device': 'desktop',
      'cacheLimit' : '0',
      'delay' : '200',
      'zoom' : '100'
      }


    api_url = generate_screenshot_api_url(customer_key, secret_phrase, options)

    em = discord.Embed(color=ctx.author.color)
    em.set_image(url=api_url)
    s = await ctx.send("> <a:loading:865563025586389003> Loading screenshot...")
    await s.edit(embed=em)
  else:
    em = discord.Embed(description='Uh oh! This command is NSFW', color=0xf62323)
    em.set_image(url="https://i.imgur.com/oe4iK5i.gif")
    em.set_author(name="Error while running this command", icon_url="https://cdn.discordapp.com/emojis/867269410644557834.png?v=1")
    await ctx.send(embed=em)
  
@client.command(aliases=["delete"])
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
  
  
@client.command(aliases=["affect"])
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
  
@client.command(aliases=["sus"])
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
 
#calculates answer
def calculate(exp):
    o = exp.replace('×', '*')
    o = o.replace('÷', '/')
    result = ''
    try:
        result = str(eval(o))
    except:
        result = 'An error occurred.'
    return result
 
@client.command()
async def calc(ctx):
    em = discord.Embed(description="> <a:gloading:855680101529944064> Loading calculator..")
    m = await ctx.send(embed=em)
    expression = 'None'
    delta = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    e = discord.Embed(title=f'{ctx.author.name}\'s calculator | {ctx.author.id}', description=expression,
                        timestamp=delta)
    await m.edit(components=buttons, embed=e)
    while m.created_at < delta:
        res = await client.wait_for('button_click')
        if res.author.id == int(res.message.embeds[0].title.split('|')[1]) and res.message.embeds[
            0].timestamp < delta:
            expression = res.message.embeds[0].description
            if expression == 'None' or expression == 'An error occurred.':
                expression = ''
            if res.component.label == 'Exit':
                await res.respond(content='Calculator Closed', type=7)
                await asyncio.sleep(2)
                await m.delete()
                break
            elif res.component.label == '←':
                expression = expression[:-1]
            elif res.component.label == 'Clear':
                expression = 'None'
            elif res.component.label == '=':
                expression = calculate(expression)
            else:
                expression += res.component.label
            f = discord.Embed(title=f'{res.author.name}\'s calculator|{res.author.id}', description=expression,
                                timestamp=delta)
            await res.respond(content='', embed=f, components=buttons, type=7)
  

@client.command()
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

@client.command()
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

 
@client.group(invoke_without_command=True)
async def enhance(ctx):
    em = discord.Embed(title="Image enhancement commands", description="**<a:dot:860177926851002418> g!enhance [option]**\n > <:image:873933502435962880> options:\n`color`, `contrast`, `brightness`, `sharpness`, `rgb`", color=0x2F3136)
    await ctx.send(embed=em)


@enhance.command()
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

@enhance.command()
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

@enhance.command()
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


@enhance.command()
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

@enhance.command()
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
  
  
@client.command(aliases=["doesnotexist", "thispersondoesnotexist"])
async def persondoesnotexist(ctx):
  
  picture = await get_online_person()
  
  await save_picture(picture, "doesnotexist.jpeg")
  f = discord.File("doesnotexist.jpeg", filename="doesnotexist.jpeg")
  em = discord.Embed(title='This person does not exist', color=0x2F3136)
  em.set_image(url="attachment://doesnotexist.jpeg")
  em.set_footer(text='Generative adversarial network')
  await ctx.send(file=f, embed=em)


@client.command()
async def spotify(ctx, user:discord.Member=None):
  if user==None:
    user=ctx.author


  spotify_result=next((activity for activity in user.activities if isinstance(activity, discord.Spotify)),None)
  if spotify_result is None:
   em=discord.Embed(description='<:error:893501396161290320> He/She is not listening to spotify or I can\'t detect', color=0x2F3136)
   return await ctx.reply(embed=em, mention_author=False)

  components=[[Button(style=ButtonStyle.URL, label='Listen on spotify\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800', url=f'https://open.spotify.com/track/{spotify_result.track_id}', emoji=client.get_emoji(902569759323848715)), Button(style=ButtonStyle.gray, label='\u2630', disabled=True)]]

  track_background_image=Image.open('images/spotify_template.png')
  album_image=Image.open(requests.get(spotify_result.album_cover_url, stream=True).raw).convert('RGBA')
  title_font=ImageFont.truetype('theboldfont.ttf', 16)
  artist_font=ImageFont.truetype('theboldfont.ttf', 14)
  album_font=ImageFont.truetype('theboldfont.ttf', 14)
  start_duration_font=ImageFont.truetype('theboldfont.ttf', 12)
  end_duration_font=ImageFont.truetype('theboldfont.ttf', 12)
  title_text_position=150, 30
  artist_text_position=150, 60
  album_text_position=150, 80
  start_duration_text_position=150, 122
  end_duration_text_position=515, 122
  draw_on_image=ImageDraw.Draw(track_background_image)
  draw_on_image.text(title_text_position, spotify_result.title, 'white', font=title_font)
  draw_on_image.text(artist_text_position, f'by {spotify_result.artist}', 'white', font=artist_font)
  draw_on_image.text(album_text_position, spotify_result.album, 'white', font=album_font)
  draw_on_image.text(start_duration_text_position, '0:00', 'white', font=start_duration_font)
  draw_on_image.text(end_duration_text_position,f"{dateutil.parser.parse(str(spotify_result.duration)).strftime('%M:%S')}",'white', font=end_duration_font)
  album_color = album_image.getpixel((250, 100))
  background_image_color=Image.new('RGBA', track_background_image.size, album_color)
  background_image_color.paste(track_background_image, (0, 0), track_background_image)
  album_image_resize=album_image.resize((140, 160))
  background_image_color.paste(album_image_resize, (0,0),album_image_resize)
  background_image_color.convert('RGB').save('spotify.jpg','JPEG')
  f = discord.File("spotify.jpg",filename="spotify.jpg")
  await ctx.reply(f'Listening to **{spotify_result.title}** by **{spotify_result.artist}**',file=f, components=components, mention_author=False)
  
@client.command(aliases=["si"])
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
  

@client.command(aliases=["whattoken", "what_token"])
@commands.is_owner()
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

@client.command()
async def waifu(ctx):
  async with aiohttp.ClientSession() as cs:
      async with cs.get('https://api.waifu.pics/sfw/waifu') as r:
          res = await r.json()  # returns dict
          embed = discord.Embed(color=0x2F3136)
          embed.set_image(url=f"{res['url']}")
          embed.set_footer(text=f"Invoked by {ctx.author.name} · SFW - enabled", icon_url=f"{ctx.author.avatar_url}")
          await ctx.send(embed=embed)


@client.command()
async def status(ctx, status_code):
  embed = discord.Embed(color=0x2F3136)
  embed.set_image(url=f"https://http.cat/{status_code}")
  embed.set_footer(text=f"Invoked by {ctx.author.name}", icon_url=f"{ctx.author.avatar_url}")
  await ctx.send(embed=embed)



@client.command()
async def tts(ctx, *, text):
  em = discord.Embed(description="<a:ttsloading:886607614111273010> Processing your tts", color=0x2F3136)
  if len(text) >= 20:
    d = await ctx.send(embed=em)
  texttotts = f"{text}"
  language='en'
  output=gTTS(text=texttotts, lang=language, slow=False)
  output.save('tts.mp3')
  if len(text) >= 20:
    await d.delete()
  await ctx.send(f"{ctx.author.mention}",file=discord.File('tts.mp3'))



@client.command()
async def nitro(ctx):
  em=discord.Embed(title="Nitro", description="Expires in 48 hours", color=0x2F3136)
  em.set_author(name="A WILD GIFT APPEARS!")
  em.set_thumbnail(url="https://media.discordapp.net/attachments/884423056934711326/888057999875244072/2Q.png")


  components = [
    Button(style=ButtonStyle.green, label='⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ACCEPT⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀')
  ]

  main = await ctx.send(embed=em, components=components)

  while True:
    try:
      event = await client.wait_for('button_click', check=None)
      if event.component.label == '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ACCEPT⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀':
        await event.respond(
          content="Are you sure you want to claim?. This action is irreversible",
          type=4,
          components=[[Button(style=ButtonStyle.green, label='Yes'), Button(style=ButtonStyle.grey, label='No')]]
        )
        await main.edit(components=[
          Button(style=ButtonStyle.gray, label='⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀CLAIMED⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀', disabled=True)
        ])
      elif event.component.label == 'Yes':
        await event.respond(
          content="https://tenor.com/view/rick-astly-rick-rolled-gif-22755440",
          type=4
        )
      elif event.component.label == 'No':
        await event.respond(
          content="https://tenor.com/view/in-your-face-fuck-you-screw-you-fuck-off-middle-finger-gif-5474512",
          type=4
        )
    except Exception as e:
      print(e)







@client.command()
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


@client.group(invoke_without_command=True)
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

@lurking.command()
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
      




@client.command()
async def ocr(ctx, *, url):
  async with aiohttp.ClientSession() as sess:
      async with sess.get('https://api.openrobot.xyz/api/ocr', headers={'Authorization': 'X7gThnuWOuN9qWSd22VUm_NKmm1XQYMVHzxnIeJgP5XUCcayJ9XClwQdJUkGVcez0Sg'}, params={'url': f'{url}'}) as resp:
        js = await resp.json() 

        em = discord.Embed(description=f"{js['text']}", color=0x2F3136)
        em.add_field(name="Angles", value=f"{js['angles']}")
        em.add_field(name="languages", value=f"{js['languuages']}")
        em.add_field(name="Styles", value=f"{js['styles']}")
        await ctx.send(embed=em)


@client.group(invoke_without_command=True)
async def todo(ctx):
  em = discord.Embed(title="To-do is here!", description="Now you can add your to-do in gerty and bot will show you the list of to-do tasks that you should complete", color=0x2F3136)
  em.add_field(name="Commands", value="<:arrow:885193320068968508> `todo add` - Adds a task to your to-do list, usage: todo add [task]\n<:arrow:885193320068968508> `todo edit` - Edits the todo task, usage: todo edit [todo id] [new todo]\n<:arrow:885193320068968508> `todo remove` - Removes a task from your todo list, usage: todo remove [todo id]\n<:arrow:885193320068968508> `todo list` - Shows the list of tasks to do")
  await ctx.reply(embed=em, mention_author=False)

@todo.command()
async def add(ctx, *, todo):
  created = int(datetime.datetime.now().timestamp())
  await client.db.execute("INSERT INTO todo_data (todo, author_id, jump_url, created_at) VALUES ($1,$2,$3,$4)", f"{todo}", ctx.author.id, f"{ctx.message.jump_url}", created)
  await ctx.send(f"Alright I have added the task to your to-do list!\n\n> {todo}")

@todo.command()
async def list(ctx):
  todo_list = []
  todo_data = await client.db.fetch("SELECT * FROM todo_data WHERE author_id = $1", ctx.author.id)
  if todo_data:
    for todo in todo_data:
      todo_list.append(f"<:arrow:885193320068968508> **{todo[4]}**. <t:{todo[3]}:R> | [{todo[0]}]({todo[2]})")

    em = discord.Embed(description='\n'.join(todo_list), color=0x2F3136)
    em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
    mainmessage = await ctx.send(embed=em, components=[Button(style=ButtonStyle.gray, emoji=client.get_emoji(890938576563503114), id="todolistdelete")])
    while True:
      todoev = await client.wait_for("button_click")
      if todoev.author != ctx.author:
        await todoev.respond(content="Sorry, this buttons cannot be controlled by you", type=4)
      else:
        if todoev.component.id == "todolistdelete":
          try:
            await mainmessage.delete()
            await ctx.message.add_reaction("<:success:893501515107557466>")
          except:
            pass
          break
  else:
    await ctx.send("You don't have any upcoming tasks.")


@todo.command()
async def edit(ctx, todo_key: int, *, new):
  try:
    g = await client.db.fetchrow("SELECT * FROM todo_data WHERE key = $1", todo_key)
  except:
    await ctx.send(f'To-do with key "{todo_key}" was not found in your to-do list.')
  else:
    if g[1] == ctx.author.id:
      await client.db.execute("UPDATE todo_data SET todo = $1 WHERE key = $2", f"{new}", todo_key)
      await ctx.send(f"Succesfully edited your to-do list.")
    else:
      await ctx.send(f'To-do with key "{todo_key}" was not found in your to-do list.')


@todo.command(aliases=["done"])
async def remove(ctx, *, todo_key:int):
  try:
    g = await client.db.fetchrow("SELECT * FROM todo_data WHERE key = $1", todo_key)
  except:
    await ctx.send(f'To-do with key "{todo_key}" was not found in your to-do list.')
  else:
    if g[1] == ctx.author.id:
      await client.db.execute("DELETE FROM todo_data WHERE key = $1", todo_key)
      await ctx.send(f'Task "{todo_key}" removed from your to-do list.')
    else:
      await ctx.send(f'To-do with key "{todo_key}" was not found in your to-do list.')


@client.command(aliases=["src"])
async def source(ctx):
  em = discord.Embed(description="[**`Here, whole bot source code`**](https://gerty-github.web.app/)", color=0x2F3136)
  await ctx.reply(embed=em, mention_author=False)

client.run("ODU1NDQzMjc1NjU4MTY2Mjgy.YMyjog.T_9PQpggBRcXz2gA2Hnkm3OHFOA", reconnect=True)
