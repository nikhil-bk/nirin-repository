#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 14:24:23 2018
@author: uxac007
"""

import copy
import random

class Card(object):
    """
    A generic Card class
    """

    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 
             'Jack', 'Queen', 'King', 'Ace']
    suits = ['Spades', 'Clubs', 'Diamonds', 'Hearts']

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def get_rank(self):
        return self.rank

    def get_suit(self):
        return self.suit

    def __str__(self):
        return Card.ranks[self.rank] + ' of ' + Card.suits[self.suit]

class Deck(object):
    """
    A standard deck of 52 cards
    """

    def __init__(self):
        self.cards = []
        for rank in range(len(Card.ranks)):
            for suit in range(len(Card.suits)):
                self.cards.append(Card(rank, suit))

    def shuffle(self):
        random.shuffle(self.cards)

    def pop_cards(self, n):
        a = self.cards[-n:]
        del self.cards[-n:]
        return a

    def add_cards(self, cards):
        self.cards.extend(cards.copy())

    def clear_cards(self):
        self.cards.clear()

    def move_cards(self, hand, n):
        self.add_cards(self.cards)
        hand.cards = self.pop_cards(n)

    def __str__(self):
        lst = [str(card) for card in self.cards]
        return '\n'.join(lst)

class Hand(Deck):
    """
    A generic Hand class
    """

    def __init__(self, name=""):
        self.cards = []
        self.name = name

    def get_name(self):
        return self.name

    def __str__(self):
        return self.name + "'s Hand:\n" + Deck.__str__(self)


if __name__ == '__main__':    
    d = Deck()
    print(d)
    print()
    h = Hand()
    d.move_cards(h, 5)
    print(d)
    print()
    print(h)
    d.add_cards([Card(0, 0), Card(1, 1)])
    print(d) 
    print()
    d = Deck()
    h = Hand('Dealer')
    print(h)
    print()
    d.shuffle()
    d.move_cards(h, 3)
    print(h)
