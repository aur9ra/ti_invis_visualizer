import pygame, os

def load_mino_images():
        new_dict = {}
        for i in range(2,8+1):
            new_dict[i] = pygame.image.load(f"{str(i)}.png").convert()
        return new_dict

"""
Get the mino image corresponding to the cell memory address.
If none found, return default.
"""

def get_mino_image_or_default():
    return

"""
The GameScreen class is responsible for managing and rendering the visual
representation of the board using the Pygame library.

It initializes the Pygame environment, sets up the display window with
a specific resolution, and loads images for the different minos.

The class provides methods for drawing the game board based on the current
game state and handling basic events like quitting the game.

The render method is the main loop entry point, which handles event processing,
board rendering, and screen updates.
"""
class GameScreen:
    def __init__(self, height, width):
        pygame.init()
        
        self.height = height
        self.width = width

        self.screen = pygame.display.set_mode((16*self.width, 16*self.height))
        self.running = True
        
        self.mino_images = load_mino_images()
        self.active = True
        
    def __draw_board(self, board):
            for row_idx in range(self.height):
                for col_idx in range(self.width):
                    cell = board.get_cell(row_idx, col_idx)

                    # if the cell has nothing in it, just continue
                    if not cell:
                        continue

                    # if control flow gets here, the cell is full and can be drawn
                    # draw an image here
                    self.screen.blit(self.mino_images[cell], (col_idx*16,row_idx*16))
                
    def render(self, board):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            if not self.running:
                pygame.quit()

        self.screen.fill((0, 0, 0)) 
        self.__draw_board(board)
        pygame.display.flip()  # Update the display
                    
            
                    