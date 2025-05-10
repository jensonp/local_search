import time
from puzzle import Puzzle

class PuzzleGenerator:
    def __init__(self, n_rows: int, n_columns: int, min_val: int, max_val: int):
        self.n_rows = n_rows
        self.n_columns = n_columns
        self.min_val = min_val
        self.max_val = max_val
        self.max_time = 59.9  # To make sure we don't exceed a minute

    def generate_puzzle(self) -> Puzzle:
        start_time = time.time()
        random_walk_time = 5.0  # 5 seconds
        
        return self.random_walk(random_walk_time)  # Do a random walk for some time and return the solution

    def random_walk(self, time_limit: float) -> Puzzle:
        # A very simple function that starts at a random configuration and keeps randomly modifying it
        # until it hits the time limit. Returns the best solution found so far.
        
        p = Puzzle(self.n_rows, self.n_columns, self.min_val, self.max_val)  # Generate a random puzzle
        
        # Keep track of the best puzzle found so far (and its value)
        best_puzzle = p
        best_value = p.get_value()
        
        # Keep track of the time so we don't exceed it
        start_time = time.time()
        
        # Loop until we hit the time limit
        while time.time() - start_time < time_limit - 0.1:  # To make sure we don't exceed the time limit
            # Generate a successor of p by randomly changing the value of a random cell
            # (since we are doing a random walk, we just replace p with its successor)
            p = p.get_random_successor()
            value = p.get_value() 
            
            # Update the current best solution
            if value > best_value:  
                best_value = value  
                best_puzzle = p
        
        return best_puzzle 