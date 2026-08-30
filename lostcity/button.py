from discord.ui import Button

class CardSelectButton(Button):
    def __init__(self, game_instance, p, card, **kwargs):
        super().__init__(**kwargs)
        self.game = game_instance
        self.p = p
        self.card = card

class PutCardButton(CardSelectButton):
    def __init__(self, button, to_board = False, **kwargs):
        super().__init__(button.p, button.card, **kwargs)
        self.to_board = to_board
        