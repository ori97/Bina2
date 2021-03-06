import time as t
import random
import numpy as np
import functools as tls
from NotAnimatedGame import NotAnimatedGame
DECIDING_AGENT = 1
class MinimaxPlayer:
    def __init__(self):
        self.loc = None
        self.opponent_loc = None
        self.board = None
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    def set_game_params(self, board):
        self.board = board
        for i, row in enumerate(board):
            for j, val in enumerate(row):
                if val == 1:
                    self.loc = (i, j)
                elif val == 2:
                    self.opponent_loc =(i, j)

    """
    returns the steps available for player in location loc
    """
    def steps_available(self,loc):
        number_steps_available = []
        for d in self.directions:
            i = loc[0] + d[0]
            j = loc[1] + d[1]
            if 0 <= i < len(self.board) and 0 <= j < len(self.board[0]) and self.board[i][j] == 0:  # then move is legal
                number_steps_available.append(d)
        return number_steps_available
    """
    boolean function, returns True if game is tied, false if not
    """
    def game_is_tied(self):
        return len(self.steps_available(self.loc)) == 0 and\
               len(self.steps_available(self.opponent_loc)) == 0
    """
    boolean function, return True if game is won, and int the indicates the player who won.
    returns:
    bool: game_is_over
    int: 1 - Player 1 won. 2 - Player 2 won.
    """
    def is_game_won(self):
        if self.game_is_tied():
            return False, None
        my_available_steps=self.steps_available(self.loc)
        opp_available_steps = self.steps_available(self.opponent_loc)
        if len(my_available_steps) == 0:
            return True,2
        if len(opp_available_steps) == 0:
            return True,1
        return False, None

    def check_move(self, loc, move=(0,0)):
        i = loc[0] + move[0]
        j = loc[1] + move[1]
        return 0 <= i < len(self.board) and 0 <= j < len(self.board[0]) and self.board[i][j] == 0
    """
    calculating number of reacable nodes using BFS
    """
    def number_of_reachable_nodes(self,loc):
        queue=[]
        queue.append(loc)
        index=0
        while index < len(queue):
            head_loc = queue[index]
            index+=1
            for d in self.directions:
                i,j = head_loc[0] + d[0], head_loc[1]+d[1]
                if (i,j) not in queue and self.check_move((i,j)):
                    queue.append((i,j))

        return index
    def longest_route_till_block(self,loc,Hasam=10):
        if Hasam == 0:
            return 0
        max_path_length = 0
        for d in self.directions:
            if self.check_move(loc,d):
                self.board[loc[0]+d[0],loc[1]+d[1]]=-1
                cur_max_length=self.longest_route_till_block((loc[0]+d[0],loc[1]+d[1]),Hasam-1)+1
                self.board[loc[0]+d[0],loc[1]+d[1]]=0
                max_path_length=max(cur_max_length,max_path_length)
        return max_path_length
    def count_zeroes(self):
        counter = 0
        for i, row in enumerate(self.board):
            for j, val in enumerate(row):
                if val == 0:
                    counter += 1
        return counter
    def simple_player_heuristic(self,player):
        loc = (player == 1) * self.loc + (player == 2) * self.opponent_loc
        number_of_legal_moves=self.steps_available(loc)
        if len(number_of_legal_moves) == 0:
            return float('-inf')
        else:
            return 4 - len(number_of_legal_moves)

    def heuristic(self):
        # return np.abs(self.loc[0]-self.opponent_loc[0])+np.abs(self.loc[1]-self.opponent_loc[1])
        count_zeroes=self.count_zeroes()
        fictur = [count_zeroes, 9, count_zeroes]
        weights = [1, 0, 0]
        hueristics = [self.number_of_reachable_nodes(self.loc) - self.number_of_reachable_nodes(self.opponent_loc),
                      len(self.steps_available(self.loc)) - len(self.steps_available(self.opponent_loc)),
                      self.longest_route_till_block(self.loc)-self.longest_route_till_block(self.opponent_loc)]
        return tls.reduce(lambda x, y: x + y, list(map(lambda a, b, c: a * b / c, hueristics, weights, fictur)))
        # return self.simple_player_heuristic(player)
        #return self.simple_player_heuristic(player)
        """
        count = 0
        for d in self.directions:
            if self.check_move(self.loc,d):
                count+=1
        return count
        """
    def minimax(self, depth, player, leafs_count=[0]):
        game_is_won, winning_player = self.is_game_won()
        leafs_count[0] += 1  # assert that is leaf - change it after the last elif statement
        if self.game_is_tied():
            return 0
        elif game_is_won:
            if winning_player == DECIDING_AGENT and player != DECIDING_AGENT:
                return float("inf")
            elif winning_player != DECIDING_AGENT and player == DECIDING_AGENT:
                return float("-inf")
        elif depth == 0:
            return self.heuristic() # Todo change hueristic
        leafs_count[0] -= 1  # not a leaf
        if player == 1:
            cur_max = float("-inf")
            for d in self.directions:
                i = self.loc[0] + d[0]
                j = self.loc[1] + d[1]
                if 0 <= i < len(self.board) and 0 <= j < len(self.board[0]) and self.board[i][
                    j] == 0:  # if move is legal
                    self.board[i, j] = -1
                    loc_temp = self.loc
                    self.loc = (i, j)
                    minimax_val = self.minimax(depth - 1, 3 - player, leafs_count)
                    cur_max = max(minimax_val,cur_max)
                    self.loc = loc_temp
                    self.board[i, j] = 0
            return cur_max
        else:
            cur_min = float("inf")
            for d in self.directions:
                i = self.opponent_loc[0] + d[0]
                j = self.opponent_loc[1] + d[1]
                if 0 <= i < len(self.board) and 0 <= j < len(self.board[0]) and self.board[i][j] == 0:
                    self.board[i, j] = -1
                    loc_temp = self.opponent_loc
                    self.opponent_loc = (i, j)
                    minimax_val = self.minimax(depth - 1, 3 - player, leafs_count)
                    cur_min=min(cur_min,minimax_val)
                    self.opponent_loc = loc_temp
                    self.board[i, j] = 0
            return cur_min
    def choose_move(self,depth):
        max_value, max_value_move = float('-inf'), None
        for d in self.directions:
            if self.check_move(self.loc,d):
                self.board[self.loc[0]+d[0],self.loc[1]+d[1]] = -1
                self.loc=self.loc[0]+d[0],self.loc[1]+d[1]
                cur_minimax_val = self.minimax(depth-1,3-DECIDING_AGENT)
                if cur_minimax_val >= max_value:
                    max_value=cur_minimax_val
                    max_value_move = d
                self.board[self.loc] = 0
                self.loc = self.loc[0] - d[0], self.loc[1] - d[1]
        return max_value_move
    def player_got_only_one_move(self):
        count_moves=0
        one_move = None
        for d in self.directions:
            if self.check_move(self.loc,d):
                count_moves+=1
                one_move = d
        if count_moves != 1:
            return None
        return one_move
    def make_move(self, time):
        time_start = t.time()
        only_move = self.player_got_only_one_move()
        if only_move is not None:
            move = only_move
        else:
            d = 1
            leafs_count=[0]
            move = self.choose_move(d)
            last_iteration_time = t.time()-time_start
            next_iteration_max_time = 4*last_iteration_time
            time_until_now = t.time() - time_start
            # DEBUG = self.loc == (1,6)
            DEBUG = False
            while time_until_now + next_iteration_max_time < time or (DEBUG and d<100):
                d+= 1
                iteration_start_time = t.time()
                leafs_count[0]=0
                move = self.choose_move(d)
                last_iteration_time = t.time()-iteration_start_time
                next_iteration_max_time = 4*last_iteration_time
                time_until_now = t.time() - time_start
            """
            if move is None:
                # print(self.board)
                exit()
            """
        self.loc=(self.loc[0]+move[0],self.loc[1]+move[1])
        self.board[self.loc] = -1
        return move

    def set_rival_move(self, loc):
        self.board[self.opponent_loc]=-1
        self.board[loc] = -1
        self.opponent_loc=loc
