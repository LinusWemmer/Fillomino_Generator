import tkinter as tk
import re



def print_fillomino(file):
    solved = open(file, "r")
    fillomino_string = solved.read()
    fillomino_list = fillomino_string.split(".")[:-1]
    fillomino = [[0 for _ in range(7)] for _ in range(7)]
    for item in fillomino_list:
        f = re.findall(r"\(.*\)", item)[0][1:-1].split(",")
        f = [int(s) for s in f]
        fillomino[f[0] -1][f[1] - 1] = f[2]
    for row in fillomino:
        print(row)
    solved.close()



print_fillomino("partially_solved.lp")
