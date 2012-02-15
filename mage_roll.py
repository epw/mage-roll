import random, re, sys

def d10():
    "Simulate rolling one ten-sided die, returning the integer result. (Will output 10 but not 0)"
    return random.randint (1, 10)

def roll (dice, difficulty=6, count_rerolled_ones=False, output=False):
    """ roll (dice, difficulty=6, count_rerolled_ones=False, output=False)
    => (successes, rolls)

Simulate rolling dice using revised old/classic World of Darkness rules.
Ones subtract successes, and tens explode. Ones but no successes causes a
botch.

dice - Size of dice pool (number of dice being rolled)
difficulty - Minimum value counted as a success [default 6]
count_rerolled_ones - Whether ones on rerolls from tens should subtract
    successes [default False]
output - Whether to print results to stdout [default False]
"""

    rolls = []
    ones = 0
    for t in range(dice):
        rolls.append (d10())
        if rolls[-1] == 1:
            ones += 1
        while rolls[-1] == 10:
            rolls.append (d10())
            if count_rerolled_ones and rolls[-1] == 1:
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

def parse_roll (param, prefix="", count_rerolled_ones=False):
    """Parse a string with a roll expression and execute it. Roll expressions begin
with the number of dice, are followed by a / or the word "diff", and end
with the roll's difficulty. The second two parts can be left out if desired,
resulting in only the dice results being reported.

The optional prefix argument is outputted inside the [] in the output.

The argument count_rerolled_ones, defaulting to False, is passed on to the
roll() function, and designates whether ones rerolled because of exploding tens
should count against the total number of successes."""

    regex = re.match (r'\s*(\d+)\s*(?:diff|[/])\s*(\d+)', param)
    diff = None
    botch = False
    if regex:
        diff = int(regex.group(2))
        result = roll (int(regex.group(1)), diff, count_rerolled_ones)
    else:
        regex = re.match (r'(\d+)', param)
        if regex:
            diff = None
            result = roll (int(regex.group(1)), diff, count_rerolled_ones)
        else:
            return None
    rolls = ' '.join (map (str, result[1]))
    successes = result[0]
    if successes != None:
        if successes < 0:
            successes = 0
        if diff:
            if successes == 0 and not filter (lambda r: r >= diff, result[1]) \
               and len (filter (lambda r: r == 1, result[1])) > 0:
                botch = True
    else:
        return "[%s%s]: %s" % (prefix, param, rolls)

    botchstr = ""
    if botch:
        botchstr = " BOTCH!"
    return "[%s%s]: %s; successes: %d%s" % (prefix, param, rolls, successes,
                                            botchstr)
