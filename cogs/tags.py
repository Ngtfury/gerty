import datetime
import discord
from discord.ext import commands

from cogs.utils import GertyHelpCommand

def setup(client):
    client.add_cog(Tags(client))


class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot=bot


    async def get_tag(self, name:str, guild_id):
        tag=await self.bot.db.fetchrow('SELECT * FROM tags WHERE guild_id=$1 AND name=$2', guild_id, name)
        return tag


    async def get_user_tags(self, user_id, guild_id):
        tag=await self.bot.db.fetch('SELECT name FROM tags WHERE owner_id=$1 AND guild_id=$2', user_id, guild_id)
        return tag

    async def create_tag(self, ctx, name:str, content:str, guild_id, owner_id):
        if len(name) > 100:
            em=discord.Embed(description='<:error:893501396161290320> Tag name is a maximum of 100 characters', color=0x2F3136)
            return await ctx.send(embed=em)
        if len(content) > 2000:
            em=discord.Embed(description='<:error:893501396161290320> Tag content is a maximum of 2000 characters', color=0x2F3136)
            return await ctx.send(embed=em)
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

    @commands.group(brief='tags', description='Retrieves a tag with the given name', usage='[name]', invoke_without_command=True)
    async def tag(self, ctx, *, tag):
        is_tag=await self.get_tag(name=f'{tag}', guild_id=ctx.guild.id)
        if is_tag:
            content=is_tag['content']
            if ctx.message.reference:
                await ctx.message.reference.resolved.reply(f'{content}')
            else:
                await ctx.send(content)
            await self.bot.db.execute('UPDATE tags SET tag_uses=$1 WHERE name=$2 AND guild_id=$3', is_tag['tag_uses']+1, tag, ctx.guild.id)
        else:
            em=discord.Embed(description=f'<:error:893501396161290320>  Tag named `{tag}` does not exist in this server', color=0x2F3136)
            return await ctx.send(embed=em)
    
    @tag.command(brief='tags', description='Creates a tag', usage='[name] [content]', aliases=['make'])
    async def create(self, ctx, name:str, *, content:commands.clean_content):
        await self.create_tag(ctx=ctx, name=name, content=content, guild_id=ctx.guild.id, owner_id=ctx.author.id)



    @tag.command(brief='tags', description='Deletes a tag with the given name', usage='[name]', aliases=['del'])
    async def delete(self, ctx, *, name:str):
        tag=await self.get_tag(name=name, guild_id=ctx.guild.id)
        if not tag:
            em=discord.Embed(description=f'<:error:893501396161290320>  Tag named `{name}` does not exists', color=0x2F3136)
            return await ctx.send(embed=em)
        if tag['owner_id'] == ctx.author.id:
            await self.bot.db.execute('DELETE FROM tags WHERE name=$1 AND guild_id=$2', name, ctx.guild.id)
            em=discord.Embed(description=f'<:success:893501515107557466> Tag `{name}` deleted successfully', color=0x2F3136)
            await ctx.send(embed=em)
        else:
            em=discord.Embed(description=f'<:error:893501396161290320> Tag `{name}` is not owned by you', color=0x2F3136)
            await ctx.send(embed=em)



    @tag.command(brief='tags', description='Transfers the tag ownership', usage='[user] [name]')
    async def transfer(self, ctx, member: discord.Member, *, name):
        if member.bot:
            return await ctx.send('You cannot transfer tag to a bot')

        is_tag=await self.get_tag(name=name, guild_id=ctx.guild.id)
        if not is_tag:
            em=discord.Embed(description=f'<:error:893501396161290320>  Tag named `{name}` does not exists', color=0x2F3136)
            return await ctx.send(embed=em)
        elif is_tag['owner_id']==ctx.author.id:
            await self.bot.db.execute('UPDATE tags SET owner_id=$1 WHERE name=$2 AND guild_id=$3', member.id, name, ctx.guild.id)  
            em=discord.Embed(description=f'<:success:893501515107557466> Tag `{name}` transfered successfully to {member.mention}', color=0x2F3136)
            await ctx.send(embed=em)
        else:
            em=discord.Embed(description=f'<:error:893501396161290320> Tag `{name}` is not owned by you', color=0x2F3136)
            await ctx.send(embed=em)



    @tag.command(brief='tags', description='Edits the tag with the given name to given content', usage='[name] [content]')
    async def edit(self, ctx, name:str, *, content:commands.clean_content):
        is_tag=await self.get_tag(name=name, guild_id=ctx.guild.id)
        if not is_tag:
            em=discord.Embed(description=f'<:error:893501396161290320>  Tag named `{name}` does not exists', color=0x2F3136)
            return await ctx.send(embed=em)
        elif is_tag['owner_id']==ctx.author.id:
            await self.bot.db.execute('UPDATE tags SET content=$1 WHERE name=$2 AND guild_id=$3', content, name, ctx.guild.id)
            em=discord.Embed(description=f'<:success:893501515107557466> Tag `{name}` edited successfully', color=0x2F3136)
            await ctx.send(embed=em)
        else:
            em=discord.Embed(description=f'<:error:893501396161290320> Tag `{name}` is not owned by you', color=0x2F3136)
            await ctx.send(embed=em)

    @tag.command(brief='tags', description='Gets the stats of the tag with given name', usage='[name]')
    async def info(self, ctx, *, tag):
        is_tag=await self.get_tag(name=tag, guild_id=ctx.guild.id)
        if not is_tag:
            em=discord.Embed(description=f'<:error:893501396161290320>  Tag named `{tag}` does not exist in this server', color=0x2F3136)
            return await ctx.send(embed=em)
        owner=ctx.guild.get_member(is_tag['owner_id'])
        time=is_tag['created_at']
        uses=is_tag['tag_uses']
        embed=discord.Embed(description=f'**Owner**: {owner.name}/{owner.mention}\n**Created at**: <t:{time}>/<t:{time}:R>\n**Uses**: {uses}', color=0x2F3136)
        embed.set_author(name=f'Info - {tag}', icon_url=owner.avatar.url)
        embed.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)


    @commands.command(brief='tags', description='Shows your/users tags in current server', usage='(member)')
    async def tags(self, ctx, member: discord.Member=None):
        if member==None:
            member=ctx.author

        tag_list=[]
        tags=await self.get_user_tags(user_id=member.id, guild_id=ctx.guild.id)
        if tags:
            count=0
            for x in tags:
                name=x['name']
                count=count+1
                tag_list.append(f'{count}. {name}')
            em=discord.Embed(description='\n'.join(tag_list),color=0x2F3136)
            em.set_footer(text=f'Do “tag info [name]“ or “tag [name]“')
            em.set_author(name=f'Tags by {member.name} in {ctx.guild.name}', icon_url=member.avatar.url)
            await ctx.send(embed=em)
        else:
            await ctx.send(f'{member.name} does not have any tags in this server')


    @commands.Cog.listener('on_guild_remove')
    async def tag_cleanup_on_leave(self, guild):
        await self.bot.db.execute('DELETE FROM tags WHERE guild_id=$1', guild.id)