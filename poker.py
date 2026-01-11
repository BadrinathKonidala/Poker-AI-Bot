'''
Hand Ranks:
1 - Royal Flush
2 - Straight Flush
3 - 4 of a Kind
4 - Full House
5 - Flush
6 - Straight
7 - 3 of a Kind
8 - Two Pair
9 - Pair
10 - High Card

Suits:
1 - Hearts
2 - Diamonds
3 - Spades
4 - Clubs

Ranks:
1 - A
2 - 2
3 - 3
4 - 4
5 - 5
6 - 6
7 - 7
8 - 8
9 - 9
10 - 10
11 - J
12 - Q
13 - K


'''


"""Represents a single Card"""

from consts import royal_ranks
from math import comb


class Card:
    def __init__(self, suit : int, rank : int):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
        ranks = ['Ace','2','3','4','5','6','7','8','9','10','Jack','Queen','King']
        return f"{ranks[self.rank-1]} of {suits[self.suit-1]}"
    
    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return self.suit == other.suit and self.rank == other.rank


"""Represents a Hand of Cards"""
class Hand:
    def __init__(self, cards: list[Card]):
        # if len(cards) != 5:
        #     raise ValueError("A poker hand must contain exactly 5 cards.")
        self.cards = cards
        self.ranks = [card.rank for card in cards]
        self.suits = [card.suit for card in cards]
    
    def __repr__(self):
        return str(list(map(repr,self.cards)))
    
    def __len__(self):
        return len(self.cards)
    
    def add_card(self, card: Card):
        if len(self.cards) == 5:
            raise ValueError("A poker hand cannot contain more than 5 cards.")
        self.cards.append(card)
        self.ranks.append(card.rank)
        self.suits.append(card.suit)


"""Represents hole cards - the 2 private cards a player holds in a round"""
class HoleCards:
    def __init__(self, cards: list[Card]):
        if len(cards) != 2:
            raise ValueError("There must be exactly 2 hole cards")
        self.cards = cards
        self.ranks = [card.rank for card in cards]
        self.suits = [card.suit for card in cards]
    
    def __repr__(self):
        return str(list(map(repr,self.cards)))
        


'''Returns what type of hand it is'''
def hand_rank(hand : Hand):
    # all cards are the same suit (flush)
    if len(set(hand.suits)) == 1:
        ranks = sorted(hand.ranks)
        # royal flush
        if ranks == [1,10,11,12,13]:
            return 1
        
        # straight flush
        min_rank = min(ranks)
        if [rank - min_rank for rank in ranks] == [0,1,2,3,4]:
            return 2
        
        # regular flush
        return 5
    
    # only 2 different ranks in hand
    if len(set(hand.ranks)) == 2:
        # 4 of a kind
        if hand.ranks.count(hand.ranks[0]) in [1,4]:
            return 3

        # full house
        return 4
    
    # only 3 different ranks in hand
    if len(set(hand.ranks)) == 3:
        # 2 pair
        for rank in hand.ranks:
            if hand.ranks.count(rank) == 2:
                return 8
        
        # 3 of a kind
        return 7

    # pair
    if len(set(hand.ranks)) == 4:
        return 9
    
    
    # straight
    # Note that we are doing straight last since it is the most time consuming to check for
    ranks = sorted(hand.ranks)
    min_rank = min(ranks)
    if [rank - min_rank for rank in ranks] == [0,1,2,3,4] or ranks == royal_ranks:
        return 6

    # high card
    return 10


def royal_probability(board : Hand, hole : HoleCards):
    # count number of royal cards (10, jack, queen, king, ace) we have for each suit across the hole cards and the board
    royal_suits = {1 : 0, 2 : 0, 3 : 0, 4 : 0}
    board_len = len(board)
    for i in range(board_len):
        if board.ranks[i] in royal_ranks:
            royal_suits[board.suits[i]] += 1
    for i in range(2):
        if hole.ranks[i] in royal_ranks:
            royal_suits[hole.suits[i]] += 1
    
    # sum the the individual probabilities of getting a royal for each suit
    probability = 0
    for royals in royal_suits.values():
        # if suits <= board_len, royal is not possible, so probability is 0
        if royals >= board_len:
            # 52 - (board_len+2) cards left to choose rest of board from
            # (52 - (board_len+2)) choose (5 - board_len) total ways to choose rest of the board 
            # 52 - (board_len+2 + 5-suits) choose (5 - board_len - (5-suits)) ways to choose rest of board such that the remaning royal in this suit are on the board
            probability += comb(52 - (board_len+2 + 5-royals) , (5 - board_len - (5 - royals)))/comb(52 -  (board_len+2), 5 - board_len)
    return probability


def quads_prob(board : Hand, hole : HoleCards):
    # count number of cards we have for each rank across the hole cards and the board
    ranks = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0}
    board_len = len(board)
    for i in range(board_len):
        ranks[board.ranks[i]]+=1
    for i in range(2):
        ranks[hole.ranks[i]]+=1
    # sum the the individual probabilities of getting quads for each rank
    probability = 0
    for count in ranks.values():
        # if 4-count > 5-board_len, quads is not possible, so probability is 0
        if 4-count <= 5-board_len:
            # 52 - (board_len+2) cards left to choose rest of board from
            # (52 - (board_len+2)) choose (5 - board_len) total ways to choose rest of the board 
            # 52 - (board_len+2 + 4-count) choose (5 - board_len - (4-count)) ways to choose rest of board such that the remaning cards of this rank are on the board
            probability += comb(52 - (board_len+2 + 4-count), (5 - board_len - (4-count)))/comb(52 -  (board_len+2), 5 - board_len)
    return probability
