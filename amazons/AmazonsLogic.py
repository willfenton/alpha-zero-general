# 1 = white, -1 = black, 0 = empty, 2 = blocked

class Board():
    # list of all 8 directions on the board, as (x,y) offsets
    __directions = [(1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1), (0,1)]

    def __init__(self, n=4):
        "Set up initial board configuration."

        self.n = n

        assert(4 <= self.n <= 12)

        # Create the empty board array.
        self.pieces = [[0 for y in range(self.n)] for x in range(self.n)]

        # Set up the initial Amazons
        if self.n == 4:
            white = [(1, 0), (0, 2)]
            black = [(2, 3), (3, 1)]

        elif self.n == 10:
            white = [(0, 3), (3, 0), (6, 0), (9, 3)]
            black = [(0, 6), (3, 9), (6, 9), (9, 6)]

        starting_positions = {
            4: {"white" : [(1, 0), (0, 2)], "black" : [(2, 3), (3, 1)]},
            5: {"white" : [(0, 1), (1, 0), (3, 0), (4, 1)], "black" : [(0, 3), (1, 4), (3, 4), (4, 3)]},
            6: {"white" : [(0, 1), (1, 0), (4, 0), (5, 1)], "black" : [(0, 4), (1, 5), (4, 5), (5, 4)]},
            7: {"white" : [(0, 2), (2, 0), (4, 0), (6, 2)], "black" : [(0, 4), (2, 6), (4, 6), (6, 4)]},
            8: {"white" : [(0, 2), (2, 0), (5, 0), (7, 2)], "black" : [(0, 5), (2, 7), (5, 7), (7, 5)]},
            9: {"white" : [(0, 2), (2, 0), (6, 0), (8, 2)], "black" : [(0, 6), (2, 8), (6, 8), (8, 6)]},
            10: {"white" : [(0, 3), (3, 0), (6, 0), (9, 3)], "black" : [(0, 6), (3, 9), (6, 9), (9, 6)]},
            11: {"white" : [(0, 3), (3, 0), (7, 0), (10, 3)], "black" : [(0, 7), (3, 10), (7, 10), (10, 7)]},
            12: {"white" : [(0, 3), (3, 0), (8, 0), (11, 3)], "black" : [(0, 8), (3, 11), (8, 11), (11, 8)]},
        }

        for x, y in starting_positions[self.n]["white"]:
            self.pieces[x][y] = 1

        for x, y in starting_positions[self.n]["black"]:
            self.pieces[x][y] = -1
            
    # add [][] indexer syntax to the Board
    def __getitem__(self, index): 
        return self.pieces[index]
    
    def count_diff(self, color):
        count = 0
        for x in range(self.n):
            for y in range(self.n):
                if self[x][y] == color:
                    count += 1
                if self[x][y] == -color:
                    count -= 1
        return count
    
    def pack_move(self, x1, y1, x2, y2, x3, y3):
        return '-'.join([chr(x1+65)+str(y1+1), chr(x2+65)+str(y2+1), chr(x3+65)+str(y3+1)])

    def unpack_move(self, move):
        coords = move.split('-')
        unpacked = []
        for c in coords:
            unpacked.append(ord(c[0])-65)
            unpacked.append(int(c[1:])-1)
        return unpacked
    
    def expand_moves(self, x1, y1):
        valid_coords = set(range(self.n))
        
        assert(x1 in valid_coords)
        assert(y1 in valid_coords)
        assert(self[x1][y1] in (-1, 1))

        moves = []
        
        for x2_delta, y2_delta in self.__directions:
            x2 = x1
            y2 = y1
            while True:
                x2 += x2_delta
                y2 += y2_delta
                
                if x2 not in valid_coords or y2 not in valid_coords:
                    break
                if self[x2][y2] != 0:
                    break
                    
                for x3_delta, y3_delta in self.__directions:
                    x3 = x2
                    y3 = y2
                    while True:
                        x3 += x3_delta
                        y3 += y3_delta
                        
                        if x3 not in valid_coords or y3 not in valid_coords:
                            break
                        if self[x3][y3] != 0 and not (x3 == x1 and y3 == y1):
                            break
                            
                        moves.append(self.pack_move(x1, y1, x2, y2, x3, y3))
        return moves
    
    def get_legal_moves(self, colour):
        moves = []
        for x in range(self.n):
            for y in range(self.n):
                if self[x][y] == colour:
                    moves += self.expand_moves(x, y)
        return moves
    
    def has_legal_moves(self, colour):
        for x in range(self.n):
            for y in range(self.n):
                if self[x][y] == colour:
                    if len(self.expand_moves(x, y)) > 0:
                        return True
        return False
    
    def execute_move(self, move, colour):
        x1, y1, x2, y2, x3, y3 = self.unpack_move(move)
        assert(self[x1][y1] == colour)
        self[x2][y2] = self[x1][y1]
        self[x1][y1] = 0
        self[x3][y3] = 2

    def is_valid_move(self, x1, y1, x2, y2):
        if x1 == x2 and y1 == y2:
            return False
        if x1 == x2 and y1 != y2:
            return True
        if x1 != x2 and y1 == y2:
            return True
        if (x2 - x1) == (y2 - y1):
            return True
        if (x2 - x1) == -1 * (y2 - y1):
            return True
        return False
    
    def all_valid_moves(self):
        valid_moves = []
        for x1 in range(self.n):
            for y1 in range(self.n):
                for x2 in range(self.n):
                    for y2 in range(self.n):
                        for x3 in range(self.n):
                            for y3 in range(self.n):
                                if self.is_valid_move(x1, y1, x2, y2) and self.is_valid_move(x2, y2, x3, y3):
                                    valid_moves.append(self.pack_move(x1, y1, x2, y2, x3, y3))
        return valid_moves

    def construct_move_dict(self):
        valid_moves = self.all_valid_moves()
        move_dict = {}
        for i in range(len(valid_moves)):
            move_dict[valid_moves[i]] = i
            move_dict[i] = valid_moves[i]
        return move_dict