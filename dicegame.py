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
    s = 0
    while len(dice) > 0:
        dim = len(set(dice))
        if len(dice) == 6 and dim == 1:
            dice = []
            s += 3000
            break
        elif len(dice) == 6 and all([dice.count(die) == 3 for die in set(dice)]):
            dice = []
            s += 2500
            break
        elif len(dice) == 6 and dim == 6:
            dice = []
            s += 1500
            break
        elif len(dice) == 6 and all([dice.count(die) == 2 for die in set(dice)]):
            dice = []
            s += 1500
            break
        elif any([dice.count(die) == 5 for die in set(dice)]):
            dice = [die for die in dice if dice.count(die) != 5]
            s += 2000
            break
        elif any([dice.count(die) == 4 for die in set(dice)]):
            dice = [die for die in dice if dice.count(die) != 4]
            s += 1000
            break
        elif any([dice.count(die) == 3 for die in set(dice)]):
            d = [die for die in set(dice) if dice.count(die) == 3][0]
            dice = [die for die in dice if die != d]
            s += 300 if d == 1 else 100 * d
            break
        else:
            for die in dice:
                if die == 1:
                    s += 100
                elif die == 5:
                    s += 50
            dice = []
            break
    return s

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
