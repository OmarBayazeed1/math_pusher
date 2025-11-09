
# Import all of your game classes
from board import Board
from player import Player
from number_block import NumberBlock
from operator_block import OperatorBlock

from goal_block import GoalBlock
from hole import Hole
from wall import Wall

def setup_level():
    """Creates and returns the game board for a level."""
    print("--- Setting Up Level ---")
    board = Board(width=10, height=5)
    board.add_player(Player(1,3))
    board.add_hole(Hole(8, 1))

    # Create the equation: 2 + 3 = 5
    board.add_number_block(NumberBlock(2, 1, 2))
    board.add_operator_block(OperatorBlock(3, 1, '+'))
    board.add_number_block(NumberBlock(4, 1, 3))
    board.add_goal_block(GoalBlock(5, 1, 5))

    # Add walls for the border
    for i in range(10):
        board.add_wall(Wall(i, 0))
        board.add_wall(Wall(i, 4))
    for i in range(5):
        board.add_wall(Wall(0, i))
        board.add_wall(Wall(9, i))
    
    print("Level setup complete.\n")
    return board

def get_user_input():
    """Asks the user for their move and returns a direction."""
    while True:
        # Ask the user for input
        choice = input("Enter your move (W/A/S/D or R to reset): ").lower()
        
        if choice in ['w', 'a', 's', 'd']:
            if choice == 'w':
                return 0, -1 # Up
            if choice == 's':
                return 0, 1  # Down
            if choice == 'a':
                return -1, 0 # Left
            if choice == 'd':
                return 1, 0  # Right
        elif choice == 'r':
            return 'reset'
        else:
            print("Invalid input. Please use W, A, S, or D.")

# --- The Main Game ---
def main():
    """The main function to run the game."""
    my_board = setup_level()

    # The main game loop
    while True:
        # 1. Display the board
        my_board.show_board()

        # 2. Check for a win before asking for input
        if my_board.is_game_won():
            print("\n🎉🎉🎉 CONGRATULATIONS! YOU HAVE WON THE GAME! 🎉🎉🎉")
            break # Exit the loop

        # 3. Get user input
        direction = get_user_input()

        # 4. Process the input
        if direction == 'reset':
            print("\n--- Resetting Level ---")
            my_board = setup_level()
        else:
            dx, dy = direction
            my_board.move_player(dx, dy)

# This line makes the script runnable
if __name__ == "__main__":
    main()