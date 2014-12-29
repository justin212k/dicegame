#!/usr/bin/env python
# state of game: dice, turn, scores, escrow
# e.g.: [1,3,3,5], 0, [100, 300], 200

import random
def dumb1(dice):
    if dice == []: return [], 'roll'
    if 1 in dice:
        return [1], 'roll'
    return [], 'bank'


def play_dice(players=[dumb1, dumb1]):
    """ currently doesn't allow building off scores
        also doesn't allow rebuttals
        or bottoms
    """
    dice, turn, scores, escrow = [], 0, [0]*len(players), 0
    while max(scores) < 10000:
        print dice, turn, scores, escrow
        to_escrow, move = players[turn](dice)
        print to_escrow, move
         # to_escrow is e.g. [1,2,2,2]
        for die in to_escrow:
            dice.remove(die)
        escrow += value(to_escrow)
        if move == 'bank':
            dice = []
            scores[turn] += escrow
            turn = (turn + 1) % len(players)
            escrow = 0
        if move == 'roll':
            dice = roll(len(dice))
            dice.sort()
            if not can_score(dice): # fail to score: next turn
                print 'fail to score with ' + str(dice)
                turn = (turn + 1) % len(players)
                dice = []
                escrow = 0
    return scores

def value(dice):
    return 500

def can_score(dice):
    if 1 not in dice and 5 not in dice:
        return False
    return True

def roll(num_dice):
    if num_dice == 0:
        num_dice = 6
    return [random.randint(1,6) for a in range(num_dice)]


if __name__ == '__main__':
    print play_dice()