import discord
import random
import praw
import urllib.parse, urllib.request, re
import os
import requests
import members
import math
import spotify
import moderation
import AFK
import aiofiles
import datetime
import asyncio
import json
import DiscordUtils
import covid
import asyncpg
from PIL import Image
from io import BytesIO
from discord import asset
from discord_components import *
from discord import channel
from discord import embeds, DMChannel
from random import choice
from asyncio import TimeoutError
from discord.colour import Color
from discord.ext import commands
from googleapiclient.discovery import build

cogs = [covid, members, spotify, AFK, moderation]


client = commands.Bot(command_prefix = commands.when_mentioned_or('g!'), intents=discord.Intents.all())
client.remove_command("help")


ch1 = ["Rock", "Scissors", "Paper"]

for i in range(len(cogs)):
  cogs[i].setup(client)




api_key = "AIzaSyDNgIRLXv0XcvFw_gJ_dpG2Cx-pkoN4Cio"

user = discord.user
####
####
#ai
snipe_message_author = {}
snipe_message_content = {}


@client.event
async def on_message_delete(message):
  snipe_message_author[message.channel.id]= message.author
  snipe_message_content[message.channel.id]= message.content
  await asyncio.sleep(60)
  del snipe_message_author[message.channel.id]
  del snipe_message_content[message.channel.id]

@client.event
async def on_guild_join(guild):
    if guild.system_channel:
        embed=discord.Embed(title="<:dot_2:862321994983669771> Gerty Information <:dot_2:862321994983669771>", url="https://discord.com/api/oauth2/authorize?client_id=855443275658166282&permissions=8&scope=bot", description="The bot is developed by Fury Alt#0143, `g!help` for commands! :)", color=0xd400ff)
        embed.set_author(name="Gerty", url="https://discord.com/api/oauth2/authorize?client_id=855443275658166282&permissions=8&scope=bot", icon_url="https://images-ext-1.discordapp.net/external/rr_qjkmIgbvvfmM9VFMX6bKvaO1yb6LoAadw81lOdjk/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/855443275658166282/277983486fab2a474f49ed47fcdcc25b.webp?width=586&height=586")
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/783652973502922752.gif?v=1")
        embed.add_field(name="My ID:", value="> 855443275658166282", inline=True)
        embed.add_field(name="Username:", value="> Gerty", inline=True)
        embed.add_field(name="Tag:", value="> Gerty#9317  <:bot:860140819964887099>", inline=True)
        embed.add_field(name="Created at:", value="> Fri, 18 June 2021, 01:46 pm", inline=True)
        embed.add_field(name="Servers in:", value=f"> {len(client.guilds)} Servers", inline=True)
        embed.add_field(name="Invite Me:", value="> [Invite](https://discord.com/api/oauth2/authorize?client_id=855443275658166282&permissions=8&scope=bot)", inline=True)
        embed.add_field(name="Join support server", value="> [Support server](https://discord.gg/XkF3VFbQWU)", inline=True)
        embed.set_footer(text=f"Thanks for inviting me to {guild.name}! :]")
        await guild.system_channel.send(embed=embed)



@client.command()
@commands.has_permissions(manage_messages=True)
@commands.cooldown(1,10,commands.BucketType.channel)
async def snipe(ctx):
  channel = ctx.channel
  try:
    snipeEmbed = discord.Embed(description=f"Last deleted message within 60s in {channel.mention} :\n {snipe_message_content[channel.id]}", color=0xa6ff00, timestamp=datetime.datetime.utcnow())
    snipeEmbed.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}")
    snipeEmbed.set_author(name=f"Message by {snipe_message_author[channel.id]}", icon_url=f"{snipe_message_author[channel.id].avatar_url}")
    snipeEmbed.set_thumbnail(url=f"{snipe_message_author[channel.id].avatar_url}")
    await ctx.send(embed=snipeEmbed)
  except:
    m = await ctx.send(f"{ctx.author.mention} There are no deleted messages within 60s in {channel.mention}")
    await asyncio.sleep(4)
    await m.delete()


@snipe.error
async def snipe_error(ctx, error):
  print(error)
  if isinstance(error, commands.MissingPermissions):
    v = await ctx.send(f"{ctx.author.mention} looks like you don't have permission to use this command. contact {ctx.guild.name} admins")
    await asyncio.sleep(4)
    await v.delete()


@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online, activity=discord.Game(f'with {len(client.guilds)} servers and {len(client.users)} users | v9.0 | g!help'))
  print('Gerty is ready')
  DiscordComponents(client)
  async with aiofiles.open("ticket_configs.txt", mode="a") as temp:
        pass

  async with aiofiles.open("ticket_configs.txt", mode="r") as file:
        lines = await file.readlines()
        for line in lines:
            data = line.split(" ")
            client.ticket_configs[int(data[0])] = [int(data[1]), int(data[2]), int(data[3])]

  print(f"{client.user.name} is ready.")



#filterd words
filtered_words = ["fuck", "sex", "neger", "maadarchod", "thendi", "chetta", "Fuck", "Sex", "Neger", "Myr", "Maadarchod", "Thendi", "Chetta"]
#react_words





#mention help





@client.command()
@commands.is_owner()
async def servers(ctx):
    activeservers = client.guilds
    for guild in activeservers:
        await ctx.send(f"Guild name = `{guild.name}` | Guild id = `{guild.id}`")



@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    msg = "> <:slowmode:861261195621040138> Please wait **{:.2f}** seconds before using this command again".format(error.retry_after)
    await ctx.send(msg)


#on reaction add
@client.event
async def on_raw_reaction_add(payload):
  if payload.member.id != client.user.id and str(payload.emoji) == u"\U0001F3AB":
        msg_id, channel_id, category_id = client.ticket_configs[payload.guild_id]

        if payload.message_id == msg_id:
            guild = client.get_guild(payload.guild_id)

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
                await client.wait_for("message", check=lambda m: m.channel == ticket_channel and m.author == payload.member and m.content == "-close", timeout=3600)

            except asyncio.TimeoutError:
                await ticket_channel.delete()

            else:
                await ticket_channel.delete()

  if payload.member.bot:
    pass

  else:

    with open('reactrole.json') as react_file:

      data = json.load(react_file)
      for x in data:
        if x['emoji'] == payload.emoji.name and x['message_id'] == payload.message_id:
          role = discord.utils.get(client.get_guild(payload.guild_id).roles, id=x['role_id'])

          await payload.member.add_roles(role)

        
#on reaction remove
@client.event
async def on_raw_reaction_remove(payload):

    with open('reactrole.json') as react_file:

      data = json.load(react_file)
      for x in data:
        if x['emoji'] == payload.emoji.name and x['message_id'] == payload.message_id:
          role = discord.utils.get(client.get_guild(payload.guild_id).roles, id=x['role_id'])

          await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)


#ping command
@client.command(aliases=['ms', 'latency'])
async def ping(ctx):
  v = await ctx.reply("PONG!! :joy:")
  await asyncio.sleep(1)
  await v.edit("LOL NO <:gavatar1:855833931726061588>")
  await asyncio.sleep(1)
  await v.edit(f'**<a:gloading:855680101529944064> | Response in! {round(client.latency * 1000)}ms**')

#8ball command
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
  await ctx.reply(f':question: Question: {question}\n<a:ganswer:855676717368213564>  Answer: {random.choice(responses)}')


#developer command
@client.command()
async def dev(ctx):
  await ctx.reply('**My developer is __Fury Alt#0143__ <a:fury_evil:855450553575407676>  <a:fury_dream:855450669090865163>**')



@client.command(aliases=["invite", "info", "botinfo"])
async def bot(ctx):
  embed=discord.Embed(title="<:dot_2:862321994983669771> Gerty Information <:dot_2:862321994983669771>", url="https://discord.com/api/oauth2/authorize?client_id=855443275658166282&permissions=8&scope=bot", description="The bot is developed by Fury Alt#0143", color=0xd400ff)
  embed.set_author(name="Gerty", url="https://discord.com/api/oauth2/authorize?client_id=855443275658166282&permissions=8&scope=bot", icon_url="https://images-ext-1.discordapp.net/external/rr_qjkmIgbvvfmM9VFMX6bKvaO1yb6LoAadw81lOdjk/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/855443275658166282/277983486fab2a474f49ed47fcdcc25b.webp?width=586&height=586")
  embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/783652973502922752.gif?v=1")
  embed.add_field(name="My ID:", value="> 855443275658166282", inline=True)
  embed.add_field(name="Username:", value="> Gerty", inline=True)
  embed.add_field(name="Tag:", value="> Gerty#9317  <:bot:860140819964887099>", inline=True)
  embed.add_field(name="Created at:", value="> Fri, 18 June 2021, 01:46 pm", inline=True)
  embed.add_field(name="Servers in:", value=f"> {len(client.guilds)} Servers", inline=True)
  embed.add_field(name="Invite Me:", value="> [Invite](https://discord.com/api/oauth2/authorize?client_id=855443275658166282&permissions=8&scope=bot)", inline=True)
  embed.add_field(name="Join support server", value="> [Support server](https://discord.gg/XkF3VFbQWU)", inline=True)
  embed.set_footer(text=f"Hello {ctx.author.name}! nice to meet you")
  await ctx.send(embed=embed)


#brain_update fun command

@client.command()
async def brain_update(ctx):
  embed=discord.Embed(title="Brain Update", color=0xff0000, timestamp=ctx.message.created_at)
  embed.set_author(name="Fury Alt#0143", icon_url="https://cdn.discordapp.com/avatars/770646750804312105/a_315213b92bc2fcebcbf393efe505c845.gif?size=256")
  embed.add_field(name="Update your brain", value="**Your brain is __outdated__ [click here](https://youtu.be/dQw4w9WgXcQ) to __update your brain__**", inline=False)
  await ctx.reply(embed=embed)






#avatar command

@client.command()
async def avatar(ctx, member : discord.Member = None):
  if member == None:
    member = ctx.author

  memberAvatar = member.avatar_url

  avaembed = discord.Embed(title = f"{member.name}'s avatar", color=0x00eeff, timestamp=ctx.message.created_at)
  avaembed.set_image(url=memberAvatar )

  await ctx.reply(embed=avaembed)
#commands or help command

#code command
@client.command()
async def code(ctx):
    await ctx.reply("**<:gpython:855690635351425034> i'm running in python __discord.py__**")


#dm command
@client.command(aliases=["dm"])
async def mail(ctx, user: discord.User = None, *, msg):
      await user.send(f'You have a mail from **{ctx.author.name}** : {msg}')
      await ctx.reply('**Mail send <a:gdmsend:856043489187069952>**')



#announce command



#delete channel command
@client.command()
@commands.has_permissions(manage_channels=True)
async def deletechannel(ctx, channel: discord.TextChannel):
      if ctx.author.guild_permissions.manage_channels:
        await ctx.message.add_reaction('✅')
        await channel.delete()


#delete voice channel command
@client.command(aliases=["deletevc", "dvc"])
@commands.has_permissions(manage_channels=True)
async def deletevoicechannel(ctx, channel: discord.VoiceChannel):
      if ctx.author.guild_permissions.manage_channels:
        await ctx.message.add_reaction('✅')
        await channel.delete()


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
@client.command()
async def say(ctx, *, message):
  await ctx.message.delete()
  await ctx.send(f'**{ctx.author.name}** : {message}' .format(message))

@client.command()
async def saymodonly(ctx, *, message):
  await ctx.message.delete()
  await ctx.send(f'{message}' .format(message))

#reactrole command
@client.command()
@commands.has_permissions(administrator=True)
async def reactrole(ctx, emoji, role: discord.Role, *, message):
  if ctx.author.guild_permissions.manage_roles:
    emb = discord.Embed(title="React role", description=message, color=ctx.author.color, timestamp=ctx.message.created_at)
  msg = await ctx.channel.send(embed=emb)
  await msg.add_reaction(emoji)

  with open('reactrole.json') as json_file:
    data = json.load(json_file)

    new_react_role = {
      'role_name':role.name,
      'role_id':role.id,
      'emoji':emoji,
      'message_id':msg.id
    }

    data.append(new_react_role)

  with open('reactrole.json', 'w') as j:
    json.dump(data,j,indent=4)

@reactrole.error
async def reactrole_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("> Please fill the required arguments correctly")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.mention} you have no permission to use this command")


  #mute command
@client.command()
@commands.has_permissions(manage_channels=True)
async def mute(ctx, member: discord.Member, *, reason=None):
  guild= ctx.guild
  mutedRole = discord.utils.get(guild.roles, name='Muted')

  if not mutedRole:
    mutedRole = await guild.create_role(name="Muted")

    for channel in guild.channels:
      await channel.set_permissions(mutedRole, speak=False, send_messages=False)

  await member.add_roles(mutedRole, reason=reason)
  if reason == None:
    embed = discord.Embed(description=f"✅ Muted {member.name}#{member.discriminator}", color=0x2bff00)
    await ctx.send(embed=embed)
    await member.send(f'You were muted in the server **{guild.name}**')
  else:
    embed2 = discord.Embed(description=f"✅ Muted {member.name}#{member.discriminator} for reason **{reason}**", color=0x2bff00)
    await ctx.send(embed=embed2)
    await member.send(f'You were muted in the server **{guild.name}** for reason: __{reason}__')

@mute.error
async def mute_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("> **Please mention someone to mute.**")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.mention} you have no permission to use this command")



#unmute command
@client.command()
@commands.has_permissions(manage_channels=True)
async def unmute(ctx, member: discord.Member):
  mutedRole = discord.utils.get(ctx.guild.roles, name='Muted')

  await member.remove_roles(mutedRole)
  em = discord.Embed(description=f"✅ Unmuted {member.name}#{member.discriminator}", color=0x2bff00)
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

@giveaway.error
async def giveaway_error(ctx, error):
  print(error)
  if isinstance(error, commands.MissingAnyRole):
    await ctx.send(f'You need admin permission to use this command. Please contact {ctx.guild.name} owner')
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




#giveaway command time asyncio
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
        await ctx.send("> **Please start a new game using the !tictactoe command.**")


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

#img search
@client.command(aliases=["show", "search", "img"])
@commands.cooldown(1,5,commands.BucketType.user)
async def showpic(ctx, *, search):
    ran = random.randint(0, 9)
    resource = build("customsearch", "v1", developerKey=api_key).cse()
    result = resource.list(
        q=f"{search}", cx="b53b2dd813c49255f", searchType="image"
    ).execute()
    url = result["items"][ran]["link"]
    embed1 = discord.Embed(title=f"__{search.title()}__")
    embed1.set_image(url=url)
    await ctx.send(embed=embed1)


#help command


#memes


reddit = praw.Reddit(client_id = "vuwfZiZXYnPZlg",
                     client_secret = "aOLy1GQJrhCIPAe7UCeCMGvIoP0JLw",
                     username = "Gerty_1",
                     password = "82xPm!erQA$adt6",
                     user_agent = "Gerty")



@client.command()
@commands.cooldown(1,5,commands.BucketType.user)
async def meme(ctx, subred = "memes"):
  subreddit = reddit.subreddit(subred)
  all_subs = []

  top = subreddit.top(limit = 50)

  for submission in top:
    all_subs.append(submission)

  random_sub = random.choice(all_subs)

  name = random_sub.title
  url = random_sub.url

  em = discord.Embed(title = name)

  em.set_image(url = url)

  await ctx.send(embed= em)




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

@client.command()
async def dropdown(ctx):
  m = await ctx.send("Dropdown test",
                  components=[
                    Select(placeholder='Select something!', options=[SelectOption(label="first drop", value='a'), SelectOption(label="second drop", value='b')])
                  ])
  def check(res):
    return ctx.author == res.user and res.channel == ctx.channel

  try:
    res = await client.wait_for("select_option", check=check, timeout=15)
    value = res.component.label
    if value == "second drop":
      await res.respond("second")
    if value == "first drop":
      await res.respond("first")

  except TimeoutError:
    await m.edit("Timed out")
  
#userinfo
@client.command()
@commands.cooldown(1,5,commands.BucketType.user)
async def whois(ctx, member: discord.Member=None):
  if member == None:
    member = ctx.author



  roles = [role for role in member.roles]



  embed=discord.Embed(color=member.color, timestamp=ctx.message.created_at)

  embed.set_author(name=f"User info - {member}")
  embed.set_thumbnail(url=member.avatar_url)
  embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

  embed.add_field(name="ID:", value=member.id)
  embed.add_field(name="Server Name:", value=member.display_name)
  

  embed.add_field(name="Account created at:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %P UTC"))
  embed.add_field(name="Joined this server at:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %P UTC"))

  embed.add_field(name=f"Roles <:greactionrole:856129896106688522> ({len(roles)})", value=" ".join([role.mention for role in roles]))
  embed.add_field(name="Top role <:greactionrole:856129896106688522>", value=member.top_role.mention)

  embed.add_field(name="Is member a Bot? <:bot:860140819964887099>", value=member.bot)
  if member.public_flags.hypesquad_balance is True:
    embed.add_field(name="Hypesquad", value="<:balance:866614979214049290>")
  elif member.public_flags.hypesquad_bravery is True:
    embed.add_field(name="Hypesquad", value="<:bravery:866614978864873523>")
  elif member.public_flags.hypesquad_brilliance is True:
    embed.add_field(name="Hypesquad", value="<:brilliance:866614979250487316>")
  await ctx.send(embed=embed)


@mail.error
async def mail_error(ctx, error):
    print(error)
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send(f"> <a:gcooldown:855749809582768139> **{ctx.author.mention} That mentioned members' dm is off cannot send message**")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("> **<:discordPoop:813895205115265035> something went wrong**")

@meme.error
async def meme_error(ctx, error):
    print(error)
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send(f"> **<:discordpoop:860138531241328660> something went wrong**")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("> **<:discordPoop:813895205115265035> something went wrong**")

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
async def lock(ctx):
  await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
  embed = discord.Embed(description=f"✅ {ctx.channel.mention} is now locked", color=0x2bff00)
  await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(manage_channels = True)
async def unlock(ctx):
  await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
  embed = discord.Embed(description=f"✅ {ctx.channel.mention} is now unlocked", color=0x2bff00)
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
  await ctx.send(f'Set the slowmode delay in {ctx.channel.mention} to {seconds} seconds! <:slowmode:861261195621040138>')

@slowmode.error
async def slowmode_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"> <a:gcooldown:855749809582768139> {ctx.author.mention} Please enter seconds")

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

@nick.error
async def nick_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"> <a:gcooldown:855749809582768139> {ctx.author.mention} Please mention a member and after a new nickname")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.mention} You cannot use this command you need manage nickname permission. Please contact {ctx.guild.name} admins")

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
@massunban.error
async def massunban_error(ctx, error):
  print(error)
  if isinstance(error, commands.MissingPermissions):
    await ctx.send(f"{ctx.author.mention} You have no permission to use this command")

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

@hack.error
async def hack_error(ctx, error):
  print(error)
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(f"{ctx.author.mention} Please mention a user to hack")



@client.group(invoke_without_command=True)
async def help(ctx):
  embed=discord.Embed(title="<:stagechannel:861997716053032991> Main Page <:stagechannel:861997716053032991>", description=" <:dot_2:862321994983669771> Bot prefix is `g!` <a:wumpycodes:862724245267283998> \n <:dot_2:862321994983669771> `g!help [category]` for specific category details <:wumplus:862723850693247016> \n <:dot_2:862321994983669771> `g!info` for my details <:dealwumpusit:862723850617487370> \n <:dot_2:862321994983669771> if there is any bug roaming around please report it by using `g!report` command <:cow_boy_bug:862723348928528464>", color=0xff00ea)
  embed.set_author(name="How can i help you?", icon_url="https://images-ext-1.discordapp.net/external/rr_qjkmIgbvvfmM9VFMX6bKvaO1yb6LoAadw81lOdjk/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/855443275658166282/277983486fab2a474f49ed47fcdcc25b.webp?width=586&height=586")
  embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/2SMx3hT4Tal6WPc8AaveG0ftBtGgR3Vowuzvd1ggEec/%3Fv%3D1/https/cdn.discordapp.com/emojis/850646273530658876.gif")
  embed.add_field(name="Categories:", value="> <:blurplemoderator:862212401080434698> _Fun commands_\n > <:blurplemoderator:862212401080434698> _Mod commands_\n > <:blurplemoderator:862212401080434698> _Music commands_\n > <:blurplemoderator:862212401080434698> _Miscellaneous commands_\n > <:blurplemoderator:862212401080434698> _Roleplay commands_", inline=False)
  embed.add_field(name="Useful links:", value="> :link: [Invite me](https://bit.ly/3wGFgl7)\n > :link: [Support server](https://discord.gg/XkF3VFbQWU)\n > :link: [Dashboard](https://youtu.be/dQw4w9WgXcQ)", inline=False)
  embed.set_footer(text=f"Hello {ctx.author.name}! nice to meet you :]")
  await ctx.send(embed=embed)

@help.command(aliases=["Funcommand", "Fun", "funcommand"])
async def fun(ctx):
  embed=discord.Embed(title="<:stagechannel:861997716053032991> Fun Commands <:stagechannel:861997716053032991>", description="Bot prefix is `g!`,, `g!info` for details <a:gallset:857139110976290847>", color=0xff00ea)
  embed.set_author(name="How can i help you?", icon_url="https://images-ext-1.discordapp.net/external/rr_qjkmIgbvvfmM9VFMX6bKvaO1yb6LoAadw81lOdjk/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/855443275658166282/277983486fab2a474f49ed47fcdcc25b.webp?width=586&height=586")
  embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/2SMx3hT4Tal6WPc8AaveG0ftBtGgR3Vowuzvd1ggEec/%3Fv%3D1/https/cdn.discordapp.com/emojis/850646273530658876.gif")
  embed.add_field(name="Fun commands:", value="> g!emojify\n > g!meme, g!meme [keyword]\n > g!rps - (Rock paper scissors)\n > g!8ball\n > g!brain_update\n > g!ttt - (tic tac toe)\n > g!place - (tic tac toe sub command)\n > g!hack --new\n > g!calculate, calc --new\n > g!wanted\n > g!drake\n > g!spongebob, sponge\n > g!coin, flip")
  embed.set_footer(text=f"Hello {ctx.author.name}! nice to meet you :]")
  await ctx.send(embed=embed)

@help.command(aliases=["Mod", "Modcommand", "modcommand"])
async def mod(ctx):
  embed=discord.Embed(title="<:stagechannel:861997716053032991> Mod Commands <:stagechannel:861997716053032991>", description="Bot prefix is `g!`,, `g!info` for details <a:gallset:857139110976290847>", color=0xff00ea)
  embed.set_author(name="How can i help you?", icon_url="https://images-ext-1.discordapp.net/external/rr_qjkmIgbvvfmM9VFMX6bKvaO1yb6LoAadw81lOdjk/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/855443275658166282/277983486fab2a474f49ed47fcdcc25b.webp?width=586&height=586")
  embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/2SMx3hT4Tal6WPc8AaveG0ftBtGgR3Vowuzvd1ggEec/%3Fv%3D1/https/cdn.discordapp.com/emojis/850646273530658876.gif")
  embed.add_field(name="Mod commands:", value="> g!clear\n > g!kick\n > g!ban\n > g!unban\n > g!announce\n > g!deletechannel\n > g!deletevc\n > g!reactrole\n > g!mute\n > g!unmute\n > g!giveaway\n > g!reroll -(giveaway sub command)\n > g!channelinfo, ci\n > g!lock\n > g!unlock\n > g!slowmode\n > g!massunban\n > g!members\n > g!nick\n > g!resetnick\n > g!ticket [message id] [category id]\n > g!addrole\n > g!removerole\n > g!snipe\n > g!nuke\n > g!clone")
  embed.set_footer(text=f"Hello {ctx.author.name}! nice to meet you :]")
  await ctx.send(embed=embed)

@help.command(aliases=["Music", "Musiccommand", "musiccommand"])
async def music(ctx):
  embed=discord.Embed(title="<:stagechannel:861997716053032991> Music Commands <:stagechannel:861997716053032991>", description="Bot prefix is `g!`,, `g!info` for details <a:gallset:857139110976290847>", color=0xff00ea)
  embed.set_author(name="How can i help you?", icon_url="https://images-ext-1.discordapp.net/external/rr_qjkmIgbvvfmM9VFMX6bKvaO1yb6LoAadw81lOdjk/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/855443275658166282/277983486fab2a474f49ed47fcdcc25b.webp?width=586&height=586")
  embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/2SMx3hT4Tal6WPc8AaveG0ftBtGgR3Vowuzvd1ggEec/%3Fv%3D1/https/cdn.discordapp.com/emojis/850646273530658876.gif")
  embed.add_field(name="Music commands:", value="> g!join\n > g!play\n > g!pause\n > g!resume\n > g!queue\n > g!loop\n > g!remove [song position]\n > g!nowplaying, np\n > g!volume\n > g!skip\n > g!dc")
  embed.set_footer(text=f"Hello {ctx.author.name}! nice to meet you :]")
  await ctx.send(embed=embed)

@help.command(aliases=["Misc", "miscellaneous", "Miscellaneous"])
async def misc(ctx):
  embed=discord.Embed(title="<:stagechannel:861997716053032991> Miscellaneous Commands <:stagechannel:861997716053032991>", description="Bot prefix is `g!`,, `g!info` for details <a:gallset:857139110976290847>", color=0xff00ea)
  embed.set_author(name="How can i help you?", icon_url="https://images-ext-1.discordapp.net/external/rr_qjkmIgbvvfmM9VFMX6bKvaO1yb6LoAadw81lOdjk/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/855443275658166282/277983486fab2a474f49ed47fcdcc25b.webp?width=586&height=586")
  embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/2SMx3hT4Tal6WPc8AaveG0ftBtGgR3Vowuzvd1ggEec/%3Fv%3D1/https/cdn.discordapp.com/emojis/850646273530658876.gif")
  embed.add_field(name="Misc commands:", value="> g!ping\n > g!dev\n > g!avatar\n > g!code\n > g!mail\n > g!say\n > g!show\n > g!whois\n > g!nick\n > g!covid\n > g!spotify\n > g!afk")
  embed.set_footer(text=f"Hello {ctx.author.name}! nice to meet you :]")
  await ctx.send(embed=embed)

@help.command(aliases=["Roleplay", "roleplay", "roleplaycommands"])
async def role(ctx):
  embed=discord.Embed(title="<:stagechannel:861997716053032991> Roleplay Commands <:stagechannel:861997716053032991>", description="Bot prefix is `g!`,, `g!info` for details <a:gallset:857139110976290847>", color=0xff00ea)
  embed.set_author(name="How can i help you?", icon_url="https://images-ext-1.discordapp.net/external/rr_qjkmIgbvvfmM9VFMX6bKvaO1yb6LoAadw81lOdjk/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/855443275658166282/277983486fab2a474f49ed47fcdcc25b.webp?width=586&height=586")
  embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/2SMx3hT4Tal6WPc8AaveG0ftBtGgR3Vowuzvd1ggEec/%3Fv%3D1/https/cdn.discordapp.com/emojis/850646273530658876.gif")
  embed.add_field(name="Roleplay commands:", value="> g!hug\n > g!kiss\n > g!slam\n > g!punch")
  embed.set_footer(text=f"Hello {ctx.author.name}! nice to meet you :]")
  await ctx.send(embed=embed)

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

@hug.error
async def hug_error(ctx, error):
  print(error)
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(f"{ctx.author.mention} please mention the user you want to hug")

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

@kiss.error
async def kiss_error(ctx, error):
  print(error)
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(f"{ctx.author.mention} please mention the user you want to kiss")

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

@slam.error
async def slam_error(ctx, error):
  print(error)
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(f"{ctx.author.mention} please mention the user you want to slam")

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

@punch.error
async def punch_error(ctx, error):
  print(error)
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(f"{ctx.author.mention} please mention the user you want to punch")



#reports 
@client.command()
async def report(ctx, *, report=None):
  report_channel = client.get_channel(862593162618339329)
  invite = await ctx.channel.create_invite(max_age = 0, max_uses = 0)
  if report is None:
    return await ctx.send(f"{ctx.author.mention} Please include information about the report. Like g!report [information]")
  if len(ctx.message.content) < 20:
    await ctx.send("Your report must be at least 20 characters in length")
  else:
    embed = discord.Embed(title="Bug reports", description=f"{ctx.author.name} has reported an issue regarding Gerty.", color=0xff0040)
    embed.set_thumbnail(url=f"{ctx.author.avatar_url}")
    embed.add_field(name="More information:", value=f"{report}", inline=False)
    embed.add_field(name="Server invite:", value=f"[Server invite]({invite})", inline=False)
    embed.add_field(name="Perm invite link:", value=f"{invite}", inline=False)
    embed.add_field(name="Server name:", value=f"{ctx.guild.name}", inline=False)
    embed.set_footer(icon_url=f"{ctx.author.avatar_url}", text=f" | ID: {ctx.author.name}#{ctx.author.discriminator}")
    await ctx.send(":incoming_envelope: | _Your report has been sent to staff team!_")
    report_message = await report_channel.send(embed=embed)
    await report_message.add_reaction('✅')

    try:
      def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["✅"]

      reaction, user = await client.wait_for("reaction_add", timeout=604800, check=check)

      if str(reaction.emoji) == "✅":
        await ctx.author.send(":envelope_with_arrow: | _Your report has been looked into and dealt with. Thanks for your report_")
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
  await player.delete()

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
    data = await player.skip(force=True)
    if len(data) == 2:
        embed = discord.Embed(title="Skipped", description=f"[{data[0].name}]({data[0].url})", color=0xfff700)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description=f"> Stopped playing [{data[0].name}]({data[0].url}) nothing in the queue!", color=0x80ff00)
        await ctx.send(embed=embed)

@client.command(aliases=["vol"])
async def volume(ctx, vol):
    player = music.get_player(guild_id=ctx.guild.id)
    song, volume = await player.change_volume(float(vol) / 100) # volume should be a float between 0 to 1
    embed = discord.Embed(description=f"Set volume to {volume*100}%", color=0xfff700)
    await ctx.send(embed=embed)


@client.command()
async def pause(ctx):
  player = music.get_player(guild_id=ctx.guild.id)
  song = await player.pause()
  embed = discord.Embed(title="Paused playing", description=f"[{song.name}]({song.url})", color=0xfff700)
  await ctx.send(embed=embed)

@client.command()
async def resume(self, ctx):
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
  embed.add_field(name="⏳ Duration", value=f"{song.duration} seconds")
  embed.add_field(name="Channel Name <:youtube:865883178904059924>", value=f"[{song.channel}]({song.channel_url})")
  embed.add_field(name="Views 👀", value=f"{song.views}")
  embed.add_field(name="looping 🔂?", value=f"{song.is_looping}")
  embed.set_image(url=f"{song.thumbnail}")
  await ctx.send(embed=embed)

@client.command()
async def remove(ctx, index):
  player = music.get_player(guild_id=ctx.guild.id)
  song = await player.remove_from_queue(int(index))
  embed = discord.Embed(title="Removed from Queue", description=f"[{song.name}]({song.url}) has been removed from queue! [{ctx.author.mention}]", color=0xfff700)
  await ctx.send(embed=embed)


#calc
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
 
 
def calculate(exp):
    o = exp.replace('×', '*')
    o = o.replace('÷', '/')
    result = ''
    try:
        result = str(eval(o))
    except:
        result = '> <:discordpoop:860138531241328660> An error occurred.'
    return result
 
@client.command(aliases=["calculate", "calculator"])
async def calc(ctx):
    embed = discord.Embed(description = "> <a:gloading:855680101529944064> Loading Calculators...", color=0x2bff00)
    m = await ctx.send(embed=embed)
    await asyncio.sleep(1)
    expression = 'None'
    delta = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    e = discord.Embed(title=f'{ctx.author.name}\'s calculator 🖩 | {ctx.author.id}', description=expression,
                        timestamp=delta, color=0xfbff00)
    e.set_footer(text="Exit calculator after use")
    await m.edit(components=buttons, embed=e)
    while m.created_at < delta:
        res = await client.wait_for('button_click')
        if res.author.id == int(res.message.embeds[0].title.split('|')[1]) and res.message.embeds[
            0].timestamp < delta:
            expression = res.message.embeds[0].description
            if expression == 'None' or expression == 'An error occurred.':
                expression = ''
            if res.component.label == 'Exit':
                await res.respond(content='**> :closed_lock_with_key:  Calculator Closed**', type=7)
                break
            elif res.component.label == '←':
                expression = expression[:-1]
            elif res.component.label == 'Clear':
                expression = 'None'
            elif res.component.label == '=':
                expression = calculate(expression)
            else:
                expression += res.component.label
            f = discord.Embed(title=f'{res.author.name}\'s calculator | {res.author.id}', description=expression,
                                timestamp=delta, color=0xfbff00)
            f.set_footer(text="Exit calculator after use")
            await res.respond(content='', embed=f, components=buttons, type=7)

#wanted
@client.command()
async def wanted(ctx, user: discord.Member = None):
  if user == None:
    user = ctx.author

  wanted = Image.open("wanted.jpg")
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

  drake = Image.open("drake.jpg")
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

  sponge = Image.open("spongebob.jpg")
  asset  = user.avatar_url_as(size = 128)
  data = BytesIO(await asset.read())
  pfp = Image.open(data)

  pfp = pfp.resize((186,244))
  sponge.paste(pfp, (75,123))

  sponge.save("spongebob2.jpg")
  await ctx.send(file = discord.File("spongebob2.jpg"))


@client.command(aliases=["nuke"])
@commands.has_permissions(manage_channels=True)
async def n(ctx, channel_name):
    channel_id = int(''.join(i for i in channel_name if i.isdigit())) 
    existing_channel = client.get_channel(channel_id)
    if existing_channel:
        await existing_channel.delete()
        clone_channel = await existing_channel.clone(reason="Has been nuked")
        
        embed = discord.Embed(title="Nuked", description=f"This channel was nuked by {ctx.author.mention}", color=ctx.author.color)
        embed.add_field(name="New channel ID:", value=f"`{clone_channel.id}`")
        await clone_channel.send(embed=embed)
    else:
        await ctx.send(f'No channel named **{channel_name}** was found')

@client.command(aliases=["c"])
@commands.has_permissions(manage_channels=True)
async def clone(ctx, channel_name):
    channel_id = int(''.join(i for i in channel_name if i.isdigit())) 
    existing_channel = client.get_channel(channel_id)
    if existing_channel:
        clone_channel = await existing_channel.clone(reason="Has been cloned")
        
        embed = discord.Embed(title="Cloned", description=f"This channel was cloned by {ctx.author.mention}", color=ctx.author.color)
        embed.add_field(name="channel ID:", value=f"`{clone_channel.id}`")
        c = await clone_channel.send(embed=embed)

        d = discord.Embed(description=f"{channel_name} was cloned [jump to channel]({c.jump_url})", color=ctx.author.color)
        await ctx.channel.send(embed=d)
    else:
        await ctx.send(f'No channel named **{channel_name}** was found')


@n.error
async def n_error(ctx, error):
  print(error)
  if isinstance(error, commands.MissingPermissions):
    v = await ctx.send(f"{ctx.author.mention} looks like you don't have permission to use this command. contact {ctx.guild.name} admins")
    await asyncio.sleep(4)
    await v.delete()
  if isinstance(error, commands.MissingRequiredArgument):
    m = await ctx.send(f"{ctx.author.mention} please mention a channel to nuke")
    await asyncio.sleep(3)
    await m.delete()

@clone.error
async def clone_error(ctx, error):
  print(error)
  if isinstance(error, commands.MissingPermissions):
    v = await ctx.send(f"{ctx.author.mention} looks like you don't have permission to use this command. contact {ctx.guild.name} admins")
    await asyncio.sleep(4)
    await v.delete()
  if isinstance(error, commands.MissingRequiredArgument):
    m = await ctx.send(f"{ctx.author.mention} please mention a channel to clone")
    await asyncio.sleep(3)
    await m.delete()




#client.run





client.run("ODU1NDQzMjc1NjU4MTY2Mjgy.YMyjog.T_9PQpggBRcXz2gA2Hnkm3OHFOA")
