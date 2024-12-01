from game import Game
import threading
import time, random

game = Game(render=True, invis=True)

while True:
    game.update_state()
    
# todo - clean up this file