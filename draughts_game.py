import colorama
from colorama import Fore, Back, Style
import os

colorama.init()

class Player:
    pieces = []
    def __init__(self,name,p_color,num):
        self.name = name
        self.p_color = p_color
        self.num = num
        self.pieces = []
    
    def get_name_player(self):
        return self.name
    
    def add_piece(self,piece):
        self.pieces.append(piece)

    def remove_piece(self,piece):
        if piece in self.pieces:
            self.pieces.remove(piece)

    def get_amount_pieces(self):
        return len(self.pieces)

    def get_last_piece(self):
        return self.pieces[-1]
    
    def get_player_color(self):
        return self.p_color
    
    def get_player_num(self):
        return self.num


class Piece:
    
    def __init__(self,p_color,player_num):
        self.player_num = player_num
        self.p_color = p_color
    
    def get_piece_color(self):
        return self.p_color
    
    def get_player_num(self):
        return self.player_num




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
    
    def get_piece_player_num(self):
        return self.piece.get_player_num()

    def get_piece(self):
        return self.piece


class Board:

    def __init__(self,size_m = 8):
        self.matrix = []
        self.size_m = size_m

    def generate_squares(self,player1,player2):
        i = True
        for y in range(0,self.size_m):
            aux = []
            for x in range(0,self.size_m):
                if y < (self.size_m/2) -1 or y >= (self.size_m/2) + 1:                        
                    if i:
                        aux.append(Square(Fore.WHITE))
                        i = False
                    else:
                        if y > self.size_m/2:
                            player1.add_piece(Piece(player1.get_player_color(),player1.get_player_num()))
                            aux.append(Square(Fore.RED,player1.get_last_piece()))
                        else:
                            player2.add_piece(Piece(player2.get_player_color(),player2.get_player_num()))
                            aux.append(Square(Fore.RED,player2.get_last_piece()))
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

    def draw_matrix(self):
        clear = lambda: os.system('clear')
        clear()
        draw_b = ''
        reset = Style.RESET_ALL
        con = 0
        for a in range(1,self.size_m+1):
            draw_b += str(a) + ' '
        draw_b += '\n'
        for row in self.matrix:
            for col in row:
                if col.is_piece_inside():
                    draw_b += col.piece_color() + '© ' + reset
                else:
                    draw_b += col.color + '■ '+ reset
            con += 1
            draw_b += '|'+str(con) +'\n'
        print(draw_b)

    def move_piece(self,from_x,from_y,to_x,to_y,player_turn,opponent):
        
        dif_y,dir_y = difference_between_and_direction(from_y,to_y)
        dif_x,dir_x = difference_between_and_direction(from_x,to_x)

        if dif_x == 0 or dif_y == 0 or not self.coordinates_is_in_range(from_x,from_y) or not self.coordinates_is_in_range(to_x,to_y):
            return self.wrong(player_turn)
        
        if self.matrix[from_y][from_x].is_piece_inside():
        
            if self.matrix[from_y][from_x].get_piece_player_num() == player_turn:
                if self.matrix[to_y][to_x].is_piece_inside():
                    return self.wrong(player_turn)
        
                else:
                    if dif_x > 2 or dif_y > 2 or dif_x != dif_y:
                        return self.wrong(player_turn)
                    
                    elif dif_x == 2:
                        if self.matrix[to_y - dir_y][to_x - dir_x].is_piece_inside():
                            if self.matrix[to_y - dir_y][to_x - dir_x].get_piece_player_num() != player_turn:
                                opponent.remove_piece(self.matrix[to_y - dir_y][to_x - dir_x].get_piece())
                                self.matrix[to_y - dir_y][to_x - dir_x].deallocate_piece()

                        else:
                            return self.wrong(player_turn)
                    
                    elif dif_x == 1:
                        if player_turn == 1:
                            if from_y < to_y:
                                return self.wrong(player_turn)
                
                        else:
                            if from_y > to_y:
                                return self.wrong(player_turn)
                                
                    self.matrix[to_y][to_x].assign_piece(self.matrix[from_y][from_x].piece)
                    self.matrix[from_y][from_x].deallocate_piece()
                    self.draw_matrix()
        
                    if player_turn == 1:
                        player_turn = 2
        
                    else:
                        player_turn = 1

                    return player_turn
        
            else:
                return self.wrong(player_turn,'Wrong piece')
        
        else:
            return self.wrong(player_turn)

    def wrong(self,pt,message = 'Wrong coordinates'):
        self.draw_matrix()
        print(message)
        return pt
    
    def verify_forced_movements(self):
        pass
        
    def get_matrix(self):
        return self.matrix
    
    def coordinates_is_in_range(self,x,y):
        if (x < self.size_m and x > 0) and (y <self.size_m and y > 0):
            return True
        return False


def difference_between_and_direction(a,b):
    if a > b:
        return a - b,-1
    else:
        return b - a,+1


while True:
    name_player1 = input('Write name of player number 1: ')
    name_player2 = input('Write name of player number 2: ')
    player1 = Player(name_player1,Fore.GREEN,1)
    player2 = Player(name_player2,Fore.YELLOW,2)
    board = Board(12)
    board.generate_squares(player1,player2)
    board.draw_matrix()
    player_turn = player1.get_player_num()
    while player1.get_amount_pieces() > 0 or player2.get_amount_pieces() > 0:
        if player_turn == player1.get_player_num():
            print(player1.get_name_player() + ' Turn ' +str(player1.get_amount_pieces()) + ' Pieces' )
            opponent = player2
        else:
            print(player2.get_name_player() + ' Turn ' +str(player2.get_amount_pieces()) + ' Pieces' )
            opponent = player1
        print('Enter the coordinates (x, y) of the tab to move')
        from_x = int(input('x: ')) - 1
        from_y = int(input('y: ')) - 1
        print('Enter the coordinates (x, y) of where to move')
        to_x = int(input('x: ')) - 1
        to_y = int(input('y: ')) - 1
        if from_x == -1 and from_y == -1:
            break
        player_turn =board.move_piece(from_x,from_y,to_x,to_y,player_turn,opponent)
    salir = input('Write \'s\' if you want to end the game: ')
    if salir == 's' or salir == 'S':
        break