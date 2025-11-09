from player import Player
from wall import Wall
from hole import Hole
import numpy as np
from number_block import NumberBlock
from coordinate import Coordinate
from goal_block import GoalBlock
from operator_block import OperatorBlock
from tabulate import tabulate

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
    
    def check_for_solved_goal(self):
        # 1. First, check if we have at least one of each required piece.
        if not self.number_blocks or not self.goal_blocks or not self.operator_blocks:
            return False
        # 2. Get the first available piece of each type.
        num1=self.number_blocks[0]
        op=self.operator_blocks[0]
        num2=self.number_blocks[1] if len(self.number_blocks) > 1 else self.number_blocks[0]
        goal=self.goal_blocks[0]

        # 3. Calculate the result.
        if len(self.number_blocks) < 2:
            num2_value=0
        else:
            num2_value=self.number_blocks[1].value
        result=0
        if op.operator=='+':
            result=num1.value + num2.value
        elif op.operator=='-':
            result=num1.value - num2.value
        elif op.operator=='*':
            result=num1.value * num2.value
        elif op.operator=='/':
            if num2_value==0:
                print(f'Can not divide by zero')
                return False
            result=num1.value / num2.value
        # 4. Compare the result to the goal's target value.
        if result == goal.target_value:
            print(f"\n!!! GOAL SOLVED !!!")
            print(f"Solved: {num1.value} {op.operator} {num2_value} = {result}")
            # 5. If it matches, remove the goal block.
            self.remove_object(goal)
            if self.hole:
                self.hole.unlock()
            return True
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
    # In board.py, inside the Board class
    def show_board(self):
        """
        Prints a 2D visual representation of the board.
        This method ALWAYS starts with a clean grid to prevent smears.
        """
        # 1. Create a brand new, empty grid. This is the "eraser".
        self.grid = [[' ' for _ in range(self.width)] for _ in range(self.height)]

        # 2. Draw all objects on the new, clean grid.
        # The order doesn't matter as much as starting with a clean grid.
        if self.hole:
            self._set_cell(self.hole.position.x, self.hole.position.y, str(self.hole))

        for wall in self.walls:
            self._set_cell(wall.position.x, wall.position.y, '🧱')

        for block in self.number_blocks:
            self._set_cell(block.position.x, block.position.y, str(block.value))

        for op_block in self.operator_blocks:
            self._set_cell(op_block.position.x, op_block.position.y, op_block.operator)

        for goal_block in self.goal_blocks:
            self._set_cell(goal_block.position.x, goal_block.position.y, '🏁')

        if self.player:
            self._set_cell(self.player.position.x, self.player.position.y, '🤖')

        # 3. Print the final grid.
        print("\n--- Board Visual ---")
        for row in self.grid:
            print(" ".join(row))
        print("--------------------\n")
        
    def is_game_won(self) -> bool:
        if not self.hole:
            return False # No hole, can't win
        return self.player.position == self.hole.position