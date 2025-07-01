import clingo 
import subprocess
import json
import time
from Fillomino_Generator import *


def on_model(model):
    print(model)
clingo.SymbolType

def print_fillomino(gen_model, size: int):
    #solved = open(file, "r")
    #fillomino_string = solved.read()
    fillomino_list = gen_model
    fillomino = [[0 for _ in range(int(size))] for _ in range(int(size))]
    for item in fillomino_list:
        cell = item.arguments
        cell = [s.number for s in cell]
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
    largest_region = 5
    max_regions = 25
    start_time = time.time()
    print("Starting!\n")
    gen = Fillomino_Generator(size, largest_region, max_regions)
    gen_model = gen.generate_fillomino()
    print_fillomino(gen_model, size)
    puzzle = print_fillomino(gen.generate_puzzle_naive(), size)   
    result = subprocess.run(['node', 'puzzle.js', json.dumps(puzzle)], capture_output=True, text=True)
    print(result.stdout)
    print(f"Total Computation Time:{time.time()-start_time}")

