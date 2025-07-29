cell(R,C) :- R = 1..n, C = 1..n.

region_id(1..r).
%Arbitrary number of regions, might be changed to input


1 {region(R,C,ID): region_id(ID)} 1 :- cell(R,C).
% Randomly assign each cell to a region

1 {region_start(R,C,ID): region (R,C,ID)} 1 :- region_id(ID), region(_,_,ID).
% Give each region a starting cell

adjacent(R1,C,R2,C) :- cell(R1,C), cell(R2,C), R2 = R1 + 1.
adjacent(R1,C,R2,C) :- cell(R1,C), cell(R2,C), R2 = R1 - 1.
adjacent(R,C1,R,C2) :- cell(R,C1), cell(R,C2), C2 = C1 + 1.
adjacent(R,C1,R,C2) :- cell(R,C1), cell(R,C2), C2 = C1 - 1.

reachable(R,C,ID) :- region_start(R,C,ID).
% starting cell of each region cell is reachable
reachable(R1,C1,ID) :- region(R1,C1,ID), adjacent(R1,C1,R2,C2), reachable(R2,C2,ID).
% transitivity of reachability

:- region(R,C,ID), not reachable(R,C,ID).
% regions are connected

region_size(ID,S) :- S = #count{R,C : region(R,C,ID)}, region(_,_,ID).
% Size of each region
:- region_size(_,S), S > k.
% regions are limited in size by the max region size k

fillomino(R,C,N) :- region(R,C,ID), region_size(ID,N).

ID1 = ID2 :- adjacent(R1,C1,R2,C2), fillomino(R1,C1,N), region(R1,C1,ID1), fillomino(R2,C2,N), region(R2,C2,ID2).
% adjacent cells with the same number have to be in the same region.
%used_regions(N) :-  N = #count{ID : region(_,_,ID)}.
%

%N = k:- N = #count{R,C : fillomino(R,C,k)}. 
% there is only one region of maximal size

#show fillomino/3.
% #show used_regions/1.

%#maximize{N: used_regions(N)}.
