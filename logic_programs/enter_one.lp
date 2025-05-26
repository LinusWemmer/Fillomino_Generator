cell(R,C) :- R = 1..n, C = 1..n.
% Assumption: We get a valid fillomino as input (a solvable one)

1 {removed(R,C,1): fillomino(R,C,1)} 1.
% Guess a Cell filled with a one to remove .

remaining(R,C,N) :- fillomino(R,C,N), not removed(R,C,N).

free(R,C) :- cell(R,C), not remaining(R,C,_).
% all cells not filled by a number.

adjacent(R1,C,R2,C) :- cell(R1,C), cell(R2,C), R2 = R1 + 1.
adjacent(R1,C,R2,C) :- cell(R1,C), cell(R2,C), R2 = R1 - 1.
adjacent(R,C1,R,C2) :- cell(R,C1), cell(R,C2), C2 = C1 + 1.
adjacent(R,C1,R,C2) :- cell(R,C1), cell(R,C2), C2 = C1 - 1.

neighbor(R1,C1,N) :- adjacent(R1,C1,R2,C2), removed(R2,C2,1), remaining(R1,C1,N).

remaining_regions(R1,C,R2,C) :- remaining(R1,C,N), remaining(R2,C,N), adjacent(R1,C,R2,C).
remaining_regions(R,C1,R,C2) :- remaining(R,C1,N), remaining(R,C2,N), adjacent(R,C1,R,C2).
% achieved: neighboring cells with the same number are connected.

remaining_regions(R,C,R,C) :- remaining(R,C,_).
% achieved: connectedness is reflexive

remaining_regions(R1,C1,R2,C2) :- remaining_regions(R1,C1,R3,C3), remaining_regions(R3,C3,R2,C2).
% achieved: connectedness is transitive

remaining_region_size(R,C,N) :- N = #count{R2,C2 : remaining_regions(R,C,R2,C2)}, remaining(R,C,_).
%The region sizes of all remaining regions

:- removed(R1,C1,1), neighbor(R2,C2,N), not remaining_region_size(R2,C2,N).
% all neighboring regions have to be full
 
:- removed(R1,C1,1), adjacent(R1,C1,R2,C2), free(R2,C2).

#show removed/3.
#show remaining/3.


