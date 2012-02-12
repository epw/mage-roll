#! /usr/bin/python

import random, sys

def d10():
    return random.randint (1, 10)

def roll (dice, difficulty=6, output=True):
    rolls = []
    ones = 0
    for t in range(dice):
        rolls.append (d10())
        while rolls[-1] == 10:
            rolls.append (d10())
        if rolls[-1] == 1:
            ones += 1
    if difficulty != None:
        successes = len(filter (lambda x: x >= difficulty, rolls))
    else:
        successes = None
    if output:
        print "Difficulty:", difficulty
        print "Roll:", rolls
        if difficulty != None:
            if successes == 0:
                print "Botch!"
            else:
                successes -= ones
                if successes < 0:
                    successes = 0
                print "Successes:", successes
    else:
        if successes != None:
            successes -= ones
    return (successes, rolls)

if __name__ == "__main__":
    dice = None
    difficulty = 6

    if len(sys.argv) >= 2:
        dice = int(sys.argv[1])
    if len(sys.argv) >= 3:
        if sys.argv[2] == "none":
            difficulty = None
        else:
            difficulty = int(sys.argv[2])

    roll (dice, difficulty)
