%#const n=7.
%#const k=6.

pos(R,C) :- R = 1..n, C = 1..n.

1 {fillomino(R,C,1..k)} 1 :- pos(R,C).
% achieved: A n×n grid is fillomino with random numbers from 1 to k.

connected(R1,C,R2,C) :- fillomino(R1,C,N), fillomino(R2,C,N), R2 = R1+1.
connected(R,C1,R,C2) :- fillomino(R,C1,N), fillomino(R,C2,N), C2 = C1+1.
% achieved: neighboring cells with the same number are connected.

connected(R,C,R,C) :- pos(R,C).
% achieved: connectedness is reflexive 

connected(R1,C1,R2,C2) :- connected(R2,C2,R1,C1).
% achieved: connectedness is symmetric

connected(R1,C1,R2,C2) :- connected(R1,C1,R3,C3), connected(R3,C3,R2,C2).
% achieved: connectedness is transitive

connected_count(R1,C1,N) :- N = #count{R2,C2 : connected(R1,C1,R2,C2)}, pos(R1,C1).

N1 = N2 :- connected_count(R,C,N1), fillomino(R,C,N2).
% achieved: Cells fillomino with number N are in a region of size N.

#show fillomino/3.
