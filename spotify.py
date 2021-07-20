import discord
import requests
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw


class Spotify(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def spotify(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        spotify_result = next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)

        if spotify_result is None:
            await ctx.send(f'{user.name} is not listening to Spotify or [He/She] is not connected [her/his] account to discord.')

        await ctx.send(f"{ctx.author.mention} {user.name} is now Playing! <:spotify:861975105227849738> \n > https://open.spotify.com/track/{spotify_result.track_id}")




def setup(client):
    client.add_cog(Spotify(client))
