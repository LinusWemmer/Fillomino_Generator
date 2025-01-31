import tkinter as tk
import re
import clingo 


class Fillomino_Generator:
    def __init__(self, length:int, max_region:int):
        self.ctl = clingo.Control(arguments=["-t 8", "--stats"])
        self.length = clingo.Number(int(length))
        self.max_region = clingo.Number(int(max_region))
        solver = open("logic_programs/Fillomino_Solver.lp", "r")
        self.gen = solver.read()
        solver.close()
        self.solution_fillomino = None
        self.solution_program = ""
        self.current_program = ""

    def store_solution(self, model):
        self.solution_fillomino =  model.symbols(shown=True)
        for atom in self.solution_fillomino:
            self.solution_program += str(atom) + ". "
        self.current_program = self.solution_program

    def store_puzzle(self, model):
        self.current_puzzle =  model.symbols(shown=True)
        #TODO: remove only:
        self.current_program = ""
        for atom in self.current_puzzle:
            if not ("only_cell" in str(atom)):   #TODO: this is very inefficient + inelegenant(though tolearble complexity wise), remove this
                self.current_program += str(atom).replace("remaining", "fillomino") + ". "
        print(self.current_program)
        #for atom in self.solution_fillomino:
        #    self.solution_program += str(atom) + ". "

    def generate_fillomino(self):
        #It seems no randomization is needed.
        self.ctl.add("base", ["n", "k"], self.gen)
        self.ctl.ground([("base", [self.length, self.max_region])])
        print("Grounded")
        self.ctl.solve(on_model=self.store_solution)
        print(self.ctl.statistics["summary"]["times"])
        return self.solution_fillomino
    
    def generate_puzzle(self):
        
        satisfiable = True
        step = 1
        while satisfiable:
            print(step)
            self.ctl = clingo.Control(arguments=["-t 8", "--stats"])
            self.ctl.add("base", [], self.current_program)
            self.ctl.ground([("base",[])])
            solver = open("logic_programs/only_space.lp", "r")
            one_step = solver.read()
            solver.close()
            self.ctl.add("base", ["n", "k"], one_step)
            self.ctl.ground([("base",[self.length, self.max_region])])
            if self.ctl.solve(on_model=self.store_puzzle).unsatisfiable:
                satisfiable = False        
        return self.current_puzzle
