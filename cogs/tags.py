from datetime import datetime
import discord
from discord.ext import commands

def setup(client):
    client.add_cog(Tags(client))


class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot=bot


    async def get_tag(self, name:str, guild_id):
        tag=await self.bot.db.fetchrow('SELECT * FROM tags WHERE guild_id=$1 AND name=$2', guild_id, name)
        return tag

    async def create_tag(self, ctx, name:str, content:str, guild_id, owner_id):
        root = self.bot.get_command('tag')
        if name in root.all_commands:
            NoMbed=discord.Embed(description='<:error:893501396161290320> This tag name starts with a reserved word', color=0x2F3136)
            return await ctx.send(embed=NoMbed)

        already_exsits=await self.get_tag(name=name, guild_id=guild_id)
        if already_exsits:
            em=discord.Embed(description=f'<:error:893501396161290320> Tag named `{name}` already exists', color=0x2F3136)
            return await ctx.send(embed=em)
        else:
            await self.bot.db.execute('INSERT INTO tags (name,content,guild_id,owner_id,created_at,tag_uses) VALUES ($1,$2,$3,$4,$5,$6)', name, content, guild_id, owner_id, int(datetime.datetime.now().timestamp()), 0)
            em=discord.Embed(description=f'<:success:893501515107557466> Tag `{name}` succesfully created', color=0x2F3136)
            await ctx.send(embed=em)

    @commands.group(invoke_without_command=True)
    async def tag(self, ctx, *, tag):
        tag=await self.get_tag(name=f'{tag}', guild_id=ctx.guild.id)
        if tag:
            content=tag['content']
            return await ctx.send(f'{content}')
        else:
            return await ctx.send(f'Tag named `{tag}` does not exists')
    
    @tag.command(aliases=['make'])
    async def create(self, ctx, name:str, *, content:commands.clean_content):
        await self.create_tag(ctx=ctx, name=name, content=content, guild_id=ctx.guild.id, owner_id=ctx.author.id)