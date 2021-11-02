import datetime
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


    async def get_user_tags(self, user_id, guild_id):
        tag=await self.bot.db.fetch('SELECT name FROM tags WHERE user_id=$1 AND guild_id=$2', user_id, guild_id)
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
        is_tag=await self.get_tag(name=f'{tag}', guild_id=ctx.guild.id)
        if is_tag:
            content=is_tag['content']
            if ctx.message.reference:
                return await ctx.message.reference.resolved.reply(f'{content}')
            else:
                return await ctx.send(content)
        else:
            em=discord.Embed(description=f'<:error:893501396161290320>  Tag named `{tag}` does not exist in this server', color=0x2F3136)
            return await ctx.send(embed=em)
    
    @tag.command(aliases=['make'])
    async def create(self, ctx, name:str, *, content:commands.clean_content):
        await self.create_tag(ctx=ctx, name=name, content=content, guild_id=ctx.guild.id, owner_id=ctx.author.id)


    @tag.command(aliases=['del'])
    async def delete(self, ctx, *, name:str):
        tag=await self.get_tag(name=name, guild_id=ctx.guild.id)
        if not tag:
            em=discord.Embed(description=f'<:error:893501396161290320>  Tag named `{name}` does not exists', color=0x2F3136)
            return await ctx.send(embed=em)
        if tag['owner_id'] == ctx.author.id:
            await self.bot.db.execute('DELETE FROM tags WHERE name=$1', name)
            em=discord.Embed(description=f'<:success:893501515107557466> Tag `{name}` deleted successfully', color=0x2F3136)
            await ctx.send(embed=em)
        else:
            em=discord.Embed(description=f'<:error:893501396161290320> Tag `{name}` is not owned by you', color=0x2F3136)
            await ctx.send(embed=em)

    @tag.command()
    async def edit(self, ctx, name:str, *, content):
        is_tag=await self.get_tag(name=name, guild_id=ctx.guild.id)
        if not is_tag:
            em=discord.Embed(description=f'<:error:893501396161290320>  Tag named `{name}` does not exists', color=0x2F3136)
            return await ctx.send(embed=em)
        elif is_tag['owner_id']==ctx.author.id:
            await self.bot.db.execute('UPDATE tags SET content=$1 WHERE name=$2', content, name)
            em=discord.Embed(description=f'<:success:893501515107557466> Tag `{name}` edited successfully', color=0x2F3136)
            await ctx.send(embed=em)
        else:
            em=discord.Embed(description=f'<:error:893501396161290320> Tag `{name}` is not owned by you', color=0x2F3136)
            await ctx.send(embed=em)


    @commands.command()
    async def tags(self, ctx, member: discord.Member=None):
        if member==None:
            member=ctx.author

        tag_list=[]
        tags=await self.get_user_tags(user_id=member.id, guild_id=ctx.guild.id)
        if tags:
            count=0
            for x in tags:
                count=count+1
                tag_list.append(f'{count} {x}')
            em=discord.Embed(title=f'Tags by {member.name} in {ctx.guild.name}', description='\n'.join(tag_list),color=0x2F3136)
            await ctx.send(embed=em)