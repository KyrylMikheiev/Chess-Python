class Pawn:
    def __init__(self):
        pass
    
    def validate_pawn_check(self, direction, enemy_color):
        players_pawns_directions = ((-1, -1), (-1, +1))
        enemys_pawns_directions = ((+1, -1), (+1, +1))
        if self.is_players_color_white and enemy_color == "w" or not self.is_players_color_white and enemy_color == "b":
            return direction in enemys_pawns_directions
        else:
            return direction in players_pawns_directions
        
        