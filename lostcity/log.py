from lostcity.card import Card
from enum import Enum

class Log:
    class Move(Enum):
        DISCARD = auto()
        PUT = auto()
        DRAW = auto()
        GET = auto()

    def __init__(self, move, card):
        self.move: Move = move
        self.card: Card = card

    def __str__(self):
        string = ""
        match(self.move)
            case Move.DISCARD:
                string += self.card.__str__() + "을(를) 버리고"
            case Move.PUT:
                string += self.card.__str__() + "을(를) 놓고"
            case Move.DRAW:
                string += "덱 위에서 카드를 한 장 가져갔습니다."
            case Move.GET:
                string += self.card.__str__() + " 카드를 가져갔습니다."
        return string
        
        



    