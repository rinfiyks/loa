# Largely copied from here: http://aima.cs.berkeley.edu/python/games.html

def alphabeta_search(board, d=2):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""
    infinity = 1.0e400

    cutoff_test = lambda board, depth: depth >= d or board.is_terminal_state()

    def max_value(board, alpha, beta, depth):
        if cutoff_test(board, depth):
            return board.score()
        v = -infinity
        for next_move in board.get_available_moves():
            v = max(v, min_value(next_move, alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(board, alpha, beta, depth):
        if cutoff_test(board, depth):
            return board.score()
        v = infinity
        for next_move in board.get_available_moves():
            v = min(v, max_value(next_move, alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    chosen_board = argmax(board.get_available_moves(),
       lambda next_board: min_value(next_board, -infinity, infinity, 0))

    return chosen_board

def argmax(seq, fn):
    """Return an element with lowest fn(seq[i]) score; tie goes to first one.
    >>> argmax(['one', 'to', 'three'], len)
    'three'
    """
    best = seq[0]; best_score = -fn(best)
    for x in seq:
        x_score = -fn(x)
        if x_score < best_score:
            best, best_score = x, x_score
    return best
