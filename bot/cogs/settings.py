import discord
from discord import app_commands
from discord.ext import commands
import logging
from database import Database
from config import *


class Settings(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = Database(DATABASE_PATH)

        self.logger = logging.getLogger('discord.cog.settings')

    @app_commands.command(description='Set a channel for Wattpad notifications.')
    async def set_notification_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        if self.db.check_guild_exists(interaction.guild.id):
            self.db.set_notification_channel(interaction.guild.id, channel.id)

            await interaction.response.send_message(
                f'Set {channel.mention} as the notification channel for Wattpad.'
            )

            self.logger.info(
                f'Guilds id: {interaction.guild.id} has set the notification channel to channel id: {channel.id}'
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Settings(bot), guilds=bot.guilds)
