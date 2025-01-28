import tkinter as tk
import re
import clingo 
from Fillomino_Generator import *

def on_model(model):
    print(model)


def print_fillomino(fillomino_model: str):
    #solved = open(file, "r")
    #fillomino_string = solved.read()
    fillomino_list = fillomino_model.split(" ")[:-1]
    fillomino = [[0 for _ in range(7)] for _ in range(7)]
    for item in fillomino_list:
        f = re.findall(r"\(.|\s*\)", item)[0][1:-1].split(",")
        f = [int(s) for s in f]
        fillomino[f[0] -1][f[1] - 1] = f[2]
    for row in fillomino:
        print(row)
    #solved.close()


def generate_fillomino(max_region: int, width: int, ctl):
    pass


if __name__ == "__main__":
    #length = input("Length: ")
    #max_region = input("Maximum Region: ")
    length = 1
    max_region = 1
    
    gen = Fillomino_Generator(length, max_region)
    fillomino = gen.generate_fillomino()
    print_fillomino(fillomino.model().symbols(terms=True))
    print_fillomino()
