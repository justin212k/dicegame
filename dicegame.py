#!/usr/bin/env python
import random
import itertools

# state of game: dice, turn, scores, escrow
# e.g.: [1,3,3,5], 0, [100, 300], 200
# see dumb1 for the API for a player

def dumb1(dice, scores, escrow):
    """ takes a list of dice. 
    returns a subset of dice to move to escrow, and a move
    """
    if dice == []: return [], 'roll'
    if 1 in dice:
        if len(dice) == 2:
            return [1], 'bottoms'
        else:
            return [1], 'roll'
    return [], 'bank'

def threshold(dice, scores, escrow):
    if escrow >= 400:
        return [], 'bank'
    else:
        if 1 in dice:
            return [1], 'roll'
        else:
            return [5], 'roll'


def play_dice(players=[dumb1, dumb1], building=False):
    """ currently doesn't allow building off scores
        also doesn't allow rebuttals
    """
    dice, turn, scores, escrow = [], 0, [0]*len(players), 0
    while max(scores) < 2000:
        # a turn starts with dice presented to a player,
        # they must first choose what to escrow,
        # then whether to bank or roll
        # sometimes a player is presented with [] as dice
        # they must roll in this case?
        print "\nnew round. scores: %s" % (scores,)
        print "player %s is presented with dice: %s, and %s in escrow " % (turn, dice, escrow)
        to_escrow, move = players[turn](dice, scores, escrow)
        print "player %s escrows %s, and elects to " % (turn, to_escrow) + move
        # to_escrow is e.g. [1,2,2,2]
        for die in to_escrow:
            dice.remove(die)
        escrow += value(to_escrow)
        if move == 'bank':
            scores[turn] += escrow
            if not building:
                dice = []
                escrow = 0
            turn = (turn + 1) % len(players)
        elif move == 'bottoms':
            dice = roll(len(dice))
            print "player %s rolls %s ..." % (turn, dice)
            dice = bottoms(dice)
            print "bottoms makes it %s !" % (dice,)
            if not can_score(dice): # fail to score: next turn
                print 'fail to score with ' + str(dice)
                turn = (turn + 1) % len(players)
                dice = []
                escrow = 0
        elif move == 'roll':
            dice = roll(len(dice))
            dice.sort()
            print "player %s rolls %s " % (turn, dice)
            if value(dice) == 0: # fail to score: next turn
                if len(dice) == 6:
                    print "farkle! " + str(dice)
                else:
                    print 'fail to score with ' + str(dice)
                turn = (turn + 1) % len(players)
                dice = []
                escrow = 0
    return scores

def options(dice):
    opts = []
    dice.sort()
    for i in range(len(dice)):
        for combination in itertools.combinations(dice, i):
            opt = value(combination, True)
            if opt[0] > 0 and opt not in opts:
                opts.append(opt)
    return tuple(reversed(sorted(opts, key=lambda opt: opt[0])))

def value(dice, return_used=False):
    pts = 0
    used = []
    while len(dice) > 0:
        dim = len(set(dice))
        if len(dice) == 6 and dim == 1:
            pts += 3000
            used += dice
            break
        elif len(dice) == 6 and all([dice.count(die) == 3 for die in set(dice)]):
            pts += 2500
            used += dice
            break
        elif len(dice) == 6 and dim == 6:
            pts += 1500
            used += dice
            break
        elif len(dice) == 6 and all([dice.count(die) == 2 for die in set(dice)]):
            pts += 1500
            used += dice
            break
        elif any([dice.count(die) == 5 for die in set(dice)]):
            pts += 2000
            used += [die for die in dice if dice.count(die) == 5]
            dice = [die for die in dice if dice.count(die) != 5]
            continue
        elif any([dice.count(die) == 4 for die in set(dice)]):
            pts += 1000
            used += [die for die in dice if dice.count(die) == 4]
            dice = [die for die in dice if dice.count(die) != 4]
            continue
        elif any([dice.count(die) == 3 for die in set(dice)]):
            d = [die for die in set(dice) if dice.count(die) == 3][0]
            pts += 300 if d == 1 else 100 * d
            used += [die for die in dice if die == d]
            dice = [die for die in dice if die != d]
            continue
        else:
            for die in dice:
                if die == 1:
                    pts += 100
                    used.append(die)
                elif die == 5:
                    pts += 50
                    used.append(die)
            break
    if return_used: return pts, used
    return pts

def can_score(dice):
    if 1 not in dice and 5 not in dice:
        return False
    return True

def roll(num_dice):
    if num_dice == 0:
        num_dice = 6
    return [random.randint(1,6) for a in range(num_dice)]

def bottoms(dice):
    return [7 - die for die in dice]

if __name__ == '__main__':
    print "\n\nfinal score: " + str(play_dice(building=True))
