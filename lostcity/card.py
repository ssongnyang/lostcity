from enum import Enum

class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __eq__(self, other):
        return self.color == other.color and self.value == other.value

    @property
    def color_emoji(self):
        return str(self.color)

    @property
    def value_emoji(self):
        match(self.value):
            case 0:
                emoji = "🤝"
            case 2:
                emoji = "2️⃣"
            case 3:
                emoji = "3️⃣"
            case 4:
                emoji = "4️⃣"
            case 5:
                emoji = "5️⃣"
            case 6:
                vmoji = "6️⃣"
            case 7:
                emoji = "7️⃣"
            case 8:
                emoji = "8️⃣"
            case 9:
                emoji = "9️⃣"
            case 10:
                emoji = "🔟"
        return emoji

    def is_wager(self):
        return self.value == 0

    def is_number(self):
        return not self.is_wager()

    def __str__(self):  
        return f"{self.color_emoji}{self.value_emoji}"
        
class Color(Enum):
    RED = 0
    YELLOW = 1
    GREEN = 2
    BLUE = 3
    WHITE = 4
    PURPLE = 5

    def __str__(self):
        match(self):
            case Color.RED:
                emoji = ":red_square:"
            case Color.YELLOW:
                emoji = ":yellow_square:"
            case Color.GREEN:
                emoji = ":green_square:"
            case Color.BLUE:
                emoji = ":blue_square:"
            case Color.WHITE:
                emoji = ":white_large_square:"
            case Color.PURPLE:
                emoji = ":purple_square:"
        return emoji

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


