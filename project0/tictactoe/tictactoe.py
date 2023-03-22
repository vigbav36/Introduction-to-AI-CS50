"""
Tic Tac Toe Player
"""
from copy import deepcopy
import math

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

    for i in range (3):
         for j in range(3):
            
            if board[i][j] == X:
                count_x +=1

            if board[i][j] == O:
                count_o +=1

    if count_x > count_o:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action_list = list()

    for i in range (3):
         for j in range(3):

            if board[i][j] == EMPTY:
                action_list.append((i,j))

    return action_list


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_copy = deepcopy(board)

    x = action[0]
    y = action[1]

    if board_copy[x][y] != EMPTY:
        raise "invalid_move"
    else:
        if player(board) == X:
            board_copy[x][y] = X 
        else:   
            board_copy[x][y] = O

    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for score in [X, O]:
        for row in range(0, 3):
            if all(board[row][col] == score for col in range(0, 3)):
                return score

        for col in range(0, 3):
            if all(board[row][col] == score for row in range(0, 3)):
                return score

        diagonals = [[(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]]

        for diagonal in diagonals:
            if all(board[row][col] == score for (row, col) in diagonal):
                return score

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False
    
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1

    return 0
    
def min_max(board,min_move):

    if terminal(board):
        return utility(board)

    action_list = actions(board)

    if min_move == True:

        min_val = 999

        for action in action_list :
            min_val = min(min_val,min_max(result(board,action),False))
        
        return min_val

    else:
        max_val = -999
        
        for action in action_list :
            max_val = max(max_val,min_max(result(board,action),True))
        
        return max_val


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board) :
        return None
    
    turn = player(board)
    action_list = actions(board)

    if turn == 'X':

        best_val = -999
        best_action = ()

        for action in action_list:
            
            val = min_max(result(board,action),True)

            if val>best_val:
                best_val = val
                best_action = action

        return best_action
        
    else:

        best_val = 999
        best_action = ()

        for action in action_list:
            
            val = min_max(result(board,action),False)

            if val<best_val:
                best_val = val
                best_action = action

        return best_action
