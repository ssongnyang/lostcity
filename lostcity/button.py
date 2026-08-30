from discord.ui import Button

class CardSelectButton(Button):
    def __init__(self, index, **kwargs):
        super.__init__(**kwargs)
        self.index = index

    async def callback(self, _itc):
        