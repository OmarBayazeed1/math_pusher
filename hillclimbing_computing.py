import time
import random

DIRECTIONS = {
    (-1, 0): "LEFT",
    (1, 0): "RIGHT",
    (0, -1): "UP",
    (0, 1): "DOWN"
}

class HillClimbing:
    def __init__(self, start_board, heuristic=None, max_steps=500, random_restarts=0):
        self.start_board = start_board
        self.heuristic = heuristic if heuristic else self.default_heuristic
        self.max_steps = max_steps
        self.random_restarts = random_restarts
        self.solution_path = None   # (moves_list, boards_list)
        self.elapsed_time = 0
        self.visited_count = 0

    @staticmethod
    def default_heuristic(board):
        # Simple heuristic: Manhattan distance from player to hole
        if board.player and board.hole:
            px, py = board.player.position.x, board.player.position.y
            hx, hy = board.hole.position.x, board.hole.position.y
            return abs(px - hx) + abs(py - hy)
        return 0

    def solve(self):
        start_time = time.time()

        # Try multiple restarts if requested
        for restart in range(self.random_restarts + 1):
            current_board = self.start_board.clone()
            current_h = self.heuristic(current_board)
            moves = []
            path = [current_board]

            for step in range(self.max_steps):
                self.visited_count += 1

                # Goal check
                if current_board.is_game_won():
                    self.solution_path = (moves, path)
                    self.elapsed_time = time.time() - start_time
                    return True

                # Generate neighbors
                neighbors = current_board.get_possible_states()
                if not neighbors:
                    break

                # Pick best neighbor
                best_neighbor = None
                best_h = float("inf")
                best_move = None

                for next_state in neighbors:
                    h = self.heuristic(next_state)
                    if h < best_h:
                        best_h = h
                        best_neighbor = next_state
                        dx = next_state.player.position.x - current_board.player.position.x
                        dy = next_state.player.position.y - current_board.player.position.y
                        best_move = DIRECTIONS.get((dx, dy), "UNKNOWN")

                # If no improvement, stop (local minimum)
                if best_h >= current_h:
                    break

                # Move to best neighbor
                current_board = best_neighbor
                current_h = best_h
                moves.append(best_move)
                path.append(current_board)

            # If solution found, stop restarts
            if self.solution_path:
                break

        # No solution found
        self.elapsed_time = time.time() - start_time
        return False

    def report(self):
        print("===== Hill Climbing Report =====")
        print(f"Visited states: {self.visited_count}")
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
            print("No solution found (stuck in local optimum).")
        print("======================")
