from MinimaxPlayer import MinimaxPlayer
from AlphaBetaPlayer import AlphaBetaPlayer
class LiteAlphaBetaPlayer(AlphaBetaPlayer):
    def heuristic(self):
        return 2*len(self.steps_available(self.loc))\
               - len(self.steps_available(self.opponent_loc))

