import time as t
import functools as tls
import random as rand
import numpy as np
from MinimaxPlayer import MinimaxPlayer
class AlphaBetaPlayer(MinimaxPlayer):
    """
    def __init__(self):
        super(AlphaBetaPlayer, self).__init__()
    """
    def heuristic(self):
        # return np.abs(self.loc[0]-self.opponent_loc[0])+np.abs(self.loc[1]-self.opponent_loc[1])
        fictur = [self.count_zeroes(), 3, 6]
        weights = [1, 0, 0]
        hueristics = [self.number_of_reachable_nodes(self.loc)- self.number_of_reachable_nodes(self.opponent_loc),
                      len(self.steps_available(self.loc)) - len(self.steps_available(self.opponent_loc)),
                      2 * len(self.steps_available(self.loc)) - len(self.steps_available(self.opponent_loc))]
        return tls.reduce(lambda x, y: x + y, list(map(lambda a, b, c: a * b / c, hueristics, weights, fictur)))
        # return self.simple_player_heuristic(player)
        #return self.simple_player_heuristic(player)
    def minimax(self, depth, player, leafs_count=[0], alpha=float('-inf'), beta=float('inf')):
        game_is_won, winning_player = self.is_game_won()
        leafs_count[0] += 1  # assert that is leaf - change it after the last elif statement
        if self.game_is_tied():
            return 0
        elif game_is_won:
            if winning_player == DECIDING_AGENT:
                return float("inf")
            else:
                return float("-inf")
        elif depth == 0:
            return self.heuristic()  # Todo change hueristic
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
                    minimax_val = self.minimax(depth - 1, 3 - player, leafs_count, alpha, beta)
                    cur_max = max(minimax_val, cur_max)
                    alpha = max(cur_max, alpha)
                    self.loc = loc_temp
                    self.board[i, j] = 0
                    if cur_max >= beta:
                        return float("inf")
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
                    minimax_val = self.minimax(depth - 1, 3 - player, leafs_count, alpha, beta)
                    cur_min = min(cur_min, minimax_val)
                    beta = min(cur_min, beta)
                    self.opponent_loc = loc_temp
                    self.board[i, j] = 0
                    if cur_min <= alpha:
                        return float("-inf")
            return cur_min
DECIDING_AGENT = 1
"""
class AlphaBetaPlayer():
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
                    self.opponent_loc = (i, j)

    # returns the steps available for player in location loc

    def steps_available(self, loc):
        steps_available = []
        for d in self.directions:
            i = loc[0] + d[0]
            j = loc[1] + d[1]
            if 0 <= i < len(self.board) and 0 <= j < len(self.board[0]) and self.board[i][j] == 0:  # then move is legal
                steps_available.append(d)
        return steps_available

    # boolean function, returns True if game is tied, false if not

    def game_is_tied(self):
        return len(self.steps_available(self.loc)) == 0 and \
               len(self.steps_available(self.opponent_loc)) == 0

    # boolean function, return True if game is won, and int the indicates the player who won.
    # returns:
    # bool: game_is_over
    # int: 1 - Player 1 won. 2 - Player 2 won.

    def is_game_won(self):
        if self.game_is_tied():
            return False, None
        my_available_steps = self.steps_available(self.loc)
        opp_available_steps = self.steps_available(self.opponent_loc)
        if len(my_available_steps) == 0:
            return True, 2
        if len(opp_available_steps) == 0:
            return True, 1
        return False, None

    def check_move(self, loc, move=(0, 0)):
        i = loc[0] + move[0]
        j = loc[1] + move[1]
        return 0 <= i < len(self.board) and 0 <= j < len(self.board[0]) and self.board[i][j] == 0

    def number_of_reachable_nodes(self, loc):
        visited = []
        queue = []
        queue.append(loc)
        count_reachable = 0
        while len(queue) > 0:
            head_loc = queue[0]
            visited.append(head_loc)
            queue.remove(head_loc)
            for d in self.directions:
                i, j = head_loc[0] + d[0], head_loc[1] + d[1]
                if (i, j) not in visited and (i, j) not in queue and self.check_move((i, j)):
                    queue.append((i, j))
                    count_reachable += 1
        return count_reachable

    def count_zeroes(self):
        counter = 0
        for i, row in enumerate(self.board):
            for j, val in enumerate(row):
                if val == 0:
                    counter += 1
        return counter

    def simple_player_heuristic(self, player):
        number_of_legal_moves = self.steps_available(self.loc)
        if len(number_of_legal_moves) == 0:
            return float('-inf')
        else:
            return 4 - len(number_of_legal_moves)

    def heuristic(self):
        # return np.abs(self.loc[0]-self.opponent_loc[0])+np.abs(self.loc[1]-self.opponent_loc[1])
        # return rand.randrange(10)
        fictur = [self.count_zeroes(), 3, 6]
        weights = [1, 0, 1]
        hueristics = [self.number_of_reachable_nodes(self.loc),
                      len(self.steps_available(self.loc)) - len(self.steps_available(self.opponent_loc)),
                      2 * len(self.steps_available(self.loc)) - len(self.steps_available(self.opponent_loc))]
        return tls.reduce(lambda x, y: x + y, list(map(lambda a, b, c: a * b / c, hueristics, weights, fictur)))
        # return self.simple_player_heuristic(player)

    def set_rival_move(self, loc):
        self.board[loc] = -1
        self.opponent_loc = loc

    def minimax(self, depth, player, leafs_count=[0], alpha=float('-inf'), beta=float('inf')):
        game_is_won, winning_player = self.is_game_won()
        leafs_count[0] += 1  # assert that is leaf - change it after the last elif statement
        if self.game_is_tied():
            return 0
        elif game_is_won:
            if winning_player == DECIDING_AGENT:
                return float("inf")
            else:
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
                    minimax_val = self.minimax(depth - 1, 3 - player, leafs_count,alpha,beta)
                    cur_max = max(minimax_val,cur_max)
                    alpha = max(cur_max, alpha)
                    self.loc = loc_temp
                    self.board[i, j] = 0
                    if cur_max >= beta:
                        return float("inf")
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
                    minimax_val = self.minimax(depth - 1, 3 - player, leafs_count,alpha,beta)
                    cur_min=min(cur_min,minimax_val)
                    beta = min(cur_min, beta)
                    self.opponent_loc = loc_temp
                    self.board[i, j] = 0
                    if cur_min <= alpha:
                        return float("inf")
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
    def make_move(self, time):
        time_start = t.time()
        d = 1
        leafs_count = [0]
        move = self.choose_move(d)
        last_iteration_time = t.time() - time_start
        next_iteration_max_time = 3 * last_iteration_time
        time_until_now = t.time() - time_start
        DEBUG = False
        while time_until_now + next_iteration_max_time < time or (DEBUG and d < 9940):
            d += 1
            iteration_start_time = t.time()
            leafs_count[0] = 0
            move = self.choose_move(d)
            last_iteration_time = t.time() - iteration_start_time
            next_iteration_max_time = 3 * last_iteration_time
            time_until_now = t.time() - time_start

        self.loc = (self.loc[0] + move[0], self.loc[1] + move[1])
        self.board[self.loc] = -1
        return move
"""

