import colorama
from colorama import Fore, Back, Style
from player import Player
from piece import Piece
from queen_piece import Queen_piece
from square import Square
from board import Board
import os
colorama.init()

#While of the game
clear = lambda: os.system('clear')
menu_index = 0
menu = {"1":"New game","2": "Exit"}
while menu_index not in menu or menu[menu_index] != "Exit":
    clear()
    print("\n\n\n")
    for element in menu:
        print("\t\t\t"+element +"- " + menu[element])
    menu_index = input()
    if menu_index in menu:
        if menu[menu_index] == "New game":
            name_player1 = input('Write name of player number 1: ')
            name_player2 = input('Write name of player number 2: ')
            player1 = Player(name_player1,Fore.GREEN,1)
            player2 = Player(name_player2,Fore.YELLOW,2)
            board = Board(8)
            board.generate_squares(player1,player2)            
            board.draw_matrix()
            playing = player1
            while player1.get_amount_pieces() > 0 and player2.get_amount_pieces() > 0:
                print(playing.get_name_player() + ' Turn ' +str(playing.get_amount_pieces()) + ' Pieces' )
                opponent = player1 if playing == player2 else player2
                print('Enter > 0the coordinates (x, y) of the tab to move')
                from_x = input('x: ')
                from_y = input('y: ')
                print('Enter the coordinates (x, y) of where to move')
                to_x = input('x: ')
                to_y = input('y: ')
                if len(from_x) == 1 and len(from_y) == 1 and len(to_y) == 1 and len(to_x) == 1:
                    if (48 <= ord(from_x) <= 57 and 48 <= ord(from_y) <= 57 and 48 <= ord(to_x) <= 57 and 48 <= ord(to_y) <= 57):
                        from_x,from_y,to_x,to_y = int(from_x) - 1,int(from_y) - 1,int(to_x) - 1,int(to_y) - 1
                        forced_movements = board.verify_forced_movements(playing)
                        if forced_movements != []:
                            if [from_x,from_y,to_x,to_y] in forced_movements:
                                playing =board.move_piece(from_x,from_y,to_x,to_y,playing,opponent)
                            else:
                                board.draw_matrix()
                                print("Mandatory movements")
                        else:
                            playing = board.move_piece(from_x,from_y,to_x,to_y,playing,opponent)
                    else:
                        board.draw_matrix()
                        print("Please write a number")
                else:
                    board.draw_matrix()
                    print("Please write a number")
                if from_x == -1 and from_y == -1:
                    salir = input('Write \'s\' if you want to end the game: ').upper()
                    if salir == 'S':
                        break
        if menu_index == "1" and (player2.get_amount_pieces() <= 0 or player1.get_amount_pieces() <= 0):
            winner = player1 if player2.get_amount_pieces() <= 0 else player2
            clear = lambda: os.system('clear')
            clear()
            print("\n\n\n\t\t\t"+winner.get_name_player() + " IS THE WINNER!!!!!")
        if menu[menu_index] != "Exit":
            menu_index = "1" if input("\n\nWrite R to play again, write something else to end: ").upper() == "R" else "2"