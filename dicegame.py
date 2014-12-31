#!/usr/bin/env python
import random
import itertools

ACTIONS = ['start fresh', 'roll', 'bank', 'bottoms']
# state of game: dice, turn, scores, escrow, piggybackable
# e.g.: [1,3,3,5], 0, [100, 300], 200, False
# see dumb1 for the API for a player
def manual(dice, turn, scores, escrow, piggybackable=False):
    while True:
        print "dice: " + str(dice)
        print "escrow: " + str(escrow)
        print "type a list of dice to escrow, followed by an action"
        print "e.g. 1: [], 'start fresh'"
        print "e.g. 2: [1,5,5], 'bank'"
        print "e.g. 3: [2,2,2], 'roll'"
        try:
            to_escrow, action = input()
            if type(to_escrow) != list or action not in ACTIONS:
                raise ValueError('try again')
            return to_escrow, action
        except Exception as e:
            print e

def dumb1(dice, turn, scores, escrow, piggybackable=False):
    """ takes the state of the game and returns a move

    returns a subset of dice to move to escrow, and an action
    """
    if piggybackable:
        return [], 'start fresh'
    if dice == []:
        return [], 'roll'
    new_value, to_escrow = options(dice)[0]
    if escrow + new_value >= 400:
        return to_escrow, 'bank'
    else:
        return to_escrow, 'roll'

def builder1(dice, turn, scores, escrow, piggybackable=False):
    """ takes the state of the game and returns a move

    returns a subset of dice to move to escrow, and an action
    """
    if piggybackable:
        return [], 'roll'
    if dice == []:
        return [], 'roll'
    new_value, to_escrow = options(dice)[0]
    if escrow + new_value >= 400:
        return to_escrow, 'bank'
    else:
        return to_escrow, 'roll'


def rational1(dice, turn, scores, escrow, buildable=False):
    def expected_value_next_roll(option):
        option_value, to_escrow = option
        if len(to_escrow) == len(dice): return escrow + option_value
        expected_value = { 1: 75, 2: 113, 3: 197, 4: 250, 5: 300, 6: 350 }
        pr_farkel = { 1: 0.6667, 2: 0.4444, 3: 0.2778, 4: 0.1574, 5: 0.0772, 6: 0.0231 }
        pr_next_roll = 1.0 - pr_farkel[len(dice) - len(to_escrow)]
        value_next_roll = escrow + option_value + expected_value[len(dice) - len(to_escrow)]
        return pr_next_roll * value_next_roll

    if buildable:
        if expected_value_next_roll((0, [])) < 350:
            return [], 'start fresh'
        else:
            return [], 'roll'
    if dice == []:
        return [], 'roll'

    choice = max(options(dice), key=expected_value_next_roll)
    if escrow + choice[0] >= expected_value_next_roll(choice):
        return choice[1], 'bank'
    else:
        return choice[1], 'roll'

def play_dice(players=[dumb1, dumb1], building=True, end_score=10000, rebuttals=True):
    """ one game of dice
    """

    finished = [False]*len(players)
    dice, turn, scores, escrow, piggybackable = [], 0, [0]*len(players), 0, False
    while not all(finished):
        # each loop is a roll, there may be multiple rolls per turn
        # a turn starts with dice presented to a player,
        # they must first choose what to escrow,
        # then whether to bank or roll
        # sometimes a player is presented with [] as dice
        # they must roll in this case?
        turn_over = False
        print "\nnew roll. scores: %s" % (scores,)
        # print "player %s is presented with dice: %s, and %s in escrow " % (turn, dice, escrow)
        to_escrow, action = players[turn](dice, turn, scores, escrow, piggybackable)
        # to_escrow is e.g. [1,2,2,2]
        for die in to_escrow:
            dice.remove(die)
        escrow += value(to_escrow)
        print "player %s escrows %s, now has %s points in escrow, and elects to " % (turn, to_escrow, escrow) + action
        if action == 'bank':
            turn_over = True
            piggybackable = True
            scores[turn] += escrow
            if not building:
                dice = []
                escrow = 0
        elif action in ["roll", "bottoms", "start fresh"]:
            piggybackable = False
            # all others are some kind of dice rolling
            if action == "start fresh":
                dice = []
                escrow = 0
            dice = roll(len(dice))
            dice.sort()
            print "player %s rolls %s " % (turn, dice)
            if action == "bottoms":
                dice = bottoms(dice)
                print "bottoms makes it %s !" % (dice,)

            if len(options(dice)) == 0: # fail to score: next turn
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
                    print "\n now entering rebuttals phase!\n"
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

def roll(num_dice):
    if num_dice == 0:
        num_dice = 6
    return [random.randint(1,6) for a in range(num_dice)]

def bottoms(dice):
    return [7 - die for die in dice]

def evaluate_strategies(players=[dumb1, dumb1, builder1], building=True, end_score=10000, rebuttals=True):
    wins = [0] * len(players)
    for i in range(100):
        # say the index 0 player wins
        order = range(len(players))
        random.shuffle(order) # order is now e.g. [2,0,1]
        shuffled_players = [players[i] for i in order]
        scores = play_dice(shuffled_players, building, end_score, rebuttals)
        shuffled_winner = max( (v, i) for i, v in enumerate(scores) )[1] # eg index 0 (was index 2)
        winner = order[shuffled_winner] # eg index 2
        wins[winner] += 1
    return wins

if __name__ == '__main__':
    print "\n\nfinal score: " + str(play_dice(players=[dumb1, rational1, manual], building=True))
    # print "\n\n wins: " + str(evaluate_strategies())
