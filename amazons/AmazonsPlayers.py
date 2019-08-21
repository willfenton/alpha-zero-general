import numpy as np


class RandomPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        while valids[a] != 1:
            a = np.random.randint(self.game.getActionSize())
        return a


class HumanAmazonsPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        while True:
            a = input()
            if a in self.game.move_dict.keys() and self.game.getValidMoves(board, 1)[self.game.move_dict[a]] == 1:
                a = self.game.move_dict[a]
                break
            else:
                print('Invalid')
        return a


# class GreedyAmazonsPlayer():
#     def __init__(self, game):
#         self.game = game

#     def play(self, board):
#         valids = self.game.getValidMoves(board, 1)
#         candidates = []
#         for a in range(self.game.getActionSize()):
#             if valids[a]==0:
#                 continue
#             nextBoard, _ = self.game.getNextState(board, 1, a)
#             score = self.game.getScore(nextBoard, 1)
#             candidates += [(-score, a)]
#         candidates.sort()
#         return candidates[0][1]
