import tkinter as tk
import re
import clingo 

def on_model(model):
        print(model)

class Fillomino_Generator:
    def __init__(self, length:int, max_region:int):
        self.ctl = clingo.Control(arguments=["-t 8"])
        self.length = clingo.Number(int(length))
        self.max_region = clingo.Number(int(max_region))

    

    def generate_fillomino(self) -> clingo.SolveHandle:
        solver = open("Fillomino_Solver.lp", "r")
        gen = solver.read()
        solver.close()
        self.ctl.add("base", ["n", "k"], gen)
        self.ctl.ground([("base", [self.length, self.max_region])])
        print("grounded")
        return self.ctl.solve(yield_=True)
