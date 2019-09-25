#Class of piece
class Piece:
    #Set the character of normal pieces
    character = "©"
    #Init method to save piece values
    def __init__(self,p_color):
        self.p_color = p_color
    #Method to return piece color    
    def get_piece_color(self):
        return self.p_color
    #Method to return piece character  
    def get_character(self):
        return self.character