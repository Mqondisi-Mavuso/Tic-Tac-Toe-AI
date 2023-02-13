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
    total_X = sum(x.count(X) for x in board)
    total_O = sum(o.count(O) for o in board)

    if total_X == 0 and total_O == 0 and actions(board) != 0:       # when it's the start of the game
        return X

    if total_X == total_O and actions(board) != 0:
        return X

    elif total_O < total_X and actions(board) != 0:
        return O
    else:
        return "The game is already Over!"


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_moves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_moves.add((i, j))

    if possible_moves is not None:
        return possible_moves

    return None


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    deep_copy_board = copy.deepcopy(board)
    if action in actions(deep_copy_board):
        deep_copy_board[action[0]][action[1]] = player(deep_copy_board)

    return deep_copy_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    num_X = 0
    num_O = 0
    # horizontal traversal
    for row in range(3):
        for col in range(3):
            if board[row][col] == "X":
                num_X += 1
            elif board[row][col] == "O":
                num_O += 1
            if num_O == 3 and num_X < 3:
                return "O"
            elif num_X == 3 and num_O < 3:
                return "X"
        else:
            num_O = 0
            num_X = 0

    num_X = 0
    num_O = 0
    # vertical traversal
    for row in range(3):
        for col in range(3):
            if board[col][row] == "X":
                num_X += 1
            elif board[col][row] == "O":
                num_O += 1
            if num_O == 3 and num_X < 3:
                return "O"
            elif num_X == 3 and num_O < 3:
                return "X"
        else:
            num_O = 0
            num_X = 0

    num_X = 0
    num_O = 0
    # diagonal traversal top left to bottom right
    for i in range(3):
        if board[i][i] == "X":
            num_X += 1
        elif board[i][i] == "O":
            num_O += 1
        if num_O == 3 and num_X < 3:
            return "O"
        elif num_X == 3 and num_O < 3:
            return "X"

    num_X = 0
    num_O = 0
    # diagonal traversal bottom left to top right
    count = 0
    for i in range(2, -1, -1):
        if board[i][count] == "X":
            num_X += 1
        elif board[i][count] == "O":
            num_O += 1
        if num_O == 3 and num_X < 3:
            return "O"
        elif num_X == 3 and num_O < 3:
            return "X"
        count += 1

    # This is for when it is a draw
    if actions(board) is None:
        return "Draw"

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) or actions(board) is None or actions(board) == "Draw":
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == "X":
        return 1
    elif winner(board) == "O":
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # for when the game is already over
    if terminal(board):
        return None

    all_possible_moves = actions(board)
    scores_of_move = {}
    best_move = None

    # for when "X" is playing, recall, "X" is trying to maximise
    if player(board) == "X":
        mxv = -math.inf
        for move in all_possible_moves:
            child_state = result(board, move)
            move_score = max_value(child_state)
            (best_move, mxv) = (move, move_score) if move_score > mxv else (best_move, mxv)
            scores_of_move[move] = move_score

    else:
        mxv = math.inf
        for move in all_possible_moves:
            child_state = result(board, move)
            move_score = min_value(child_state)
            (best_move, mxv) = (move, move_score) if move_score < mxv else (best_move, mxv)
            scores_of_move[move] = move_score
    return best_move


def max_value(the_board):
    """
    Return the maximum value after the terminal state
    """
    if terminal(the_board):                     # if we at the end of the game
        return utility(the_board)               # who is the winner

    v = -math.inf                               # negative infinite because we can always do better than this
    for action in actions(the_board):
        v = max(v, min_value(result(the_board, action)))
    return v


def min_value(the_board):
    """
    Returns the minimum value after the terminal state
    """
    if terminal(the_board):
        return utility(the_board)

    v = math.inf                # positive infinite because we can always do better than this
    for action in actions(the_board):
        v = min(v, max_value(result(the_board, action)))
    return v
