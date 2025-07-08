import clingo 
import copy
import random


class Fillomino_Generator:
    def __init__(self, size:int, largest_region:int, max_regions:int):
        self.size = clingo.Number(int(size))
        self.board_size = size * size
        self.largest_region = clingo.Number(int(largest_region))
        self.max_regions = clingo.Number(int(max_regions))

        generator = open("logic_programs/Fillomino_Generator.lp", "r")
        self.gen = generator.read()
        generator.close()

        solver = open("logic_programs/Fillomino_Solver.lp", "r")
        self.solver = solver.read()
        solver.close()

        h_strats = open("logic_programs/human_strategies.lp", "r")
        self.h_strats = h_strats.read()
        h_strats.close()

        # Number of steps taking in generating the puzzle
        self.step = 0

        # Solution of generated Puzzle (model & as string)
        self.solution_program_str = ""

        # The program string of the current iteration 
        self.current_program_str = ""
        # The model of the current iteration, as a List
        self.current_program_list = []

        #Steps to get from the puzzle to the solution
        self.solution_steps = []
    

    def store_solution(self, model):
        solution_fillomino = model.symbols(shown=True)
        solution_string = ""
        for atom in solution_fillomino:
            solution_string += str(atom) + ". "
            self.current_program_list.append(str(atom) + ".")
        self.solution_program_str = solution_string
        self.current_program_str = solution_string

    def generate_fillomino(self):
        # No randomization is needed; a different Fillomino is generated every time
        # For large sizes, we probably need to give random cells to reduce the search space.
        ctl = clingo.Control(arguments=["-t 8", "--stats"])
        ctl.add("base", ["n", "k", "r"], self.gen)
        ctl.ground([("base", [self.size, self.largest_region, self.max_regions])])
        print("Grounded")
        ctl.solve(on_model=self.store_solution)
        print(ctl.statistics["summary"]["times"])
        return self.current_program_list
    
    #generates a puzzle by removing random clues until there is no longer a unique solution
    def generate_puzzle_naive(self):
        self.step = 1
        removal_queue = copy.deepcopy(self.current_program_list.copy())
        copied_board = copy.deepcopy(self.current_program_list.copy())
        random.shuffle(removal_queue)
        while removal_queue:
            cell = removal_queue.pop()
            print(f"Queue Size: {len(removal_queue)}, Trying Cell: {cell}")
            copied_board.remove(cell)
            current_str = ""
            for atom in copied_board:
                current_str += atom
            ctl = clingo.Control(arguments=["-t 8", "--stats", "0"])
            ctl.add("base", [], current_str)
            ctl.ground([("base",[])])
            ctl.add("base", ["n", "k"], self.solver)
            ctl.ground([("base",[self.size, self.largest_region])])
            model_list = []
            unique = True
            with ctl.solve(yield_=True) as hnd:
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
                self.current_program_str = current_str
                self.current_program_list = copied_board
            else: 
                print(f"Failed to remove {cell}.")
                copied_board.append(cell)  
        print(self.current_program_str)                       
        return self.current_program_list
    
    def get_human_solvable_puzzle(self):
        computed_cells = self.current_program_str
        derived_cells = ""
        solved_cells = len(self.current_program_list)
        derivable = True
        fillable = False
        while not fillable:
            while derivable:
                ctl = clingo.Control(arguments=["-t 8", "--stats"])
                ctl.add("base", [], computed_cells)
                ctl.ground([("base",[])])
                ctl.add("base", ["n"], self.h_strats)
                ctl.ground([("base",[self.size])])
                print("grounded")
                with ctl.solve(yield_=True) as handle:
                    for model in handle:
                        sym_seq = model.symbols(shown=True)
                        if len(sym_seq) == 0:
                            derivable = False
                        for atom in sym_seq:
                            derived_cells += str(atom) + ". "
                            solved_cells += 1
                            computed_cells += str(atom).replace("derivable", "fillomino") + "."
                        print(derived_cells)
            if solved_cells == self.board_size:
                print("Puzzle can be solved! ")
                fillable = True
            else: 
                fillable = True
        print(solved_cells)
        print("Done.")
    
    
    def store_puzzle(self, model):
        sym_seq =  model.symbols(shown=True)
        self.current_program_list = []
        self.current_program_str = ""
        removed_cells = f"{self.step}: "
        for atom in sym_seq:
            if atom.name == "removed":
                removed_cells += str(([s.number for s in atom.arguments]))
                self.step += 1
            elif "blocked" in atom.name:
                removed_cells +="b"
            else:
                self.current_program_str += str(atom).replace("remaining", "fillomino") + ". "
                self.current_program_list.append(str(atom))
        self.solution_steps.append(removed_cells)

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
            ctl = clingo.Control(arguments=["-t 8", "--stats"])
            ctl.add("base", [], self.current_program_str)
            ctl.ground([("base",[])])
            ctl.add("base", ["n", "k"], expand_area)
            ctl.ground([("base",[self.size, self.largest_region])])
            with ctl.solve(yield_=True) as handle:
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
        return self.current_program_list
    
    

