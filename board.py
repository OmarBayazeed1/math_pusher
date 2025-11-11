import re
from player import Player
from wall import Wall
from hole import Hole
import numpy as np
from tabulate import tabulate
from number_block import NumberBlock
from coordinate import Coordinate
from goal_block import GoalBlock
from operator_block import OperatorBlock


class Board:
    def __init__(self,width:int,height:int):
        self.width=width
        self.height=height
        self.player: Player | None=None
        self.hole : Hole | None=None
        self.walls: list[Wall] = [] 
        self.number_blocks: list[NumberBlock]=[]
        self.goal_blocks: list[GoalBlock]=[]
        self.operator_blocks: list[OperatorBlock]=[]
        self.grid = [['🟪' for _ in range(self.width)] for _ in range(self.height)]
        self.EMOJI_MAP = {
        '🟪': None, # Empty space, do nothing
        '🧱': Wall,
        '🤖': Player,
        '🕳️': Hole,
        '+': OperatorBlock,
        '-': OperatorBlock,
        '*': OperatorBlock,
        '/': OperatorBlock,
         }
    def add_player(self,player:Player):
        self.player=player
        print(f'Board: player has been add to the game')
    def add_wall(self,wall:Wall):
        self.walls.append(wall)
        print(f'A wall at position {wall.position} has been added')
    def add_number_block(self,number_block:NumberBlock):
        self.number_blocks.append(number_block)
        print(f'A number block {number_block.value} at  {number_block.position} has been added to the board')
    def add_goal_block(self,goal_block: GoalBlock):
            self.goal_blocks.append(goal_block)
            print(f'A goal block {goal_block.target_value} at {goal_block.position}  has been added to board')
    def add_operator_block(self,operator_block: OperatorBlock):
        self.operator_blocks.append(operator_block)
        print(f'An operator block {operator_block.operator} at {operator_block.position} has been added to the board.')
    def add_hole(self,hole: Hole):
        self.hole=hole
        print(f'A hole at {hole.position} has been added to board.')
    def show_status(self):
        print('\n----Board-----')
        if self.player:
            print(self.player)
        print(f'There are {len(self.walls)} walls on the board')
        for wall in self.walls:
            print(f' -{wall}')
        print(f'There are {len(self.number_blocks)} number_blocks on the board')
        for block in self.number_blocks:    
            print(f' -{block}')
        print(f'There are {len(self.operator_blocks)} operator_blocks on the board')
        for operator_block in self.operator_blocks:
            print(f' -{operator_block}')
        print(f'---------------')

    def remove_object(self, object_to_remove):
        """Removes a given object from the board."""
        if isinstance(object_to_remove, GoalBlock):
            if object_to_remove in self.goal_blocks:
                self.goal_blocks.remove(object_to_remove)
                print(f"GoalBlock at {object_to_remove.position} has been removed.")
                return True
        
        return False
    
    # In board.py, replace your entire check_for_solved_goal method with this:

    def check_for_solved_goal(self):
        """
        Uses the new expression evaluator to check for a solved goal.
        """
        # 1. Find an expression on the board.
        expression_str = self._find_expression_on_board()
         # --- DEBUG PRINT 1 ---
        print(f"DEBUG: Found expression string: '{expression_str}'")
        # 2. If no expression, we can't solve anything.
        if not expression_str:
            print("DEBUG: No expression found. Exiting check.")
            return False

        # 3. Get the first goal to check against.
        if not self.goal_blocks:
            print("DEBUG: No goal blocks on the board. Exiting check.")
            return False
        goal = self.goal_blocks[0]

        print(f"\nFound expression: {expression_str}")

        # 4. Evaluate the expression using your powerful function!
        calculated_result = self.evaluate_expression(expression_str)
        print(f"DEBUG: Calculated result from expression is: {calculated_result}")
        # 5. Compare the result to the goal's target value.
        if calculated_result == goal.target_value:
            print(f"!!! GOAL SOLVED !!!")
            print(f"Solved: {expression_str} = {calculated_result}")
            
            # 6. If it matches, remove the goal block and unlock the hole.
            self.remove_object(goal)
            
            return True
         # If we get here, no goal was solved
        
        return False

    
    def get_object_at(self,x,y):
        if self.player and self.player.position.x==x and self.player.position.y==y:
            return self.player
        for wall in self.walls:
            if wall.position.x==x and wall.position.y==y:
                return wall
        for number_block in self.number_blocks:
            if number_block.position.x==x and number_block.position.y==y:
                return number_block
        for goal_block in self.goal_blocks:
            if goal_block.position.x==x and goal_block.position.y==y:
                return goal_block
        for operator_block in self.operator_blocks:
            if operator_block.position.x==x and operator_block.position.y==y:
                return operator_block
        return None
    def move_player(self, direction_x, direction_y):
        if not self.player:
            print("Board: There's no player to move!")
            return

        # 1. Calculate the player's NEW potential position
        new_x = self.player.position.x + direction_x
        new_y = self.player.position.y + direction_y
        new_position = Coordinate(new_x, new_y)

        print(f"\nBoard: Player wants to move to {new_position}.")

        # 2. Check if the new position is outside the board boundaries
        if not (0 <= new_x < self.width and 0 <= new_y < self.height):
            print("Board: Cannot move! That's off the board.")
            return
        target_object=self.get_object_at(new_position.x,new_position.y)
        if isinstance(target_object,Hole):
            if not target_object.is_passable:
                print('Board: The hole is closed ! solve the goal first!')
                return
        if target_object is None:
            print('The square is Empty , you can move the player..')
            self.player.position=new_position
            self.check_for_solved_goal()
            
            return
        if isinstance(target_object,Wall):
            print('Board: Can\'t move, there is a WALL!')
            return
        
        if isinstance(target_object,OperatorBlock):
            position_behind_nblock=Coordinate(new_position.x + direction_x,new_position.y + direction_y)
        
            if (0 <= position_behind_nblock.x < self.width and 0 <= position_behind_nblock.y < self.height and self.get_object_at(position_behind_nblock.x,position_behind_nblock.y) is None):
                print('Board: Push is valid ..')
                print('Board: moving the the block..')
                print('Board: Moving the player')
                target_object.position=position_behind_nblock
                self.player.position=new_position
                self.check_for_solved_goal()
                
                return
            else:
                print('Board: Can not push there is somthing behind the block')
                return    
        if isinstance(target_object,NumberBlock):
            position_behind_nblock=Coordinate(new_position.x + direction_x,new_position.y + direction_y)
        
            if (0 <= position_behind_nblock.x < self.width and 0 <= position_behind_nblock.y < self.height and self.get_object_at(position_behind_nblock.x,position_behind_nblock.y) is None):
                print('Board: Push is valid ..')
                print('Board: moving the the block..')
                print('Board: Moving the player')
                target_object.position=position_behind_nblock
                self.player.position=new_position
                self.check_for_solved_goal()
                
                return
            else:
                print('Board: Can not push there is somthing behind the block')
                return    
    

    def _get_cell(self, x, y):
        """
        A helper to get the grid cell at a natural (x, y) coordinate.
        This makes the rest of our code much more readable.
        """
        # This is the only place we have to remember the ugly [y][x] pattern.
        return self.grid[y][x]

    def _set_cell(self, x, y, value):
        """
        A helper to set the grid cell at a natural (x, y) coordinate.
        """
        self.grid[y][x] = value
    

    def show_board(self):
        """
        Prints a clean, aligned 2D visual representation of the board.
        This version is more reliable than tabulate.
        """
        # 1. Create an empty grid, with padding for alignment
        grid = [[' 🟪 ' for _ in range(self.width)] for _ in range(self.height)]

        # 2. Place all the objects on the grid
        if self.hole:
            x, y = self.hole.position.x, self.hole.position.y
            grid[y][x] = ' 🕳️ ' # Padded hole

        for wall in self.walls:
            x, y = wall.position.x, wall.position.y
            grid[y][x] = ' 🧱 ' # Padded wall

        for block in self.number_blocks:
            x, y = block.position.x, block.position.y
            grid[y][x] = f' {block.value} ' # Padded number

        for op_block in self.operator_blocks:
            x, y = op_block.position.x, op_block.position.y
            grid[y][x] = f' {op_block.operator} ' # Padded operator

        for goal_block in self.goal_blocks:
            x, y = goal_block.position.x, goal_block.position.y
            
            grid[y][x] = f' {goal_block.target_value} '

        if self.player:
            x, y = self.player.position.x, self.player.position.y
            grid[y][x] = ' 🤖 ' # Padded player

        # 3. Print the grid row by row
        print("\n--- Board Visual ---")
        print(tabulate(grid,tablefmt='grid'))
        print("--------------------\n")    
    def is_game_won(self) -> bool:
        if not self.hole:
            return False # No hole, can't win
        return self.player.position.x == self.hole.position.x and self.player.position.y == self.hole.position.y
    def evaluate_expression(self,expr):
        """
        Evaluates a mathematical expression string like "2+3*4".
        Handles operator precedence.
        """
        # Remove spaces
        expr = expr.replace(' ', '')

        # Handle double operators like -- or ++
        expr = re.sub(r'\+\+', '+', expr)
        expr = re.sub(r'--', '+', expr)
        expr = re.sub(r'\+-', '-', expr)
        expr = re.sub(r'-\+', '-', expr)

        # Handle leading negative numbers
        if expr and expr[0] == '-':
            expr = '0' + expr

        # Find all numbers and operators
        tokens = re.findall(r'\d+|[+\-*/]', expr)

        # Convert number strings to actual integers
        i = 0
        while i < len(tokens):
            if re.fullmatch(r'\d+', tokens[i]):
                tokens[i] = int(tokens[i])
            i += 1

        # Evaluate multiplication and division first
        i = 0
        while i < len(tokens):
            if tokens[i] in ('*', '/'):
                left = tokens[i - 1]
                right = tokens[i + 1]
                if tokens[i] == '*':
                    result = left * right
                else:
                    if right == 0: return float('NOT_DEFINED') # Handle division by zero
                    result = left / right
                tokens[i - 1:i + 2] = [result]
                i -= 1 # Go back and re-evaluate
            else:
                i += 1

        # Evaluate addition and subtraction
        if not tokens:
            return 0
        result = tokens[0]
        i = 1
        while i < len(tokens):
            op = tokens[i]
            num = tokens[i + 1]
            if op == '+':
                result += num
            elif op == '-':
                result -= num
            i += 2

        return int(result) # Ensure the result is an integer
    
    
    

    def load_level_from_data(self, level_data: list[list[str]]):
        """
        Reads level data from a 2D list of emojis and creates game objects.
        This version uses the GoalType Enum for robustness.
        """
        self.height = len(level_data)
        self.width = max(len(row) for row in level_data)
        print(f"Loading a level of size {self.width}x{self.height}...")

        # Loop through the data and create objects
        for y, row in enumerate(level_data):
            for x, emoji in enumerate(row):
                if emoji in ['0️⃣','1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣']:
                    target_value=int(emoji[0])
                    self.add_goal_block(GoalBlock(x,y,target_value))
                # 1. Handle digits first (for NumberBlocks)
                if emoji.isdigit():
                    value = int(emoji)
                    self.add_number_block(NumberBlock(x, y, value))
                    continue # Move to the next square
                # 3. Handle all other emojis with our map
                object_class = self.EMOJI_MAP.get(emoji)
                if object_class:
                    
                    if object_class == GoalBlock:
                        self.add_goal_block(GoalBlock(x,y))
                    if object_class == Wall:
                        self.add_wall(Wall(x, y))
                    elif object_class == Player:
                        self.add_player(Player(x, y))
                    elif object_class == Hole:
                        self.add_hole(Hole(x, y))
                    elif object_class == OperatorBlock:
                        self.add_operator_block(OperatorBlock(x, y, emoji)) # The emoji is the operator
                # '🟪' (empty) and unknown emojis are ignored
                
        print("Level loading complete.\n")   
    def _find_expression_on_board(self):
        """
        Scans the board to find a simple Num-Op-Num pattern.
        Returns the expression as a string (e.g., "2+3") or None if not found.
        This is a simplified version. A more advanced version could scan in all directions.
        """
            # --- 1. Check for Horizontal Patterns (left-to-right) ---
        for y in range(self.height):
            for x in range(self.width - 2): # -2 because we need space for 3 items
                obj1 = self.get_object_at(x, y)
                obj_op = self.get_object_at(x + 1, y)
                obj2 = self.get_object_at(x + 2, y)

                if (isinstance(obj1, NumberBlock) and
                    isinstance(obj_op, OperatorBlock) and
                    isinstance(obj2, NumberBlock)):
                    
                    return (obj1.value, obj_op.operator, obj2.value, 'horizontal')
            # 2) Look for vertical patterns (top -> bottom)
                for x in range(self.width):
                    for y in range(self.height - 2):
                        obj1 = self.get_object_at(x, y)
                        obj2 = self.get_object_at(x, y + 1)
                        obj3 = self.get_object_at(x, y + 2)
    
                        if (isinstance(obj1, NumberBlock) and
                            isinstance(obj2, OperatorBlock) and
                            isinstance(obj3, NumberBlock)):
        
                            # Build the expression string in top->bottom order
                            expr_str = f"{obj1.value}{obj2.operator}{obj3.value}"
                            return expr_str
 
        return None # No expression found