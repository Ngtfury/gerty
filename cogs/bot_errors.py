import discord
from discord.ext import commands



class UserBlacklisted(commands.CheckFailure):
  def __init__(self, user, reason, *args, **kwargs):
    self.user=user
    self.reason=reason
    super().__init__(*args, **kwargs)


class DisabledCommand(commands.CheckFailure):
  pass