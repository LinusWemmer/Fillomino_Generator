import clingo 
import subprocess
import json
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
    # This works quite reliably for size up to 7 (and works with 8)
    # For quicker testing for now:
    size = 9
    max_region = 10

    gen = Fillomino_Generator(size, max_region)
    gen_model = gen.generate_fillomino()
    print_fillomino(gen_model, size)
    puzzle = print_fillomino(gen.generate_puzzle(), size)   
    result = subprocess.run(['node', 'puzzle.js', json.dumps(puzzle)], capture_output=True, text=True)
    print(result.stdout)

