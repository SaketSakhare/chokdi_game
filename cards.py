import secrets
from collections import defaultdict

all_suit = ["SPADE", "HEART", "CLUB", "DIAMOND"]
class Card:
    def __init__(self):
        self.all_cards = [(value, suit) for suit in all_suit for value in range(1,14)]
        # print(self.all_cards)

    def shuffle_and_deal(self, number_of_player=4):
        self.number_of_player = number_of_player
        shuffled_cards = dict()
        for player in range(1, number_of_player+1):
            player_cards = defaultdict(list)
            for _ in range(13):
                val, suite = secrets.choice(self.all_cards)
                player_cards[suite].append(val)
                self.all_cards.remove((val,suite))
            shuffled_cards[player] = player_cards
        # assinging remaining cards to last player
        #shuffled_cards[number_of_player] = self.all_cards
        self.shuffled_cards = shuffled_cards
                
    
    def get_cards_by_player(self, player_number):
        if player_number > 0 and player_number <= self.number_of_player:
            return self.shuffled_cards[player_number]
        else:
            raise Exception
    
    def play_an_card(self, card):
        val, suit, player = card
        # print(self.shuffled_cards[player][suit], val)
        self.shuffled_cards[player][suit].remove(val)
        # print(self.shuffled_cards[player][suit], val)


# obj = Card()
# obj.shuffle()
# print(obj.shuffled_cards)
#print(obj.get_cards_by_player(2))
