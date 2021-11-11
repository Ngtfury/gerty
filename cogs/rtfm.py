import aiohttp
import discord
from discord.ext import commands
import functools
import io
import json
import os
import re
import urllib
import zlib
from inspect import Parameter
import typing
import yarl

from cogs.utils import GertyHelpCommand


def setup(client):
    client.add_cog(Rtfm(client))


def finder(text, collection, *, key=None, lazy=True):
    suggestions = []
    text = str(text)
    pat = '.*?'.join(map(re.escape, text))
    regex = re.compile(pat, flags=re.IGNORECASE)
    for item in collection:
        to_search = key(item) if key else item
        r = regex.search(to_search)
        if r:
            suggestions.append((len(r.group()), r.start(), item))

    def sort_key(tup):
        if key:
            return tup[0], tup[1], key(tup[2])
        return tup

    if lazy:
        return (z for _, _, z in sorted(suggestions, key=sort_key))
    else:
        return [z for _, _, z in sorted(suggestions, key=sort_key)]


class SphinxObjectFileReader:
    # Inspired by Sphinx's InventoryFileReader
    BUFSIZE = 16 * 1024

    def __init__(self, buffer):
        self.stream = io.BytesIO(buffer)

    def readline(self):
        return self.stream.readline().decode('utf-8')

    def skipline(self):
        self.stream.readline()

    def read_compressed_chunks(self):
        decompressor = zlib.decompressobj()
        while True:
            chunk = self.stream.read(self.BUFSIZE)
            if len(chunk) == 0:
                break
            yield decompressor.decompress(chunk)
        yield decompressor.flush()

    def read_compressed_lines(self):
        buf = b''
        for chunk in self.read_compressed_chunks():
            buf += chunk
            pos = buf.find(b'\n')
            while pos != -1:
                yield buf[:pos].decode('utf-8')
                buf = buf[pos + 1:]
                pos = buf.find(b'\n')




class Rtfm(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    async def build_rtfm_lookup_table(self, page_types):
        cache = {}
        for key, page in page_types.items():
            sub = cache[key] = {}
            async with aiohttp.ClientSession().get(page + '/objects.inv') as resp:
                if resp.status != 200:
                    channel = self.bot.get_channel(880181130408636456)
                    await channel.send(f'```py\nCould not create RTFM lookup table for {page}\n```')
                    continue

                stream = SphinxObjectFileReader(await resp.read())
                cache[key] = self.parse_object_inv(stream, page)

        self._rtfm_cache = cache

    def parse_object_inv(self, stream, url):
        # key: URL
        # n.b.: key doesn't have `discord` or `discord.ext.commands` namespaces
        result = {}

        # first line is version info
        inv_version = stream.readline().rstrip()

        if inv_version != '# Sphinx inventory version 2':
            raise RuntimeError('Invalid objects.inv file version.')

        # next line is "# Project: <name>"
        # then after that is "# Version: <version>"
        projname = stream.readline().rstrip()[11:]
        version = stream.readline().rstrip()[11:]

        # next line says if it's a zlib header
        line = stream.readline()
        if 'zlib' not in line:
            raise RuntimeError('Invalid objects.inv file, not z-lib compatible.')

        # This code mostly comes from the Sphinx repository.
        entry_regex = re.compile(r'(?x)(.+?)\s+(\S*:\S*)\s+(-?\d+)\s+(\S+)\s+(.*)')
        for line in stream.read_compressed_lines():
            match = entry_regex.match(line.rstrip())
            if not match:
                continue

            name, directive, prio, location, dispname = match.groups()
            domain, _, subdirective = directive.partition(':')
            if directive == 'py:module' and name in result:
                # From the Sphinx Repository:
                # due to a bug in 1.1 and below,
                # two inventory entries are created
                # for Python modules, and the first
                # one is correct
                continue

            # Most documentation pages have a label
            if directive == 'std:doc':
                subdirective = 'label'

            if location.endswith('$'):
                location = location[:-1] + name

            key = name if dispname == '-' else dispname
            prefix = f'{subdirective}:' if domain == 'std' else ''

            if projname == 'discord.py':
                key = key.replace('discord.ext.commands.', '').replace('discord.', '')

            result[f'{prefix}{key}'] = os.path.join(url, location)

        return result

    async def do_rtfm(self, ctx, key, obj):
        page_types = {
            'latest': 'https://discordpy.readthedocs.io/en/latest',
            'latest-jp': 'https://discordpy.readthedocs.io/ja/latest',
            'python': 'https://docs.python.org/3',
            'python-jp': 'https://docs.python.org/ja/3',
            'master': 'https://discordpy.readthedocs.io/en/master',
            'edpy': 'https://enhanced-dpy.readthedocs.io/en/latest',
            'chai': 'https://chaidiscordpy.readthedocs.io/en/latest',
            'bing': 'https://asyncbing.readthedocs.io/en/latest',
            'pycord': 'https://pycord.readthedocs.io/en/master',
            'aiohttp': 'https://aiohttp.readthedocs.io/en/latest/'
        }
        embed_titles = {
            'latest': 'Documentation for discord.py v1.7.3',
            'latest-jp': 'Documentation for discord.py v1.7.3 in Japanese',
            'python': 'Documentation for python',
            'python-jp': 'Documentation for python in Japanese',
            'master': 'Documentation for discord.py v2.0.0a',
            'edpy': 'Documentation for enhanced-dpy',
            'chai': 'Documentation for chaidiscord.py',
            'bing': 'Documentation for asyncbing',
            'pycord': 'Documentation for pycord',
            'aiohttp': 'Documentation for aiohttp'
        }

        if obj is None:
            await ctx.send(page_types[key])
            return

        if not hasattr(self, '_rtfm_cache'):
            await ctx.trigger_typing()
            await self.build_rtfm_lookup_table(page_types)

        obj = re.sub(r'^(?:discord\.(?:ext\.)?)?(?:commands\.)?(.+)', r'\1', obj)

        if key.startswith('latest'):
            # point the abc.Messageable types properly:
            q = obj.lower()
            for name in dir(discord.abc.Messageable):
                if name[0] == '_':
                    continue
                if q == name:
                    obj = f'abc.Messageable.{name}'
                    break

        cache = list(self._rtfm_cache[key].items())

        matches = finder(obj, cache, key=lambda t: t[0], lazy=False)[:8]

        e = discord.Embed(colour=discord.Colour.blurple())
        e.set_author(name=embed_titles.get(key, 'Documentation'))
        if len(matches) == 0:
            return await ctx.send('Could not find anything. Sorry.')

        e.description = '\n'.join(f'[`{key}`]({url})' for key, url in matches)
        await ctx.send(embed=e)

    @commands.command(brief='rtfm', description='Gives you a documentation link according your query', aliases=['rtfd', 'rtdm'], invoke_without_command=True)
    async def rtfm(self, ctx):
        return await GertyHelpCommand(self.bot).send_command_help(ctx, command='rtfm')

    @rtfm.command(brief='rtfm', description="Gives you a documentation link for a discord.py entity.", usage='[query]', aliases=['dpy', 'discord.py'])
    async def rtfm_dpy(self, ctx, *, obj: str = None):
        await self.do_rtfm(ctx, 'latest', obj)

    @rtfm.command(brief='rtfm', description="""Gives you a documentation link for a discord.py entity (Japanese).""", usage='[query]', name='jp')
    async def rtfm_jp(self, ctx, *, obj: str = None):
        await self.do_rtfm(ctx, 'latest-jp', obj)

    @rtfm.command(brief='rtfm', description="""Gives you a documentation link for a Python entity.""", name='python', aliases=['py'], usage='[query]')
    async def rtfm_python(self, ctx, *, obj: str = None):
        await self.do_rtfm(ctx, 'python', obj)

    @rtfm.command(description='Gives you a documentation link for a Python entity (Japanese)', usage='[query]', name='py-jp', aliases=['py-ja'])
    async def rtfm_python_jp(self, ctx, *, obj: str = None):
        await self.do_rtfm(ctx, 'python-jp', obj)

    @rtfm.command(description='Gives you a documentation link for a discord.py entity (master branch)', usage='[query]', name='dpy-master', aliases=['dpy-2.0'])
    async def rtfm_master(self, ctx, *, obj: str = None):
        await self.do_rtfm(ctx, 'master', obj)

    @rtfm.command(description='Gives you a documentation link for a enhanced-discord.pu entity', usage='[query]', name='enhanced-dpy', aliases=['edpy'])
    async def rtfm_edpy(self, ctx, *, obj: str = None):
        await self.do_rtfm(ctx, 'edpy', obj)

    @rtfm.command( description='Gives you a documentation link for a asyncbing entity', usage='[query]', name='asyncbing', aliases=['bing'])
    async def rtfm_asyncbing(self, ctx, *, obj: str = None):
        await self.do_rtfm(ctx, 'bing', obj)

    @rtfm.command(description='Gives you a documentation link for a chaidiscord.py entity', usage='[query]', name='chaidiscordpy', aliases=['chaidpy', 'cdpy'])
    async def rtfm_chai(self, ctx, *, obj: str = None):
        await self.do_rtfm(ctx, 'chai', obj)

    @rtfm.command(name='pycord', description='Gives you a documentation link for a pycord entity', usage='[query]')
    async def rtfm_pycord(self, ctx, *, obj: str = None):
        await self.do_rtfm(ctx, 'pycord', obj)


    @rtfm.command(name='aiohttp', description='Gives you a documentation link for a aiohttp entity')
    async def rtfm_aiohttp(self, ctx, *, obj:str=None):
        await self.do_rtfm(ctx, 'aiohttp', obj)

