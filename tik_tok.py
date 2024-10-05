import os
import random
import pygame
pygame.init()
pygame.mixer.init()

player1_sound = pygame.mixer.Sound(r"D:\project\oop\tic_tac_game\zapsplat_household_aerosol_deodorant_can_set_down_table_004_103261.mp3")
player2_sound = pygame.mixer.Sound(r"D:\project\oop\tic_tac_game\zapsplat_household_aerosol_deodorant_can_set_down_table_004_103261.mp3")

def clear_screen():
    os.system("cls")

class Players:
    def __init__(self, is_computer=False):
        self.name = "Computer" if is_computer else ""
        self.symbol = ""
        self.is_computer = is_computer

    def choose_name(self):
        if not self.is_computer:
            while True:
                name = input("Enter name: ")
                if name.isalpha():
                    self.name = name
                    break
                print("Name must be alphabetic only.")

    def choose_symbol(self):
        if not self.is_computer:
            while True:
                symbol = input(f"Welcome {self.name}, choose a symbol (X or O): ").upper()
                if symbol in ["X", "O"]:
                    self.symbol = symbol
                    break
                print("Symbol must be either X or O.")
        else:
            self.symbol = "O" if self.symbol == "X" else "X"

    def make_move(self, board):
        if self.is_computer:
            available_moves = [i + 1 for i, cell in enumerate(board.board) if cell.isdigit()]
            move = self.choose_best_move(board, available_moves)
            return move
        else:
            while True:
                try:
                    move = int(input("Choose a cell between 1-9: "))
                    if 1 <= move <= 9:
                        return move
                    else:
                        print("Invalid move! Please enter a number between 1 and 9.")
                except ValueError:
                    print("Please enter a valid number.")

    def choose_best_move(self, board, available_moves):
        for move in available_moves:
            board_copy = Board()
            board_copy.board = board.board.copy()
            board_copy.update_board(move, self.symbol)
            if board_copy.check_win(self.symbol):
                return move
        return random.choice(available_moves)

class Menu:
    def display_main_menu(self):
        print("Welcome to my X-O game!")
        print("1. Start Game")
        print("2. Quit Game")
        while True:
            choice = input("Enter your choice (1 or 2): ")
            if choice in ["1", "2"]:
                return choice
            print("Enter a valid choice.")

    def display_end_menu(self):
        print("Game Over")
        print("1. Restart Game")
        print("2. Quit Game")
        while True:
            choice = input("Enter your choice (1 or 2): ")
            if choice in ["1", "2"]:
                return choice

class Board:
    def __init__(self):
        self.board = [str(i) for i in range(1, 10)]

    def display_board(self):
        for i in range(0, 9, 3):
            print("|".join(self.board[i:i+3]))
            if i < 6:
                print("-" * 5)

    def update_board(self, choice, symbol):
        if self.valid_move(choice):
            self.board[choice - 1] = symbol
            return True
        return False

    def valid_move(self, choice):
        return self.board[choice - 1].isdigit()
    
    def reset_board(self):
        self.board = [str(i) for i in range(1, 10)]
    
    def check_win(self, symbol):
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for comb in win_combinations:
            if self.board[comb[0]] == self.board[comb[1]] == self.board[comb[2]] == symbol:
                return True
        return False

    def check_draw(self):
        return all(not cell.isdigit() for cell in self.board)

class Game:
    def __init__(self):
        self.players = []   
        self.board = Board()
        self.menu = Menu()
        self.current_player_index = 0

    def start_game(self):
        choice = self.menu.display_main_menu()
        if choice == "1":
            self.setup_players()
            self.play_game()
        else:
            self.quit_game()
            
#Check if user want to play with combuter
    def setup_players(self):
        print("Do you want to play against the computer? (y/n)")
        play_vs_computer = input().lower() == 'y'
        
        player1 = Players()
        player1.choose_name()
        player1.choose_symbol()
        self.players.append(player1)

        if play_vs_computer:
            player2 = Players(is_computer=True)
            player2.symbol = "O" if player1.symbol == "X" else "X"
        else:
            player2 = Players()
            player2.choose_name()
            player2.choose_symbol()
        
        self.players.append(player2)

        clear_screen()

    def play_turn(self):
        player = self.players[self.current_player_index]
        print(f"{player.name}'s turn ({player.symbol})")
        self.board.display_board()

        move = player.make_move(self.board)
        if self.board.update_board(move, player.symbol):
            if self.current_player_index == 0:
                player1_sound.play()  
            else:
                player2_sound.play()  

            clear_screen()
            return True  #successful move
        return False  #unsuccessful move

    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index

    def play_game(self):
        while True:
            if not self.play_turn():
                continue  # Retry the turn if the move was unsuccessful
            
            if self.check_win():
                if self.players[self.current_player_index].is_computer:
                    print("GAME OVER! The Computer wins!")
                else:
                    print(f"Congratulations {self.players[self.current_player_index].name}, you win!")
                choice = self.menu.display_end_menu()
                if choice == "1":
                    self.restart()
                else:
                    self.quit_game()
                    break
            elif self.check_draw():
                print("It's a draw!")
                choice = self.menu.display_end_menu()
                if choice == "1":
                    self.restart()
                else:
                    self.quit_game()
                    break
            
            self.switch_player()  # Switch player 

    def check_win(self):
        return self.board.check_win(self.players[self.current_player_index].symbol)
    
    def check_draw(self):
        return self.board.check_draw()
    
    def restart(self):
        self.board.reset_board()
        self.current_player_index = 0
        self.play_game()

    def quit_game(self):
        print("Thank you for playing")

game = Game()
game.start_game()
