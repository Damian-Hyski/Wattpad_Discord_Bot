import discord
from discord import app_commands
from discord.ext import commands
import logging
from api import WattpadAPI
from database import Database
from config import *
from utils import convert_date_to_int


class Wattpad(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.api = WattpadAPI()
        self.db = Database(DATABASE_PATH)
        self.logger = logging.getLogger('discord.cog.wattpad')

    @app_commands.command(description='Add user to the watchlist.')
    async def add_to_watchlist(self, interaction: discord.Interaction, user: discord.Member, wattpad_name: str):
        if not self.db.check_user_exists(user.id):
            try:
                # get stories
                stories = self.api.get_stories_data(wattpad_name)

                # set user id
                dc_user_id = user.id

                # set wattpad name
                wp_name = wattpad_name

                # set last message date
                if self.api.get_message_data(wattpad_name)[0]['createDate']:
                    wp_last_message_date = convert_date_to_int(self.api.get_message_data(wattpad_name)[0]['createDate'])
                else:
                    wp_last_message_date = 0

                # set number of stories
                wp_number_of_stories = len(stories)

                # set last part date
                wp_last_part_date = 0
                for story in stories:
                    if convert_date_to_int(story['lastPublishedPart']['createDate']) > wp_last_part_date:
                        wp_last_part_date = convert_date_to_int(story['lastPublishedPart']['createDate'])

                # set guild id
                dc_guild_id = interaction.guild.id

                # add to database
                self.db.add_user(dc_user_id, wp_name, wp_last_message_date, wp_number_of_stories, wp_last_part_date)
                self.db.add_relation(dc_user_id, dc_guild_id)

                # send message in discord
                await interaction.response.send_message(
                    f'The user {user.mention} has been added to the list of followed users as **{wattpad_name}** on '
                    f'Wattpad.'
                )
            except TypeError as e:
                self.logger.error(e)

                await interaction.response.send_message(
                    f'Failed to link {user.mention} with **{wattpad_name}** as the user was not found. '
                    f'Please make sure you have entered your Wattpad username correctly.'
                )


async def setup(bot: commands.Bot):
    await bot.add_cog(Wattpad(bot), guilds=bot.guilds)
