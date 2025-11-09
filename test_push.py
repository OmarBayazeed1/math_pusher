# test_push.py
from board import Board
from player import Player
from number_block import NumberBlock

# --- Setup for a Push Test ---
print("Setting up a push test...")
my_board = Board(width=5, height=5)
player_one = Player(1, 2) # Player is to the left of the block
block_to_push = NumberBlock(2, 2, 5) # Block is at (2, 2)

my_board.add_player(player_one)
my_board.add_number_block(block_to_push)
my_board.show_status()

# --- Action! ---
print("\nLet's push the block to the down.")

# Move the player down into the block.
# The player is at (1,2), the block is at (2,2).
# The space behind the block is (3,2), which is empty.
# This should be a valid push.
my_board.move_player(direction_x=1, direction_y=0)

# --- Check the Result ---
my_board.show_status()
print("\nExpected Result:")
print("Player should be at (2, 2)")
print("NumberBlock(5) should be at (3, 2)")