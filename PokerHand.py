#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 12:47:22 2018

@author: uxac007
"""

import copy
from Card import Card, Hand, Deck


class ThreeCardPokerDeck(Deck):
    """
    Three-Card Poker deck
    """

    def deal_hand(self, name=""):
        hand = ThreeCardPokerHand(self.pop_cards(3), name)
        return hand


class ThreeCardPokerHand(Hand):
    """
    Three-Card Poker hand
    """

    all_labels = ['Nothing', 'Pair', 'Flush', 'Straight', 'Three of a Kind',
                  'Straight Flush']

    def _compute_rank(self):
        self.ranks.sort(reverse=True)
        if self.is_straight_flush():
            self.rank = 5  # Straight Flush
        elif self.is_three_of_a_kind():
            self.rank = 4  # Three of a Kind
        elif self.is_straight():
            self.rank = 3  # Straight
        elif self.is_flush():
            self.rank = 2  # Flush
        elif self.is_pair():
            self.rank = 1  # Pair
        else:
            self.rank = 0  # Nothing
        return self.rank

    def is_straight_flush(self):
        if self.ranks == [12, 2, 0] or len(set(self.suits)) == 1:
            return True
        return self.is_straight() and self.is_flush()

    def is_three_of_a_kind(self):
        return len(set(self.ranks)) == 1
    
    @staticmethod
    def rank_to_value(rank):
        """
        Convert card rank to numerical value for straight evaluation.
        """
        if rank in Card.ranks[:-1]:  # Exclude 'Ace' from numerical comparison
            return Card.ranks.index(rank)
        else:
            return Card.ranks.index('Ace')
    def is_straight(self):
        rank_values = [self.rank_to_value(rank) for rank in self.ranks]
        return max(rank_values) - min(rank_values) == 2 and len(set(rank_values)) == 3
        # return max(self.ranks) - min(self.ranks) == 2 and len(set(self.ranks)) == 3

    def is_flush(self):
        return len(set(self.suits)) == 1

    def is_pair(self):
        return len(set(self.ranks)) == 2

    # def _compare(self, other):
        """
        Compare this hand with another hand according to the game rules.
        Return -1 if other is winning, 0 if tied, and 1 if self is winning.
        """
        if self.rank != other.rank:
            return 1 if self.rank > other.rank else -1
        else:
            # Same rank, use tie-breaking rules
            if self.rank == 5:  # Straight Flush or Straight
                # Compare the highest ranks of both hands
                return 1 if self.ranks[0] > other.ranks[0] else -1 if self.ranks[0] < other.ranks[0] else 0
            elif self.rank == 4:  # Three of a Kind
                # Compare the rank of an arbitrary card in both hands
                return 1 if self.ranks[0] > other.ranks[0] else -1
            elif self.rank == 3:  # Straight
                # Compare the highest ranks of both hands
                return 1 if self.ranks[0] > other.ranks[0] else -1 if self.ranks[0] < other.ranks[0] else 0
            elif self.rank == 2 or self.rank == 0:  # Flush or Nothing
                # Compare the ranks in lexicographical order
                return self._compare_lexicographical(other.ranks)
            elif self.rank == 1:  # Pair
                # Compare the ranks of the paired cards first
                return 1 if self._compare_pairs(other.ranks) else 0
    def _compare(self, other):
        if self.rank != other.rank:
            return 1 if self.rank > other.rank else -1
        else:
            # Same rank, use tie-breaking rules
            if self.rank == 5:  # Straight Flush or Straight
                # Compare the highest ranks of both hands
                return 1 if self.rank_to_value(self.ranks[0]) > self.rank_to_value(other.ranks[0]) else \
                       -1 if self.rank_to_value(self.ranks[0]) < self.rank_to_value(other.ranks[0]) else 0
            elif self.rank == 4:  # Three of a Kind
                # Compare the rank of an arbitrary card in both hands
                return 1 if self.rank_to_value(self.ranks[0]) > self.rank_to_value(other.ranks[0]) else \
                       -1 if self.rank_to_value(self.ranks[0]) < self.rank_to_value(other.ranks[0]) else 0
            elif self.rank == 3:  # Straight
                # Compare the highest ranks of both hands
                return 1 if self.rank_to_value(self.ranks[0]) > self.rank_to_value(other.ranks[0]) else \
                       -1 if self.rank_to_value(self.ranks[0]) < self.rank_to_value(other.ranks[0]) else 0
            elif self.rank == 2 or self.rank == 0:  # Flush or Nothing
                # Compare the ranks in lexicographical order
                return self._compare_lexicographical(self.ranks, other.ranks)
            elif self.rank == 1:  # Pair
                # Compare the ranks of the paired cards first
                return 1 if self._compare_pairs(self.ranks, other.ranks) else \
                       -1 if self._compare_pairs(other.ranks, self.ranks) else 0
    
    # def _compare_lexicographical(self, other_ranks):
    #     """
    #     Compare ranks lexicographically.
    #     Return 1 if self is winning, -1 if other is winning, and 0 if tied.
    #     """
    #     for self_rank, other_rank in zip(self.ranks, other_ranks):
    #         if self_rank > other_rank:
    #             return 1
    #         elif self_rank < other_rank:
    #             return -1
    #     return 0
    
    def _compare_lexicographical(self, self_ranks, other_ranks):
        """
        Compare ranks lexicographically.
        Return 1 if self is winning, -1 if other is winning, and 0 if tied.
        """
        for self_rank, other_rank in zip(self_ranks, other_ranks):
            if self.rank_to_value(self_rank) > self.rank_to_value(other_rank):
                return 1
            elif self.rank_to_value(self_rank) < self.rank_to_value(other_rank):
                return -1
        return 0
    
    def _compare_pairs(self, other_ranks):
        """
        Compare ranks of paired cards.
        Return True if self is winning, False otherwise.
        """
        self_pair_rank = [rank for rank in set(self.ranks) if self.ranks.count(rank) == 2][0]
        other_pair_rank = [rank for rank in set(other_ranks) if other_ranks.count(rank) == 2][0]
        return self_pair_rank > other_pair_rank
    
    def get_rank(self):
        return self.rank

    def __init__(self, cards, name=""):
        Hand.__init__(self, name)
        self.cards = copy.deepcopy(cards)
        self.ranks = [card.get_rank() for card in self.cards]
        self.ranks.sort(reverse=True)
        self.suits = [card.get_suit() for card in self.cards]
        self._compute_rank()

    def __lt__(self, other):
        return True if self._compare(other) < 0 else False

    def __le__(self, other):
        
        return True if self._compare(other) <= 0 else False

    def __gt__(self, other):
        return True if self._compare(other) > 0 else False

    def __ge__(self, other):
        return True if self._compare(other) >= 0 else False

    def __eq__(self, other):
        return True if self._compare(other) == 0 else False

    def __ne__(self, other):
        return True if self._compare(other) != 0 else False

    def get_label(self):
        return ThreeCardPokerHand.all_labels[self.rank]

    def get_full_label(self):
        return Card.ranks[self.ranks[0]] + '-High' if self.rank == 0 else \
            self.get_label()

    def __str__(self):
        return Hand.__str__(self) + '\nHand Rank: ' + self.get_full_label()


if __name__ == '__main__':
    """
    Test cases
    """
#   Queen-high
    hand1 = ThreeCardPokerHand([Card(10, 0), Card(1, 1), Card(0, 2)])
    print(hand1)
    print()

#   Straight Flush
    hand2 = ThreeCardPokerHand([Card(12, 0), Card(1, 0), Card(0, 0)])
    print(hand2)
    print()

    print(hand1 < hand2)  # True
    print(hand1 > hand2)  # False
    print(hand1 <= hand2)  # True
    print(hand1 >= hand2)  # False
    print(hand1 == hand2)  # False
    print(hand1 != hand2)  # True
    print()

#   3-Pair + Jack
    hand1 = ThreeCardPokerHand([Card(1, 0), Card(1, 1), Card(9, 2)])
    print(hand1)
    print()

#   2-Pair + Ace
    hand2 = ThreeCardPokerHand([Card(12, 0), Card(0, 1), Card(0, 0)])
    print(hand2)
    print()

    print("-------")

    print(hand1 < hand2)  # False
    print(hand1 > hand2)  # True
    print(hand1 <= hand2)  # False
    print(hand1 >= hand2)  # True
    print(hand1 == hand2)  # False
    print(hand1 != hand2)  # True
    print()

    deck = ThreeCardPokerDeck()
    deck.shuffle()
    hand = deck.deal_hand()
    print(hand)

#   Straight Flush
    print()
    hand3 = ThreeCardPokerHand([Card(0, 0), Card(1, 0), Card(12, 0)], 'Ruben')
    print(hand3)

#   Straight
    print()
    hand3 = ThreeCardPokerHand([Card(0, 1), Card(12, 2), Card(1, 0)], 'Greg')
    print(hand3)

#   Straight Flush
    print()
    hand3 = ThreeCardPokerHand(
        [Card(12, 1), Card(10, 1), Card(11, 1)], 'Dealer')
    print(hand3)

#   Flush
    print()
    hand3 = ThreeCardPokerHand([Card(0, 1), Card(1, 1), Card(11, 1)], 'Player')
    print(hand3)
