import colorama
from colorama import Fore, Back, Style
from player import Player
from piece import Piece
from queen_piece import Queen_piece
from square import Square
import os
#Class of board
class Board:

    #Init method to save board values
    def __init__(self,size_m = 8):
        self.matrix = []
        self.size_m = size_m

    #Method to generate the squares inside the board according to the size of the board and with the pieces where they correspond
    def generate_squares(self,player1,player2):

        #Variable for roaming between white and red squares
        i = True
        for y in range(0,self.size_m):
            aux = []
            x = 0
            while x < self.size_m:

                #If to leave 2 rows of empty squares
                if y < (self.size_m/2) -1 or y >= (self.size_m/2) + 1:                        
                    if i:
                        aux.append(Square(Fore.WHITE))
                        i = False
                    else:

                        #If to choose which player will own the piece
                        if y > self.size_m/2:
                            player1.add_piece(Piece(player1.get_player_color()))
                            aux.append(Square(Fore.RED,player1.get_last_piece()))
                        else:
                            player2.add_piece(Piece(player2.get_player_color()))
                            aux.append(Square(Fore.RED,player2.get_last_piece()))
                        i = True
                else:
                    if i:
                        aux.append(Square(Fore.WHITE))
                        i = False
                    else:
                        aux.append(Square(Fore.RED))   
                        i = True
                x += 1

            #If to begin every row with a different color of square
            if i:
                i = False
            else:
                i = True
            self.matrix.append(aux)

    #Method to draw the board
    def draw_matrix(self):
        clear = lambda: os.system('clear')
        clear()
        draw_b = 'x→ '
        reset = Style.RESET_ALL
        con = 0
        for a in range(1,self.size_m+1):
            draw_b += str(a) + ' '
        draw_b += ' y↓'
        draw_b += '\n'
        for row in self.matrix:
            draw_b += '   '
            for col in row:
                if col.is_piece_inside():
                    piece_string = col.get_piece().get_character() +' '
                    draw_b += col.piece_color() + piece_string+ reset
                else:
                    draw_b += col.color + '■ '+ reset
            con += 1
            draw_b += '|'+str(con) +'\n'
        print(draw_b)

    #Method to move a piece in the board
    def move_piece(self,from_x,from_y,to_x,to_y,playing,opponent):

        #Variables that establish difference of squares and the direction that the piece is trying to move
        dif_y,dir_y = self.difference_between(from_y,to_y), self.direction(from_y,to_y)
        dif_x,dir_x = self.difference_between(from_x,to_x), self.direction(from_x,to_x)
        
        #If to verify that the movement being attempted is correct
        if not self.verify_moves(from_x,from_y,to_x,to_y,playing,dif_x,dif_y,dir_y):
            return self.wrong(playing)
        
        #If to verify if the piece tries to move two squares which means that it tries to eat
        if dif_x == 2:
        
            #If to verify if the piece can eat
            if not self.piece_can_eat(from_x,from_y,to_x,to_y,playing,dir_x,dir_y):
                return self.wrong(playing)
        
            #If the piece can eat it proceeds to make the move and eliminate the attacked piece of the opponent and the board
            opponent.remove_piece(self.matrix[to_y - dir_y][to_x - dir_x].get_piece())
            self.matrix[to_y - dir_y][to_x - dir_x].deallocate_piece()
            self.matrix[to_y][to_x].assign_piece(self.matrix[from_y][from_x].piece)
            self.matrix[from_y][from_x].deallocate_piece()
        
            #If to continue eating if the piece moved can do it
            if self.piece_can_eat_after_eat(to_x,to_y,playing) != []:
                self.draw_matrix()
                return playing
        
        #if the difference of square is one perform the movement
        else:
            self.matrix[to_y][to_x].assign_piece(self.matrix[from_y][from_x].piece)
            self.matrix[from_y][from_x].deallocate_piece()
        
        #Variable that is true if the piece would become queen with the movement made
        become_queen = to_y == 0 if playing.get_player_dir() == -1 and isinstance(self.matrix[to_y][to_x].get_piece(),Piece) else to_y == self.size_m -1
        
        #If he becomes king, he replaces the piece moved by a queen class
        if become_queen:
            playing.remove_piece(self.matrix[to_y][to_x].get_piece())
            new_queen = Queen_piece(self.matrix[to_y][to_x].piece_color())
            playing.add_piece(new_queen)
            self.matrix[to_y][to_x].deallocate_piece()
            self.matrix[to_y][to_x].assign_piece(new_queen)
        
        #Draw matrix and return opponent to change the turn
        self.draw_matrix()
        return opponent        
    
    #Method to return if something is wrong about the move
    def wrong(self,pt,message = 'Wrong coordinates'):
        self.draw_matrix()
        print(message)
        return pt
    
    #Method that returns false if the movement cannot be performed
    def verify_moves(self,from_x,from_y,to_x,to_y,playing,dif_x,dif_y,dir_y):
        #Verify that the piece is moving diagonally and that the strings are in range
        if dif_x == 0 or dif_y == 0 or not self.coordinates_is_in_range(from_x,from_y) or not self.coordinates_is_in_range(to_x,to_y):
            return False
        #Verify there is a piece in the coordinate that was specified
        if not self.matrix[from_y][from_x].is_piece_inside():
            return False
        #Verify that the piece belongs to the player who is playing
        if self.matrix[from_y][from_x].get_piece() not in playing.get_list_pieces():
            return False
        #Verify that there is no piece in the square that is moving
        if self.matrix[to_y][to_x].is_piece_inside():
            return False
        #Verify that the piece is not moving more than two squares and equal amount in both x and y
        if dif_x > 2 or dif_y > 2 or dif_x != dif_y:
            return False
        #Verify that the pieces that are not queens cannot move backwards
        if not isinstance(self.matrix[from_y][from_x].get_piece(),Queen_piece) and dir_y != playing.get_player_dir():
            return False
        return True

    #Method to verify which forced movements are in this turn
    def verify_forced_movements(self,playing):
        forced = []
        #Choose the direction of the possible moves for normal pieces
        change_y = 2 if playing.get_player_dir() == 1 else -2
        index_row = 0
        #While nested to traverse the board
        while index_row < self.size_m:
            index_col = 0
            while index_col < len(self.matrix[index_row]):
                #Add the list of forced move
                forced = self.add_forced_movements(index_col,index_row,change_y,playing,forced)
                #if the piece in the square is a queen piece add the list of forced move in the other direccion
                if isinstance(self.matrix[index_row][index_col].get_piece(),Queen_piece):
                    forced = self.add_forced_movements(index_col,index_row,change_y * -1,playing,forced)
                index_col += 1
            index_row += 1
        return forced
    
    #Method to add the forced elements
    def add_forced_movements(self,index_col,index_row,change_y,playing,forced):
        #Establish the possible possession where to move
        to_x = index_col + 2
        to_y = index_row + change_y
        dif_x,dif_y,dir_x,dir_y = self.difference_between_and_direction(index_col,index_row,to_x,to_y)
        
        #Check if this movement should be added
        if self.verify_moves(index_col,index_row,to_x,to_y,playing,dif_x,dif_y,dir_y):
    
            if self.piece_can_eat(index_col,index_row,to_x,to_y,playing,dir_x,dir_y):
                forced.append([index_col,index_row,to_x,to_y])

        #Establish the possible possession where to move    
        to_x = index_col - 2
        dif_x, dir_x = self.difference_between(index_col,to_x),self.direction(index_col,to_x)

        #Check if this movement should be added
        if self.verify_moves(index_col,index_row,to_x,to_y,playing,dif_x,dif_y,dir_y):
    
            if self.piece_can_eat(index_col,index_row,to_x,to_y,playing,dir_x,dir_y):
    
                forced.append([index_col,index_row,to_x,to_y])
        return forced

    #Method to verify if the piece can eat
    def piece_can_eat(self,from_x,from_y,to_x,to_y,playing,dir_x,dir_y):
        if self.matrix[to_y - dir_y][to_x - dir_x].is_piece_inside():
            if self.matrix[to_y - dir_y][to_x - dir_x].get_piece() not in playing.get_list_pieces():
                return True
        return False
    
    #Method to return the movements in which the piece can eat after eating
    def piece_can_eat_after_eat(self,from_x,from_y,playing):
        moves = []
        to_x = from_x +2
        to_y = from_y +2
        moves = self.condition_to_eat_after_eat(from_x,from_y,playing,to_x,to_y,moves)
        to_x = from_x +2
        to_y = from_y -2
        moves = self.condition_to_eat_after_eat(from_x,from_y,playing,to_x,to_y,moves)
        to_x = from_x -2
        to_y = from_y +2
        moves = self.condition_to_eat_after_eat(from_x,from_y,playing,to_x,to_y,moves)
        to_x = from_x -2
        to_y = from_y -2
        moves = self.condition_to_eat_after_eat(from_x,from_y,playing,to_x,to_y,moves)
        return moves
    
    #Method to add to the arrangement movements that meet the condition of eating after eating
    def condition_to_eat_after_eat(self,from_x,from_y,playing,to_x,to_y,moves):
        dir_x,dir_y = self.direction(from_x,to_x),self.direction(from_y,to_y)
        if self.verify_moves(from_x,from_y,to_x,to_y,playing,2,2,dir_y):
            if self.piece_can_eat(from_x,from_y,to_x,to_y,playing,dir_x,dir_y):
                moves.append([from_x,from_y,to_x,to_y])
        return moves

    #Method to return the matrix
    def get_matrix(self):
        return self.matrix
    
    #Method to determine if the coordinates are within the range of the matrix
    def coordinates_is_in_range(self,x,y):
        return True if (x < self.size_m and x >= 0) and (y <self.size_m and y >= 0) else False

    #Method that returns the difference between two numbers
    def difference_between(self,a,b):
        return a - b if a > b else b -a
    
    #Method that returns the direction of movement
    def direction(self,a,b):
        return -1 if a > b else +1

    #Method that returns the difference between two numbers and the direction of movement
    def difference_between_and_direction(self,from_x,from_y,to_x,to_y):
        dif_x, dif_y =self.difference_between(from_x,to_x), self.difference_between(from_y,to_y)
        dir_x, dir_y = self.direction(from_x,to_x), self.direction(from_y,to_y)
        return dif_x, dif_y, dir_x, dir_y