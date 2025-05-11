import time
from puzzle import Puzzle
import math
import random

class PuzzleGenerator:
    def __init__(self, n_rows: int, n_columns: int, min_val: int, max_val: int):
        self.n_rows = n_rows
        self.n_columns = n_columns
        self.min_val = min_val
        self.max_val = max_val
        self.max_time = 59.9  # To make sure we don't exceed a minute

        self.T0  = None # Initial Temperature Declaration
        
        
        self.alpha = 0.98 # GEOMETRIC 

        self.best_of_best_splits = 10 # number of times to run the current split, and total total 
        # in order to see if it's possible to get a better time from multiple runs vs 1 

        # SPLITS
        # self.splits = 10
        self.splits = 6 # how many time intervals to create 
        # self.splits = 3
        # self.splits = 1 # no splits OR call sa()

        # TOTAL TIME
        self.total_time = self.max_time - 0.1 # THE ONE MINUTE LIMIT FOR REAL   
        # self.total_time = 50 #
        # self.total_time = 10 - 0.1
        # self.total_time = 5 - 0.1
        # self.total_time = 1 - 0.1



    def generate_puzzle(self) -> Puzzle:
        start_time = time.time() 
        # self.collect_best_of_best_splits(self.total_time) # collect best time from multiple x total_time runs

        # total_time = 5
        # return self.sa(total_time) # no splits 
        # return self.sa(self.total_time) # no splits 
        # exit()
        return self.random_walk(self.total_time)  # Do a random walk for some time and return the solution
    
    def schedule(self, k):
        return self.T0 * math.pow(self.alpha, k)
    
    # FIND INITIAL TEMP 
    def sample(self, current: Puzzle):
        start = time.time()
        s = []
        for _ in range(1000):
           candidate = current.get_random_successor()
           energy_diff = candidate.get_value() - current.get_value()
           if energy_diff > 0:
               s.append(energy_diff)
        energy_diff_mean = sum(s) / len(s) 
        # print(energy_diff_mean)
        # print(time.time() - start)
        self.T0 = energy_diff_mean
        # exit()

    def sa(self, time_limit):
        p = Puzzle(self.n_rows, self.n_columns, self.min_val, self.max_val)  # Generate a random puzzle
        while True:
            p = Puzzle(self.n_rows, self.n_columns, self.min_val, self.max_val)  # Generate a random puzzle
            if p.has_solution():
                #print(p.get_value())
                break
        
        start_time = time.time()
        best_puzzle = p
        best_value = p.get_value()
        current_puzzle = best_puzzle
        current_value = best_value
        
        # GENERATE INITIAL TEMP
        self.sample(current_puzzle)
        # k = 0 # log cooling 
        # k_max # log cooling
        while time.time() - start_time < time_limit:
            # k += 1 # log cooling

            # geometric
            # T = self.schedule(k)
            # avoid zero division
            # if T <= 0.0:
            #     T = 1e-8
            
            # log cooling
            # T = self.T0 / math.log(1+k)

            # linear 
            a = (time.time() - start_time) / time_limit
            T = self.T0 * (1 - a)

            candidate_puzzle = current_puzzle.get_random_successor()
            candidate_value = candidate_puzzle.get_value()

            # ENERGY
            # E() = -value 
            delta_E = candidate_value - current_value
            if delta_E >= 0:
                # print(delta_E)
                current_puzzle = candidate_puzzle
                current_value = candidate_value
                if current_value > best_value:
                    best_puzzle = current_puzzle
                    best_value = current_value 
            else:
                # print(delta_E)
                r = random.random()
                # print(candidate_value)
                # print(current_value)
                try: 
                    prob = math.exp(delta_E / T)
                    if r < prob:
                        current_puzzle = candidate_puzzle
                        current_value = candidate_value
                except OverflowError as e:
                    print(f"Error: {e}")
                    print(f"T: {T}")
                    #print(f"k: {k}")
                    print(f"candidate value: {candidate_value}")
                    print(f"current value: {candidate_value}")
                    print(f"diff : {delta_E}")
                    # exit()

                # if a <= math.exp(-1 * (candidate_value - current_value)/ T ):
                #     current_puzzle = candidate_puzzle
                #     current_value = candidate_value

        return best_puzzle
    def collect_best_of_best_splits(self, total_time):
        v = []
        for _ in range(self.best_of_best_splits):
            a = self.random_walk(total_time).get_value()
            v.append(a) 
        print(v)
        print(f"MAX {max(v)}")
        exit()

    def random_walk(self, total_time : float) -> Puzzle:
        #print(p.get_value())
        # temp = 10
        # total_time = 50
        # a = time.time()

        # Restarting  
        time_interval = total_time / float(self.splits)
        ALL_TIME_BEST_PUZZLE_POOL = []
        for _ in range(self.splits):
            ALL_TIME_BEST_PUZZLE_POOL.append(self.sa(time_interval))
        absolute_best_puzzle = max(ALL_TIME_BEST_PUZZLE_POOL, key=lambda p: p.get_value())
        # absolute_best_puzzle.print_puzzle()
        #exit()
        return absolute_best_puzzle