import clingo
from Fillomino_Generator import *
import matplotlib.pyplot as plt
from collections import Counter
import statistics


def most_frequent(List):
    occurence_count = Counter(List)
    return occurence_count.most_common(1)[0][0]

def check_naive(iterations: int):
    size = 5
    largest_region = 7
    max_regions = 25
    removals = []
    gen = Fillomino_Generator(size, largest_region, max_regions)
    for i in range(0,iterations):
        gen.generate_fillomino()
        size = len(gen.generate_puzzle_naive())
        removals.append(size)
    plt.hist(removals, bins=range(min(removals), max(removals) + 2), align='left', rwidth=0.8, color='skyblue', edgecolor='black')
    max_count = removals.count(most_frequent(removals)) 

    plt.xlabel('Remaining')
    plt.xticks(range(min(removals), max(removals) + 1))
    plt.ylabel('Frequency')
    plt.yticks((range(0,max_count + 1)))
    plt.show()

def check_top_down(iterations:int):
    size = 6
    largest_region = 7
    max_regions = 25
    removals = []
    gen = Fillomino_Generator(size, largest_region, max_regions)
    for i in range(0,iterations):
        gen.generate_fillomino()
        size = len(gen.generate_puzzle())
        removals.append(size)
    plt.hist(removals, bins=range(min(removals), max(removals) + 2), align='left', rwidth=0.8, color='skyblue', edgecolor='black')
    max_count = removals.count(most_frequent(removals)) 

    plt.xlabel('Remaining')
    plt.xticks(range(min(removals), max(removals) + 1))
    plt.ylabel('Frequency')
    plt.yticks((range(0,max_count + 1)))
    plt.show()

if __name__ == "__main__":
    check_top_down(50)