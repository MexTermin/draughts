import colorama
from colorama import Fore, Back, Style
colorama.init()

class Player:
    
    def __init__(self,name,p_color):
        self.name = name
        self.p_color = p_color
    
    def get_name_player(self):
        return self.name


class Piece:
    
    def __init__(self,player):
        self.player = player
    
    def get_piece_color(self):
        return self.player.p_color



class Square:
    
    def __init__(self,color,piece = None):
        self.color = color
        self.piece = piece

    def assign_piece(self,piece):
        self.piece = piece

    def deallocate_piece(self):
        self.piece =  None
    
    def is_piece_inside(self):
        return self.piece != None

    def piece_color(self):
        return self.piece.get_piece_color()

    def get_piece(self):
        return self.piece


class Board:
    
    matrix = []
    def __inti___(self):
        self.matrix = []

    def generate_squares(self,player1,player2):
        i = True
        for y in range(0,8):
            aux = []
            for x in range(0,8):
                if y < (8/2) -1 or y >= (8/2) + 1:                        
                    if i:
                        aux.append(Square(Fore.WHITE))
                        i = False
                    else:
                        if y > 8/2:
                            aux.append(Square(Fore.RED,Piece(player1)))
                        else:
                            aux.append(Square(Fore.RED,Piece(player2)))
                        i = True
                else:
                    if i:
                        aux.append(Square(Fore.WHITE))
                        i = False
                    else:
                        aux.append(Square(Fore.RED))   
                        i = True                    
            if i:
                i = False
            else:
                i = True
            self.matrix.append(aux)
    
    def get_matrix(self):
        return self.matrix


player1 = Player('Jose',Fore.GREEN)
player2 = Player('Carlos',Fore.YELLOW)
reset = Style.RESET_ALL
board = Board()
board.generate_squares(player1,player2)
b_matrix = board.get_matrix()
b_matrix[3][0].assign_piece(b_matrix[2][1].piece)
b_matrix[2][1].deallocate_piece()

draw_b = ''
for row in b_matrix:
    for col in row:
        if col.is_piece_inside():
            draw_b += col.piece_color() + '@ ' + reset
        else:
            draw_b += col.color + '0 '+ reset
    draw_b += '\n'
#         if col.is_piece_inside():
#             draw_b += str(col.piece.get_piece_color) + '@ ' + str(reset)
#         else:
#             draw_b += str(col.color) + '0 ' + str(reset)
#     draw_b += '\n'
print(draw_b)




# Set the color semi-permanentlys
# red = Fore.RED
# yellow = Fore.YELLOW
# cyan = Fore.CYAN
# reset = Style.RESET_ALL

# mensaje = red + "klk" + reset + yellow + " hola "+ reset
# print(mensaje)