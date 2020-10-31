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
    playerXMoves = 0
    playerOMoves = 0

    for rows in board:
        for element in rows:
            if (element != EMPTY):
                if (element == X):
                    playerXMoves += 1
                else:
                    playerOMoves += 1
    
    return (O if playerXMoves > playerOMoves else X)


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    i = 0

    for row in board:
        j = 0

        for element in row:
            if board[i][j] == EMPTY:
                actions.add((i, j))
        
            j += 1
        
        i += 1

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if (board[action[0]][action[1]] != EMPTY):
        raise Exception('Invalid Move')

    copiedBoard = copy.deepcopy(board)
    copiedBoard[action[0]][action[1]] =  player(board)

    return copiedBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winner = None

    #check rows
    for row in board:
        if (len(set(row))) == 1 and row[0] != EMPTY:
            winner = X if row[0] == X else O
    
    #check diagonals
    if len(set([board[i][i] for i in range(len(board))])) == 1 and board[0][0] != EMPTY:
        winner = X if board[0][0] == X else O

    if len(set([board[i][len(board)-i-1] for i in range(len(board))])) == 1 and board[0][2] != EMPTY and board[1][1] != EMPTY and board[2][0] != EMPTY:
        winner = X if board[0][2] == X else O
    
    #check columns
    for col in range(0, 3):
        if len(set([board[0][col], board[1][col], board[2][col]])) == 1 and  board[0][col] != EMPTY:
            winner = X if board[0][col] == X else O

    return winner

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if (winner(board) != None):
        return True

    for row in board:
        if EMPTY in row:
            return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    gameWinner = winner(board)

    return (0 if gameWinner == None else (-1 if gameWinner == O else 1))


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if (terminal(board)):
        return None

    if (player(board) == X):
        maxValueForBoard = maxValue(board)
        return maxValueForBoard['action']
    else:
        minValueForBoard = minValue(board)
        return minValueForBoard['action']

def maxValue(board):
    if (terminal(board)):
        return {'value': utility(board)}

    value = -999
    moves = {}

    for action in actions(board):
        oldValue = value
        value = max(value, minValue(result(board, action))['value'])

        if (oldValue != value):
            moves[value] = action

    return {'value': value, 'action': moves[value]}

def minValue(board):
    if (terminal(board)):
        return {'value': utility(board)}

    value = 999
    moves = {}

    for action in actions(board):
        oldValue = value
        value = min(value,  maxValue(result(board, action))['value'])

        if (oldValue != value):
            moves[value] = action

    return {'value': value, 'action': moves[value]}