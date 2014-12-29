#!/usr/bin/env python
import random
import itertools

# state of game: dice, turn, scores, escrow, buildable
# e.g.: [1,3,3,5], 0, [100, 300], 200, False
# see dumb1 for the API for a player

def dumb1(dice, turn, scores, escrow, buildable=False):
    """ takes the state of the game and returns a move

    returns a subset of dice to move to escrow, and an action
    """
    if dice == []:
        return [], 'roll'
    if buildable:
        return [], 'start fresh'
    to_escrow = escrow_possibilities(dice)[0][1]
    if escrow >= 200:
        return to_escrow, 'bank'
    else:
        return to_escrow, 'roll'

def play_dice(players=[dumb1, dumb1], building=False, end_score=2000, rebuttals=True):
    """ one game of dice
    """

    finished = [False]*len(players)
    dice, turn, scores, escrow, buildable = [], 0, [0]*len(players), 0, False
    while not all(finished):
        # each loop is a round, there may be multiple rounds per turn
        # a turn starts with dice presented to a player,
        # they must first choose what to escrow,
        # then whether to bank or roll
        # sometimes a player is presented with [] as dice
        # they must roll in this case?
        turn_over = False
        print "\nnew round. scores: %s" % (scores,)
        print "player %s is presented with dice: %s, and %s in escrow " % (turn, dice, escrow)
        to_escrow, move = players[turn](dice, turn, scores, escrow, buildable)
        print "player %s escrows %s, and elects to " % (turn, to_escrow) + move
        # to_escrow is e.g. [1,2,2,2]
        for die in to_escrow:
            dice.remove(die)
        escrow += value(to_escrow)
        if move == 'bank':
            turn_over = True
            buildable = True
            scores[turn] += escrow
            if not building:
                dice = []
                escrow = 0
        elif move in ["roll", "bottoms", "start fresh"]:
            buildable = False
            # all others are some kind of dice rolling
            if move == "start fresh":
                dice = []
                escrow = 0
            dice = roll(len(dice))
            dice.sort()
            print "player %s rolls %s " % (turn, dice)
            if move == "bottoms":
                dice = bottoms(dice)
                print "bottoms makes it %s !" % (dice,)

            if not can_score(dice): # fail to score: next turn
                turn_over = True
                if len(dice) == 6:
                    print "farkle! " + str(dice)
                else:
                    print 'fail to score with ' + str(dice)
                dice = []
                escrow = 0

        if turn_over:
            if not rebuttals:
                if scores[turn] > end_score:
                    finished = [True]*len(players)
            else:
                if any(finished):
                    finished[turn] = True
                elif scores[turn] > end_score:
                    finished[turn] = True
            turn = (turn + 1) % len(players)
    return scores

def options(dice):
    opts = []
    dice.sort()
    for i in range(len(dice)):
        for combination in itertools.combinations(dice, i+1):
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

def escrow_possibilities(dice):
    p = []
    if 1 in dice:
        p.append((100, [1]))
    if 5 in dice:
        p.append((50, [5]))
    return p

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
