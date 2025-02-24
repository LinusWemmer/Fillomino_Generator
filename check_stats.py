import clingo
from Fillomino_Generator import *

import statistics


if __name__ == "__main__":
    size = 6
    max_region = 5

    gen1 = Fillomino_Generator(size, max_region)
    times1 = gen1.generate_stats()
    average1 = statistics.mean(times1)

    gen2 = Fillomino_Generator_Alt(size, max_region)
    times2 = gen1.generate_stats()
    average2 = statistics.mean(times2)
    print("Old Method Average Time: " + str(average1))
    print("New Method Average Time: " + str(average2))