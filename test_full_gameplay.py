# test_full_gameplay.py
from board import Board
from player import Player
from number_block import NumberBlock
from operator_block import OperatorBlock
from goal_block import GoalBlock
from hole import Hole

# --- Setup a level ---
my_board = Board(width=10, height=5)
my_board.add_player(Player(0, 2))
my_board.add_hole(Hole(8, 2))

# Create the equation: 2 + 3 = 5
my_board.add_number_block(NumberBlock(2, 2, 2))
my_board.add_operator_block(OperatorBlock(3, 2, '+'))
my_board.add_number_block(NumberBlock(4, 2, 3))
my_board.add_goal_block(GoalBlock(5, 2, 5))

my_board.show_board()

# --- Action! ---
# 1. Move player to be in position to solve the goal
my_board.move_player(1, 0) # Right
my_board.move_player(1, 0) # Right (now at 2,2)
my_board.show_board()

# 2. Move player again to trigger the goal check
my_board.move_player(1, 0) # Right (now at 3,2)
my_board.show_board()

# 3. Move player to the unlocked hole
print("\nMoving to the hole...")
my_board.move_player(1, 0) # Right
my_board.move_player(1, 0) # Right
my_board.move_player(1, 0) # Right
my_board.move_player(1, 0) # Right (now at 7,2)
my_board.move_player(1, 0) # Right (now in the hole!)
my_board.show_board()

# --- Final Check ---
if my_board.is_game_won():
    print("\n🎉🎉🎉 YOU HAVE WON THE GAME! 🎉🎉🎉")
else:
    print("\nGame not won yet.")