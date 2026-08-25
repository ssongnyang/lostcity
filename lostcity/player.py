import discord
from lostcity.card import Card

class Player:
    def __init__(self, itc: discord.Interaction):
        self.itc = itc
        self.client = itc.user
        self.id = itc.user.id
        self.card: list[Card] = []

    def __eq__(self, other):
        if type(other)==int:
            return self.id==other
        elif other==None:
            return False
        else:
            return self.id==other.id