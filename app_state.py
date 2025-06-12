class AppState:
    
    def __init__(self):
        self.running = True
        self.current_menu = "main"
        self.board = None
        self.is_players_color_white = None
        
    def get_running_state(self):
        return self.running
    
    def get_current_menu(self):
        return self.current_menu
    
    def get_board(self):
        return self.board
    
    def set_running_state(self, state):
        self.running = state
    
    def set_current_menu(self, menu):
        self.current_menu = menu
    
    def set_board(self, board):
        self.board = board