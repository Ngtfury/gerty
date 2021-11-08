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
            session = aiohttp.ClientSession()
            async with session.get(page + '/objects.inv') as resp:
                if resp.status != 200:
                    raise RuntimeError('Cannot build rtfm lookup table, try again later.')

                stream = SphinxObjectFileReader(await resp.read())
                cache[key] = self.parse_object_inv(stream, page)
                await session.close()

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
            'edpy': 'https://enhanced-dpy.readthedocs.io/en/latest/',
            'chai': 'https://chaidiscordpy.readthedocs.io/en/latest/',
            'bing': 'https://asyncbing.readthedocs.io/en/latest',
            'pycord': 'https://pycord.readthedocs.io/en/latest/',
            'discord-components': 'https://discord-components.readthedocs.io/en/0.5.2.4/'
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
        if len(matches) == 0:
            return await ctx.send('Could not find anything. Sorry.')

        e.description = '\n'.join(f'[`{key}`]({url})' for key, url in matches)
        await ctx.send(embed=e)

    @commands.group(brief='rtfm', description="""Gives you a documentation link for a discord.py entity.
        Events, objects, and functions are all supported through
a cruddy fuzzy algorithm.""", usage='[query]', aliases=['rtfd', 'rtdm'], invoke_without_command=True)
    async def rtfm(self, ctx, *, obj: str = None):
        await self.do_rtfm(ctx, 'latest', obj)

    @rtfm.command(brief='rtfm', description="""Gives you a documentation link for a discord.py entity (Japanese).""", usage='[query]', name='jp')
    async def rtfm_jp(self, ctx, *, obj: str = None):
        
        await self.do_rtfm(ctx, 'latest-jp', obj)

    @rtfm.command(brief='rtfm', description="""Gives you a documentation link for a Python entity.""", name='python', aliases=['py'])
    async def rtfm_python(self, ctx, *, obj: str = None):
        await self.do_rtfm(ctx, 'python', obj)

    @rtfm.command(name='py-jp', aliases=['py-ja'])
    async def rtfm_python_jp(self, ctx, *, obj: str = None):
        """Gives you a documentation link for a Python entity (Japanese)."""
        await self.do_rtfm(ctx, 'python-jp', obj)

    @rtfm.command(name='master', aliases=['2.0'])
    async def rtfm_master(self, ctx, *, obj: str = None):
        """Gives you a documentation link for a discord.py entity (master branch)"""
        await self.do_rtfm(ctx, 'master', obj)

    @rtfm.command(name='enhanced-dpy', aliases=['edpy'])
    async def rtfm_edpy(self, ctx, *, obj: str = None):
        """Gives you a documentation link for a enhanced-discord.py entity"""
        await self.do_rtfm(ctx, 'edpy', obj)

    @rtfm.command(name='asyncbing', aliases=['bing'])
    async def rtfm_asyncbing(self, ctx, *, obj: str = None):
        """Gives you a documentation link for an asyncbing entity """
        await self.do_rtfm(ctx, 'bing', obj)

    @rtfm.command(name='chaidiscordpy', aliases=['chaidpy', 'cdpy'])
    async def rtfm_chai(self, ctx, *, obj: str = None):
        """Gives you a documentation link for a chaidiscord.py entity"""
        await self.do_rtfm(ctx, 'chai', obj)

    @rtfm.command(name='pycord')
    async def rtfm_pycord(self, ctx, *, obj: str = None):
        """Gives you a documentation link for a pycord entity"""
        await self.do_rtfm(ctx, 'pycord', obj)

    @rtfm.command(name='discord-components', aliases=['dc'])
    async def rtfm_discord_components(self, ctx, *, obj:str=None):
        """"Gives you a documentation link for a discord-components entity"""
        await self.do_rtfm(ctx, 'discord-components', obj)

