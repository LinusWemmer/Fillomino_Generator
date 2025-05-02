cell(R,C) :- R = 1..n, C = 1..n.
% Assumption: We get a valid fillomino as input (a solvable one)

1 {removed(R,C,N): fillomino(R,C,N)} 1.
% Guess a Cell to remove .

remaining(R,C,N) :- fillomino(R,C,N), not removed(R,C,N).
% achieved: a random cell ist removed ist removed.

:- remaining(R,C,N), removed(R,C,N).

free(R,C) :- cell(R,C), not remaining(R,C,_).
% all cells not filled by a number.

adjacent(R1,C,R2,C) :- cell(R1,C), cell(R2,C), R2 = R1 + 1.
adjacent(R1,C,R2,C) :- cell(R1,C), cell(R2,C), R2 = R1 - 1.
adjacent(R,C1,R,C2) :- cell(R,C1), cell(R,C2), C2 = C1 + 1.
adjacent(R,C1,R,C2) :- cell(R,C1), cell(R,C2), C2 = C1 - 1.

remaining_regions(R1,C,R2,C) :- remaining(R1,C,N), remaining(R2,C,N), adjacent(R1,C,R2,C).
remaining_regions(R,C1,R,C2) :- remaining(R,C1,N), remaining(R,C2,N), adjacent(R,C1,R,C2).
% achieved: neighboring cells with the same number are connected.

remaining_regions(R,C,R,C) :- remaining(R,C,_).
% reflexivity

remaining_regions(R1,C1,R2,C2) :- remaining_regions(R1,C1,R3,C3), remaining_regions(R3,C3,R2,C2).
% transitivity

remaining_region_size(R,C,N) :- N = #count{R2,C2 : remaining_regions(R,C,R2,C2)}, remaining(R,C,_).
%The region sizes of all remaining regions

blocked(R1,C1) :-  free(R1,C1), removed_region(R2,C2,N), adjacent(R1,C1,R2,C2), (AREA +1) > N, AREA = #sum{S : remaining_region_size(R3,C3,S), adjacent(R3,C3,R1,C1), remaining(R3,C3,N)}.
% A cell is blocked if expanding into this cell would yield a region that is to large.


removed_region(R2,C2,N) :- removed(R1,C1,N), remaining(R2,C2,N), adjacent(R1,C1,R2,C2).
removed_region(R2,C2,N) :- removed_region(R1,C1,N), remaining(R2,C2,N), adjacent(R1,C1,R2,C2).
% contains all cells that were in the region containing the removed number.


max_region(R1,C1,R1,C1) :- removed(R2,C2,N), adjacent(R1,C1,R2,C2), remaining(R1,C1,N).
% Cells that are empty or in the same region as the removed block are in the maximum expansion of the region

max_region(R1,C1,R2,C2) :- max_region(R2,C2,R2,C2), remaining(R2,C2,N), remaining(R1,C1,N), adjacent(R1,C1,R2,C2).
max_region(R1,C1,R2,C2) :- max_region(R2,C2,R2,C2), free(R1,C1), not removed(R1,C1,_), adjacent(R1,C1,R2,C2), not blocked(R1,C1).

max_region(R1,C1,R2,C2) :- max_region(R2,C2,R1,C1).
%symmetry

max_region(R,C,R,C) :- max_region(R,C,_,_).
%reflexivity

max_region(R1,C1,R2,C2) :- max_region(R1,C1,R3,C3), max_region(R3,C3,R2,C2).
%transitivity

max_region_size(R1,C1,MAX) :- max_region(R1,C1,_,_), MAX = #count{R3,C3 : max_region(R3,C3,R1,C1)}, adjacent(R1,C1,R2,C2), removed(R2,C2,_).

expandable_cell(R1,C1,N) :- removed(R1,C1,N), adjacent (R1,C1,R2,C2), remaining(R2,C2,N), max_region_size(R2,C2,MAX), MAX < N.

derivable(R,C,N) :- expandable_cell(R,C,N).
:- removed(R,C,N), not derivable(R,C,N), N > 1.

neighbor(R1,C1,N) :- adjacent(R1,C1,R2,C2), removed(R2,C2,1), remaining(R1,C1,N).

:- removed(R1,C1,1), neighbor(R2,C2,N), not remaining_region_size(R2,C2,N).
% all neighboring regions have to be full
 
:- removed(R1,C1,1), adjacent(R1,C1,R2,C2), free(R2,C2).

#maximize{1 : blocked(_,_)}.
% Try to guide the program to apply "more interesting" rules

#show remaining/3.
#show removed/3.
#show blocked/2.
