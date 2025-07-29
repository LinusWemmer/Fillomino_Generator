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

        h_max = open("logic_programs/max_human_strategies_choice.lp", "r")
        self.h_max = h_max.read()
        h_max.close()

        h_min = open("logic_programs/min_human_strategies_choice.lp", "r")
        self.h_min = h_min.read()
        h_min.close()

        h_unique = open("logic_programs/human_strategies_non_unique.lp", "r")
        self.h_unique = h_unique.read()
        h_unique.close()

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
        self.solution_program_str = ""
        for atom in solution_fillomino:
            solution_string += str(atom) + ". "
            self.current_program_list.append(str(atom) + ".")
        self.current_program_str = solution_string
        self.solution_program_str = solution_string.replace("fillomino", "solution")

    def generate_fillomino(self):
        # No randomization is needed; a different Fillomino is generated every time
        # For large sizes, we probably need to give random cells to reduce the search space.
        self.current_program_list= []
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
            ctl = clingo.Control(arguments=["-t 8", "--stats", "2"])
            ctl.add("base", [], current_str)
            ctl.ground([("base",[])])
            ctl.add("base", ["n", "k"], self.solver)
            ctl.ground([("base",[self.size, self.largest_region])])
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
    
    def get_human_solvable_puzzle(self, options="max"):
        computed_cells = self.current_program_str
        derived_cells = ""
        solved_cells = len(self.current_program_list)
        filled = False
        derivable = True
        if options == "max":
            h_opt = self.h_max
        elif options == "min":
            h_opt = self.h_min
        else:
            print("enter valid stuff")
            return
        while not filled:
            while derivable:
                # Derive cells using human strategies until failure
                ctl = clingo.Control(["-t 8", "--stats"])
                ctl.add("base", [], computed_cells)
                ctl.ground([("base",[])])
                ctl.add("base", ["n"], self.h_strats)
                ctl.ground([("base",[self.size])])
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
                filled = True
            else: 
                # Add cell such that more information can be derived
                ctl = clingo.Control(arguments=["-t 8", "--opt-mode=optN"])
                ctl.add("base", [], self.solution_program_str)
                ctl.ground([("base",[])])
                ctl.add("base", [], computed_cells)
                ctl.ground([("base",[])])
                ctl.add("base", ["n"], h_opt)
                ctl.ground([("base",[self.size])])
                with ctl.solve(yield_=True) as handle:
                    for model in handle:
                        print(model.cost)
                        if model.optimality_proven:
                            for atom in model.symbols(shown=True):
                                selected = str(atom).replace("selected", "fillomino") 
                                self.current_program_str += selected + "."
                                computed_cells += selected + "."
                                self.current_program_list.append(selected)
                                solved_cells += 1
                                print(f"Added {selected} to puzzle.")
                            derivable = True
                            break
        print("Done.")
        return self.current_program_list
    
    
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
            solved_cells = len(copied_board)
            computed_cells = current_str
            derivable = True
            # Derive cells using human strategies until failure
            while derivable:
                ctl = clingo.Control(["-t 8", "--stats"])
                ctl.add("base", [], computed_cells)
                ctl.ground([("base",[])])
                ctl.add("base", ["n"], self.h_unique)
                ctl.ground([("base",[self.size])])
                with ctl.solve(yield_=True) as handle:
                    for model in handle:
                        sym_seq = model.symbols(shown=True)
                        if len(sym_seq) == 0:
                            derivable = False
                        for atom in sym_seq:
                            solved_cells += 1
                            computed_cells += str(atom).replace("derivable", "fillomino") + "."
            if solved_cells == self.board_size:
                print(f"{self.step}: Removed Cell: {cell}")
                self.step += 1
                self.current_program_str = current_str
                self.current_program_list = copied_board
            else: 
                print(f"Failed to remove {cell}")
                copied_board.append(cell) 
        print(self.current_program_str)
        return self.current_program_list
    
    

