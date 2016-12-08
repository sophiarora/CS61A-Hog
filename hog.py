"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100 # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################

def roll_dice(num_rolls, dice=six_sided):
    """Roll DICE for NUM_ROLLS times.  Return either the sum of the outcomes,
    or 1 if a 1 is rolled (Pig out). This calls DICE exactly NUM_ROLLS times.

    num_rolls:  The number of dice rolls that will be made; at least 1.
    dice:       A zero-argument function that returns an integer outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    dice_nums, k=[],0
    while k< num_rolls:
        new_dice=[dice()]
        dice_nums, k=dice_nums+new_dice, k+1
    def sum_list(a):
        sum_num, n=0, 0
        while n<len(a):
            sum_num, n=sum_num+a[n], n+1
        return sum_num
    if 1 in dice_nums:
        total=1
    else:
        total=sum_list(dice_nums)
    return total


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free bacon).

    opponent_score:  The total score of the opponent.
    num_rolls:       The number of dice rolls that will be made.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    def beacon(x):
        return 1+abs(x//10 - x%10)
    if num_rolls!=0:
        turn_num = roll_dice(num_rolls,dice)
    else:
        turn_num = beacon(opponent_score)
    return turn_num

def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    """
    if (score+opponent_score)%7==0:
        dice=four_sided
    else:
        dice=six_sided
    return dice

def bid_for_start(bid0, bid1, goal=GOAL_SCORE):
    """Given the bids BID0 and BID1 of each player, returns three values:

    - the starting score of player 0
    - the starting score of player 1
    - the number of the player who rolls first (0 or 1)
    """
    assert bid0 >= 0 and bid1 >= 0, "Bids should be non-negative!"
    assert type(bid0) == int and type(bid1) == int, "Bids should be integers!"

    # The buggy code is below-corrected
    if bid0 == bid1:
        start0, start1, who_first = goal, goal, "tie"
    elif abs(bid0-bid1)==5:
        if bid0>bid1:
            start0, start1, who_first = 10 ,0, 0
        else:
            start0,  start1,who_first = 0, 10, 1
    else:
        if bid0>bid1:
            start0, start1, who_first = bid1, bid0, 0
        else:
            start0, start1, who_first = bid1, bid0, 1
    return start0, start1, who_first

def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who

def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    who = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    while score1 < goal and score0 < goal:
        def current_strategy(x):
            if x == 1:
                strategy_current_player = strategy1
            else:
                strategy_current_player = strategy0
            return strategy_current_player
        def score(x):
            if x == 1:
                score_player=score1
            else:
                score_player=score0
            return score_player
        score_current_player = take_turn(current_strategy(who)(score(who), score(other(who))), score(other(who)), select_dice(score(who), score(other(who))))
        if who == 0:
            score0, score1=score_current_player + score0, score1
        else:
            score0, score1=score0, score1 + score_current_player
        if score0==2*score1 or score1==2*score0:
            score0, score1=score1, score0
        who = other(who)
    return score0, score1 # You may want to change this line.
def always(n):
    return always_roll(n)

#######################
# Phase 2: Strategies #
#######################

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy

# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    6.0

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 1.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 6.0.
    """
    def average_dice(*args):
        sum_fn , k = 0, 0
        while k < num_samples:
            sum_fn, k = fn(*args) + sum_fn, k+1
        return sum_fn/num_samples
    return average_dice

def max_scoring_num_rolls(dice=six_sided):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE.  Assume that dice always
    return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    result, k = 1, 1
    max_average = make_averaged(roll_dice, 1000)(k, dice)
    while k < 10:
        k = k+1
        max_average_new = make_averaged(roll_dice, 1000)(k, dice)
        if max_average_new > max_average:
            max_average = max_average_new
            result = k
        else:
            result = result + 0
    return result

def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1

def average_win_rate(strategy, baseline=always_roll(5)):
    """Return the average win rate (0 to 1) of STRATEGY against BASELINE."""
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)
    return (win_rate_as_player_0 + win_rate_as_player_1) / 2 # Average results

def run_experiments():
    """Run a series of strategy experiments and report results."""
    if False: # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False: # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False: # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if True: # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if False: # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"

# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    def beacon(x):
        return 1+abs(x//10 - x%10)
    bacon_opponent = beacon(opponent_score)
    if bacon_opponent >= margin:
        result = 0
    else:
        result = num_rolls
    return result

def swap_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice when it would result in a beneficial swap and
    rolls NUM_ROLLS if it would result in a harmful swap. It also rolls
    0 dice if that gives at least MARGIN points and rolls
    NUM_ROLLS otherwise.
    """
    def beacon(x):
        return 1+abs(x//10 - x%10)
    bacon_opponent = beacon(opponent_score)
    if (bacon_opponent + score)*2 == opponent_score:
        result = 0
    elif bacon_opponent >= margin and bacon_opponent + score != opponent_score*2:
        result = 0
    else:
        result = num_rolls
    return result


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    "*** YOUR CODE HERE ***"
    return 5 # Replace this statement


##########################
# Command Line Interface #
##########################

# Note: Functions in this section do not need to be changed.  They use features
#       of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')
    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
