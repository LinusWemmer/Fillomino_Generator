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
        self.solution_steps = []


    def store_solution(self, model):
        self.solution_fillomino =  model.symbols(shown=True)
        for atom in self.solution_fillomino:
            self.solution_program += str(atom) + ". "
        self.current_program = self.solution_program

    def store_puzzle(self, model):
        sym_seq =  model.symbols(shown=True)
        self.current_puzzle = []
        #print(self.current_puzzle)
        #TODO: get the removed item from the puzzle
        self.current_program = ""
        for atom in sym_seq:
            if atom.name == "removed":
                self.solution_steps.append([s.number for s in atom.arguments])
            else:
                self.current_program += str(atom).replace("remaining", "fillomino") + ". "
                self.current_puzzle.append(atom)
        #for atom in self.solution_fillomino:
        #    self.solution_program += str(atom) + ". "

    def generate_fillomino(self):
        # No randomization is needed; a different Fillomino is generated every time
        # For large sizes, we probably need to give random cells to reduce the search space.
        self.ctl.add("base", ["n", "k"], self.gen)
        self.ctl.ground([("base", [self.length, self.max_region])])
        print("Grounded")
        self.ctl.solve(on_model=self.store_solution)
        print(self.ctl.statistics["summary"]["times"])
        return self.solution_fillomino
    
    def generate_stats(self):
        self.ctl.add("base", ["n", "k"], self.gen)
        self.ctl.ground([("base", [self.length, self.max_region])])
        print("Grounded")
        statistics_list = []
        for i in range (0,50):
            self.ctl.solve()
            statistics_list.append(self.ctl.statistics["summary"]["times"]["total"])
        return statistics_list
    
    
    def generate_puzzle(self):
        #TODO: probably a subset of the program should be preground to avoid recomputation, e.g. pos and the adjacency predicate
        #Though this only constitutes a small part of the computation time
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
            step +=1
        print(self.solution_steps)
        return self.current_puzzle
