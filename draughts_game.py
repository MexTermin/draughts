class Player:
    
    def __init__(self,name):
        self.name = name


class Piece:
    
    def __init__(self,player):
        self.player = player


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


class Board:

    matrix =[]
    
    def __inti___(self,size = 8):
        self.size = size

    def generate_squares(self,player1,player2):
        self.matrix = []
        for y in range(0,self.size):
            aux = []
            for x in range(0,self.size):
                if x%2 == 0:
                    aux.append(Square('white'))
                else:
                    if y > self.size/2:
                        aux.append(Square('red',Piece(player1)))
                    else:
                        aux.append(Square('red',Piece(player2)))
            self.matrix.append(aux)

import colorama
from colorama import Fore, Back, Style
colorama.init()

# Set the color semi-permanently
red = Fore.RED
yellow = Fore.YELLOW
cyan = Fore.CYAN
reset = Style.RESET_ALL

mensaje = red + "klk" + reset + yellow + " hola "+ reset
print(mensaje)

