# main_game.py

# Import all of your game classes
from board import Board
from player import Player
from number_block import NumberBlock
from operator_block import OperatorBlock

from goal_block import GoalBlock
from hole import Hole

# --- Your Level Data ---
level_1_data =[['🟪','🟪','🟪','🟪','🟪','🟪','🟪','🟪','🟪','🟪','🟪','🧱','🟪','🟪'],
                ['🟪','🟪','🟪','🟪','🟪','1','🟪','🟪','🟪','🟪','🟪','🧱','🧱','🧱'],
                ['🟪','🟪','🟪','🤖','🟪','🟪','🟪','+','🟪','🟪','🟪','3️⃣','🟪','🕳️'],
                ['🟪','🟪','🟪','🟪','🟪','2','🟪','🟪','🟪','🟪','🟪','🧱','🧱','🧱'],
                ['🟪','🟪','🟪','🟪','🟪','🟪','🟪','🟪','🟪','🟪','🟪','🧱','🟪','🟪'],  
    ]

# --- The Main Game ---
def main():
    """The main function to run the game."""
    # Create a new board
    my_board = Board(width=0, height=0) # Size will be set by the loader

    # Load the level data into the board
    my_board.load_level_from_data(level_1_data)

    # The main game loop (this is the same as before)
    while True:
        # 1. Display the board
        my_board.show_board()

        # 2. Check for a win
        if my_board.is_game_won():
            print("\n🎉🎉🎉 CONGRATULATIONS! YOU HAVE WON THE GAME! 🎉🎉🎉")
            break # Exit the loop

        # 3. Get user input
        choice = input("Enter your move (W/A/S/D or R to reset): ").lower()

        # 4. Process the input
        if choice == 'w':
            my_board.move_player(0, -1)
        elif choice == 's':
            my_board.move_player(0, 1)
        elif choice == 'a':
            my_board.move_player(-1, 0)
        elif choice == 'd':
            my_board.move_player(1, 0)
        elif choice == 'r':
            print("\n--- Resetting Level ---")
            my_board.load_level_from_data(level_1_data)

# This line makes the script runnable
if __name__ == "__main__":
    main()