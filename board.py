from gamescreen import GameScreen

"""
The Board class represents a 2D grid used for storing the state of 
TIREF's game board. It exists to plug into GameScreen.

It initializes a board with default values and provides methods to 
access and modify the board state. The class includes methods to 
retrieve cell values, clear the board, and update the board from a 
list of cell values.
"""
class Board:
    def __init__(self, height=20, width=10):
        self.default_cell = 0
        self.height = height
        self.width = width
        
        self.board = [[self.default_cell for i in range(width)] for i in range(height)]
        
        self.gamescreen = GameScreen(height, width)

    def __getitem__(self, item):
        return self.board[item]

    # return False if cell is empty
    def get_cell(self, row, column):
        cell = self.board[row][column]
        return cell if cell <= 8 and cell >= 2 else False
    
    def clear(self):
        self.board = [[self.default_cell for i in range(self.width)] for i in range(self.height)]
        
    def list_format_to_board_and_render(self, cells):
        if len(cells) != self.width*self.height:
            raise ValueError(f"Expected list of length 200, got {len(cells)} instead")
            
        for cell_index, cell in enumerate(cells):
            row_index = cell_index // 10
            col_index = cell_index % 10

            self.board[row_index][col_index] = cell
            
        self.gamescreen.render(self)
    