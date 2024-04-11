from dataclasses import dataclass

@dataclass
class DataClassCard:
    rank: str
    suit: str
    num = 1


def test_dataclass():
    card = DataClassCard('A', 'spades')
    print(card)
    print(card.rank)
    print(card.suit)
    print(card.num)
    card.num = 2
    print(card.num)
    print(card)
    print(card.__dict__)
    print(card.__annotations__)
    

if __name__ == '__main__':
    test_dataclass()