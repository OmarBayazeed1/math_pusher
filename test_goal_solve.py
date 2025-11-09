# test_goal_solve.py

# Import all the classes we need
from board import Board
from player import Player
from number_block import NumberBlock
from operator_block import OperatorBlock
from goal_block import GoalBlock

# --- Setup ---
print("Setting up a goal-solving test...")
my_board = Board(width=10, height=10)

# The player's position doesn't matter for this test, but let's add one.
player_one = Player(0, 0)

# Create the pieces for the equation: 2 + 3 = 5
num1 = NumberBlock(5, 5, 2)
op_block = OperatorBlock(6, 6, '+')
num2 = NumberBlock(7, 7, 3)
goal = GoalBlock(8, 8, 5)

# Add all the pieces to the board
my_board.add_player(player_one)
my_board.add_number_block(num1)
my_board.add_operator_block(op_block)
my_board.add_number_block(num2)
my_board.add_goal_block(goal)

# --- Initial State Check ---
print(f"\nInitial number of goals on the board: {len(my_board.goal_blocks)}")
print("Expected: 1")

# --- Action! ---
# The board will now check its pieces and see if they form a valid solution.
print("\nAttempting to solve the goal...")
did_solve = my_board.check_for_solved_goal()

# --- Verification ---
print(f"\nFinal number of goals on the board: {len(my_board.goal_blocks)}")
print("Expected: 0")

# --- Test Result ---
if did_solve and len(my_board.goal_blocks) == 0:
    print("\n✅ TEST PASSED: The goal was correctly solved and removed.")
else:
    print("\n❌ TEST FAILED: The goal was not solved correctly.")
    print(f"Method returned: {did_solve}")
    print(f"Final goals list length: {len(my_board.goal_blocks)}")
