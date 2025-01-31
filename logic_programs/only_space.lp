%#const n=7.
%#const k=6.

pos(R,C) :- R = 1..n, C = 1..n.
% Assumption: We get a valid fillomino as input (a solvable one)

1 {removed(R,C,N): fillomino(R,C,N)} 1.
 % nextfillomino(R,C,N) :- fillomino(R,C,N), not remove(R,C,N).

remaining(R,C,N) :- fillomino(R,C,N), not removed(R,C,N).
% achieved: a random tile ist removed ist removed.

free(R,C) :- pos(R,C), not remaining(R,C,_).
% all board positions not filled.

adjacent(R1,C,R2,C) :- pos(R1,C), pos(R2,C), R2 = R1 + 1.
adjacent(R1,C,R2,C) :- pos(R1,C), pos(R2,C), R2 = R1 - 1.
adjacent(R,C1,R,C2) :- pos(R,C1), pos(R,C2), C2 = C1 + 1.
adjacent(R,C1,R,C2) :- pos(R,C1), pos(R,C2), C2 = C1 - 1.


removed_region(R2,C2,N) :- removed(R1,C1,N), remaining(R2,C2,N), adjacent(R1,C1,R2,C2).
removed_region(R2,C2,N) :- removed_region(R1,C1,N), remaining(R2,C2,N), adjacent(R1,C1,R2,C2).
% contains all cells that were in the region containing the removed number.

removed_region_block(R,C,R,C) :- removed_region(R,C,_).
removed_region_block(R1,C1,R2,C2) :- removed_region(R1,C1,_), removed_region(R2,C2,_), adjacent(R1,C1,R2,C2).
removed_region_block(R1,C1,R3,C3) :- removed_region_block(R1,C1,R2,C2), removed_region_block(R2,C2,R3,C3).
% contains all cells that are still "together" after removing an element (incl reflexivity). A single cell of this region can be a "representative" of this region

blocked_neighbor(R1,C1) :- remaining(R1,C1,N1), removed_region(R2,C2,N2), adjacent(R1,C1,R2,C2), N1 != N2.
%TODO: blocked neighbor probably relevant later, not now (for marking empty cells which are blocked by logic). 

free_neighbor(R1,C1,R2,C2) :- free(R1,C1), removed_region_block(R2,C2,_,_), adjacent(R1,C1,R2,C2).
% all free neighbors of the region (can probably be optimized to use adjacent cells of the removed cell only)

free_neighbor_count(R,C,N) :- removed_region(R,C,_), N = #count{R1,C1 : free_neighbor(R1,C1,R2,C2), removed_region_block(R2,C2,R,C)}. 

only_cell(R1,C1,N) :- removed(R1,C1,N), adjacent (R1,C1,R2,C2), free_neighbor_count(R2,C2,1).

only_cell :- only_cell(_,_,_).

:- not only_cell.

%derivable(R,C,N) :- only_cell(R,C,N).
% only one free neighbor next to region.
% TODO: what if the removal "breaks" a region in half/more pieces?

#show remaining/3.
%#show removed_region_block/4.
%#show derivable/3.
%#show only_cell/3.
%#show free_neighbor/4.
