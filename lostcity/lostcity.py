import discord
from discord import ui, app_commands
from discord.ext import commands

from lostcity.card import Card
from lostcity.player import Player

class LostCityGame:
    def __init__(self, players: list[Player], thread: discord.Thread):
        self.players = players
        self.thread = thread
        self.turn: int = 0

    

class LostCityGameManager:
    scouting: bool = True
    running: bool = False

    def __init__(self, starter: Player):
        self.starter = starter
        self.players: list[Player] = [starter]

        self.thread = None
        self.root_msg = None
    
    

class LostCity(commands.Cog):
    games: dict[int, LostCityGameManager] = {}
    embed_color = 0x000000

    def end_game(self, id: int):
        del(self.games[id])

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="로스트시트", description="새로운 로스트시티 게임을 모집합니다.")
    @app_commands.choices(모드=[
        app_commands.Choice(name='기본', value=0),
        app_commands.Choice(name='확장', value=1),
    ])
    async def scout(self, itc: discord.Interaction, 모드: int):
        id = itc.channel.id
        if id in self.games:
            await itc.response.send_message("이미 모집 중이거나 진행 중인 게임이 있습니다.", ephemeral=True)
            return

        self.games[id] = LostCityGameManager(Player(itc))
