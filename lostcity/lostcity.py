import discord
from discord import ui, app_commands
from discord.ext import commands

from random import shuffle

from lostcity.card import Card, Color, all_cards
from lostcity.player import Player
from lostcity.log import Log
from lostcity.button import CardSelectButton

class LostCityGame:
    def __init__(self, players: list[Player], expansion: bool, thread: discord.Thread):
        self.players = players
        self.expansion = expansion
        self.thread = thread
        self.turn: int = 0
        self.deck: list[Card] = all_cards(expansion)
        self.board: dict[Color, list[Card]] = {}
        self.log: list[Log] = []
        shuffle(self.deck)

        self.embed_msg = None


    @property
    def now_player(self):
        return players[self.turn % 2]

    @property
    def previous_player(self):
        return players[self.turn % 2 - 1]

    async def start(self):
        try:
            for p in self.players:
                await p.itc.response.defer()
        except discord.errors.InteractionResponded:
            pass

        for p in self.players:
            for i in range(8):
                self.draw_card(p)
        self.log.clear()
        
    def draw_card(self, p: Player, from_board = False, color: None | Color = None):
        if from_board:
            if color == None:
                raise TypeError("from_board 값이 true일 때, color 값은 항상 함께 주어져야 합니다")
            if len(self.board[color]) == 0:
                raise IndexError("해당 색깔의 카드는 보드에 없으므로 뽑을 수 없습니다")
            c = self.board[color].pop()
            p.hand.append(c)
            log.append(Log(Log.Move.DRAW, c))
        else:
            c = self.deck.pop()
            p.hand.append(c)
            log.append(Log(Log.Move.GET, c))

    def put_card(self, p, card, to_board = False):
        if to_board:
            c = p.delete_card(card)
            self.board[card.color].append(c)
            log.append(Log(Log.Move.DISCARD, c))
        else:
            c = p.delete_card(card)
            p.board[card.color].append(c)
            log.append(Log(Log.Move.PUT), c)

    def play_turn(self, p: Player):
        buttons = []
        view = ui.View()
        for i in range(8):
            button = CardSelectButton(p, card = p.hand[i], style=discord.ButtonStyle.blurple, label = str(p.hand[i]), row = i // 4)
            button.callback = self.card_select_callback

            
                    
            view.add_item(button)

    
    def card_select_callback(_self, _itc):
        _self.p.delete_card(_self.card)
        _view = ui.View()

        #카드 버리는 버튼
        btn_discard = discord.ui.Button(style=discord.Buttonstyle.red, label = "버리기", row = 0)
        def btn_discard_callback(__self, __itc):
            self.put_card(p, p_card, to_board = True)

            #카드를 어디서 얻을지 물어보는 버튼
            __view = ui.View()
            for c in Color:
                if c == Color.PURPLE and not expansion:
                    continue
                if self.board[c]: #버려진 카드가 있는 경우
                    btn = discord.ui.Button(style = discord.ButtonStyle.blurple, label = str(self.board[c][-1]), row = c.value // 3)
                    btn.callback
        btn_discard.callback = btn_discard_callback

        #카드 놓는 버튼
        btn_put = discord.ui.Button(style = discord.Buttonstyle.green, label = "놓기", row = 0)
        def btn_put_callback(__self, __itc):
            self.put_card(p, p_card, to_board = False)

            #카드를 어디서 얻을지 물어보는 버튼
        btn_put.callback = btn_put_callback
        
        

    async def update_embed(self, first = False):
        embed = discord.Embed(title="로스트 시티", color = LostCity.embed_color)
        if self.log:
            embed.description = f"{self.now_player.mention}님이 {self.log[-2]} {self.log[-1]}"
            self.log.clear()

        #첫 번째 플레이어 앞 카드    
        p = self.players[0]
        for c in Color:
            if c == Color.PURPLE and expansion == False:
                continue
            embed.add_field(name=p.mention, value=f"{c}: {" ".join([x.value_emoji for x in p.board[c]])}", inline = False)
            
        #중앙 보드판
        string = ""
        for c in Color:
            if c == Color.PURPLE and expansion == False:
                continue
            if len(self.board[c]) == 0:
                string += f"{c}(:x:)  "
            else:
                string += f"{c}({self.board[c][-1]})  "
        embed.add_field(name="중앙", value=string)

        #두 번째 플레이어 앞 카드 
        p = self.players[1]
        for c in Color:
            if c == Color.PURPLE and expansion == False:
                continue
            embed.add_field(name=p.mention, value=f"{c}: {" ".join([x.value_emoji for x in p.board[c]])}", inline = False)
            
        embed.set_footer(text=f"턴 : {self.turn}")

        if first:
            self.embed_msg = await self.thread.send(embed=embed)
        else:
            self.embed_msg.edit(embed = embed)

        if self.deck:
            
            

    




        
    

class LostCityGameManager:
    scouting: bool = True
    running: bool = False

    def __init__(self, starter: Player):
        self.starter = starter
        self.players: list[Player] = [starter]
        self.expansion: bool = True

        self.thread = None
        self.root_msg = None
    
    async def start(self, itc: discord.Interaction):
        self.running = True
        
        self.thread = await self.root_msg.create_thread(name='게임 보기')
        
        self.round=LostCityGame(self.players, self.expansion, self.thread)

        await self.round.start()
    
    def find_player(self, player: discord.Member):
            for i in range(self.player_num()):
                if self.players[i]==player:
                    return i
            return False

    def player_num(self):
        return len(self.players)

    def is_player(self, player: discord.Member):
        for p in self.players:
            if p==player:
                return True
        return False

    def add_player(self, player: discord.Interaction):
        if not self.is_player(player.user):
            self.players.append(Player(player))
            return True
        else: return False

    def del_player(self, player: discord.Member):
        for p in self.players:
            if p==player: 
                self.players.remove(player)
                return True
        return False

    def print_player_mention(self, between: str="\n") -> str:
        string=""
        for p in self.players:
            string+=p.mention+between
        return string[:-len(between)]

    
    

class LostCity(commands.Cog):
    games: dict[int, LostCityGameManager] = {}
    embed_color = 0x000000

    def end_game(self, id: int):
        del(self.games[id])  

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="로스트시티", description="새로운 로스트시티 게임을 모집합니다.")
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
        game: LostCityGameManager = self.games[id]
        if game.running:
            await itc.response.send_message( "이미 게임이 진행 중입니다.", ephemeral=True)
            return
        game.expansion = bool(모드)
        embed=discord.Embed(title="로스트 시티", description=f"{itc.user.mention}님이 새로운 로스트 시티 게임을 모집합니다.", color=self.embed_color)
        embed.add_field(name="탐험 지역 개수", value=f'{6 if game.expansion else 5}개({"확장" if game.expansion else "(기본)"})', inline = True)
        embed.add_field(name="현재 멤버", value=game.print_player_mention(), inline=True)

        async def participate(_itc: discord.Interaction):
            await _itc.response.defer()
            if len(game.players) > 2:
                await _itc.response.send_message(f"이미 자리가 꽉 찼습니다.", ephemeral=True)
            elif game.add_player(_itc):
                embed.remove_field(1)
                embed.add_field(name="현재 멤버", value=game.print_player_mention(), inline=True)
                await _itc.message.edit(embed=embed)
            else:
                await _itc.response.send_message(f"{_itc.user.mention}님은 이미 게임에 참여해 있습니다.", ephemeral=True)

            
        async def get_out(_itc: discord.Interaction):
            if game.del_player(_itc.user):
                if game.player_num()==0:
                    await game_cancel(_itc)
                    return
                else:
                    embed.remove_field(1)
                    embed.add_field(name="현재 멤버", value=game.print_player_mention(), inline=True)
                    await _itc.message.edit(embed=embed)
                    await _itc.response.send_message("참여를 취소했습니다.", ephemeral=True)
            else:
                await _itc.response.send_message("현재 게임에 참여하고 있지 않습니다.", ephemeral=True)

        async def start(_itc: discord.Interaction):
            if game.starter!=_itc.user: 
                await _itc.response.send_message("처음 모집한 사람만 게임을 시작할 수 있습니다.", ephemeral=True)
                return
            
            game.scouting=False
            game.running=True

            btn_game_cancel=discord.ui.Button(style=discord.ButtonStyle.red, label="게임 취소", row=0)
            btn_game_cancel.callback=game_cancel
            
            view=ui.View()
            view.add_item(btn_game_cancel)
            
            embed=discord.Embed(title="러브레터", description=f"{game.starter.client.mention}님이 새로운 로스트 시티 게임을 시작했습니다.\nㅤ\n스레드에서 진행을 확인하세요.", color=self.embed_color)

            await _itc.response.defer()
            await _itc.followup.edit_message(message_id=_itc.message.id, embed=embed, view=view)
            await game.start(itc)


        async def game_cancel(_itc: discord.Interaction):
            game=self.games[_itc.channel.id]
            if game.starter==_itc.user:
                del self.games[_itc.channel.id]
                await _itc.response.send_message("모집을 취소합니다.")
                await _itc.message.delete()
            else:
                await _itc.response.send_message("처음 모집한 사람만 게임을 취소할 수 있습니다.", ephemeral=True)


        btn_participate=discord.ui.Button(style=discord.ButtonStyle.blurple, label="참가",row=0)
        btn_participate.callback = participate
        
        btn_get_out=discord.ui.Button(style=discord.ButtonStyle.gray, label="참가 취소", row=0)
        btn_get_out.callback = get_out
        
        btn_start=discord.ui.Button(style=discord.ButtonStyle.green, label="시작", row=0)
        btn_start.callback=start
        
        btn_game_cancel=discord.ui.Button(style=discord.ButtonStyle.red, label="게임 취소", row=0)
        btn_game_cancel.callback=game_cancel
        
        
        
        view=ui.View()
        view.add_item(btn_participate)
        view.add_item(btn_get_out)
        view.add_item(btn_game_cancel)
        view.add_item(btn_start)
        
        msg = await itc.response.send_message(embed=embed, view=view)
        async for msg in itc.channel.history(limit=1):
            game.root_msg=msg