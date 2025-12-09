import re
from tabulate import tabulate
from player import Player
from wall import Wall
from hole import Hole
from number_block import NumberBlock
from coordinate import Coordinate
from goal_block import GoalBlock
from operator_block import OperatorBlock

class Board:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.player: Player | None = None
        self.hole: Hole | None = None

        self.walls: list[Wall] = []
        self.number_blocks: list[NumberBlock] = []
        self.goal_blocks: list[GoalBlock] = []
        self.operator_blocks: list[OperatorBlock] = []

        # Authoritative occupancy map
        self.objects_map: dict[tuple[int, int], object] = {}

        # Emoji maps
        self.EMOJI_MAP = {
            '🟪': None,
            '🧱': Wall,
            '🤖': Player,
            '🕳️': Hole,
            '+': OperatorBlock,
            '-': OperatorBlock,
            '*': OperatorBlock,
            '/': OperatorBlock,
        }
        self.GOAL_EMOJI_MAP = {
            '0️⃣': 0, '1️⃣': 1, '2️⃣': 2, '3️⃣': 3, '4️⃣': 4,
            '5️⃣': 5, '6️⃣': 6, '7️⃣': 7, '8️⃣': 8, '9️⃣': 9
        }

        # Hash cache for performance
        self._cached_hash: int | None = None

    # ------------- Core helpers -------------
    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def get_object_at(self, x: int, y: int):
        return self.objects_map.get((x, y), None)

    def _invalidate_hash(self):
        self._cached_hash = None

    # ------------- Adders keep objects_map in sync -------------
    def add_player(self, player: Player):
        self.player = player
        self.objects_map[(player.position.x, player.position.y)] = player
        self._invalidate_hash()

    def add_hole(self, hole: Hole):
        self.hole = hole
        self.objects_map[(hole.position.x, hole.position.y)] = hole
        self._invalidate_hash()

    def add_wall(self, wall: Wall):
        self.walls.append(wall)
        self.objects_map[(wall.position.x, wall.position.y)] = wall
        self._invalidate_hash()

    def add_number_block(self, number_block: NumberBlock):
        self.number_blocks.append(number_block)
        self.objects_map[(number_block.position.x, number_block.position.y)] = number_block
        self._invalidate_hash()

    def add_operator_block(self, operator_block: OperatorBlock):
        self.operator_blocks.append(operator_block)
        self.objects_map[(operator_block.position.x, operator_block.position.y)] = operator_block
        self._invalidate_hash()

    def add_goal_block(self, goal_block: GoalBlock):
        self.goal_blocks.append(goal_block)
        self.objects_map[(goal_block.position.x, goal_block.position.y)] = goal_block
        self._invalidate_hash()

    # ------------- Clone (lean and consistent) -------------
    def clone(self):
        new_board = Board(self.width, self.height)

        if self.player:
            new_board.player = Player(self.player.position.x, self.player.position.y)
        if self.hole:
            new_board.hole = Hole(self.hole.position.x, self.hole.position.y)

        new_board.walls = [Wall(w.position.x, w.position.y) for w in self.walls]
        new_board.number_blocks = [NumberBlock(b.position.x, b.position.y, b.value) for b in self.number_blocks]
        new_board.operator_blocks = [OperatorBlock(b.position.x, b.position.y, b.operator) for b in self.operator_blocks]
        new_board.goal_blocks = [GoalBlock(g.position.x, g.position.y, g.target_value) for g in self.goal_blocks]

        # Rebuild map (authoritative)
        if new_board.player:
            new_board.objects_map[(new_board.player.position.x, new_board.player.position.y)] = new_board.player
        if new_board.hole:
            new_board.objects_map[(new_board.hole.position.x, new_board.hole.position.y)] = new_board.hole
        for w in new_board.walls:
            new_board.objects_map[(w.position.x, w.position.y)] = w
        for b in new_board.number_blocks:
            new_board.objects_map[(b.position.x, b.position.y)] = b
        for op in new_board.operator_blocks:
            new_board.objects_map[(op.position.x, op.position.y)] = op
        for g in new_board.goal_blocks:
            new_board.objects_map[(g.position.x, g.position.y)] = g

        return new_board

    # ------------- Hash and equality (tight) -------------
    def hash(self):
        if self._cached_hash is not None:
            return self._cached_hash

        player_pos = (self.player.position.x, self.player.position.y) if self.player else None
        hole_pos = (self.hole.position.x, self.hole.position.y) if self.hole else None

        # Use sorted tuples for determinism and compactness
        nb = tuple(sorted(((b.position.x, b.position.y, b.value) for b in self.number_blocks)))
        ops = tuple(sorted(((op.position.x, op.position.y, op.operator) for op in self.operator_blocks)))
        goals = tuple(sorted(((g.position.x, g.position.y, g.target_value) for g in self.goal_blocks)))
        walls = tuple(sorted(((w.position.x, w.position.y) for w in self.walls)))

        self._cached_hash = hash((player_pos, hole_pos, nb, ops, goals, walls))
        return self._cached_hash

    def eq(self, other):
        if not isinstance(other, Board):
            return False
        return self.hash() == other.hash()

    # ------------- Move generation (pruned) -------------
    def get_possible_states(self):
        # Prune impossible transitions before cloning where possible
        if not self.player:
            return []

        states = []
        px, py = self.player.position.x, self.player.position.y

        for dx, dy in ((1,0), (-1,0), (0,1), (0,-1)):
            nx, ny = px + dx, py + dy
            # Quick bounds check
            if not self.in_bounds(nx, ny):
                continue

            target = self.get_object_at(nx, ny)

            # Fast prune: walk into empty or hole or pushable chain with free destination
            if target is None or isinstance(target, Hole):
                new_board = self.clone()
                new_board.move_player(dx, dy)
                if new_board.player.position.x != px or new_board.player.position.y != py:
                    states.append(new_board)
                continue

            if isinstance(target, Wall):
                # Can't move into a wall; skip cloning
                continue

            if isinstance(target, (NumberBlock, OperatorBlock)):
                # Verify push chain destination before cloning
                cx, cy = nx, ny
                while self.in_bounds(cx, cy):
                    obj = self.get_object_at(cx, cy)
                    if isinstance(obj, (NumberBlock, OperatorBlock)):
                        cx += dx; cy += dy
                        continue
                    break

                if not self.in_bounds(cx, cy):
                    # off-board destination
                    continue

                dest_obj = self.get_object_at(cx, cy)
                if dest_obj is None or isinstance(dest_obj, Hole) and getattr(dest_obj, 'is_passable', True):
                    new_board = self.clone()
                    new_board.move_player(dx, dy)
                    if new_board.player.position.x != px or new_board.player.position.y != py:
                        states.append(new_board)
                # else blocked chain: skip

        return states

    # ------------- Movement (authoritative map updates) -------------
    def move_player(self, direction_x: int, direction_y: int):
        if not self.player:
            return

        px, py = self.player.position.x, self.player.position.y
        nx, ny = px + direction_x, py + direction_y
        if not self.in_bounds(nx, ny):
            return

        target = self.get_object_at(nx, ny)

        # Hole: move in
        if isinstance(target, Hole):
            self.objects_map.pop((px, py), None)
            self.player.position = Coordinate(nx, ny)
            self.objects_map[(nx, ny)] = self.player
            self._invalidate_hash()
            self.check_for_solved_goal()
            return

        # Empty: move
        if target is None:
            self.objects_map.pop((px, py), None)
            self.player.position = Coordinate(nx, ny)
            self.objects_map[(nx, ny)] = self.player
            self._invalidate_hash()
            self.check_for_solved_goal()
            return

        # Wall: blocked
        if isinstance(target, Wall):
            return

        # Push chain
        if isinstance(target, (NumberBlock, OperatorBlock)):
            dx, dy = direction_x, direction_y

            # Build contiguous chain
            chain: list[tuple[int, int, object]] = []
            cx, cy = nx, ny
            while self.in_bounds(cx, cy):
                obj = self.get_object_at(cx, cy)
                if isinstance(obj, (NumberBlock, OperatorBlock)):
                    chain.append((cx, cy, obj))
                    cx += dx; cy += dy
                    continue
                break

            if not chain:
                return

            if not self.in_bounds(cx, cy):
                return

            dest_obj = self.get_object_at(cx, cy)

            # Destination empty: shift all, then move player
            if dest_obj is None:
                for bx, by, obj in reversed(chain):
                    old_pos = (bx, by)
                    new_pos = (bx + dx, by + dy)
                    self.objects_map.pop(old_pos, None)
                    obj.position = Coordinate(*new_pos)
                    self.objects_map[new_pos] = obj

                self.objects_map.pop((px, py), None)
                self.player.position = Coordinate(nx, ny)
                self.objects_map[(nx, ny)] = self.player
                self._invalidate_hash()
                self.check_for_solved_goal()
                return

            # Destination hole: consume last block if passable, shift rest, move player
            if isinstance(dest_obj, Hole) and getattr(dest_obj, 'is_passable', True):
                far_bx, far_by, far_obj = chain[-1]
                self.objects_map.pop((far_bx, far_by), None)
                if isinstance(far_obj, NumberBlock):
                    if far_obj in self.number_blocks:
                        self.number_blocks.remove(far_obj)
                elif isinstance(far_obj, OperatorBlock):
                    if far_obj in self.operator_blocks:
                        self.operator_blocks.remove(far_obj)

                for bx, by, obj in reversed(chain[:-1]):
                    old_pos = (bx, by)
                    new_pos = (bx + dx, by + dy)
                    self.objects_map.pop(old_pos, None)
                    obj.position = Coordinate(*new_pos)
                    self.objects_map[new_pos] = obj

                self.objects_map.pop((px, py), None)
                self.player.position = Coordinate(nx, ny)
                self.objects_map[(nx, ny)] = self.player
                self._invalidate_hash()
                self.check_for_solved_goal()
                return

            # Otherwise blocked
            return

    # ------------- Goals and expressions -------------
    def remove_object(self, object_to_remove):
        if isinstance(object_to_remove, GoalBlock):
            for g in list(self.goal_blocks):
                if g.position == object_to_remove.position and g.target_value == object_to_remove.target_value:
                    self.goal_blocks.remove(g)
                    self.objects_map.pop((g.position.x, g.position.y), None)
                    self._invalidate_hash()
                    return True
        return False

    def check_for_solved_goal(self):
        expressions = self._find_expression_on_board()
        if not expressions or not self.goal_blocks:
            return False

        for expr_info in expressions:
            expr_str = expr_info['expr']
            calculated_result = self.evaluate_expression(expr_str)
            matching_goals = [g for g in self.goal_blocks if g.target_value == calculated_result]
            if matching_goals:
                for g in matching_goals:
                    self.remove_object(g)
                return True
        return False

    def _find_expression_on_board(self):
        expressions = []
        seen = set()
        directions = [(1, 0, 'horizontal'), (0, 1, 'vertical')]

        for y in range(self.height):
            for x in range(self.width):
                start_obj = self.get_object_at(x, y)
                if not isinstance(start_obj, NumberBlock):
                    continue

                for dx, dy, dir_name in directions:
                    positions = [(x, y)]
                    parts = [str(start_obj.value)]
                    expect_operator = True
                    nx, ny = x + dx, y + dy

                    while self.in_bounds(nx, ny):
                        obj = self.get_object_at(nx, ny)
                        if expect_operator:
                            if isinstance(obj, OperatorBlock):
                                parts.append(obj.operator)
                                positions.append((nx, ny))
                                expect_operator = False
                                nx += dx; ny += dy
                                continue
                            break
                        else:
                            if isinstance(obj, NumberBlock):
                                parts.append(str(obj.value))
                                positions.append((nx, ny))
                                expect_operator = True
                                nx += dx; ny += dy
                                continue
                            break

                    if len(parts) >= 3 and parts[-1].lstrip('-').isdigit():
                        key = tuple(positions)
                        if key not in seen:
                            seen.add(key)
                            expressions.append({'expr': ''.join(parts), 'positions': positions, 'dir': dir_name})
        return expressions

    def evaluate_expression(self, expr):
        expr = expr.replace(' ', '')
        expr = re.sub(r'\+\+', '+', expr)
        expr = re.sub(r'--', '+', expr)
        expr = re.sub(r'\+-', '-', expr)
        expr = re.sub(r'-\+', '-', expr)
        if expr and expr[0] == '-':
            expr = '0' + expr

        tokens = re.findall(r'\d+|[+\-*/]', expr)
        for i in range(len(tokens)):
            if re.fullmatch(r'\d+', tokens[i]):
                tokens[i] = int(tokens[i])

        i = 0
        while i < len(tokens):
            if tokens[i] in ('*', '/'):
                left = tokens[i - 1]; right = tokens[i + 1]
                if tokens[i] == '*':
                    res = left * right
                else:
                    if right == 0:
                        return float('nan')
                    res = left / right
                tokens[i - 1:i + 2] = [res]
                i -= 1
            else:
                i += 1

        if not tokens:
            return 0
        result = tokens[0]
        i = 1
        while i < len(tokens):
            op = tokens[i]; num = tokens[i + 1]
            if op == '+':
                result += num
            else:
                result -= num
            i += 2
        return int(result)

    # ------------- Loading and display -------------
    def load_level_from_data(self, level_data: list[list[str]]):
        self.height = len(level_data)
        self.width = max(len(row) for row in level_data)

        # Clear existing state
        self.player = None
        self.hole = None
        self.walls.clear()
        self.number_blocks.clear()
        self.goal_blocks.clear()
        self.operator_blocks.clear()
        self.objects_map.clear()
        self._invalidate_hash()

        for y, row in enumerate(level_data):
            for x, emoji in enumerate(row):
                if emoji in self.GOAL_EMOJI_MAP:
                    target_value = self.GOAL_EMOJI_MAP[emoji]
                    self.add_goal_block(GoalBlock(x, y, target_value))
                    continue

                if emoji.isdigit():
                    self.add_number_block(NumberBlock(x, y, int(emoji)))
                    continue

                object_class = self.EMOJI_MAP.get(emoji)
                if object_class == Wall:
                    self.add_wall(Wall(x, y)); continue
                elif object_class == Player:
                    self.add_player(Player(x, y)); continue
                elif object_class == Hole:
                    self.add_hole(Hole(x, y)); continue
                elif object_class == OperatorBlock:
                    self.add_operator_block(OperatorBlock(x, y, emoji)); continue
                # ignore '🟪' and unknown
        # No print in load to avoid I/O cost during solver runs

    def show_board_fast(self):
        # Lightweight ASCII for solver replay
        rows = []
        for y in range(self.height):
            row_chars = []
            for x in range(self.width):
                obj = self.get_object_at(x, y)
                if obj is None:
                    row_chars.append('.')
                elif isinstance(obj, Wall):
                    row_chars.append('#')
                elif isinstance(obj, Hole):
                    row_chars.append('O')
                elif isinstance(obj, Player):
                    row_chars.append('P')
                elif isinstance(obj, NumberBlock):
                    row_chars.append(str(obj.value))
                elif isinstance(obj, OperatorBlock):
                    row_chars.append(obj.operator)
                elif isinstance(obj, GoalBlock):
                    row_chars.append(f'G{obj.target_value}')
                else:
                    row_chars.append('?')
            rows.append(' '.join(row_chars))
        print('\n'.join(rows))

    def show_board(self):
        # Emoji renderer — keep for manual use; avoid during heavy solver runs
        grid = [['🟪' for _ in range(self.width)] for _ in range(self.height)]

        def place(x, y, sym):
            if 0 <= y < self.height and 0 <= x < self.width:
                grid[y][x] = sym

        if self.hole:
            place(self.hole.position.x, self.hole.position.y, ' 🕳️ ')
        for w in self.walls:
            place(w.position.x, w.position.y, ' 🧱 ')
        for b in self.number_blocks:
            place(b.position.x, b.position.y, f' {b.value} ')
        for op in self.operator_blocks:
            place(op.position.x, op.position.y, f' {op.operator} ')
        for g in self.goal_blocks:
            place(g.position.x, g.position.y, f'🎯{g.target_value}')
        if self.player:
            place(self.player.position.x, self.player.position.y, ' 🤖 ')

        print(tabulate(grid, tablefmt='grid'))

    def is_game_won(self) -> bool:
        if not self.hole or not self.player:
            return False
        return (self.player.position.x == self.hole.position.x
                and self.player.position.y == self.hole.position.y)

    def __repr__(self):
        return f"<Board Player={self.player.position if self.player else None}>"

    def __str__(self):
        return f"Board with Player at {self.player.position}, {len(self.walls)} walls, {len(self.number_blocks)} numbers"
