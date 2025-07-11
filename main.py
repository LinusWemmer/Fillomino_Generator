import clingo 
import subprocess
import json
import time
import re
from Fillomino_Generator import *


def on_model(model):
    print(model)
clingo.SymbolType

def print_fillomino(gen_model, size: int):
    fillomino_list = gen_model
    fillomino = [[0 for _ in range(int(size))] for _ in range(int(size))]
    for item in fillomino_list:
        cell = [int(x) for x in re.findall(r'\d+', item)]
        fillomino[cell[0] -1][cell[1] - 1] = cell[2]
    for row in fillomino:
        print(row)
    print("")
    return fillomino


if __name__ == "__main__":
    # size = input("Size: ")
    # max_region = input("Maximum Region: ")
    # For quicker testing for now:
    size = 5
    largest_region = 7
    max_regions = 25
    start_time = time.time()
    print("Starting!\n")
    gen = Fillomino_Generator(size, largest_region, max_regions)
    gen_model_str = gen.generate_fillomino()
    print_fillomino(gen_model_str, size)
    gen.generate_puzzle_naive()
    puzzle = print_fillomino(gen.get_human_solvable_puzzle(), size)   
    result = subprocess.run(['node', 'puzzle.js', json.dumps(puzzle)], capture_output=True, text=True)
    print(result.stdout)
    print(f"Total Computation Time:{time.time()-start_time}")

