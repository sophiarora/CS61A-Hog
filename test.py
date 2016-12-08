"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact


def roll_dice(num_rolls,dice=six_sided):
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    dice_nums, k=[],0
    while k< num_rolls:
        new_dice=[dice()]
        dice_nums, k=dice_nums+new_dice, k+1
    if 1 in dice_nums:
        total=1
    else:
        total=sum(dice_nums)
    return total

def take_turn(num_rolls, opponent_score, dice=six_sided):
    def beacon(x):
        return 1+abs(x//10 - x%10)
    if num_rolls!=0:
        turn_num = roll_dice(num_rolls,dice)
    else:
        turn_num = beacon(opponent_score)
    return turn_num

def select_dice(score, opponent_score):
    if (score+opponent_score)%7==0 and (score+opponent_score) != 0:
        dice=four_sided
    else:
        dice=six_sided
    return dice

GOAL_SCORE = 100
def bid_for_start(bid0, bid1, goal=GOAL_SCORE):
    assert bid0 >= 0 and bid1 >= 0, "Bids should be non-negative!"
    assert type(bid0) == int and type(bid1) == int, "Bids should be integers!"
    if bid0 == bid1:
        start0, start1, who_first = goal, goal, "tie"
    elif abs(bid0-bid1)==5:
        if bid0>bid1:
            start0, start1, who_first = 10 ,0, 0
        else:
            start0, start1,who_first = 0, 10, 1
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
            score0, score1=score_current_player+score0, score1
        else:
            score0, score1=score0, score1+score_current_player
        if score0==2*score1 or score1==2*score0:
            score0, score1=score1, score0
        who = other(who)
    return score0, score1
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

def make_averaged(fn, num_samples=1000):
    def average_dice(*args):
        sum_fn , k = 0, 0
        while k < num_samples:
            sum_fn, k = fn(*args) + sum_fn, k+1
        return sum_fn/num_samples
    return average_dice

def max_scoring_num_rolls(dice=six_sided):
    result, k = 1, 1
    max_average = make_averaged(roll_dice, 100)(k, dice)
    while k < 10:
        k = k+1
        max_average_new = make_averaged(roll_dice, 100)(k, dice)
        if max_average_new > max_average:
            max_average = max_average_new
            result = k
        else:
            result = result + 0
    return result
