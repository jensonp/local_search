import time
from puzzle import Puzzle
import math
import random
# OBSERVATION
# 10 10 1 9 : SCORE PROP TIME, SCORE PROP SPLITS
class PuzzleGenerator:
    def __init__(self, n_rows: int, n_columns: int, min_val: int, max_val: int):
        self.n_rows = n_rows
        self.n_columns = n_columns
        self.min_val = min_val
        self.max_val = max_val
        self.T0  = None # TEMP
        self.max_time = 59.9 # MAX TIME 
        self.splits = 1 # SPLITS
        self.total_time = 10
        # self.total_time = self.max_time - 0.1 

    def generate_puzzle(self) -> Puzzle:
        time_splits = self.total_time / float(self.splits) 
        puzzle_pool = []
        for _ in range(self.splits):
            puzzle_pool.append(self.sa(time_splits))
        return max(puzzle_pool, key=lambda p: p.get_value())
    # FIND INITIAL TEMP 
    def sample(self, current: Puzzle):
        start = time.time()
        s = []
        for _ in range(100):
           candidate = current.get_random_successor()
           energy_diff = candidate.get_value() - current.get_value()
           if energy_diff > 0:
               s.append(energy_diff)
        energy_diff_mean = sum(s) / len(s) 
        self.T0 = energy_diff_mean

    def sa(self, time_limit):
        p = Puzzle(self.n_rows, self.n_columns, self.min_val, self.max_val)  # Generate a random puzzle
        while True:
            p = Puzzle(self.n_rows, self.n_columns, self.min_val, self.max_val)  # Generate a random puzzle
            if p.has_solution():
                break
        
        start_time = time.time()
        best_puzzle = p
        best_value = p.get_value()
        current_puzzle = best_puzzle
        current_value = best_value
        
        self.sample(current_puzzle)
        while time.time() - start_time < time_limit:

            # LINEAR SCHEDULE
            a = (time.time() - start_time) / time_limit
            T = self.T0 * (1 - a)

            candidate_puzzle = current_puzzle.get_random_successor()
            candidate_value = candidate_puzzle.get_value()

            # ENERGY
            delta_E = candidate_value - current_value
            if delta_E >= 0:
                current_puzzle = candidate_puzzle
                current_value = candidate_value
                if current_value > best_value:
                    best_puzzle = current_puzzle
                    best_value = current_value 
            else:
                r = random.random()
                prob = math.exp(delta_E / T)
                if r < prob:
                    current_puzzle = candidate_puzzle
                    current_value = candidate_value

        return best_puzzle