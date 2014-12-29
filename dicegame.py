# state: dice, turn, scores, escrow

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

def dumb1(dice):
    if 1 in dice:
        return [1], 'roll'
    return [], 'bank'


def play_dice(players=[dumb1, dumb1]):
    dice, turn, scores, escrow = [], 0, [0]*len(players), 0
    while max(scores) < 10000:
        players