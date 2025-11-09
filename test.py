# test.py
from board import Board
from player import Player
from wall import Wall
from number_block import NumberBlock
# --- Setup ---
print("Setting up the game...")
my_board = Board(width=10, height=10)
player_one = Player(2, 2)
wall_one = Wall(1,5)
wall_two= Wall(3,2) 
number_block_1= NumberBlock(1,3,9)

my_board.add_player(player_one)
my_board.add_wall(wall_one)
my_board.add_wall(wall_two)
my_board.add_number_block(number_block_1)



# --- Action! ---
print("Let's try moving the player.")

# 1. Move Down (should be Invalid)
my_board.move_player(direction_x=1, direction_y=0)
my_board.show_status()
# 2. Move up (should be valid)
my_board.move_player(direction_x=-1,direction_y=0)
my_board.show_status()
#3. Move right(should be valid)
my_board.move_player(direction_x=0,direction_y=1)
my_board.show_status()
#4. Move right(should be Invalid)
my_board.move_player(direction_x=0,direction_y=1)
my_board.show_status()

