from MapsGenerator import ai_board
import numpy as np
from MinimaxPlayer import MinimaxPlayer
from AlphaBetaPlayer import AlphaBetaPlayer
from OrderedAlphaBetaPlayer import OrderedAlphaBetaPlayer
from LiteAlphaBetaPlayer import LiteAlphaBetaPlayer, HeavyAlphaBetaPlayer
import matplotlib.pyplot as plt

def play_for_player(player):
    times = []
    depths = []
    for t in np.linspace(0.1, 3, 50):
        player.set_game_params(ai_board.copy())
        d = player.make_move(t)
        times.append(t)
        depths.append(d)
    plt.scatter(times, depths)
    plt.show()
play_for_player(LiteAlphaBetaPlayer())
play_for_player(HeavyAlphaBetaPlayer())
