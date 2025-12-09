from board import Board
from bfs_computing import Bfs_Computing
from dfs_computing import Dfs_Computing
from astar_computing import AStar_Computing
import time
data =[ ['🟪','🟪','2️⃣','🕳️'],
                ['5','🟪','🧱','🧱'],
                ['🟪','-','🟪'],
                [ '3','🟪','🤖','🟪'],
            ]
level_7_data =[ ['🧱','🧱','🧱','1️⃣','2️⃣','🕳️','🧱'],
                ['🧱','🧱','🧱','🟪','🧱','🧱','🧱'],
                ['🟪','🟪','🟪','🟪','🟪','🟪','🟪'],
                ['🟪','🟪','🟪' ,'-','🟪','🟪','🟪'],
                ['🟪','1','🟪','🟪','🟪','3','🟪'],
                ['🟪','🟪','🟪','2','🟪','🟪','🟪',],
                ['🟪','🟪','🟪','🟪','🟪','🟪','🟪'],
                ['🟪','🟪','🟪','🤖','🟪','🟪','🟪'],
                ['🟪','🟪','🟪','🟪','🟪','🟪','🟪'], 
            ]
level_4_data =[ ['🟪','🟪','🧱','🕳️','🧱','🟪','🟪'],
                ['🟪','🟪','🧱','6️⃣','🧱','🟪','🟪'],
                ['🟪','🟪','🟪','🤖','🟪','🟪','🟪'],
                ['🟪','🟪','🟪' ,'🟪','🟪','🟪','🟪'],
                ['🟪','🟪','1','+','2','🟪','🟪'],
                ['🟪','🟪','🟪','🟪','🟪','🟪','🟪','🟪'],
                ['🟪','🟪','2','+','3','🟪','🟪'],
                ['🟪','🟪','🟪','🟪','🟪','🟪','🟪'],
                ['🟪','🟪','🟪','🟪','🟪','🟪','🟪'], 
            ]
level_5_data =[ ['🧱','🧱','🧱','🧱','🧱','🟪','🧱','🟪','+','1','+','🟪','🧱','🟪'],
                ['🧱','🧱','🧱','🧱','🧱','🟪','🟪','🟪','🟪','🟪','🟪','🟪','🟪','🟪'],
                ['🧱','🧱','🧱','🧱','🧱','🟪','🟪','1','🟪','🟪','🟪','2','🟪','🟪'],
                ['🧱','🧱','🧱' ,'🧱','🧱','🟪','🟪','🟪','🟪','🟪','🟪','🟪','🟪','🟪'],
                ['🕳️','8️⃣','5️⃣','4️⃣', '3️⃣','🟪','🟪','🟪','🟪','🤖','🟪','🟪','🟪','🟪'],
                ['🧱','🧱','🧱','🧱','🧱','🟪','🟪','🟪','🟪','🟪','🟪','🟪','🟪','🟪','🟪'],
                ['🧱','🧱','🧱','🧱','🧱','🟪','🟪','3','🟪','🟪','🟪','4','🟪','🟪'],
                ['🧱','🧱','🧱','🧱','🧱','🟪','🟪','🟪','🟪','🟪','🟪','🟪','🟪','🟪'],
                ['🧱','🧱','🧱','🧱','🧱','🟪','🧱','🟪','+','1','+','🟪','🧱','🟪'], 
            ]
#board.load_level_from_data(data)
#board.show_board()
#states=board.get_possible_states()
#for i in states:
#    i.show_board()
#    i.show_status()
def run_Astar():
    b = Board(width=0,height=0)
    b.load_level_from_data(level_5_data)
    solver = AStar_Computing(b)
    if solver.solve():
        solver.report()
run_Astar()





def run_bfs():
    b = Board(width=0,height=0)
    b.load_level_from_data(level_5_data)
    solver = Bfs_Computing(b,max_depth=100, fast_report=True)
    if solver.solve():
        solver.report()
    
   
#run_bfs()






'''
solver = Bfs_Computing(board)
start_time = time.time()
path, depth = solver.solve()
elapsed_time = time.time() - start_time

if path:
    print(f"Solved in {depth} moves, time: {elapsed_time:.4f} seconds")
    for i, state in enumerate(path):
        print(f"\n--- Step {i} (depth {i}) ---")
        state.show_board()
else:
    print(f"No solution found. Time taken: {elapsed_time:.4f} seconds")
    '''

def run_dfs():
    b = Board(width=0, height=0)
    b.load_level_from_data(data)
    solver = Dfs_Computing(b)
    solution_path = solver.solve()
    if solution_path:
        print(" 💯💯💯Found Dfs solution💯💯💯")
        for step, state in enumerate(solution_path):
            print(f"\n--- step {step} ---")
            state.show_board()
    else:
        print("No solution")
#run_dfs()