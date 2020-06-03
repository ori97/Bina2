from AlphaBetaPlayer import AlphaBetaPlayer
DECIDING_AGENT=1
class OrderedAlphaBetaPlayer(AlphaBetaPlayer):
    def __init__(self):
        super(OrderedAlphaBetaPlayer, self).__init__()
        self.sorted_directions_list = None
    def get_sorted_directions_by_heuristic(self):
        return list(map(lambda a: a[0],sorted(self.sorted_directions_list,key= lambda a: a[1],reverse=True)))
    def choose_move(self,depth):
        max_value, max_value_move = float('-inf'), None
        if depth == 1:
            self.sorted_directions_list = [[(0, 1), 0], [(0, -1), 0], [(-1, 0), 0], [(1, 0), 0]]
        new_sorted_directions_list=[]
        for d in self.get_sorted_directions_by_heuristic():
            if self.check_move(self.loc,d):
                self.board[self.loc[0]+d[0],self.loc[1]+d[1]] = -1
                self.loc=self.loc[0]+d[0],self.loc[1]+d[1]
                cur_minimax_val = self.minimax(depth-1,3-DECIDING_AGENT)
                new_sorted_directions_list.append([d,cur_minimax_val])
                if cur_minimax_val >= max_value:
                    max_value=cur_minimax_val
                    max_value_move = d
                self.board[self.loc] = 0
                self.loc = self.loc[0] - d[0], self.loc[1] - d[1]
        self.sorted_directions_list=new_sorted_directions_list
        return max_value_move