import tkinter as tk
import re
import clingo 


class Fillomino_Generator:
    def __init__(self, length:int, max_region:int):
        self.ctl = clingo.Control(arguments=["-t 8", "--stats"])
        self.length = clingo.Number(int(length))
        self.max_region = clingo.Number(int(max_region))
        self.solution_fillomino = None

    def store_model(self, model):
        self.solution_fillomino = model.symbols(shown=True)



    def generate_fillomino(self) -> clingo.SolveHandle:
        #It seems no randomization is needed.
        solver = open("Fillomino_Solver.lp", "r")
        gen = solver.read()
        solver.close()
        self.ctl.add("base", ["n", "k"], gen)
        self.ctl.ground([("base", [self.length, self.max_region])])
        print("Grounded")
        self.ctl.solve(on_model=self.store_model)
        print(self.ctl.statistics["summary"]["times"])
        return self.solution_fillomino