from AlphaBetaPlayer import AlphaBetaPlayer
class HeavyAlphaBetaPlayer(AlphaBetaPlayer):
    def heuristic(self):
        return self.number_of_reachable_nodes(self.loc) \
               - self.number_of_reachable_nodes(self.opponent_loc)