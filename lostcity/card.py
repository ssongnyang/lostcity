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
        match(self.color)
            case Color.RED:
                color_emoji = ":red_square:"
            case Color.YELLOW:
                color_emoji = ":yellow_square:"
            case Color.GREEN:
                color_emoji = ":green_square:"
            case Color.BLUE:
                color_emoji = ":blue_square:"
            case Color.WHITE:
                color_emoji = ":white_square:"
            case Color.PURPLE:
                color_emoji = ":purple_square:"
                
        match(self.value)
            case 0:
                value_emoji = "🤝"
            case 2:
                value_emoji = "2️⃣"
            case 3:
                value_emoji = "3️⃣"
            case 4:
                value_emoji = "4️⃣"
            case 5:
                value_emoji = "5️⃣"
            case 6:
                value_emoji = "6️⃣"
            case 7:
                value_emoji = "7️⃣"
            case 8:
                value_emoji = "8️⃣"
            case 9:
                value_emoji = "9️⃣"
            case 10:
                value_emoji = "🔟"
            
        return f"{color_emoji}{value_emoji}"
        
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


