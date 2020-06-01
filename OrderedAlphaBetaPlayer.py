from AlphaBetaPlayer import AlphaBetaPlayer
DECIDING_AGENT=1
class OrderedAlphaBetaPlayer(AlphaBetaPlayer):
    def get_sorted_directions_by_heuristic(self):
        sorted_directions_list=[]
        for d in self.directions:
            if self.check_move(self.loc,d):
                i,j = self.loc[0]+d[0],self.loc[1]+d[1]
                self.board[i,j]=-1
                self.loc=i,j
                sorted_directions_list.append((d,self.heuristic()))
                self.loc=i-d[0],j-d[1]
                self.board[i,j]=0
        return list(map(lambda a: a[0],sorted(sorted_directions_list,key= lambda a: a[1],reverse=True)))
    def choose_move(self,depth):
        max_value, max_value_move = float('-inf'), None
        for d in self.get_sorted_directions_by_heuristic():
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