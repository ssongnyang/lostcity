import discord
from discord import ui, app_commands
from discord.ext import commands

class LostCityGame:
    pass

class LostCityGameManager:
    pass

class LostCity(commands.Cog):
    games: dict[int, LostCityGameManager] = {}
    embed_color = 0x000000

    def end_game(self, id: int):
        del(self.games[id])

    def __init__(self, bot):
        self.bot = bot

    