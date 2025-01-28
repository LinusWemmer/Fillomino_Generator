#const n=7.
#const k=6.

pos(R,C) :- R = 1..n, C = 1..n.

1 {fillomino(R,C,1..k)} 1 :- pos(R,C).
% achieved: A n×n grid is fillomino with random numbers from 1 to k.
