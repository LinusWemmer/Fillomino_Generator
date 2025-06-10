% Input: A valid encoding for a Fillomino, constants n.. Size of the grid

cell(R,C) :- R = 1..n, C = 1..n.
empty(R,C) :- cell(R,C), not fillomino(R,C,_).

adjacent(R1,C,R2,C) :- cell(R1,C), cell(R2,C), R2 = R1 + 1.
adjacent(R1,C,R2,C) :- cell(R1,C), cell(R2,C), R2 = R1 - 1.
adjacent(R,C1,R,C2) :- cell(R,C1), cell(R,C2), C2 = C1 + 1.
adjacent(R,C1,R,C2) :- cell(R,C1), cell(R,C2), C2 = C1 - 1.

%REGIONS:
region(R1,C1,R2,C2) :- fillomino(R1,C1,N), fillomino(R2,C2,N), adjacent(R1,C1,R2,C2).
region(R,C,R,C) :- fillomino(R,C,_).
region(R1,C1,R2,C2) :- region(R2,C2,R1,C1).
region(R1,C1,R2,C2) :- region(R1,C1,R3,C3), region(R3,C3,R2,C2).
% get region through reflexivity, symmetry and transitivity

region_size(R1,C1,N) :- N = #count{R2,C2 : region(R1,C1,R2,C2)}, cell(R1,C1).

empty_region(R,C,R,C) :- empty(R,C).
empty_region(R1,C1,R2,C2) :- empty(R1,C1), empty(R2,C2), adjacent(R1,C1,R2,C2).
empty_region(R1,C1,R2,C2) :- empty_region(R2,C2,R1,C1).
empty_region(R1,C1,R2,C2) :- empty_region(R1,C1,R3,C3), empty_region(R3,C3,R2,C2).
% regions of empty cells

empty_region_size(R1,C1,N) :- N = #count{R2,C2 : empty_region(R1,C1,R2,C2)}, empty(R1,C1).

unfinished_region(R,C,N) :- fillomino(R,C,N), region_size(R,C,M), M != N.
% regions that aren't full yet.

% BLOCKED CELL:
% one neighboring region
blocked_cell(R,C,N) :- empty(R,C), adjacent(R,C,R1,C1), fillomino(R1,C1,N), region_size(R1,C1,N).
% two neighboring regions
blocked_cell(R,C,N) :- empty(R,C), adjacent(R,C,R1,C1), fillomino(R1,C1,N), adjacent(R,C,R2,C2), fillomino(R2,C2,N),
                       region_size(R1,C1,S1), region_size(R2,C2,S2), (S1 + S2 + 1) > N, not region(R1,C1,R2,C2).
%three neighboring regions
blocked_cell(R,C,N) :- empty(R,C), adjacent(R,C,R1,C1), fillomino(R1,C1,N), adjacent(R,C,R2,C2), fillomino(R2,C2,N), adjacent(R,C,R3,C3), fillomino(R3,C3,N),
                       region_size(R1,C1,S1), region_size(R2,C2,S2), region_size(R3,C3,S3), (S1 + S2 + S3 + 1) > N, 
                       not region(R1,C1,R2,C2), not region(R1,C1,R3,C3), not region(R3,C3,R2,C2).

expandable_candidate(R1,C1,N) :- unfinished_region(R2,C2,N), adjacent(R1,C1,R2,C2), empty(R1,C1), not blocked_cell(R1,C1,N).
% cells that a region could potentially be expanded to.

expandable_count(R1,C1,S) :- S = #count{R2,C2 : expandable_candidate(R2,C2,N), adjacent(R2,C2,R3,C3)}, unfinished_region(R1,C1,N), region(R1,C1,R3,C3).
% How many cells a region can be expanded to.

derivable(R1,C1,N) :- expandable_candidate(R1,C1,N), adjacent(R1,C1,R2,C2), expandable_count(R2,C2,1), unfinished_region(R2,C2,N).
% We can derive a cell if it is the only place a neighboring region can expand to

#show derivable/3. 
#show blocked_cell/3.