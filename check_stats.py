import clingo
from Fillomino_Generator import *
import matplotlib.pyplot as plt
from collections import Counter
import statistics


def most_frequent(List):
    occurence_count = Counter(List)
    return occurence_count.most_common(1)[0][0]

if __name__ == "__main__":
    size = 5
    largest_region = 7
    max_regions = 25
    removals = [8,9,9,10,11,9,8,12,9,8,10,8,8,8,8,8,8]
    gen = Fillomino_Generator(size, largest_region, max_regions)
    for i in range(0,10):
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