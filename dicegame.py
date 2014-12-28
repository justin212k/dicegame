# state: dice, turn, scores, escrow

def 

def dumb1(dice):
    if 1 in dice:
        return [1], 'roll'
    return [], 'bank'


def play_dice(players=[dumb1, dumb1]):
    dice, turn, scores, escrow = [], 0, [0]*len(players), 0
    while max(scores) < 10000:
        players