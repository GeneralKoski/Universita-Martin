% golfers.mzn
% vim: ft=zinc ts=4 sw=4 et tw=0
% Ralph Becket <rafe@csse.unimelb.edu.au>
% Mon Oct 29 13:56:25 EST 2007
%
% The social golfers problem, see
% http://www.dcs.st-and.ac.uk/~ianm/CSPLib/prob/prob001/data.txt
%
% A club has a number of golfers that play rounds in groups (the number of
% golfers is a multiple of the number of groups).  Each round, a golfer
% plays with a group of different people, such that the same pair of golfers
% never play together twice.

include "globals.mzn";

int: n_groups;                          % The number of groups.
int: n_per_group;                       % The size of each group.
int: n_rounds;                          % The number of rounds.

int: n_golfers = n_groups * n_per_group;

set of int: rounds = 1..n_rounds;
set of int: golfers = 1..n_golfers;
set of int: places = 1..n_golfers;

array [rounds, places] of var golfers: round_place_golfer;
array [golfers, golfers] of var 0..n_rounds: golfer_golfer_round;

    % Each member of each group must be distinct.
    %
constraint
    forall (r in rounds) (
        alldifferent (p in places) (round_place_golfer[r, p])
    );

    % Each pair can play together at most once.
    %
constraint
    forall (r in rounds, g in 0..(n_groups - 1), i, j in 1..n_per_group
            where i < j) (
        golfer_golfer_round[
            round_place_golfer[r, n_per_group * g + i],
            round_place_golfer[r, n_per_group * g + j]
        ] = r
    );


    % Break some symmetry by strictly ordering each group in each round.
    %
constraint
    forall (r in rounds, p in places) (
        if p mod n_per_group != 0
        then round_place_golfer[r, p] < round_place_golfer[r, p + 1]
        else true
        endif
    );

% constraint forall (r in rounds, n in 0..n_groups-1)(
%            increasing([round_place_golfer[r, n*n_per_group+g] | g in 1..n_per_group])
%            );

% constraint forall (r in rounds, n in 0..n_groups-1)(
%            strictly_increasing([round_place_golfer[r, n*n_per_group+g] | g in 1..n_per_group])
%            );


% first round is fixed
%constraint strictly_increasing([round_place_golfer[1, p] | p in places]);

%first player in first group in places
%constraint forall(r in rounds) (count([round_place_golfer[r,p] | p in 1..n_per_group],1,1));
%constraint forall(r in rounds) (round_place_golfer[r,1]=1);

%second player in second group for 2..rounds
%constraint forall(r in 2..n_rounds) (count([round_place_golfer[r,n_per_group+p] | p in 1..n_per_group],2,1));
%constraint forall(r in 2..n_rounds) (round_place_golfer[r,n_per_group+1]=2);

%third player in third group for 2..rounds
%constraint forall(r in 2..n_rounds) (count([round_place_golfer[r,2*n_per_group+p] | p in 1..n_per_group],3,1));

%4th player in 4th group for 2..rounds
%constraint forall(r in 2..n_rounds) (count([round_place_golfer[r,3*n_per_group+p] | p in 1..n_per_group],4,1));

%second column is increasing
%constraint strictly_increasing([round_place_golfer[r,2] | r in rounds]);


solve
    :: int_search([round_place_golfer[r, p] | r in rounds, p in places],
        input_order,
%        first_fail,
%        most_constrained,
        indomain_min,
%        indomain_max,
 %       indomain_split,
        complete)
    satisfy;

output [
    "Social golfers:\n\n",
    "Groups        : ", show(n_groups), "\n",
    "No. per group : ", show(n_per_group), "\n",
    "No. of rounds : ", show(n_rounds), "\n"
] ++ [
    ( if p = 1 then "\nround " ++ show(r) ++ ":" else "" endif ) ++
    ( if p mod n_per_group = 1 then "   " else " " endif ) ++
    show_int(2, round_place_golfer[r, p]) | r in rounds, p in places
];

%-----------------------------------------------------------------------------%
%-----------------------------------------------------------------------------%