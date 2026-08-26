from enum import Enum

class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __eq__(self, other):
        return self.color == other.color and self.value == other.value

    def is_wager(self):
        return self.value == 0

    def is_number(self):
        return not self.is_wager()

    def __str__(self):
        return f"Color: {self.color.name}, Value: {self.value}"

class Color(Enum):
    RED = 1
    YELLOW = 2
    GREEN = 3
    BLUE = 4
    WHITE = 5
    PURPLE = 6

def all_cards(expansion: bool = True) -> list[Card]:
    result = []
    for c in Color:
        if c == Color.PURPLE and not expansion:
            continue
        for i in range(10):
            if i == 0:
                for j in range(3):
                    result.append(Card(c, i))
            else:
                result.append(Card(c, i+1))
    return result


