int: n=8;    % n x n board

% int: selezione;
% int: selezione2;

array [1..n] of var 1..n: q;

% constraint forall(i in 1..n)(q[i]<=n);

% array [1..n,1..n] of var bool: E;
% var int: s;
% constraint s=sum(i,j in 1..n where i < j)(bool2int(E[i,j]));

% constraint q[1]=selezione;
% constraint q[2]=selezione2;

constraint
   forall(i, j in 1..n where i < j) (
%          (q[i]    != q[j] <-> E[i,j]) /\
         (q[i]    != q[j]) /\

         %%% original formulation
         j - i != abs(q[i]-q[j])

%          %%% more efficient formulation
%          q[i]+i  != q[j]+j /\
%          q[i]-i  != q[j]-j
   );

solve satisfy;

% solve maximize s;

%  solve :: int_search(q,
%  %  input_order,
%   first_fail,
% %  dom_w_deg,
% % most_constrained,

% %   indomain,
% %  indomain_split,
% %   indomain_min,
%   indomain_random,

%   complete) satisfy;

%output [ show(q) ];

output [ if fix(q[j]) == i then "Q " else ". " endif ++
          if j == n then "\n" else "" endif | i,j in 1..n]