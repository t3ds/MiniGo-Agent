import random
import sys
import heapq
from read import readInput
from write import writeOutput
from host import GO
#from host import GO, readInput, writeOutput

class AlphaBeta():
    def __init__(self):
        self.depth = 5

    def get_input(self, go, piece_type):

        possible_placements = []
        for i in range(go.size):
            for j in range(go.size):

                if go.valid_place_check(i, j, piece_type, test_check = True):
                    heapq.heappush(possible_placements, self.get_input(go, piece_type, i, j))
                    #possible_placements.append()

        if go.valid_place_check(2,2,piece_type, test_check = True):
            return (2,2)
        
        if possible_placements and possible_placements[0][0] == 0:
        
            for i in range(5):
                if i == 2:
                    continue
                if go.valid_place_check(i,i,piece_type, test_check = True):
                    return (i,i)

        if not possible_placements:
            return "PASS"

        else:
            action = self.max_level(go, piece_type, float('inf'), float('-inf'), possible_placements, 0, 0, self.depth)
            print(action)
            return action[1]

    def max_level(self, go, piece_type, alpha, beta, possible_placements, dead_player, dead_opp, depth):

        move = "PASS"
        val  = float('-inf')
        if go.game_end(piece_type) or depth == 0:
            utility = self.heuristics(go, piece_type, dead_player, dead_opp)

            if piece_type ==2:
                utility += go.komi

            return utility, move

        for _, dead_pl, board, action in possible_placements:

            deads_opp += len(go.find_died_pieces(3 - piece_type))
            board.died_pieces = dead_pl
            next_moves = []
            for i in range(go.size):
                for j in range(go.size):

                    if go.valid_place_check(i, j, 3-piece_type, test_check = True):
                        heapq.heappush(next_moves, self.get_input(board, 3- piece_type, i, j))
            
            next_val, next_move  = self.min_level(board, 3-piece_type, alpha, beta, next_moves, dead_opp, dead_player, depth-1)

            if next_val >val:
                val = next_val
                move = next_move
            if val>=beta:
                return val, move

            alpha = max(val, alpha)
        return val, move


    def min_level(self, go, piece_type, alpha, beta, possible_placements, dead_player, dead_opp, depth):

        move = "PASS"
        val  = float('-inf')
        if go.game_end(3-piece_type) or depth == 0:
            utility = self.heuristics(go, piece_type, dead_player, dead_opp)

            if piece_type ==2:
                utility += go.komi

            return -1*utility, move

        for _, dead_pl, board, action in possible_placements:

            deads_opp += len(go.find_died_pieces(3 - piece_type))
            board.died_pieces = dead_pl
            next_moves = []
            for i in range(go.size):
                for j in range(go.size):

                    if go.valid_place_check(i, j, 3-piece_type, test_check = True):
                        heapq.heappush(next_moves, self.get_input(board, 3- piece_type, i, j))
            
            next_val, next_move  = self.max_level(board, 3-piece_type, alpha, beta, next_moves, dead_opp, dead_player, depth-1)

            if next_val < val:
                val = next_val
                move = next_move
            if val<=alpha:
                return val, move

            beta = min(val, beta)
        return val, move


    def heuristic(self, go ,piece_type,dead_players, dead_opponents):
        player, opponent = 0,0
        
        for i in range(go.size):
            for j in range(go.size):
                if go.board[i][j] == piece_type:
                    player += self.count_liberty(i, j, go)
                elif go.board[i][j] == 3 - piece_type:
                    opponent += self.count_liberty(i, j, go)

        player_score = player + go.score(piece_type) + dead_opponents * 10
        opponent_score = opponent + go.score(3 - piece_type) - dead_players * 16

        return player_score - opponent_score


    def get_moves(self, go, piece_type, i, j):

        board = go.copy_board()
        board.place_chess(i,j,piece_type)
        died_pieces = board.remove_died_pieces(3-piece_type)
        num_dead = len(died_pieces)
        return (-1*num_dead, died_pieces, board, (i,j))

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
        
        if i == j:
            mult = 1
            
        elif i == 0 or i == go.size-1:
            if j == 0 or j == go.size-1:
                mult = 1

            else: mult = 0.8

        elif j == 0 or j == go.size-1:
            mult = 0.8

        return count*1


if __name__ == "__main__":
    N = 5
    piece_type, previous_board, board = readInput(N)
    go = GO(N)
    #print(go.score(piece_type))
    go.set_board(piece_type, previous_board, board)
    #print(go.score(piece_type))
    player = AlphaBeta()
    action = player.get_input(go, piece_type)
    
    writeOutput(action)
