import clingo 
import copy
import random


class Fillomino_Generator:
    def __init__(self, size:int, largest_region:int, max_regions:int):
        self.ctl = clingo.Control(arguments=["-t 8", "--stats"])
        self.size = clingo.Number(int(size))
        self.largest_region = clingo.Number(int(largest_region))
        self.max_regions = clingo.Number(int(max_regions))

        generator = open("logic_programs/Fillomino_Generator.lp", "r")
        self.gen = generator.read()
        generator.close()

        solver = open("logic_programs/Fillomino_Solver.lp", "r")
        self.solver = solver.read()
        solver.close()


        # Number of steps taking in generating the puzzle
        self.step = 0

        # Solution of generated Puzzle (model & as string)
        self.solution_fillomino = None
        self.solution_program = ""

        # The program string of the current iteration 
        self.current_program = ""
        # The model of the current iteration, as a List
        self.current_puzzle = []

        #Steps to get from the puzzle to the solution
        self.solution_steps = []
    

    def store_solution(self, model):
        self.solution_fillomino = model.symbols(shown=True)
        solution_string = ""
        for atom in self.solution_fillomino:
            solution_string += str(atom) + ". "
            self.current_puzzle.append(atom)
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
        self.ctl.add("base", ["n", "k", "r"], self.gen)
        self.ctl.ground([("base", [self.size, self.largest_region, self.max_regions])])
        print("Grounded")
        self.ctl.solve(on_model=self.store_solution)
        print(self.ctl.statistics["summary"]["times"])
        return self.solution_fillomino
    

    
    def generate_stats(self):
        # No randomization is needed; a different Fillomino is generated every time
        # For large sizes, we probably need to give random cells to reduce the search space.
        self.ctl.add("base", ["n", "k"], self.gen)
        self.ctl.ground([("base", [self.size, self.largest_region])])
        with self.ctl.solve(yield_=True) as handle:
            handle.get()
        return self.ctl.statistics["summary"]["times"]["total"]
    
    def generate_puzzle_naive(self):
        unique_solution = True
        self.step = 1
        removal_queue = copy.deepcopy(self.current_puzzle.copy())
        copied_board = copy.deepcopy(self.current_puzzle.copy())
        random.shuffle(removal_queue)
        for cell in removal_queue:
            print(f"Queue Size: {len(removal_queue)}, Trying Cell: {cell}")
            copied_board.remove(cell)
            current_str = ""
            for atom in copied_board:
                current_str += str(atom) + (".")
            self.ctl = clingo.Control(arguments=["-t 8", "--stats", "0"])
            self.ctl.add("base", [], current_str)
            self.ctl.ground([("base",[])])
            self.ctl.add("base", ["n", "k"], self.solver)
            self.ctl.ground([("base",[self.size, self.largest_region])])
            model_list = []
            unique = True
            with self.ctl.solve(yield_=True) as hnd:
                results = 0
                while unique:
                    hnd.resume()
                    results += 1
                    _ = hnd.wait()
                    m = hnd.model()
                    if m is None:
                        break
                    else:
                        model_list.append(m)
                    if results > 1:
                        unique = False
                        break
            if unique:
                print(f"{self.step}: Removed Cell: {cell}")
                self.step += 1
                self.current_program = current_str
                self.current_puzzle = copied_board
            else: 
                print(f"Failed to remove {cell}.")
                copied_board.append(cell)                            
        return self.current_puzzle
    
    
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
            self.ctl.ground([("base",[self.size, self.largest_region])])
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
    
    

