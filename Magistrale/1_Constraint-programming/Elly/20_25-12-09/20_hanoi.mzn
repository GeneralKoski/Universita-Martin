%%Hanoi tower

%%% World: rods x elements x time
%%% Actions: move(el_number, dest_rod)
%%%          move(src_rod, dest_rod)
%%%          move(el_numer, src_rod, dest_rod)

include "globals.mzn";


int: rods=3;
int: disks=3; %--> 1 2 3 4
int: length=7;

array[1..rods, 1..disks,0..length] of var 0..disks: world;

array[1..3*length] of var 1..disks: action_order;

array[1..length] of var 1..disks: action_el;
array[1..length] of var 1..rods: action_src_rod;
array[1..length] of var 1..disks: action_src_index; %% index on rod
array[1..length] of var 1..rods: action_dst_rod;
array[1..length] of var 1..disks: action_dst_index;
%% action[i]: world[i-1] --> world[i]

constraint forall(t in 1..length)(
          %%% for each action: precondition
          world[action_src_rod[t],action_src_index[t],t-1]=action_el[t]     /\
          %%% for each action: postcondition
          world[action_dst_rod[t],action_dst_index[t],t]=action_el[t] /\
          world[action_src_rod[t],action_src_index[t],t]=0          /\
          world[action_dst_rod[t],action_dst_index[t],t-1]=0
);

%inhertia
constraint forall(t in 1..length)(

          forall(r in 1..rods, d in 1..disks)(
          world[r,d,t-1]!=action_el[t] /\ world[r,d,t]!=action_el[t]
           ->
           world[r,d,t-1]=world[r,d,t]
          )
);


%%%% constraints for world

%%% disks are not repeated
constraint forall(t in 0..length)(
        alldifferent_except_0([world[r,d,t]|r in 1..rods, d in 1..disks])
);

constraint forall(t in 0..length)(
        sum([world[r,d,t]|r in 1..rods, d in 1..disks]) * 2 = (disks)*(disks+1)
);

constraint forall(t in 0..length, r in 1..rods, d in 1..disks-1)(
             %%% rod properties
             %%% elements are sorted (except 0)
             %%% elements start from first index
                (world[r,d,t]==0 -> world[r,d+1,t]==0) /\
                 (world[r,d,t]!=0 -> world[r,d,t]>world[r,d+1,t])
             );

%% beginning
 constraint forall(d in 1..disks)(
  world[1,d,0]=disks-d+1
 );

%%% end
constraint forall(d in 1..disks)(
 world[rods,d,length]=disks-d+1
);


constraint forall(t in 1..length)(

  % 1 2 3 4 ... l
  % 1 l 2 l-1 3 l-2 4 ...
   if ((t-1)*2+1 <= length) then
    action_order[3*( (t-1)*2+1 -1)+1]=action_el[(t-1)*2+1]
   endif
);

constraint forall(t in 1..length)(
   if ((t-1)*2+1 <= length) then
      action_order[3*( (t-1)*2+1 -1)+2]=action_src_rod[ (t-1)*2+1]
   endif
);

constraint forall(t in 1..length)(
   if ((t-1)*2+1 <= length) then
 action_order[3*( (t-1)*2+1-1)+3]=action_src_index[(t-1)*2+1]
   endif
);

constraint forall(t in 1..length)(

  % 1 2 3 4 ... l
  % 1 l 2 l-1 3 l-2 4 ...
   if ( 2*(length-t)+2  <= length ) then
    action_order[3*( 2*(length-t)+2 -1)+1]=action_el[2*(length-t)+2]
   endif
);

constraint forall(t in 1..length)(
   if ( 2*(length-t)+2  <= length ) then
      action_order[3*( 2*(length-t)+2 -1)+2]=action_src_rod[ 2*(length-t)+2]
   endif
);

constraint forall(t in 1..length)(
   if ( 2*(length-t)+2  <= length) then
 action_order[3*( 2*(length-t)+2-1)+3]=action_src_index[2*(length-t)+2]
   endif
);


solve :: int_search(action_el++action_src_rod++action_src_index,
                    input_order,
                    %indomain_random
                    indomain_min
                    )
%solve :: int_search( action_order, input_order, indomain_random)
%solve :: int_search(action_el++action_src_rod, input_order, indomain_random)
      %:: restart_linear(100)
      satisfy;


output [show(action_order)++"\n"]++
       ["dsk: "++show(action_el)++"\n"] ++
       ["src_rod: "++show(action_src_rod)++"\n"] ++
       ["src_idx: "++show(action_src_index)++"\n"] ++
       ["dst_rod: "++show(action_dst_rod)++"\n"] ++
       ["dst_idx: "++show(action_dst_index)++"\n"] ++

       [ show(world[r,disks-d+1,t]) ++
         if r == rods then "\n" else "" endif ++
         if d == disks /\ r == rods then "\n" else "" endif  |
          t in 0..length, d in 1..disks, r in 1..rods]