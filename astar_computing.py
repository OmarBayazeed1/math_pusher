import time
import heapq
import itertools

# Simple mapping of (dx, dy) to direction words
DIRECTIONS = {
    (-1, 0): "LEFT",
    (1, 0): "RIGHT",
    (0, -1): "UP",
    (0, 1): "DOWN"
}

class AStar_Computing:
    def __init__(self, start_board, heuristic=None):
        self.start_board = start_board
        self.visited = set()
        self.generated_count = 0   # counts all neighbors produced
        self.visited_count = 0
        self.solution_path = None   # will store (moves_list, boards_list)
        self.elapsed_time = 0
        # Default heuristic: Manhattan distance from player to hole
        self.heuristic = heuristic if heuristic else self.smart_heuristic
        # Tie-breaker counter to avoid comparing Board objects
        self._counter = itertools.count()

    @staticmethod
    def smart_heuristic(board):
        """
        A smarter heuristic for A* search:
        - Player-to-hole Manhattan distance
        - Penalty for unsolved goals
        - Distance of number blocks to matching goals
        - Corner trap penalty (optional)
        """
        h1 = 0
        if board.player and board.hole:
            px, py = board.player.position.x, board.player.position.y
            hx, hy = board.hole.position.x, board.hole.position.y
            h1 = abs(px - hx) + abs(py - hy)

        # Penalty for unsolved goals
        h2 = len(board.goal_blocks) * 5   # weight can be tuned

        # Distance of blocks to nearest matching goal
        h3 = 0
        for g in board.goal_blocks:
            distances = [
                abs(b.position.x - g.position.x) + abs(b.position.y - g.position.y)
                for b in board.number_blocks if b.value == g.target_value
            ]
            if distances:
                h3 += min(distances)

        # Optional: corner trap penalty
        h4 = 0
        for b in board.number_blocks:
            x, y = b.position.x, b.position.y
            walls = 0
            if board.get_object_at(x+1, y) and isinstance(board.get_object_at(x+1, y), type(board.walls[0])):
                walls += 1
            if board.get_object_at(x-1, y) and isinstance(board.get_object_at(x-1, y), type(board.walls[0])):
                walls += 1
            if board.get_object_at(x, y+1) and isinstance(board.get_object_at(x, y+1), type(board.walls[0])):
                walls += 1
            if board.get_object_at(x, y-1) and isinstance(board.get_object_at(x, y-1), type(board.walls[0])):
                walls += 1
            if walls >= 2:   # stuck in a corner
                h4 += 10     # heavy penalty

        return h1 + h2 + h3 + h4

    def solve(self):
        start_time = time.time()

        # Priority queue holds tuples: (f, g, counter, board_state, moves_list, boards_list)
        start_h = self.heuristic(self.start_board)
        queue = [(start_h, 0, next(self._counter), self.start_board, [], [self.start_board])]
        self.visited.add(self.start_board.hash())

        while queue:
            f, g, _, current_board, moves, path = heapq.heappop(queue)
            self.visited_count += 1

            # Goal check
            if current_board.is_game_won():
                self.solution_path = (moves, path)
                self.elapsed_time = time.time() - start_time
                return True

            # Expand neighbors using Board.get_possible_states()
            neighbors = current_board.get_possible_states()
            for next_state in neighbors:
                self.generated_count += 1   # ✅ count all neighbors produced
                h = next_state.hash()
                if h not in self.visited:
                    self.visited.add(h)
                    g_new = g + 1
                    h_new = self.heuristic(next_state)
                    f_new = g_new + h_new

                    # Derive move direction from player position difference
                    dx = next_state.player.position.x - current_board.player.position.x
                    dy = next_state.player.position.y - current_board.player.position.y
                    direction = DIRECTIONS.get((dx, dy), "UNKNOWN")

                    heapq.heappush(
                        queue,
                        (f_new, g_new, next(self._counter), next_state,
                         moves + [direction],
                         path + [next_state])
                    )

        # No solution found
        self.elapsed_time = time.time() - start_time
        return False

    def report(self):
        print("===== A* Report =====")
        print(f"Visited states: {self.visited_count}")
        print(f"Generated states: {self.generated_count}")
        print(f"Elapsed time: {self.elapsed_time:.4f} seconds")

        if self.solution_path:
            moves, boards = self.solution_path
            print("Moves list:", moves)
            for step, board_state in enumerate(boards):
                direction = moves[step-1] if step > 0 else "START"
                print(f"\n--- Step {step}: {direction} ---")
                if hasattr(board_state, "show_board_fast"):
                    board_state.show_board_fast()
                else:
                    board_state.show_board()
        else:
            print("No solution found.")
        print("======================")
