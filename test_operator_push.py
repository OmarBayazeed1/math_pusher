# test_operator_push.py
from board import Board
from player import Player
from operator_block import OperatorBlock
from wall import Wall
# --- Setup for an Operator Push Test ---
my_board = Board(width=5, height=5)
player_one = Player(1, 2)
op_to_push = OperatorBlock(2, 2, '+') # Player will push this
my_board.add_player(player_one)
my_board.add_operator_block(op_to_push)

my_board.show_status()

# --- Action! ---
print("\nLet's push the operator block to the down.")
my_board.move_player(direction_x=1, direction_y=0)

# --- Check the Result ---
my_board.show_status()
print("\nExpected Result:")
print("Player should be at (2, 2)")
print("OperatorBlock(+) should be at (3, 2)")