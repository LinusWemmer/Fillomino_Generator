import clingo 
import time


class Fillomino_Generator:
    def __init__(self, length:int, max_region:int):
        self.ctl = clingo.Control(arguments=["-t 8", "--stats"])
        self.length = clingo.Number(int(length))
        self.max_region = clingo.Number(int(max_region))

        solver = open("logic_programs/Fillomino_Solver.lp", "r")
        self.gen = solver.read()
        solver.close()

        # Solution of generated Puzzle
        self.solution_fillomino = None
        self.solution_program = ""

        # The program string of the current 
        self.current_program = ""
        # The model of the current iteration, as per the clingo api
        self.current_puzzle = []

        #Steps to get from the puzzle to the solution
        self.solution_steps = []
        


    def store_solution(self, model):
        self.solution_fillomino =  model.symbols(shown=True)
        solution_string = ""
        for atom in self.solution_fillomino:
            solution_string += str(atom) + ". "
        self.solution_program = solution_string
        self.current_program = solution_string

    def store_puzzle(self, model):
        sym_seq =  model.symbols(shown=True)
        self.current_puzzle = []
        self.current_program = ""
        removed_cells = f"{self.step}: "
        for atom in sym_seq:
            if atom.name == "removed":
                removed_cells += str(([s.number for s in atom.arguments]))
                self.step += 1
            elif "blocked" in atom.name:
                removed_cells +="b"
            else:
                self.current_program += str(atom).replace("remaining", "fillomino") + ". "
                self.current_puzzle.append(atom)
        self.solution_steps.append(removed_cells)

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
        # No randomization is needed; a different Fillomino is generated every time
        # For large sizes, we probably need to give random cells to reduce the search space.
        self.ctl.add("base", ["n", "k"], self.gen)
        self.ctl.ground([("base", [self.length, self.max_region])])
        with self.ctl.solve(yield_=True) as handle:
            handle.get()
        return self.ctl.statistics["summary"]["times"]["total"]
    
    
    def generate_puzzle(self):
        #TODO: probably a subset of the program should be preground to avoid recomputation, e.g. pos and the adjacency predicate
        #Though this only constitutes a small part of the computation time
        #TODO: probably add heuristic to prioritize numbers with few neighbours, to avoid early splitting of regions
        satisfiable = True
        self.step = 1
        expand_area_string = open("logic_programs/expand_area.lp", "r")
        expand_area = expand_area_string.read()
        expand_area_string.close()
        enter_one_string = open("logic_programs/enter_one.lp", "r")
        enter_one = enter_one_string.read()
        enter_one_string.close()
        while satisfiable:
            self.ctl = clingo.Control(arguments=["-t 8", "--stats"])
            self.ctl.add("base", [], self.current_program)
            self.ctl.ground([("base",[])])
            self.ctl.add("base", ["n", "k"], expand_area)
            self.ctl.ground([("base",[self.length, self.max_region])])
            with self.ctl.solve(yield_=True) as handle:
                best_model = None
                for model in handle:
                    best_model = model
                result = handle.get()
                if result.unsatisfiable:
                    satisfiable = False
                else:
                    self.store_puzzle(best_model)
            print(self.step)
        print(self.solution_steps)
        return self.current_puzzle
    

    # Multiple Tries to generate an efficient puzzle
    # TODO: we should probably start at a different place in the search area, as of now multiple tries can generate the same puzzle
  #  def generate_puzzle_maximize(self, n: int):
   #     solver = open("logic_programs/expand_area.lp", "r")
    #    expand_area = solver.read()
     #   solver.close()
      #  puzzle_steps = []
       # puzzle_list = []
        #for i in range(0,n):
         #   self.solution_steps = []
          #  satisfiable = True
           # self.current_program = self.solution_program
            #step = 1
            #while satisfiable:
             #   print(step)
              #  self.ctl = clingo.Control(arguments=["-t 8", "--stats"])
               # self.ctl.add("base", [], self.current_program)
                #self.ctl.ground([("base",[])])
                
                #self.ctl.add("base", ["n", "k"], expand_area)
               # self.ctl.ground([("base",[self.length, self.max_region])])
              #  if self.ctl.solve(on_model=self.store_puzzle(step)).unsatisfiable:
             #       satisfiable = False  
            #        puzzle_steps.append(step)
           #         puzzle_list.append(self.current_puzzle)
         #           self.current_program = self.solution_fillomino
          #      step +=1
        #    print(self.solution_steps)
       # max_index = puzzle_list.index(max(puzzle_list))
      #  print(puzzle_steps)
     #   return puzzle_list[max_index]
     #   return self.current_puzzle
    

