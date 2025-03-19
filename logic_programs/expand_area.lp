cell(R,C) :- R = 1..n, C = 1..n.
% Assumption: We get a valid fillomino as input (a solvable one)

1 {removed(R,C,N): fillomino(R,C,N)} 1.
% Guess a Cell to remove .

remaining(R,C,N) :- fillomino(R,C,N), not removed(R,C,N).
% achieved: a random cell ist removed ist removed.

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
% achieved: connectedness is reflexive

remaining_regions(R1,C1,R2,C2) :- remaining_regions(R1,C1,R3,C3), remaining_regions(R3,C3,R2,C2).
% achieved: connectedness is transitive

remaining_region_size(R,C,N) :- N = #count{R2,C2 : remaining_regions(R,C,R2,C2)}, remaining(R,C,_).
%The region sizes of all remaining regions

removed_region(R2,C2,N) :- removed(R1,C1,N), remaining(R2,C2,N), adjacent(R1,C1,R2,C2).
removed_region(R2,C2,N) :- removed_region(R1,C1,N), remaining(R2,C2,N), adjacent(R1,C1,R2,C2).
% contains all cells that were in the region containing the removed number.

removed_region_block(R,C,R,C) :- removed_region(R,C,_).
removed_region_block(R1,C1,R2,C2) :- removed_region(R1,C1,_), removed_region(R2,C2,_), adjacent(R1,C1,R2,C2).
removed_region_block(R1,C1,R3,C3) :- removed_region_block(R1,C1,R2,C2), removed_region_block(R2,C2,R3,C3).
% contains all cells that are still "together" after removing the cell. A single cell of this region can be a "representative" of this region

blocked(R1,C1) :-  free(R1,C1), removed_region(R2,C2,N), adjacent(R1,C1,R2,C2), AREA > N, AREA = #sum{S : remaining_region_size(R3,C3,S), adjacent(R3,C3,R1,C1), remaining(R3,C3,N)}.
% A cell is blocked if expanding into this cell would yield a region that is to large.
#show blocked/2.


free_neighbor(R1,C1,R2,C2) :- free(R1,C1), removed_region_block(R2,C2,_,_), adjacent(R1,C1,R2,C2), not blocked(R1,C1).
% all free neighbors of the region (can probably be optimized to use adjacent cells of the removed cell only)

free_neighbor_count(R,C,N) :- removed_region(R,C,_), N = #count{R1,C1 : free_neighbor(R1,C1,R2,C2), removed_region_block(R2,C2,R,C)}. 

expandable_cell(R1,C1,N) :- removed(R1,C1,N), adjacent (R1,C1,R2,C2), free_neighbor_count(R2,C2,1).

only_cell :- expandable_cell(_,_,_).

:- not only_cell.

%derivable(R,C,N) :- only_cell(R,C,N).
% only one free neighbor next to region.

#show remaining/3.
#show removed/3.
%#show removed_region_block/4.
%#show derivable/3.
%#show only_cell/3.
%#show free_neighbor/4.
