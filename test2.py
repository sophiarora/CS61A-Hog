from test import take_turn, other, select_dice
GOAL_SCORE = 100
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
        score_current_player = take_turn(current_strategy(who), score(other(who)), select_dice(score(who), score(other(who))))
        if who == 0:
            score0, score1=score_current_player+score0, score1
        else:
            score0, score1=score0, score1+score_current_player
        who = other(who)
    return score0, score1, who  # You may want to change this line.
def swine_swap(score0, score1):
    if score0==2*score1 or score1==2*score0:
        score0, score1=score1, score0
    return score0, score1
