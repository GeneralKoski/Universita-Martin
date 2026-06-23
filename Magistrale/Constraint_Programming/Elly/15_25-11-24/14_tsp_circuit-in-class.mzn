int: n=5; % number of nodes

include "globals.mzn";

% d[i,j]=1234

% array[1..n,1..n] of var 0..1: edge;
% array[1..n] of var bool: reached;

% %edge[i,j] --> i->j in the solution

% constraint edge[1,2]=1;
% constraint edge[2,3]=1;

% constraint edge[4,5]=1;
% constraint edge[5,4]=1;

% constraint reached[1]=true;

% constraint forall(i in 1..n, j in 1..n where i!=j)(
%             reached[j] <- (reached[i] /\ (edge[i,j]=1)));

% constraint forall(i in 1..n) (
%             reached[i]=false <- (edge[i,i]=1));

% constraint forall(i in 1..n)
%             (reached[i]=true);

% out degree = 1
% constraint forall(i in 1..n)
%             (sum(j in 1..n)(edge[i,j])=1)
%             ;

% in degree = 1
% constraint forall(i in 1..n)
%             (sum(j in 1..n)(edge[j,i])=1)
%             ;

% outdegree = 1 (implicit)
array[1..n] of var 1..n: next;             % the circuit
array[1..n] of var 1..n: path;             % the path path[i] ni (path n1,n2,n3.... nn )

constraint path[1]=1;
constraint path[2]=next[path[2-1]];
constraint path[3]=next[path[3-1]];
constraint path[4]=next[path[4-1]];
constraint path[5]=next[path[5-1]];

% constraint next[1]=3;
% constraint next[3]=2;

%indegree = 1
constraint all_different(next);
constraint all_different(path);

% %%% convert next --> edge
% constraint forall(i in 1..n)(
%             sum (j in 1..n) (edge[i,j])=1 /\
%             edge[i,next[i]]=1
%            );

solve satisfy;