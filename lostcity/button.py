from discord.ui import Button

class CardSelectButton(Button):
    def __init__(self, p, card, **kwargs):
        super.__init__(**kwargs)
        self.player = p
        self.card = card

    async def callback(self, _itc):
        