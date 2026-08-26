import discord
from lostcity.card import Card

class Player:
    def __init__(self, itc: discord.Interaction):
        self.itc = itc
        self.client = itc.user
        self.id = itc.user.id
        self.hand: list[Card] = []
        self.board: dict[Color, list[Card]] = {}

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


    @property
    def mention(self):
        return self.client.mention