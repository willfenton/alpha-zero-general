from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from .AmazonsLogic import Board
import numpy as np

class AmazonsGame(Game):

    # DONE
    def __init__(self, n):
        self.n = n
        b = Board(self.n)
        self.move_dict = b.construct_move_dict()
        self.num_actions = len(self.move_dict) // 2

    # DONE
    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.n)
        pieces = np.array(b.pieces)
        return self.decompose(pieces)

    # DONE
    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    # DONE
    def getActionSize(self):
        # return number of actions
        return self.num_actions

    # DONE
    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        b = Board(self.n)
        b.pieces = np.copy(self.recompose(board))
        move = self.move_dict[action]
        b.execute_move(move, player)
        return (self.decompose(b.pieces), -player)

    # DONE
    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0]*self.getActionSize()
        b = Board(self.n)
        b.pieces = np.copy(self.recompose(board))
        legalMoves =  b.get_legal_moves(player)
        for move in legalMoves:
            valids[self.move_dict[move]] = 1
        return np.array(valids)

    # DONE
    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        b = Board(self.n)
        b.pieces = np.copy(self.recompose(board))

        p1_has_legal_moves = b.has_legal_moves(player)
        p2_has_legal_moves = b.has_legal_moves(-player)

        if p1_has_legal_moves and p2_has_legal_moves:
            return 0
        if p1_has_legal_moves and not p2_has_legal_moves:
            return 1
        return -1

    # DONE
    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        if player == 1:
            return board
        else:
            b = board.copy()
            b[1] = board[0].copy()
            b[0] = board[1].copy()
            return b

    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert(len(pi) == self.num_actions)
        pi_board = np.reshape(pi[:-1], (self.n, self.n))
        l = []

        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(board, i)
                newPi = np.rot90(pi_board, i)
                if j:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)
                l += [(newB, list(newPi.ravel()) + [pi[-1]])]
        return l

    # DONE
    def stringRepresentation(self, board):
        return board.tostring()

    def decompose(self, board):
        white = np.zeros(board.shape)
        white[board == 1] = 1
        black = np.zeros(board.shape)
        black[board == -1] = 1
        arrows = np.zeros(board.shape)
        arrows[board == 2] = 1
        return np.stack((white, black, arrows), axis=0).astype(np.int64)
    
    def recompose(self, board):
        recomposed = np.zeros(board[0].shape).astype(np.int64)
        recomposed[board[0] == 1] = 1
        recomposed[board[1] == 1] = -1
        recomposed[board[2] == 1] = 2
        return recomposed

    def display(self, board):
        pieces = self.recompose(board)
        print()
        print("   -" + "-" * (3 * self.n) + "-")
        for y in range(self.n - 1, -1, -1):
            print("{:2} |".format(y + 1), end="")
            for x in range(self.n):
                piece = pieces[x][y]
                if piece == -1: print(" B ", end="")
                elif piece == 1: print(" W ", end="")
                elif piece == 2: print(" X ", end="")
                else: print(" . ", end="")
            print("|")
        print("   -" + "-" * (3 * self.n) + "-")
        print("    ", end="")
        for i in range(self.n):
            print(" {} ".format(chr(i + 65)), end="")
        print('\n')
