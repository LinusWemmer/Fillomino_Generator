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

region_size(R1,C1,N) :- N = #count{R2,C2 : region(R1,C1,R2,C2)}, fillomino(R1,C1,_).

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
blocked(R,C,N) :- empty(R,C), adjacent(R,C,R1,C1), fillomino(R1,C1,N), region_size(R1,C1,N).
% two neighboring regions
blocked(R,C,N) :- empty(R,C), adjacent(R,C,R1,C1), fillomino(R1,C1,N), adjacent(R,C,R2,C2), fillomino(R2,C2,N),
                       region_size(R1,C1,S1), region_size(R2,C2,S2), (S1 + S2 + 1) > N, not region(R1,C1,R2,C2).
%three neighboring regions
blocked(R,C,N) :- empty(R,C), adjacent(R,C,R1,C1), fillomino(R1,C1,N), adjacent(R,C,R2,C2), fillomino(R2,C2,N), adjacent(R,C,R3,C3), fillomino(R3,C3,N),
                       region_size(R1,C1,S1), region_size(R2,C2,S2), region_size(R3,C3,S3), (S1 + S2 + S3 + 1) > N, 
                       not region(R1,C1,R2,C2), not region(R1,C1,R3,C3), not region(R3,C3,R2,C2).

% EXPAND CELL:
expandable_candidate(R1,C1,N) :- unfinished_region(R2,C2,N), adjacent(R1,C1,R2,C2), empty(R1,C1), not blocked(R1,C1,N).

% cells that a region could potentially be expanded to.
max_expandable_region(R1,C1,R1,C1,R,C,N) :- expandable_candidate(R,C,N), adjacent(R,C,R1,C1), fillomino(R1,C1,N).
max_expandable_region(R1,C1,R2,C2,R,C,N) :- max_expandable_region(R1,C1,R3,C3,R,C,N), adjacent(R3,C3,R2,C2), fillomino(R2,C2,N).
max_expandable_region(R1,C1,R2,C2,R,C,N) :- max_expandable_region(R1,C1,R3,C3,R,C,N), adjacent(R3,C3,R2,C2), empty(R2,C2), not blocked(R2,C2,N), R2 != R.
max_expandable_region(R1,C1,R2,C2,R,C,N) :- max_expandable_region(R1,C1,R3,C3,R,C,N), adjacent(R3,C3,R2,C2), empty(R2,C2), not blocked(R2,C2,N), C2 !=C.

max_expansion(R,C,S,N) :- expandable_candidate(R,C,N), adjacent(R,C,R1,C1), S= #count{R2,C2 : max_expandable_region(R1,C1,R2,C2,R,C,N)}, fillomino(R1,C1,N).

derivable(R,C,N) :- max_expansion(R,C,S,N), S<N.

expandable_count(R1,C1,S) :- S = #count{R2,C2 : expandable_candidate(R2,C2,N), adjacent(R2,C2,R3,C3), region(R1,C1,R3,C3)}, unfinished_region(R1,C1,N).
% How many cells a region can be expanded to.

% ENTER REGION:
potential_expansion(R,C) :- empty_region(R,C,R1,C1), expandable_candidate(R1,C1,_).
derivable(R,C,N) :- empty_region_size(R,C,N), not potential_expansion(R,C).
% comment: if the puzzle has a unique solution, there should be no way to enter smaller regions than the derived region, as this would contradict uniqueness,
% e.g. when entering a region of size 3, entering a region of size 2 and size 1 instead. This should expand to human solutions in any case where we have to enter an entire region
% (the uniqueness should be given by construction)

derivable(R1,C1,N) :- expandable_candidate(R1,C1,N), adjacent(R1,C1,R2,C2), expandable_count(R2,C2,1), unfinished_region(R2,C2,N).
% We can derive a cell if it is the only place a neighboring region can expand to

#show derivable/3. 
