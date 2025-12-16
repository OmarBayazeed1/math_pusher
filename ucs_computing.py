import time
import heapq
import itertools

DIRECTIONS = {
    (-1, 0): "LEFT",
    (1, 0): "RIGHT",
    (0, -1): "UP",
    (0, 1): "DOWN"
}

class UniformCostSearch:
    def __init__(self, start_board):
        self.start_board = start_board
        self.visited = set()
        self.generated_count = 0
        self.visited_count = 0
        self.solution_path = None   # (moves_list, boards_list)
        self.elapsed_time = 0
        self._counter = itertools.count()

    def solve(self):
        start_time = time.time()

        # Priority queue holds tuples: (g, counter, board_state, moves_list, boards_list)
        queue = [(0, next(self._counter), self.start_board, [], [self.start_board])]
        self.visited.add(self.start_board.hash())

        while queue:
            g, _, current_board, moves, path = heapq.heappop(queue)
            self.visited_count += 1

            # Goal check
            if current_board.is_game_won():
                self.solution_path = (moves, path)
                self.elapsed_time = time.time() - start_time
                return True

            # Expand neighbors
            neighbors = current_board.get_possible_states()
            for next_state in neighbors:
                self.generated_count += 1   # count all neighbors produced
                h = next_state.hash()
                if h not in self.visited:
                    self.visited.add(h)
                    g_new = g + 1   # assume each move costs 1 (can adjust if needed)

                    # Derive move direction
                    dx = next_state.player.position.x - current_board.player.position.x
                    dy = next_state.player.position.y - current_board.player.position.y
                    direction = DIRECTIONS.get((dx, dy), "UNKNOWN")

                    heapq.heappush(
                        queue,
                        (g_new, next(self._counter), next_state,
                         moves + [direction],
                         path + [next_state])
                    )

        # No solution found
        self.elapsed_time = time.time() - start_time
        return False

    def report(self):
        print("===== Uniform Cost Search Report =====")
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
