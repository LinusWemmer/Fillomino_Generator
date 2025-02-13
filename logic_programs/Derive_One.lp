cell(R,C) :- R = 1..n, C = 1..n.
% Assumption: We get a valid fillomino as input (a solvable one)

1 {removed(R,C,1): fillomino(R,C,1)} 1.
% Try to remove a one

remaining(R,C,N) :- fillomino(R,C,N), not removed(R,C,N).
% achieved: a random tile ist removed ist removed.

free(R,C) :- cell(R,C), not remaining(R,C,_).
% all board positions not filled.

neighboring_region(R1,C1,R1,C1) :- removed(R2,C2,1), adjacent(R1,C1,R2,C2), not free(R1,C1). 
neighboring_region(R1,C1,R2,C2) :- neighboring_region(R2,C2,_,_), remaining(R1,C1,N), remaining(R2,C2,N), adjacent(R1,C1,R2,C2).
neighboring_region(R1,C1,R3,C3) :- neighboring_region(R1,C1,R2,C2), neighboring_region(R2,C2,R3,C3).
% regions defined as always for all neighbors of the removed cell filled with one. TODO: We will require the removed number to be a one if we derive these. This is again a reflexive transitive closure, but should be relatively quick to compute as we have been given a valid fillomino, so no search is necessary

%neighboring_region_count(R1,C1,N) :- removed(R2,C2,1), adjacent(R1,C1,R2,C2), N = #count{R3,C3 : neighboring_region(R3,C3,R1,C1)}.

N1 = N2:- removed(R1,C1,1), adjacent(R2,C2,R1,C1), remaining(R2,C2,N1), N2 = #count{R3,C3 : neighboring_region(R3,C3,R2,C2)}.
%TODO: Fix this one

:- removed(R1,C1,1), adjacent(R2,C2,R1,C1), free(R2,C2).


adjacent(R1,C,R2,C) :- cell(R1,C), cell(R2,C), R2 = R1 + 1.
adjacent(R1,C,R2,C) :- cell(R1,C), cell(R2,C), R2 = R1 - 1.
adjacent(R,C1,R,C2) :- cell(R,C1), cell(R,C2), C2 = C1 + 1.
adjacent(R,C1,R,C2) :- cell(R,C1), cell(R,C2), C2 = C1 - 1.

#show neighboring_region_count/3.
#show removed/3.
