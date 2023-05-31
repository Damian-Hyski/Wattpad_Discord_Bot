import os
import aiohttp
import discord
from discord.ext import commands
from config import *


class WattpadDiscordBot(commands.Bot):
    def __init__(self):
        super(WattpadDiscordBot, self).__init__(
            command_prefix='!',
            help_command=None,
            intents=discord.Intents.all()
        )

        self.session = None

    async def setup_hook(self) -> None:
        self.session = aiohttp.ClientSession()

        for name in os.listdir('./cogs'):
            if name.endswith('.py') and name != '__init__.py':
                await self.load_extension('cogs.{}'.format(name[:-3]))

        for guild in bot.guilds:
            await bot.tree.sync(guild=guild)

    async def close(self) -> None:
        await self.session.close()
        await super(WattpadDiscordBot, self).close()


if __name__ == '__main__':
    bot = WattpadDiscordBot()
    bot.run(DC_TOKEN)
