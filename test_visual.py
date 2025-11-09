# test_visual.py
from board import Board
from player import Player
from wall import Wall
from number_block import NumberBlock
from operator_block import OperatorBlock
from goal_block import GoalBlock

# --- Setup a simple level ---
my_board = Board(width=8, height=8)

# Add a player
my_board.add_player(Player(1,1))

# Add some walls to make borders
for i in range(8):
    my_board.add_wall(Wall(i, 0)) # Top wall
    my_board.add_wall(Wall(i, 4)) # Bottom wall
for i in range(5):
    my_board.add_wall(Wall(0, i)) # Left wall
    my_board.add_wall(Wall(7, i)) # Right wall

# Add the puzzle pieces
my_board.add_number_block(NumberBlock(3, 2, 2))
my_board.add_operator_block(OperatorBlock(4, 2, '+'))
my_board.add_number_block(NumberBlock(5, 2, 3))
my_board.add_goal_block(GoalBlock(6, 2, 5))


# --- Visualize! ---
my_board.show_board()

# --- Now let's move the player and see the change ---
print("Moving player right...")
my_board.move_player(direction_x=1, direction_y=0)
my_board.show_board()

print("Moving player right again (to push the block)...")
my_board.move_player(direction_x=1, direction_y=0)
my_board.show_board()