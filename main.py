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
    print("Generate Fillominos with ASP...\n")
    size = input("Size: ")
    largest_region = input("Largest Region: ")
    max_regions = input("Maximum region number (Warning: scales horribly, recommended 25): ")
    # For quicker testing for now:
    if size == "":
        size = 5
    if largest_region == "":
        largest_region = 7
    max_regions = 25
    start_time = time.time()
    print("Starting!\n")
    gen = Fillomino_Generator(int(size), int(largest_region), max_regions)
    gen_model_str = gen.generate_fillomino()
    print_fillomino(gen_model_str, size)
    puzzle = print_fillomino(gen.generate_puzzle_weighted(), int(size))
    result = subprocess.run(['node', 'puzzle.js', json.dumps(puzzle)], capture_output=True, text=True)
    print(result.stdout)
    print(f"Total Computation Time:{time.time()-start_time}")
    

