from pymem import Pymem
from board import Board

class Game:
    def __init__(self, **modes):
        self.game_height = 20
        self.game_width = 10
        self.tiref_process = Pymem('tiref.exe')
        self.board = Board(self.game_height, self.game_width)
        self.state_cache = {
            "previous_time": self.get_time(),
            "currently_invis": False,
            "m_roll_reqs_checked": False
        }
        
        self.invis = "invis" in modes and modes["invis"]
        self.render = "render" in modes and modes["render"]
        
    # main method of the game, updates state cache and performs operations accordingly
    
    def update_state(self):
        # if the game is ending, reset flags
        if self.state_cache["previous_time"] > 0 and self.get_time() == 0:
            print("Resetting state cache")
            self.state_cache["currently_invis"] = False
            self.state_cache["m_roll_reqs_checked"] = False
            self.state_cache["previous_time"] = 0
            
        if self.render: 
            self.get_board_and_render()
            
        if self.invis:
            # print(self.state_cache["previous_time"] == 0, self.get_time() > 0, self.get_level() != 999,self.is_master_mode())
            if self.state_cache["previous_time"] == 0 and self.get_time() > 0 and self.get_level() != 999 and self.is_master_mode():
                print("Enabling invis.")
                self.enable_invis()
                
            # m_roll_reqs_met() will raise "m_roll_reqs_checked" in the state cache when end_of_game_check is True. this check should only be 
            # performed once at the end of the game.
            if not self.state_cache["m_roll_reqs_checked"] and self.state_cache["currently_invis"] and self.get_level() == 999 and not self.m_roll_reqs_met(True):
                print("Disabling invis.")
                self.disable_invis()
        
        # update previous time, keep it 1 frame behind current time
        if self.state_cache["previous_time"] + 1 < self.get_time():
            self.state_cache["previous_time"] = self.get_time()
        
    def is_master_mode(self):
        return self.get_current_mode()[:2] == "02"
        
    def is_ingame(self):
        return self.get_time() > 0
        
    # this will raise the m-roll flag! this needs to be lowered at the end of the game or else you will get the m-roll when you shouldn't.
    def enable_invis(self):
        gameplay_flags = self.get_gameplay_flags()
        current_mode = self.get_current_mode()
        
        gameplay_flags = "4"+gameplay_flags[1]
        current_mode = "8"+current_mode[1]
        
        self.set_gameplay_flags(bytes.fromhex(gameplay_flags))
        self.set_current_mode(bytes.fromhex(current_mode))
        
        self.state_cache["currently_invis"] = True
    
    def disable_invis(self):
        gameplay_flags = self.get_gameplay_flags()
        current_mode = self.get_current_mode()
        
        gameplay_flags = "0"+gameplay_flags[1]
        current_mode = "0"+current_mode[1]
        
        self.set_gameplay_flags(bytes.fromhex(gameplay_flags))
        self.set_current_mode(bytes.fromhex(current_mode))
        
        self.state_cache["currently_invis"] = False
        
    # game info
    
    # level
    def get_level(self):
        return int.from_bytes(self.tiref_process.read_bytes(0x4AE300, 2), "little")
    
    # time in frames
    def get_time(self):
        return int.from_bytes(self.tiref_process.read_bytes(0x4AE33C, 2), "little")
    
    # get number of cools
    def get_cools(self):
        return int.from_bytes(self.tiref_process.read_bytes(0x4AE310, 1), "little")
    
    # internal TAP grades
    def get_internal_grade(self):
        return int.from_bytes(self.tiref_process.read_bytes(0x4ACD97, 1), "little")
        
    # gameplay flags
    # __4_ for mroll requirements met
    def get_gameplay_flags(self):
        return self.tiref_process.read_bytes(0x004AE31C, 2).hex()
        
    def set_gameplay_flags(self, b):
        self.tiref_process.write_bytes(0x004AE31C, b, 1)
        
    # gameplay flags
    # __4_ for mroll requirements met
    def get_current_mode(self):
        return self.tiref_process.read_bytes(0x004AE32A, 2).hex()
        
    def set_current_mode(self, b):
        self.tiref_process.write_bytes(0x004AE32A, b, 1)

    # we only want to check this once at the end of the game. we don't accidentally want to disable the roll when we shouldn't. 
    # true: m roll requirements met
    # false: m roll requirements not met
    def m_roll_reqs_met(self, end_of_game_check = False):
        if end_of_game_check and self.state_cache["m_roll_reqs_checked"]:
            return
            
        if end_of_game_check and not self.state_cache["m_roll_reqs_checked"]:
            self.state_cache["m_roll_reqs_checked"] = True
            
        return self.get_cools() == 9 and self.get_internal_grade() >= 27
    
    # board stuff
    def get_cell(self, cell_base):
        return int.from_bytes(self.tiref_process.read_bytes(cell_base, 1), "little")
       
    def get_board(self):
        temp_board_list = []
        base = 0x004AB9A8
        
        # from the top of the board
        for row in range(19, 19 - self.game_height, -1):
            row_base = base + (0x60 * row)
            
            for cell in range (0, self.game_width):
                cell_base = row_base + (0x8 * cell)
                
                temp_board_list.append(self.get_cell(cell_base))
                
        return temp_board_list
        
    def get_board_and_render(self):
        self.board.list_format_to_board_and_render(self.get_board())
