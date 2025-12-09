import time
from collections import deque

class Bfs_Computing:
    def __init__(self, start_board, max_depth=None, fast_report=True):
        self.start_board = start_board
        self.visited = set()
        self.generated_count = 0
        self.visited_count = 0
        self.solution_path = None
        self.elapsed_time = 0
        self.max_depth = max_depth        # optional cutoff for huge boards
        self.fast_report = fast_report    # use show_board_fast if available

    def solve(self):
        start_time = time.time()

        # Queue holds tuples: (board_state, path_taken)
        queue = deque([(self.start_board, [self.start_board])])
        self.visited.add(self.start_board.hash())

        while queue:
            current_board, path = queue.popleft()
            self.visited_count += 1

            # Goal check
            if current_board.is_game_won():
                self.solution_path = path
                self.elapsed_time = time.time() - start_time
                return True

            # Depth cutoff (optional)
            if self.max_depth and len(path) >= self.max_depth:
                continue
            
            # Expand neighbors
            for next_state in current_board.get_possible_states():
                self.generated_count += 1
                h = next_state.hash()
                if h in self.visited:
                    continue
                if next_state.player.position == current_board.player.position:
                    continue
                if h not in self.visited:
                    self.visited.add(h)
                    queue.append((next_state, path + [next_state]))

        # No solution found
        self.elapsed_time = time.time() - start_time
        return False

    def report(self):
        print("===== BFS Report =====")
        print(f"Visited states: {self.visited_count}")
        print(f"Generated states: {self.generated_count}")
        print(f"Elapsed time: {self.elapsed_time:.4f} seconds")

        if self.solution_path:
            print(f"Solution path length: {len(self.solution_path)}")
            for step, board_state in enumerate(self.solution_path):
                print(f"\n--- Step {step}: Player at {board_state.player.position} ---")
                if self.fast_report and hasattr(board_state, "show_board_fast"):
                    board_state.show_board_fast()
                else:
                    board_state.show_board()
        else:
            print("No solution found.")
        print("======================")
