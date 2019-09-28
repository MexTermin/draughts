import colorama
from colorama import Fore, Back, Style
from player import Player
from piece import Piece
from queen_piece import Queen_piece
from square import Square
from board import Board
import os
colorama.init()

#Clear console screen
clear = lambda: os.system('clear')
menu_index = 0

#Main menu
menu = {"1":"New game","2": "Exit"}

#While ending when the exit menu option is selected
while menu_index not in menu or menu[menu_index] != "Exit":
    clear()
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
            name_player1 = input('Write name of player number 1: ')
            name_player2 = input('Write name of player number 2: ')
            player1 = Player(name_player1,Fore.GREEN,1)
            player2 = Player(name_player2,Fore.YELLOW,2)

            #Create, fill and draw board
            board = Board(8)
            board.generate_squares(player1,player2)            
            board.draw_matrix()
            
            #Set first turn
            playing = player1

            #While establishing that the game will continue as long as there are players with more than zero pieces
            while player1.get_amount_pieces() > 0 and player2.get_amount_pieces() > 0:
                #Print which is current player in turn and quantity of pieces
                print(playing.get_name_player() + ' Turn ' +str(playing.get_amount_pieces()) + ' Pieces' )
                
                #Itinerate the turns
                opponent = player1 if playing == player2 else player2
                
                #Write the coordinates of the movement you want to perform
                print('Enter the coordinates (x, y) of the tab to move')
                from_x = input('x: ')
                from_y = input('y: ')
                print('Enter the coordinates (x, y) of where to move')
                to_x = input('x: ')
                to_y = input('y: ')
                
                #If sentence to determine that the input that was entered is a number
                if len(from_x) == 1 and len(from_y) == 1 and len(to_y) == 1 and len(to_x) == 1:
                    if (48 <= ord(from_x) <= 57 and 48 <= ord(from_y) <= 57 and 48 <= ord(to_x) <= 57 and 48 <= ord(to_y) <= 57):
                        from_x,from_y,to_x,to_y = int(from_x) - 1,int(from_y) - 1,int(to_x) - 1,int(to_y) - 1
                        
                        #Determine the forced movements of that turn
                        forced_movements = board.verify_forced_movements(playing)
                        
                        #If there are no mandatory movements try to make movement
                        if forced_movements != []:
                            
                            #If the movement you want to make is in the list of mandatory movements, 
                            # perform the movement but print "Mandatory movements" and restart the play
                            if [from_x,from_y,to_x,to_y] in forced_movements:
                                playing =board.move_piece(from_x,from_y,to_x,to_y,playing,opponent)
                            else:
                                board.draw_matrix()
                                print("Mandatory movements")
                        else:
                            playing = board.move_piece(from_x,from_y,to_x,to_y,playing,opponent)
                
                #If the input is not a number print "Please write a number" and restart the play
                    else:
                        board.draw_matrix()
                        print("Please write a number")
                else:
                    board.draw_matrix()
                    print("Please write a number")
                
                #Check if the command to enter the coordinates (0,0) was set, it is used to finish the game
                if from_x == -1 and from_y == -1:
                    
                    #Press s to end the current game
                    end = input('Write \'s\' if you want to end the game: ').upper()
                    if end == 'S':
                        break
        
        #If the while ends by finishing the game prints the winner and shows the option to play again
        if menu_index == "1" and (player2.get_amount_pieces() <= 0 or player1.get_amount_pieces() <= 0):
            winner = player1 if player2.get_amount_pieces() <= 0 else player2
            clear = lambda: os.system('clear')
            clear()
            print("\n\n\n\t\t\t"+winner.get_name_player() + " IS THE WINNER!!!!!")
        #If the exit option was chosen, the program will end
        if menu[menu_index] != "Exit":
            menu_index = "1" if input("\n\nWrite R to play again, write something else to end: ").upper() == "R" else "2"