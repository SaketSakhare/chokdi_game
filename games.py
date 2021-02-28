
from cards import Card, all_suit
import secrets
from collections import deque

card_value_mapping  = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]

class Chogadi_Game(Card):
    def __init__(self, number_of_player= 4):
        super(Chogadi_Game, self).__init__()
        self.number_of_player = number_of_player
        self.trump_card = secrets.choice(all_suit)
        print('Trump suit for this game is ' + self.trump_card)
        
        # winner_of_last_hand will decide who will play first in next hand
        self.winner_of_last_hand = 0

    def get_card_for_player(self, player):
        all_card_player = self.shuffled_cards[player]
        print('Cards dealt to player ' + str(player))
        for suit in all_card_player:
            print('     Suite ' + suit , end=' ')
            for card in self.shuffled_cards[player].get(suit):
                print(card_value_mapping[card-1] , end=' ')
            print('')

    def start(self):
        # shuffle and deal all the cards to each player
        self.shuffle_and_deal(number_of_player=self.number_of_player)
        
        # display 
        for i in range(1, self.number_of_player+1):
            self.get_card_for_player(i)

        self.hands_won = [0] * (self.number_of_player + 1)
        for _ in range(13):
            self.cards_on_floor = deque()
            print('New hand =================================================')
            for player in range(self.winner_of_last_hand, self.winner_of_last_hand + self.number_of_player):
                player %= self.number_of_player
                optimal_card = self.max_win_min_looses(
                    self.cards_on_floor, player + 1)
                self.play_an_card(optimal_card)
                print('     player ' + str(player + 1) + ' played ' + optimal_card[1] + " " + card_value_mapping[optimal_card[0]-1])
            winner = self.cards_on_floor[0][2]
            self.winner_of_last_hand = winner -1
            print('hand won by player ' + str(winner))
            self.hands_won[winner] +=1
        print('Final score cards')
        for i in range(1, len(self.hands_won)):
            print('Player '  + str(i) + ' has won ' + str(self.hands_won[i]) + ' hands')
        winner_list = self.select_the_winner(self.hands_won)
        if len(winner_list) == 1:
            print('Winner of the Game is player ' + str(winner_list[0]))
        else:
            print('Games has tied between following players ' + str(winner_list))

    def max_win_min_looses(self, card_on_floor, player):
        if len(card_on_floor) == 0:
            # this is first player then he/she will play highest card
            max_card_played_by_first_player = self.max_card(player)
            self.cards_on_floor.append(max_card_played_by_first_player)
            self.starting_card_suit = max_card_played_by_first_player[1]
            return max_card_played_by_first_player

        # if player_has_start_card_suit cards:
        starting_suit_card = self.shuffled_cards[player].get(
            self.starting_card_suit)
        if starting_suit_card:
            #import pdb; pdb.set_trace()
           # if top_deque_is_not_trump: ??? if starting_card is trump
            if card_on_floor[0][1] != self.trump_card or  self.trump_card == self.starting_card_suit:
                just_up_card = self.do_i_have_just_up_card(
                    starting_suit_card, self.cards_on_floor[0][0])
                if just_up_card:
                    self.cards_on_floor.appendleft(
                        (just_up_card, self.starting_card_suit, player))
                    return (just_up_card, self.starting_card_suit, player)


            lowest_card_from_same_suit = (
                min(starting_suit_card), self.starting_card_suit, player)
            self.cards_on_floor.append(lowest_card_from_same_suit)
            return lowest_card_from_same_suit

        else:
            available_trump_cards = self.shuffled_cards[player].get(
                self.trump_card)
            if available_trump_cards:
                # if top_card in floor_cards has_trump_card
                if card_on_floor[0][1] == self.trump_card:
                    just_up_card = self.do_i_have_just_up_card(
                        available_trump_cards, self.cards_on_floor[0][0])
                    if just_up_card:

                        return (just_up_card, self.trump_card, player)
                    else:
                        # return lowest_expect_trump_suit, handling below in common code
                        pass
                else:
                    # return lowest_trump_card
                    lowest_trump_card = (min(self.shuffled_cards[player].get(
                        self.trump_card)), self.trump_card, player)
                    self.cards_on_floor.appendleft(lowest_trump_card)
                    return lowest_trump_card
            else:
                # return lowest_expect_trump_suit,  handling below in common code
                pass
            lowest_card_expect_trump_suit = self.get_lowest_card_expect_trump_suit(player)
            self.cards_on_floor.append(lowest_card_expect_trump_suit)
            return lowest_card_expect_trump_suit

    def get_lowest_card_expect_trump_suit(self, player):
        if self.shuffled_cards[player].get(self.trump_card):
            min_card = (min(self.shuffled_cards[player].get(
                self.trump_card)), self.trump_card, player)
        else:
            min_card = (14, None, None)
        for suit in self.shuffled_cards[player]:
            if suit != self.trump_card:
                for val in self.shuffled_cards[player].get(suit):
                    if val < min_card[0]:
                        min_card = (val, suit, player)
        return min_card

    def do_i_have_just_up_card(self, cards, top_card):
        cards.sort()
        for card in cards:
            if card > top_card:
                return card
        return None

    def max_card(self, player):
        if self.shuffled_cards[player].get(self.trump_card):
            return (max(self.shuffled_cards[player].get(self.trump_card)), self.trump_card, player)
        mx_card = (-1, None, None)
        for suit in self.shuffled_cards[player]:
            for card_val in self.shuffled_cards[player].get(suit):
                if card_val > mx_card[0]:
                    mx_card = (card_val, suit, player)

        return mx_card
    
    def select_the_winner(self, hands_win):
        mx = max(hands_win)
        player = list()
        for i , score in enumerate(hands_win):
            if mx == score:
                player.append(i)
        return player


obj = Chogadi_Game()
# obj.get_cards()
# obj.shuffle()
# print(obj.shuffled_cards)
obj.start()