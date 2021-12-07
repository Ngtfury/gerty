import asyncio
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


class GithubRepo:
    def __init__(self, repo:str):
        self.repo = repo

    async def search_repo(self):
        async with aiohttp.ClientSession() as session:
            headers = {'Authorization': f'token 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'}
            async with session.get(f'https://api.github.com/repos/{self.repo}', headers=headers) as response:
                return await response.json()


    @property
    async def forks(self):
        async with aiohttp.ClientSession() as session:
            headers = {'Authorization': f'token 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'}
            async with session.get(f'https://api.github.com/repos/{self.repo}/forks', headers=headers) as response:
                return len(await response.json())




class GithubApi(commands.Cog):
    def __init__(self, bot):
        self.bot=bot



    async def get_repos(self, username:str):
        async with aiohttp.ClientSession() as session:
            headers = {'Authorization': f'token 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'}
            async with session.get(f'https://api.github.com/users/{username}/repos', headers=headers) as response:
                return await response.json()


    async def get_user(self, username: str):
        async with aiohttp.ClientSession() as session:
            headers = {'Authorization': f'token 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'}
            async with session.get(f'https://api.github.com/users/{username}', headers=headers) as response:
                return await response.json()



    
    @commands.command(brief='util', description='Get evety info of a user who is on github', usage='[username]')
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
            MainEmbed.description = f'<:description:917691689152438312> {_user_bio}'
        MainEmbed.add_field(name='<:plus:917468380846497904> Followers', value=f'> {_user_followers}', inline=False)
        MainEmbed.add_field(name='<:minus:917468380947177573> Following', value=f'> {_user_following}', inline=False)
        MainEmbed.add_field(name='<:codefork:917466548577374298> Public repositories', value=f'> {_user_public_repos}', inline=False)
        if _user_location:
            MainEmbed.add_field(name='<:location:917466382067699732> Location', value=f'> {_user_location}', inline=False)
        MainEmbed.add_field(name='<:account:917467039176720524> Created at', value=f'> <t:{_user_account_created_at}:D> (<t:{_user_account_created_at}:R>)', inline=False)
        MainEmbed.add_field(name='<:cog:917467039201886258> Last updated at', value=f'> <t:{_user_account_updated_at}:D> (<t:{_user_account_updated_at}:R>)', inline=False)
        
        if _user_public_repos <= 0:
            await ctx.send(embed=MainEmbed, components=[Select(placeholder=f'There are no repositories for {_user_name}', disabled=True, options=[SelectOption(label='No', value='No')])])
            return


        repo_json_object = await self.get_repos(username)

        options = []
        count = 0
        for repo in repo_json_object:
            if count >= 25:
                break
            _repo_name_basic = repo['full_name']
            if repo['fork']:
                _repo_name = f'{_repo_name_basic} (forked)'
            else:
                _repo_name = _repo_name_basic
            _repo_desc = repo['description'][:100] if repo['description'] else None
            options.append(SelectOption(label=f'{_repo_name}', value=f'{_repo_name_basic}', emoji=self.bot.get_emoji(917465967808901121), description=_repo_desc))
            count +=1

        components=[[Button(label='Home', emoji=self.bot.get_emoji(917691688984670239), id='GoBackHomeGithub'), Button(style=ButtonStyle.URL, label='Github', url=f'{_user_htmlurl}', emoji=self.bot.get_emoji(917691688984670240)), Button(label='Quit', emoji=self.bot.get_emoji(890938576563503114), id='QuitGithub')], [
            Select(placeholder=f'Select first 25 repositories of {_user_name}', options=options)
        ]]

        HomeCompo=[[Button(label='Home', emoji=self.bot.get_emoji(917691688984670239), id='GoBackHomeGithub', disabled=True), Button(style=ButtonStyle.URL, label='Github', url=f'{_user_htmlurl}', emoji=self.bot.get_emoji(917691688984670240)), Button(label='Quit', emoji=self.bot.get_emoji(890938576563503114), id='QuitGithub')], [
            Select(placeholder=f'Select first 25 repositories of {_user_name}', options=options)
        ]]


        MainMessage = await ctx.send(embed=MainEmbed, components=HomeCompo)

        while True:
            try:
                event = await self.bot.wait_for('interaction', check=lambda i: i.author == ctx.author and i.channel == ctx.channel and i.message == MainMessage, timeout=30)
                
                if isinstance(event.component, Select):
                    await event.respond(type=6)
                    value = event.values[0]

                    repo_search_object = await GithubRepo(str(value)).search_repo()
                    _repo_html_url = repo_search_object['html_url']
                    _repo_description = repo_search_object['description']
                    _repo_isForked = repo_search_object['fork']
                    _repo_forks = repo_search_object['forks_count'] if repo_search_object['forks_count'] else None
                    _repo_fullname = repo_search_object['full_name']
                    _repo_name = _repo_fullname if not _repo_isForked else f'{_repo_fullname} (forked)'
                    _repo_created_at = int(datetime.fromisoformat(repo_search_object['created_at'][:-1]).timestamp())
                    _repo_updated_at = int(datetime.fromisoformat(repo_search_object['updated_at'][:-1]).timestamp())
                    _repo_pushed_at = int(datetime.fromisoformat(repo_search_object['pushed_at'][:-1]).timestamp())
                    _repo_clone_url = repo_search_object['clone_url']
                    _repo_homepage = repo_search_object['homepage']
                    _repo_stars = repo_search_object['stargazers_count']
                    _repo_language = repo_search_object['language']
                    _repo_archived = 'Yes, archived' if repo_search_object['archived'] else 'Not archived'
                    _repo_disabled = 'Yes, disabled' if repo_search_object['disabled'] else 'Not disabled'
                    _repo_open_issues_count = repo_search_object['open_issues_count']
                    _repo_license = repo_search_object['license']['name'] if repo_search_object['license'] else None
                    _repo_topics = ', '.join(repo_search_object['topics']) if repo_search_object['topics'] else None
                    _repo_default_branch = repo_search_object['default_branch']

                    RepoEmbed = discord.Embed(title=f'<:repo:917465967808901121> {_repo_name}', url=f'{_repo_html_url}',color=Utils.BotColors.invis())
                    RepoEmbed.set_author(name=_user_name, icon_url=_user_avatar_url, url=_user_htmlurl)
                    if _repo_description:
                        RepoEmbed.description = f'<:description:917691689152438312> {_repo_description}'
                    RepoEmbed.add_field(name='<:plus:917468380846497904> Created at', value=f'<t:{_repo_created_at}:D> (<t:{_repo_created_at}:R>)')
                    RepoEmbed.add_field(name=f'<:cog:917467039201886258> Updated at', value=f'<t:{_repo_updated_at}:D> (<t:{_repo_updated_at}:R>)')
                    RepoEmbed.add_field(name='<:repo2:917691689060139048> Pushed at', value=f'<t:{_repo_pushed_at}:D> (<t:{_repo_pushed_at}:R>)')
                    RepoEmbed.add_field(name='<:copy:917691689051758652> Clone URL', value=f'[Copy clone URL]({_repo_clone_url})')
                    if _repo_homepage:
                        RepoEmbed.add_field(name='<:home:917691688984670239> Homepage', value=f'[Copy homepage URL]({_repo_homepage})')
                    RepoEmbed.add_field(name='<:star:917691689278251048> Stars', value=_repo_stars)
                    if _repo_forks:
                        RepoEmbed.add_field(name='<:codefork:917466548577374298> Forks', value=_repo_forks, inline=False)
                    if _repo_language:
                        RepoEmbed.add_field(name='<:code:917691688963698718> Language', value=_repo_language)
                    RepoEmbed.add_field(name='<:archive:917691688980467762> Archived', value=_repo_archived)
                    RepoEmbed.add_field(name='<:cross:917691689060139028> Disabled', value=_repo_disabled)
                    RepoEmbed.add_field(name='<:issue:917691689236324362> Issues', value=_repo_open_issues_count)
                    if _repo_license:
                        RepoEmbed.add_field(name='<:creative:917691688997257266> License', value=_repo_license)
                    if _repo_topics:
                        RepoEmbed.add_field(name='<:github:917691688984670240> Topics', value=_repo_topics)
                    RepoEmbed.add_field(name='<:gitbranch:917691689102094377> Default branch', value=_repo_default_branch)

                    await event.respond(type=7, embed=RepoEmbed, components=components)

                elif isinstance(event.component, Button):
                    if event.component.id=='GoBackHomeGithub':
                        await event.respond(type=7, embed=MainEmbed, components=HomeCompo)
                    elif event.component.id == 'QuitGithub':
                        await MainMessage.delete()
                        await ctx.message.add_reaction(Utils.BotEmojis.success())
                        break

            except asyncio.TimeoutError:
                await MainMessage.disable_components()
                break


