"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_x = 0
    count_o = 0
    # Count X, O in board
    for j in board:
        for i in j:
            if i == X:
                count_x += 1
            if i == O:
                count_o += 1
    # X get the first move
    if count_x == 0:
        return X
    elif count_x <= count_o:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible = set()
    for i, b in enumerate(board):
        for j, c in enumerate(b):
            if c == EMPTY:
                act = (i, j)
                possible.add(act)
    return possible


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    cp = copy.deepcopy(board)
    lst = [0, 1, 2]
    if action[0] not in lst or action[1] not in lst:
        raise Exception("Negative out-of-bounds move")
    play = player(board)
    if board[action[0]][action[1]] != EMPTY:
        raise Exception("Invalid move")
    cp[action[0]][action[1]] = play
    return cp


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for p in [X, O]:
        for i in board:
            if len([j for j in i if j == p]) == 3:
                return p
        if board[0][0] == board[1][1] == board[2][2] == p or board[0][2] == board[1][1] == board[2][0] == p:
            return p
        for i in range(3):
            count = 0
            for j in range(3):
                count += 1 if board[j][i] == p else 0
            if count == 3:
                return p
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    else:
        for i in board:
            if EMPTY in i:
                return False
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    match winner(board):
        case "X":
            return 1
        case "O":
            return -1
        case _:
            return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None
    match player(board):
        case "X":
            win = 1
        case "O":
            win = -1
    maxi = []

    for action in actions(board):
        if win == 1:
            m = min_value(result(board, action))
            if m == win:
                return action
            elif m == 0:
                maxi.append(action)
        else:
            m = max_value(result(board, action))
            if m == win:
                return action
            elif m == 0:
                maxi.append(action)
    if len(maxi) > 0:
        return maxi[0]


def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v
