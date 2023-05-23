import random
import sys
from read import readInput
from write import writeOutput

from host import GO

class MinMax():
    def __init__(self):
        self.type = 'minimax'
        self.depth = 5
        self.search_depth = 0

    def get_input(self, go, piece_type):
        '''
        Get one input.

        :param go: Go instance.
        :param piece_type: 1('X') or 2('O').
        :return: (row, column) coordinate of input.
        '''        
        possible_placements = []
        for i in range(go.size):
            for j in range(go.size):
                if go.valid_place_check(i, j, piece_type, test_check = True):

                    possible_placements.append((i,j))


        if not possible_placements:
            return "PASS"

        elif go.n_move <2:
            print("HI")
            if go.valid_place_check(0, 0, piece_type, test_check = True):
                return (0,0)

            elif go.valid_place_check(0, go.size-1, piece_type, test_check = True):
                return (0,go.size-1)

            elif go.valid_place_check(go.size-1, 0, piece_type, test_check = True):
                return (go.size-1,0)

            elif go.valid_place_check(go.size-1, go.size-1, piece_type, test_check = True):
                return (go.size-1,go.size-1)

        else:
            self.depth -=1
            curMax, move = self.max_level(go, piece_type, float('-inf'), float('inf'), possible_placements, 0,0)
            return move

    def min_level(self, go, piece_type, alpha, beta, possible_placements, dead_opp, dead_pl):
        next_move = "PASS"
        if go.game_end(piece_type) or self.depth<0:

            player_libs, opponent_libs = self.calculate_liberties(go,piece_type)

            overall_utility = 0
            if piece_type == 2:
                overall_utility = go.komi
            player_utility = player_libs +go.score(piece_type) + dead_opp
            opp_utility = opponent_libs +go.score(3-piece_type) - dead_pl

            overall_utility = player_utility - opp_utility
            print("min")
            return -1*overall_utility, "PASS"
            


        else:

            val = float('inf')

            for place in possible_placements:
                board = go.copy_board()
                board.place_chess(place[0], place[1], piece_type)
                board.n_move += 1
                self.depth -= 1

                dead_opp += len(board.find_died_pieces(3 - piece_type))
                board.died_pieces = board.remove_died_pieces(3 - piece_type)

                enemy_placements = []
                for  i in range(go.size):
                    for j in range(go.size):
                        if go.valid_place_check(i, j, 3-piece_type, test_check = True):

                            enemy_placements.append((i,j))

                next_val, _ = self.max_level(board, 3-piece_type, alpha, beta, enemy_placements, dead_pl,dead_opp)

                if next_val < val:
                    val = next_val
                    next_move = place

                beta = min(beta, val)
                if alpha>= beta:
                    print("min in")
                    return val, next_move
            print("min out")
            return val, next_move

        

    def max_level(self, go, piece_type, alpha, beta, possible_placements, dead_opp, dead_pl):
        next_move = "PASS"
        if go.game_end(piece_type) or self.depth<0:

            player_libs, opponent_libs = self.calculate_liberties(go,piece_type)

            overall_utility = 0
            if piece_type == 2:
                overall_utility = go.komi
            player_utility = player_libs +go.score(piece_type) + dead_opp
            opp_utility = opponent_libs +go.score(3-piece_type) - dead_pl

            overall_utility = player_utility - opp_utility
            print("max")
            return overall_utility, "PASS"
            


        else:

            val = float('-inf')

            for place in possible_placements:
                board = go.copy_board()
                board.place_chess(place[0], place[1], piece_type)
                board.n_move += 1
                self.depth -= 1

                dead_opp += len(board.find_died_pieces(3 - piece_type))
                board.died_pieces = board.remove_died_pieces(3 - piece_type)

                enemy_placements = []
                for  i in range(go.size):
                    for j in range(go.size):
                        if go.valid_place_check(i, j, 3-piece_type, test_check = True):

                            enemy_placements.append((i,j))

                next_val, _ = self.min_level(board, 3-piece_type, alpha, beta, enemy_placements, dead_pl,dead_opp)

                if next_val > val:
                    val = next_val
                    next_move = place

                alpha = max(alpha, val)
                if alpha>= beta:
                    print("max in")
                    return val, next_move
            print("max Out")
            return val, next_move

        
    #def action(i,j,piece_type):
    #    return

    def count_liberties(self,i,j, go):

        count = 0
        mult = 1
        board = go.board
        ally_members = go.ally_dfs(i, j)
        for member in ally_members:
            neighbors = go.detect_neighbor(member[0], member[1])
            for piece in neighbors:
                # If there is empty space around a piece, it has liberty
                if board[piece[0]][piece[1]] == 0:
                    count+=1
        
        if i == 0 or i == go.size-1:
            if j == 0 or j == go.size-1:
                mult = 1.5

            else: mult = 1.25

        elif j == 0 or j == go.size-1:
            mult = 1.25

        return count*mult

    def calculate_liberties(self, go, piece_type):
        player_libs, opponent_libs = 0,0

        for i in range(go.size):
            for j in range(go.size):

                libs = self.count_liberties(i,j,go)
                if go.board[i][j] == piece_type:
                    player_libs += libs

                elif go.board[i][j] == 3- piece_type:
                    opponent_libs += libs

        return player_libs, opponent_libs

if __name__ == "__main__":
    N = 5
    piece_type, previous_board, board = readInput(N)
    go = GO(N)
    print(go.n_move)
    go.set_board(piece_type, previous_board, board)
    player = MinMax()
    action = player.get_input(go, piece_type)
    
    writeOutput(action)