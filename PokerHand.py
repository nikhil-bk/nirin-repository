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
        """
        Creates a new instance of ThreeCardPokerHand
        hand and initializes it with 3 cards from the deck.
        An optional name argument can be used to specify the 
        name of the player.
        Returns the instance of ThreeCardPokerHand thus created
        """
        hand = ThreeCardPokerHand(self.pop_cards(3), name)
        return hand

class ThreeCardPokerHand(Hand):
    """
    Three-Card Poker hand
    """
    
    all_labels = ['Nothing', 'Pair', 'Flush', 'Straight', 'Three of a Kind',
                  'Straight Flush']
    
#   Question 2
    
    def _compute_rank(self):
        """
        self, this instance of ThreeCardPokerHand
        Computes the ranking of self and stores it 
        in the self.rank attribute according to the 
        rules described in Question 2 of the project brief.
        Returns None
        """
        self.ranks.sort(reverse=True) 
            # Check for Straight Flush
        if self.is_straight_flush():
            self.rank = 5  # Straight Flush
        # Check for Three of a Kind
        elif self.is_three_of_a_kind():
            self.rank = 4  # Three of a Kind
        # Check for Straight
        elif self.is_straight():
            self.rank = 3  # Straight
        # Check for Flush
        elif self.is_flush():
            self.rank = 2  # Flush
        # Check for Pair
        elif self.is_pair():
            self.rank = 1  # Pair
        # If none of the above, it's Nothing
        else:
            self.rank = 0

        return self.rank
       
    
    def is_straight_flush(self):
        """
        Checks if the hand is a Straight Flush.
        Returns True if it is, False otherwise.
        """
        # Check for Ace, 2, 3 of the same suit
      
        if self.ranks == [12, 2, 0] or  len(set(self.suits)) == 1:
            return True

        # Check for three cards of sequential rank and the same suit
        return self.is_straight() and self.is_flush()

    def is_three_of_a_kind(self):
        """
        Checks if the hand is Three of a Kind.
        Returns True if it is, False otherwise.
        """
        # Check if there are three cards of the same rank
        return len(set(self.ranks)) == 1

    def is_straight(self):
        """
        Checks if the hand is a Straight.
        Returns True if it is, False otherwise.
        """
        # Check for three cards of sequential rank
        return max(self.ranks) - min(self.ranks) == 2 and len(set(self.ranks)) == 3

    def is_flush(self):
        """
        Checks if the hand is a Flush.
        Returns True if it is, False otherwise.
        """
        # Check for three cards of the same suit
        return len(set(self.suits)) == 1

    def is_pair(self):
        """
        Checks if the hand is a Pair.
        Returns True if it is, False otherwise.
        """
        # Check if there is a pair of cards of the same rank
        return len(set(self.ranks)) == 2
#   Question 3    
   
    # Inside the ThreeCardPokerHand class

    def _compare(self, other):
        """
            self, this instance of ThreeCardPokerHand
            other, an instance of ThreeCardPokerHand
            Implements the comparison rules for two ThreeCardPoker
            hands as per the description in Question 3 of the project brief.
            Returns -1 if other is a winning hand, 1 if self is the winning hand,
            and 0 if self and other are tied up.
        """
        # 1. If the hand rankings are not equal
        if self.rank < other.rank:
            return -1
        elif self.rank > other.rank:
            return 1
        else:
            # 2. If the hand rankings are the same, apply tie-breaking rules

            # (a) Straight Flush or Straight
            if self.rank in {3, 5}:
                self_highest_rank = 3 if 12 in self.ranks else max(self.ranks)
                other_highest_rank = 3 if 12 in other.ranks else max(other.ranks)

                if self_highest_rank != other_highest_rank:
                    return -1 if self_highest_rank > other_highest_rank else 1

            # (b) Three of a Kind
            elif self.rank == 4:
                self_arbitrary_rank = max(set(self.ranks), key=self.ranks.count)
                other_arbitrary_rank = max(set(other.ranks), key=other.ranks.count)
                return -1 if self_arbitrary_rank > other_arbitrary_rank else 1

            # (c) Flush or Nothing
            elif self.rank in {0, 2}:
                self_sorted_ranks = sorted(self.ranks, reverse=True)
                other_sorted_ranks = sorted(other.ranks, reverse=True)

                for self_rank, other_rank in zip(self_sorted_ranks, other_sorted_ranks):
                    if self_rank != other_rank:
                        return -1 if self_rank > other_rank else 1

            # (d) Pairs
            elif self.rank == 1:
                self_pair_rank = max(set(self.ranks), key=self.ranks.count)
                other_pair_rank = max(set(other.ranks), key=other.ranks.count)
                if self_pair_rank != other_pair_rank:
                    return -1 if self_pair_rank > other_pair_rank else 1

                # If pair ranks are equal, compare the ranks of the highest cards
                self_highest_rank = max(self.ranks)
                other_highest_rank = max(other.ranks)
                return -1 if self_highest_rank > other_highest_rank else 1

            # If none of the specific cases apply, it's a tie
            return 0
   
    
    def get_rank(self):
        """
        getter method for the 
        rank attribute
        Returns 0, 1, 2, 3, 4, 5 if the
        self's rank is respectively Nothing, 
        Pair, Flush, Straight, Three of a Kind, and Straight Flush
        """
        return self.rank
    

    def __init__(self, cards, name=""):
        Hand.__init__(self, name)
        self.cards = copy.deepcopy(cards)
        self.ranks = [card.get_rank() for card in self.cards]
        self.ranks.sort(reverse = True)
        self.suits = [card.get_suit() for card in self.cards]
    
        self._compute_rank()

    def __lt__(self, other):
        return True if self._compare(other) < 0 else False
    
    def __le__(self, other):
        return True if self._compare(other) <= 0 else False

#   Question 3
    def __gt__(self, other):
        """
        self, this instance of ThreeCardPokerHand
        other, an instance of ThreeCardPokerHand
        Returns True if self is the winning hand, False otherwise
        """
        return self._compare(other) < 0
    
#   Question 3    
    def __ge__(self, other):
        """
        self, this instance of ThreeCardPokerHand
        other, an instance of ThreeCardPokerHand
        Returns True if self is the winning hand or
        self and other are tied; False otherwise
        """
        return self._compare(other) <= 0
    
#   Question 3    
    def __eq__(self, other):
        """
        self, this instance of ThreeCardPokerHand
        other, an instance of ThreeCardPokerHand
        Returns True if self and other are tied; 
        False otherwise
        """
        return self._compare(other) == 0


#   Question 3    
    def __ne__(self, other):
        """
        self, this instance of ThreeCardPokerHand
        other, an instance of ThreeCardPokerHand
        Returns True if self and other are not tied; 
        False otherwise
        """
        return self._compare(other) != 0

    def get_label(self):
        """
        self, this instance of ThreeCardPokerHand
        Returns a string representation of self.
        """
        return ThreeCardPokerHand.all_labels[self.rank]
    
    def get_full_label(self):
        """
        self, this instance of ThreeCardPokerHand
        Returns a string representation of self replacing
        the Nothing ranking with the highest ranking card.
        Used internally by __str__().
        """
        return  Card.ranks[self.ranks[0]] + '-High' if self.rank == 0 else \
            self.get_label()
        
    def __str__(self):
        """
        self, this instance of ThreeCardPokerHand
        Returns a string representation of self that 
        includes the list of the cards, and the rank.
        """
        # return ""
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
    
    print(hand1 < hand2) # True
    print(hand1 > hand2) # False
    print(hand1 <= hand2) # True
    print(hand1 >= hand2) # False
    print(hand1 == hand2) # False
    print(hand1 != hand2) # True
    print()
    
#   3-Pair + Jack
    hand1 = ThreeCardPokerHand([Card(1, 0), Card(1, 1), Card(9, 2)])
    print(hand1)
    print()

#   2-Pair + Ace
    hand2 = ThreeCardPokerHand([Card(12, 0), Card(0, 1), Card(0, 0)])
    print(hand2)
    print()
    
    print(hand1 < hand2) # False
    print(hand1 > hand2) # True
    print(hand1 <= hand2) # False
    print(hand1 >= hand2) # True
    print(hand1 == hand2) # False
    print(hand1 != hand2) # True
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
    hand3 = ThreeCardPokerHand([Card(12, 1), Card(10, 1), Card(11, 1)], 'Dealer')   
    print(hand3)                      
    
#   Flush
    print()
    hand3 = ThreeCardPokerHand([Card(0, 1), Card(1, 1), Card(11, 1)], 'Player')   
    print(hand3)                      