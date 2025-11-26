from collections import deque

class Bfs_Computing:
    def __init__(self, current_board):
        self.current_board = current_board

    def solve(self):
        queue = deque()
        queue.append((self.current_board, []))  

        visited = set()
        visited.add(self.current_board)

        while queue:
            current, path = queue.popleft()

            if current.is_game_won():
                solution_path = path + [current]
                
                return solution_path

            for next_state in current.get_possible_states():
                if next_state not in visited:
                    visited.add(next_state)
                    queue.append((next_state, path + [current]))

        return None
