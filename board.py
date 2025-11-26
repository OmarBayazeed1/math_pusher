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
import copy

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
        self.grid = [["" for _ in range(self.width)] for _ in range(self.height)]
        
        
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
    
   
    

    def clone(self):
        return copy.deepcopy(self)
    '''def clone(self):
        new_board = Board(self.width, self.height)

        # Copy player
        if self.player:
            new_board.player = Player(self.player.position.x, self.player.position.y)

        # Copy blocks
        new_board.number_blocks = [NumberBlock(b.position.x, b.position.y, b.value) for b in self.number_blocks]
        new_board.operator_blocks = [OperatorBlock(b.position.x, b.position.y, b.operator) for b in self.operator_blocks]
        new_board.goal_blocks = [GoalBlock(b.position.x, b.position.y, b.target_value) for b in self.goal_blocks]

        # Copy hole
        if self.hole:
            new_board.hole = Hole(self.hole.position.x, self.hole.position.y)

        # Copy walls
        new_board.walls = [Wall(w.position.x, w.position.y) for w in self.walls]

        # Copy grid (optional, if you use it for display)
        new_board.grid = [row[:] for row in self.grid]

        return new_board
'''
    def __eq__(self, other):
        if not isinstance(other, Board):
            return False

        return (
            (self.player.position if self.player else None) ==
            (other.player.position if other.player else None)
            and {(b.position, b.value) for b in self.number_blocks} ==
                {(b.position, b.value) for b in other.number_blocks}
            and {(b.position, b.operator) for b in self.operator_blocks} ==
                {(b.position, b.operator) for b in other.operator_blocks}
            and {(b.position, b.target_value) for b in self.goal_blocks} ==
                {(b.position, b.target_value) for b in other.goal_blocks}
            and (self.hole.position if self.hole else None) ==
                (other.hole.position if other.hole else None)
            and {w.position for w in self.walls} ==
                {w.position for w in other.walls}
        )

    def __hash__(self):
        return hash((
            (self.player.position if self.player else None),
            frozenset((b.position, b.value) for b in self.number_blocks),
            frozenset((b.position, b.operator) for b in self.operator_blocks),
            frozenset((b.position, b.target_value) for b in self.goal_blocks),
            (self.hole.position if self.hole else None),
            frozenset(w.position for w in self.walls)
        ))



    def get_possible_states(self):
        states = []
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        for dx, dy in directions:
            new_board = self.clone()
            before = (new_board.player.position.x, new_board.player.position.y)
            new_board.move_player(dx, dy)
            after = (new_board.player.position.x, new_board.player.position.y)
            if before != after:
                states.append(new_board)
        return states



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
        
        if isinstance(object_to_remove, GoalBlock):
            if object_to_remove in self.goal_blocks:
                self.goal_blocks.remove(object_to_remove)
                print(f"GoalBlock at {object_to_remove.position} has been removed.")
                return True
        
        return False
    
    def check_for_solved_goal(self):
        
        expressions = self._find_expression_on_board()
        print(f"DEBUG: Found {len(expressions)} expression(s) on board: {[e['expr'] for e in expressions]}")
        if not expressions:
            return False

        if not self.goal_blocks:
            print("DEBUG: No goal blocks on the board. Exiting check.")
            return False

        # Try each found expression against all goals
        for expr_info in expressions:
            expr_str = expr_info['expr']
            print(f"DEBUG: Evaluating expression {expr_str} (dir={expr_info.get('dir')}, positions={expr_info.get('positions')})")
            calculated_result = self.evaluate_expression(expr_str)
            print(f"DEBUG: Result of '{expr_str}' = {calculated_result}")

            # collect goals that match this expression result
            matching_goals = [g for g in self.goal_blocks if g.target_value == calculated_result]
            if matching_goals:
                # remove all matching goals (if there are multiple with the same target)
                for g in matching_goals:
                    self.remove_object(g)
                    print(f"DEBUG: Removed goal with target {g.target_value} at {g.position}")
                print(f"!!! GOAL(S) SOLVED by '{expr_str}' !!!")
                return True

        # No expression solved any goal
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
    def in_bounds(self,x,y):
        return (0 <= x< self.width and 0 <=y < self.height)
        
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
        if not self.in_bounds(new_x,new_y):
            print("Board: Cannot move! That's off the board.")
            return
        

        target_object = self.get_object_at(new_position.x, new_position.y)

        # If target is a hole
        if isinstance(target_object, Hole):
            
            self.player.position = new_position
            self.check_for_solved_goal()
            return

        # Empty cell -> just move
        if target_object is None:
            print('The square is Empty, you can move the player..')
            self.player.position = new_position
            self.check_for_solved_goal()
            return

        # Wall blocks movement
        if isinstance(target_object, Wall):
            print('Board: Can\'t move, there is a WALL!')
            return

        # Handle pushing for NumberBlock or OperatorBlock (supports chains)
        if isinstance(target_object, (OperatorBlock, NumberBlock)):
            dx, dy = direction_x, direction_y

            # Build contiguous chain of pushable blocks starting from the target cell
            chain = []  # list of (x, y, object)
            cx, cy = new_position.x, new_position.y
            while self.in_bounds(cx,cy):
            #while 0 <= cx < self.width and 0 <= cy < self.height:
                obj = self.get_object_at(cx, cy)
                if isinstance(obj, (NumberBlock, OperatorBlock)):
                    chain.append((cx, cy, obj))
                    cx += dx
                    cy += dy
                    continue
                else:
                    break

            # If chain is empty (shouldn't happen because target_object is pushable),
            # treat as cannot push
            if not chain:
                print('Board: Nothing to push.')
                return

            # Now (cx, cy) is the first cell after the last pushable block
            # Check bounds and occupancy
            if not (0 <= cx < self.width and 0 <= cy < self.height):
                print('Board: Can not push there is something off the board behind the block(s).')
                return

            dest_obj = self.get_object_at(cx, cy)
            # Destination must be empty to shift the chain
            if dest_obj is None:
                # Move blocks from farthest to nearest to avoid overwriting
                for bx, by, obj in reversed(chain):
                    obj.position = Coordinate(bx + dx, by + dy)
                # Move player into the first block's old position
                self.player.position = new_position
                print('Board: Push succeeded; moved chain and player.')
                self.check_for_solved_goal()
                return
            # If destination is a passable hole (rare), allow block to fall in? treat similar to empty? Here we treat hole as blocked unless passable semantics needed.
            if isinstance(dest_obj, Hole):
                if dest_obj.is_passable:
                    # allow moving block into hole (remove block), then move player
                    far_bx, far_by, far_obj = chain[-1]
                    # Remove the last block from board (simulate falling into hole)
                    if isinstance(far_obj, NumberBlock) and far_obj in self.number_blocks:
                        self.number_blocks.remove(far_obj)
                    elif isinstance(far_obj, OperatorBlock) and far_obj in self.operator_blocks:
                        self.operator_blocks.remove(far_obj)
                    # Shift remaining blocks forward
                    for bx, by, obj in reversed(chain[:-1]):
                        obj.position = Coordinate(bx + dx, by + dy)
                    self.player.position = new_position
                    print('Board: Pushed block(s) and one fell into a passable hole.')
                    self.check_for_solved_goal()
                    return
                else:
                    print('Board: Can not push there is a closed hole behind the block(s).')
                    return

            # If destination is a wall, goal, player, or any other non-pushable, block the push
            print('Board: Can not push there is something behind the block(s)')
            return

        # If target is any other non-handled object, block movement
        print('Board: Can not move there.')
        return
    
    def show_board(self):
        # Reset grid each time to avoid leftover values
        self.grid = [["🟪" for _ in range(self.width)] for _ in range(self.height)]

        def safe_place(x, y, symbol):
            if 0 <= y < self.height and 0 <= x < self.width:
                self.grid[y][x] = symbol
            else:
                print(f"⚠️ Warning: Tried to place {symbol} at ({x},{y}) outside grid")

        if self.hole:
            safe_place(self.hole.position.x, self.hole.position.y, ' 🕳️ ')

        for wall in self.walls:
            safe_place(wall.position.x, wall.position.y, ' 🧱 ')

        for block in self.number_blocks:
            safe_place(block.position.x, block.position.y, f' {block.value} ')

        for op_block in self.operator_blocks:
            safe_place(op_block.position.x, op_block.position.y, f' {op_block.operator} ')

        for goal_block in self.goal_blocks:
            safe_place(goal_block.position.x, goal_block.position.y, f' {goal_block.target_value} ')

        if self.player:
            safe_place(self.player.position.x, self.player.position.y, ' 🤖 ')

        print("\n--- Board Visual ---")
        print(tabulate(self.grid, tablefmt='grid'))
        print("--------------------\n")

    '''def show_board(self):
        #self.grid = [[ '🟪' for _ in range(self.width)] for _ in range(self.height)]
        
        if self.hole:
            x, y = self.hole.position.x, self.hole.position.y
            self.grid[y][x] = ' 🕳️ ' 
        for wall in self.walls:
            x, y = wall.position.x, wall.position.y
            self.grid[y][x] = ' 🧱 '
        for block in self.number_blocks:
            x, y = block.position.x, block.position.y
            self.grid[y][x] = f' {block.value} ' 

        for op_block in self.operator_blocks:
            x, y = op_block.position.x, op_block.position.y
            self.grid[y][x] = f' {op_block.operator} ' 

        for goal_block in self.goal_blocks:
            x, y = goal_block.position.x, goal_block.position.y
            
            self.grid[y][x] = f' {goal_block.target_value} '

        if self.player:
            x, y = self.player.position.x, self.player.position.y
            self.grid[y][x] = ' 🤖 ' 

        # 3. Print the grid row by row
        print("\n--- Board Visual ---")
        print(tabulate(self.grid,tablefmt='grid'))
        print("--------------------\n")
'''
    def is_game_won(self) -> bool:
        if not self.hole:
            return False # No hole, can't win
        return self.player.position.x == self.hole.position.x and self.player.position.y == self.hole.position.y
    def evaluate_expression(self,expr):
        
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
       
        self.height = len(level_data)
        self.width = max(len(row) for row in level_data)
        print(f"Loading a level of size {self.width}x{self.height}...")

        # Loop through the data and create objects
        for y, row in enumerate(level_data):
            for x, emoji in enumerate(row):
                if emoji in ['3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','0️⃣','1️⃣','2️⃣']:
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
        
        expressions = []
        # to ensure no duplicate expressinons
        seen = set()  

        # directions: (dx, dy, name)
        # horizontal left --> right
        # vertical   top --> down
        directions = [(1, 0, 'horizontal'), (0, 1, 'vertical')]

        for y in range(self.height):
            for x in range(self.width):
                start_obj = self.get_object_at(x, y)
                #expression must start with a number
                if not isinstance(start_obj, NumberBlock):
                    continue

                for dx, dy, dir_name in directions:
                    positions = [(x, y)]
                    parts = [str(start_obj.value)]
                    expect_operator = True
                    nx, ny = x + dx, y + dy

                    while 0 <= nx < self.width and 0 <= ny < self.height:
                        obj = self.get_object_at(nx, ny)
                        if expect_operator:
                            if isinstance(obj, OperatorBlock):
                                parts.append(obj.operator)
                                positions.append((nx, ny))
                                expect_operator = False
                                nx += dx; ny += dy
                                continue
                            else:
                                break
                        else:  # expect a number
                            if isinstance(obj, NumberBlock):
                                parts.append(str(obj.value))
                                positions.append((nx, ny))
                                expect_operator = True
                                nx += dx; ny += dy
                                continue
                            else:
                                break

                    # valid chain must be at least Num Op Num -> parts len >= 3 and last part must be a number
                    if len(parts) >= 3 and parts[-1].lstrip('-').isdigit():
                        key = tuple(positions)
                        if key not in seen:
                            seen.add(key)
                            expressions.append({
                                'expr': ''.join(parts),
                                'positions': positions,
                                'dir': dir_name
                            })

        return expressions