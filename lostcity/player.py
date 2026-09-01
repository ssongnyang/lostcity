import discord
from lostcity.card import Card, Color

from collections import defaultdict

class Player:
    def __init__(self, itc: discord.Interaction):
        self.itc = itc
        self.client = itc.user
        self.id = itc.user.id
        self.hand: list[Card] = []
        self.board: dict[Color, list[Card]] = defaultdict(lambda: [])
        self.player_msg = None

        self.score = 0
    
    @property
    def not_turn_embed(self):
        self.sort()
        embed = discord.Embed(title=":x: 지금은 당신의 차례가 아닙니다.", description="잠시 차례를 기다려 주세요.", color = 0xff0000)
        embed.add_field(name="당신의 카드", value=", ".join([str(c) for c in self.hand]))
        return embed

    @property
    def turn_start_embed(self):
        self.sort()
        embed = discord.Embed(title="당신의 차례입니다.", description="버리거나 놓을 카드를 선택해 주세요.", color = 0x00ff00)
        embed.add_field(name="당신의 카드", value=", ".join([str(c) for c in self.hand]))
        return embed

    @property
    def discard_or_put_embed(self):
        self.sort()
        embed = discord.Embed(title="당신의 차례입니다.", description="카드를 버릴지 놓을지 선택해 주세요.", color = 0x00ff00)
        embed.add_field(name="당신의 카드", value=", ".join([str(c) for c in self.hand]))
        return embed

    @property
    def draw_card_embed(self):
        self.sort()
        embed = discord.Embed(title="당신의 차례입니다.", description="손으로 가져올 카드를 선택해 주세요.", color = 0x00ff00)
        embed.add_field(name="당신의 카드", value=", ".join([str(c) for c in self.hand]))
        return embed
        
    def __eq__(self, other):
        if type(other)==int:
            return self.id==other
        elif other==None:
            return False
        else:
            return self.id==other.id

    def delete_card(self, card):
        for i in range(len(self.hand)):
            if self.hand[i] == card:
                return self.hand.pop(i)
        return False

    def sort(self):
        self.hand.sort(key=lambda x: (x.color.value, x.value))

    def score(self):
        result = []
        for c in Color:
            if not self.board[c]:
                continue
            s = sum([card.value for card in self.board[c]])
            if len(self.board[c]) >= 8:
                s += 20
            cnt = 1
            for card in self.board[c]:
                if card.is_wager():
                    cnt += 1
            s *= cnt
            
            result.append((c, s))
        return result


    @property
    def mention(self):
        return self.client.mention