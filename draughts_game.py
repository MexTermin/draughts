import colorama
from colorama import Fore, Back, Style
from player import Player
from board import Board
import os
import platform
colorama.init()

class Game:
    clear_text = ""
    elements = {'board': None, 'player1': None, 'player2': None}
    def __init__(self):
        self.choose_os()
        self.play()
    #Method that returns true if the coordinates are single character
    def is_one_char(self,coordinates):
        for coor in coordinates:
            if len(coordinates[coor]) != 1:
                return False
        return True
    
    #Method that returns true if the input coordinates are numbers
    def is_only_number(self,coordinates):
        for coor in coordinates:
            if 48 > ord(coordinates[coor]) or ord(coordinates[coor]) > 57:
                return False
        return True
    
    #Method to select the OS on the current platform
    def choose_os(self):
        os = {'Windows':'cls','Linux':'clear'}
        self.clear_text = os[platform.system()]
        Board.clear_text = self.clear_text

    
    #Method Clear console screen
    def clear_console(self):
        clear = lambda: os.system(self.clear_text)
        clear()
    
    #Method to create players
    def add_players(self):
        name_player1 = input('Write name of player number 1: ')
        name_player2 = input('Write name of player number 2: ')
        self.elements['player1'] = Player(name_player1,Fore.GREEN,1)
        self.elements['player2'] = Player(name_player2,Fore.YELLOW,2)
    
    #Method to create board
    def add_board(self):
        self.elements['board'] = Board(8)
    
    #Method to fill board
    def fill_board(self):
        self.elements['board'].generate_squares(self.elements['player1'],self.elements['player2'])
    
    #Method to draw board
    def draw_board(self):
        self.elements['board'].draw_matrix()
    
    #Method to return player 1
    def get_player1(self):
        return self.elements['player1']
    
    #Method to return player 2    
    def get_player2(self):
        return self.elements['player2']
    
    #Method to convert coordinates to int
    def convert_int(self,coordinates):
        for coor in coordinates:
            coordinates[coor] = int(coordinates[coor]) - 1
        return coordinates
    
    #Method that returns true if pieces left in the board
    def pieces_left(self):
        return self.get_player1().get_amount_pieces() > 0 and self.get_player2().get_amount_pieces() > 0
    
    #Method that return the forced movements in the current turn
    def forced_movements(self,playing):
        return self.elements['board'].verify_forced_movements(playing)
    
    #Method to enter coordinates
    def enter_coordinates(self):
        print('Enter the coordinates (x, y) of the tab to move')
        from_x = input('x: ')
        from_y = input('y: ')
        print('Enter the coordinates (x, y) of where to move')
        to_x = input('x: ')
        to_y = input('y: ')
        coordinates = {
            'from_x': from_x ,
            'from_y': from_y,
            'to_x': to_x,
            'to_y': to_y
        }
        return coordinates
    
    #Method to make a move
    def make_move(self,coordinates,playing,opponent):
        return self.elements['board'].move_piece(coordinates,playing,opponent)
    
    #Method to show the win message 
    def show_winner(self):
        winner = self.get_player1() if self.get_player2().get_amount_pieces() <= 0 else self.get_player2()
        self.clear_console()
        print("\n\n\n\t\t\t"+winner.get_name_player() + " IS THE WINNER!!!!!")
    
    #Method where the game runs
    def play(self):
        menu_index = 0
        menu = {"1":"New game","2": "Exit"}
        #While ending when the exit menu option is selected
        while menu_index not in menu or menu[menu_index] != "Exit":
            self.clear_console()
            #Show main menu
            print("\n\n\n")
            for element in menu:
                print("\t\t\t"+element +"- " + menu[element])
            
            #Choose menu option
            menu_index = input()
            if menu_index in menu:
                #If the option chosen is the main menu
                if menu[menu_index] == "New game":

                    #Create players
                    self.add_players()

                    #Create, fill and draw board
                    self.add_board()
                    self.fill_board()
                    self.draw_board()
                    
                    #Set first turn
                    playing = self.get_player1()

                    #While establishing that the game will continue as long as there are players with more than zero pieces
                    while self.pieces_left():
                        #Print which is current player in turn and quantity of pieces
                        print(playing.get_name_player() + ' Turn ' +str(playing.get_amount_pieces()) + ' Pieces' )
                        
                        #Itinerate the turns
                        opponent = self.get_player1() if playing == self.get_player2() else self.get_player2()
                        
                        #Write the coordinates of the movement you want to perform
                        coordinates = self.enter_coordinates()
                        
                        #If sentence to determine that the input that was entered is a number
                        if self.is_one_char(coordinates):
                            if self.is_only_number(coordinates):
                                #Convert coordinates to int
                                coordinates = self.convert_int(coordinates)
                                
                                #Determine the forced movements of that turn
                                forced_movements = self.forced_movements(playing)
                                
                                #If there are no mandatory movements try to make movement
                                if forced_movements != []:
                                    
                                    #If the movement you want to make is in the list of mandatory movements, 
                                    # perform the movement but print "Mandatory movements" and restart the play
                                    if [coordinates] in forced_movements:
                                        playing = self.make_move(coordinates,playing,opponent)
                                    else:
                                        self.draw_board()
                                        print("Mandatory movements")
                                else:
                                    playing = self.make_move(coordinates,playing,opponent)
                        
                            #If the input is not a number print "Please write a number" and restart the play
                            else:
                                self.draw_board()
                                print("Please write a number")
                        else:
                            self.draw_board()
                            print("Please write a number")
                        
                        #Check if the command to enter the coordinates (0,0) was set, it is used to finish the game
                        if coordinates['from_x'] == -1 and coordinates['from_y'] == -1:
                            
                            #Press s to end the current game
                            end = input('Write \'s\' if you want to end the game: ').upper()
                            if end == 'S':
                                break
                
                #If the while ends by finishing the game prints the winner and shows the option to play again
                if menu_index == "1" and not self.pieces_left():
                    self.show_winner()
                
                #If the exit option was chosen, the program will end
                if menu[menu_index] != "Exit":
                    menu_index = "1" if input("\n\nWrite R to play again, write something else to end: ").upper() == "R" else "2"
game = Game()