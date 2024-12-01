from game import Game
import threading
import time, random

game = Game(invis=True)

while True:
    game.update_state()
    
# todo - clean up this file