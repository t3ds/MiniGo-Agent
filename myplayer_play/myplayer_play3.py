import random
import sys
import heapq
from read import readInput
from write import writeOutput
from host import GO
#from host import GO, readInput, writeOutput

class AlphaBeta():
    def __init__(self, moves):
        self.depth = 5
        self.move = moves

    def get_input(self, go, piece_type):

        possible_placements = []
        c = 1
        for i in range(go.size):
            for j in range(go.size):

                if self.check_neighbors(go, i, j, piece_type) and go.valid_place_check(i, j, piece_type, test_check = True):
                    heapq.heappush(possible_placements, self.get_moves(go, piece_type, i, j, c))
                    c+=1
                    #possible_placements.append()
        #print(possible_placements)
        if go.valid_place_check(2,2,piece_type, test_check = True):
            return (2,2)
        '''print(possible_placements[0][0])
        if possible_placements and possible_placements[0][0] == 0:
        
            for i in range(5):
                if i == 2:
                    continue
                if go.valid_place_check(i,i,piece_type, test_check = True):
                    return (i,i)'''

        if not possible_placements:
            #print("HI")
            return "PASS"

        else:
            action = self.max_level(go, piece_type, float('-inf'), float('inf'), possible_placements, 0, 0, self.depth)
            #print(action)
            return action[1]

    def max_level(self, go, piece_type, alpha, beta, possible_placements, dead_player, dead_opp, depth):

        #print(depth)
        move = "PASS"
        val  = float('-inf')
        if go.game_end(piece_type) or depth == 0:
            utility = self.heuristic(go, piece_type, dead_player, dead_opp)

            if piece_type ==2:
                utility += go.komi

            return utility, move

        while possible_placements:
            _, _,dead_pl, board, action  = heapq.heappop(possible_placements)
            #print()

            dead_opp += len(go.find_died_pieces(3 - piece_type))
            board.died_pieces = dead_pl
            next_moves = []
            c=1
            for i in range(go.size):
                for j in range(go.size):
                    
                    if self.check_neighbors(board, i, j, 3 -piece_type) and board.valid_place_check(i, j, 3-piece_type, test_check = True):
                        heapq.heappush(next_moves, self.get_moves(board, 3- piece_type, i, j,c))
                        c+=1
            #print("HEY")
            next_val, next_move  = self.min_level(board, 3-piece_type, alpha, beta, next_moves, dead_opp, dead_player, depth-1)
            #print("max", next_val, next_move)
            if next_val > val:
                
                val = next_val
                move = action
                #print(move)
            
            if val>=beta:
                #print(val,beta)
                return val, move
            alpha = max(val, alpha)
            
            
        return val, move


    def min_level(self, go, piece_type, alpha, beta, possible_placements, dead_player, dead_opp, depth):
        #print(depth)
        move = "PASS"
        val  = float('inf')
        if go.game_end(3-piece_type) or depth == 0:
            utility = self.heuristic(go, piece_type, dead_player, dead_opp)

            if piece_type ==2:
                utility += go.komi

            return -1*utility, move

        while possible_placements:
            _, _,dead_pl, board, action  = heapq.heappop(possible_placements)

            dead_opp += len(go.find_died_pieces(3 - piece_type))
            board.died_pieces = dead_pl
            next_moves = []
            c=1
            for i in range(go.size):
                for j in range(go.size):

                    if self.check_neighbors(board, i, j, 3- piece_type) and board.valid_place_check(i, j, 3-piece_type, test_check = True):
                        heapq.heappush(next_moves, self.get_moves(board, 3- piece_type, i, j,c))
                        c+=1
            #print("HI")
            next_val, next_move  = self.max_level(board, 3-piece_type, alpha, beta, next_moves, dead_opp, dead_player, depth-1)
            #print("min", next_val, next_move)
            if next_val < val:
                
                val = next_val
                move = action
                #print(move)
            
            if val<=alpha:
                #print(alpha,val)
                return val, move
            beta = min(val, beta)
            #print(alpha,beta)
            
        return val, move


    def heuristic(self, go ,piece_type,dead_players, dead_opponents):
        player, opponent = 0,0
        
        for i in range(go.size):
            for j in range(go.size):
                if go.board[i][j] == piece_type:
                    player += self.count_liberties(i, j, go)
                elif go.board[i][j] == 3 - piece_type:
                    opponent += self.count_liberties(i, j, go)

        player_score = player + go.score(piece_type) + dead_opponents * 10
        opponent_score = opponent + go.score(3 - piece_type) - dead_players * 16

        return player_score - opponent_score


    def get_moves(self, go, piece_type, i, j,c):

        board = go.copy_board()
        board.place_chess(i,j,piece_type)
        died_pieces = board.remove_died_pieces(3-piece_type)
        num_dead = len(died_pieces)
        #print(num_dead)
        return (-1*num_dead, c, died_pieces, board, (i,j))

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
            mult = 1.2
            
        elif i == 0 or i == go.size-1:
            if j == 0 or j == go.size-1:
                mult = 1.1

            else: mult = 0.8

        elif j == 0 or j == go.size-1:
            mult = 0.8

        return count*mult

    def check_neighbors(self,go,i,j, piece_type):
        if go.board[i][j] == 0:
            neighbors = go.detect_neighbor(i, j)
            for piece in neighbors:
            
                if go.board[piece[0]][piece[1]] == 3 - piece_type:
                    return True
            
        return False

if __name__ == "__main__":
        N = 5
        piece_type, previous_board, board = readInput(N)
        go = GO(N)
        #print(go.score(piece_type))
        go.set_board(piece_type, previous_board, board)
        #print(go.score(piece_type))
        
        with open('moves.txt', 'r') as f:
            moves = f.read()
            
            moves = int(moves)

        print(go.n_move)  
        moves += 1
        if moves>25:
            moves = 1
        player = AlphaBeta(moves)
        action = player.get_input(go, piece_type)
        moves += 1
        with open('moves.txt', 'w') as f:
            f.write(str(moves))
        writeOutput(action)
