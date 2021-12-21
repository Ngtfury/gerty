from time import time
import discord
import discord_components
from discord_components import *
from discord.ext import commands
from discord.ext.commands import Context
import parsedatetime as pdt
import asyncio
import datetime



class TimeConverter:
    def convert(argument):
        cal = pdt.Calendar(version=pdt.VERSION_CONTEXT_STYLE)

        dt = cal.parseDT(str(argument))[0]
        timestamp = int(dt.timestamp())
        return timestamp


class Reminder:
    def __init__(self, ctx: Context, timestamp, reason):
        self.ctx = ctx
        self.timestamp = timestamp
        self.reason = reason

    @property
    def ctx(self):
        return self.ctx

    @property
    def timestamp(self):
        return self.timestamp

    @property
    def seconds(self):
        return int(datetime.datetime.now().timestamp()) - self.timestamp

    @property
    def reason(self):
        return self.reason

def setup(bot):
    bot.add_cog(ReminderCog(bot))

class ReminderCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._task = bot.loop.create_task(self.dispatch_reminders())

    def add_reminder(self, reminder: Reminder):
        try:
            self.bot.reminder[reminder.ctx.author.id]
        except:
            self.bot.reminder[reminder.ctx.author.id] = []

        self.bot.reminder[reminder.ctx.author.id].append(reminder)

    def remove_reminder(self, reminder: Reminder):
        self.bot.reminder[reminder.ctx.author.id].remove(reminder)

    async def call_reminder(self, reminder: Reminder):
        self.remove_reminder(reminder)
        offset = f'<t:{reminder.timestamp}:R>'
        await reminder.ctx.send(f'{reminder.ctx.author.mention}, {offset}: {reminder.reason}', components=[Button(style=ButtonStyle.URL, label='Go to message', url=f'{reminder.ctx.message.jump_url}')])
        return


    async def wait_for_short_reminder(self, reminder: Reminder):
        await asyncio.sleep(reminder.seconds)
        await self.call_reminder(reminder)
        return


    async def dispatch_reminders(self):
        try:
            while not self.bot.is_closed():
                for reminder in self.bot.reminder.items():
                    for timer in reminder[1]:
                        if timer.timestamp >= int(datetime.datetime.now().timestamp()):
                            await asyncio.sleep(timer.seconds)
                        await self.call_reminder(timer)
        except:
            self._task.cancel()
            self._task = self.bot.loop.create_task(self.dispatch_reminders())


    @commands.command()
    @commands.is_owner()
    async def remind(self, ctx, time, reason):
        timestamp = TimeConverter.convert(time)
        reminder = Reminder(ctx, timestamp, reason)
        self.add_reminder(reminder)

        await ctx.send(
            f"""Alright, {ctx.author.mention} <t:{timestamp}:R>: {reason}"""
        )
        return
