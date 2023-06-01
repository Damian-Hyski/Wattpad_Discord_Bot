import logging
import os
import discord
from discord.ext import commands
from database import Database
from config import *


class Basic(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger('discord.cog.basic')
        self.db = Database(DATABASE_PATH)

    @commands.Cog.listener()
    async def on_ready(self):
        for name in os.listdir('bot/cogs'):
            if name.endswith('.py') and name != '__init__.py':
                await self.bot.reload_extension('cogs.{}'.format(name[:-3]))

        for guild in self.bot.guilds:
            await self.bot.tree.sync(guild=guild)

            if not self.db.check_guild_exists(guild.id):
                self.db.add_guild(guild.id)
                self.logger.info(f"The bot has joined a new guild: {guild.name} ({guild.id})")

        self.logger.info(f'We have logged in as {self.bot.user}')

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        for name in os.listdir('bot/cogs'):
            if name.endswith('.py') and name != '__init__.py':
                await self.bot.reload_extension('cogs.{}'.format(name[:-3]))

        await self.bot.tree.sync(guild=guild)

        if not self.db.check_guild_exists(guild.id):
            self.db.add_guild(guild.id)
            self.logger.info(f"The bot has joined a new guild: {guild.name} ({guild.id})")


async def setup(bot: commands.Bot):
    await bot.add_cog(Basic(bot), guilds=bot.guilds)
