import json
import re
import discord
import datetime
from discord.ext import commands
import aiohttp
from datetime import datetime
import discord_components
from discord_components import *
from cogs.utils import Utils, GertyHelpCommand


def setup(bot):
    bot.add_cog(GithubApi(bot))



class GithubApi(commands.Cog):
    def __init__(self, bot):
        self.bot=bot



    async def get_repos(self, username:str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.github.com/users/{username}/repos') as response:
                return await response.json()


    async def get_user(self, username: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.github.com/users/{username}') as response:
                return await response.json()

    
    @commands.command()
    @commands.is_owner()
    async def github(self, ctx, username: str):
        user_object_json = await self.get_user(username)

        try:
            _user_name = user_object_json['login']
        except KeyError:
            await ctx.send(embed=Utils.BotEmbed.error(f'Sorry, there is no one with name "{username}" on github'))
            return

        _user_avatar_url = user_object_json['avatar_url']
        _user_htmlurl = user_object_json['html_url']
        _user_bio = user_object_json['bio']
        _user_public_repos = user_object_json['public_repos']
        _user_followers = user_object_json['followers']
        _user_following = user_object_json['following']
        _user_location = user_object_json['location']
        _user_account_created_at = int(datetime.fromisoformat(user_object_json['created_at'][:-1]).timestamp())
        _user_account_updated_at = int(datetime.fromisoformat(user_object_json['updated_at'][:-1]).timestamp())

        MainEmbed=discord.Embed(color=Utils.BotColors.invis())
        MainEmbed.set_author(name=_user_name, icon_url=_user_avatar_url, url=_user_htmlurl)
        MainEmbed.set_thumbnail(url='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png')
        if _user_bio:
            MainEmbed.description = _user_bio
        MainEmbed.add_field(name='Followers', value=_user_followers, inline=False)
        MainEmbed.add_field(name='Following', value=_user_following, inline=False)
        MainEmbed.add_field(name='Public repositories', value=_user_public_repos, inline=False)
        if _user_location:
            MainEmbed.add_field(name='Location', value=_user_location, inline=False)
        MainEmbed.add_field(name='Created at', value=f'<t:{_user_account_created_at}:D> (<t:{_user_account_created_at}:R>)', inline=False)
        MainEmbed.add_field(name='Last updated at', value=f'<t:{_user_account_updated_at}:D> (<t:{_user_account_updated_at}:R>)', inline=False)
        
        repo_json_object = await self.get_repos(username)

        options = []
        count = 0
        for repo in repo_json_object:
            if count <= 25:
                break
            _repo_name = repo['full_name']
            options.append(SelectOption(label=f'{_repo_name}', value=f'{_repo_name}'))
            count +=1

        components=[[
            Select(placeholder=f'Select first 25 repositories of {_user_name}', options=options)
        ]]

        await ctx.send(embed=MainEmbed, components=components)


