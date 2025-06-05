% Input: A valid encoding for a Fillomino, constants n.. Size of the grid

cell(R,C) :- R = 1..n, C = 1..n.
free(R,C) :- cell(R,C), not fillomino(R,C,_).

adjacent(R1,C,R2,C) :- cell(R1,C), cell(R2,C), R2 = R1 + 1.
adjacent(R1,C,R2,C) :- cell(R1,C), cell(R2,C), R2 = R1 - 1.
adjacent(R,C1,R,C2) :- cell(R,C1), cell(R,C2), C2 = C1 + 1.
adjacent(R,C1,R,C2) :- cell(R,C1), cell(R,C2), C2 = C1 - 1.

region(R1,C,R2,C) :- fillomino(R1,C,N), fillomino(R2,C,N), R2 = R1+1.
region(R,C1,R,C2) :- fillomino(R,C1,N), fillomino(R,C2,N), C2 = C1+1.
% achieved: neighboring cells with the same number are region/in the same Region

region(R,C,R,C) :- fillomino(R,C,_).
% achieved: regionness is reflexive 

region(R1,C1,R2,C2) :- region(R2,C2,R1,C1).
% achieved: regionness is symmetric

region(R1,C1,R2,C2) :- region(R1,C1,R3,C3), region(R3,C3,R2,C2).
% achieved: regionness is transitive

region_size(R1,C1,N) :- N = #count{R2,C2 : region(R1,C1,R2,C2)}, cell(R1,C1).

unfinished_region(R,C,N) :- fillomino(R,C,N), region_size(R,C,M), M != N.
% regions that aren't full yet.

expandable_candidate(R1,C1,N) :- unfinished_region(R2,C2,N), adjacent(R1,C1,R2,C2), free(R1,C1).
% cells that a region could potentially be expanded to.

expandable_count(R1,C1,S) :- S = #count{R2,C2 : expandable_candidate(R2,C2,N), adjacent(R2,C2,R1,C1)}, unfinished_region(R1,C1,N), region(R1,C1,R3,C3).
% How many cells a region can be expanded to.

derivable(R1,C1,N) :- expandable_candidate(R1,C1,N), adjacent(R1,C1,R2,C2), expandable_count(R2,C2,1), unfinished_region(R2,C2,N).

#show derivable/3.