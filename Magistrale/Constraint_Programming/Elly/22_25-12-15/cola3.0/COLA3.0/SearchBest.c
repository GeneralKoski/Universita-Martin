#include <stdio.h>
#include <iostream>
#include <fstream>
#include "TrailStack.h"
#include "Search.h"
#include "Pattern.h"

#define SEARCH_DBG 0

extern char prot_name[10];
extern int n; // number of variables
extern char primary[1000]; // sequence

extern long leaves;       // leaves visited
extern long expanded_nodes;       // nodes expanded
extern long pruned_nodes;       // nodes pruned

extern int* var_on_lev;  /// for each node, stores the variable currently labelled
extern AllVariables* nodes; /// nodes of the tree (array of variables)
extern double** real_positions; 
extern double** best_real_positions; 
extern AllVariables* temp_nodes; /// temp store for search_best_guided

extern TStack trailstack;

extern double best_energy;
extern AllVariables* best_sol;


extern long fail_cons;
extern long fail_prop;


extern int directions[12][3]; // codes every lattice direction 
extern int direct_indomain[12][6];  /// for each direction, lists the 6 possible neighbors

extern int npattern;                                                /// how many patterns
extern int pattern_len[MAXNPATTERNS];                               /// length of each pattern
extern int pattern_extension[MAXNPATTERNS][2];                      /// associated start and end variables (included)
extern int pattern[MAXNPATTERNS][24][MAXPATTERNPOINTS][3];          /// for each rotation list all points (on FCC)
extern float pattern_real[MAXNPATTERNS][24][MAXPATTERNPOINTS][3];   /// for each rotation list all points (real)
extern int* pattern_code;                                           /// for each variable, set -1 if no pattern, othrw belonging pattern number
extern int* chain_code;                                           /// for each variable, set -1 if no pattern, othrw belonging pattern number


void search_best(int lev)
{
     /// implements simple search with backtrack
     /// assume that constraint propagation is applied on level 0 (initial state)

  // keep choice point info in the C stack
  int trailtop;  // top of trail at the start
  int variable;  // variable picked for labeling
  int llimit[3]; // original lower limit for labeled var
  int hlimit[3]; // original higher limit for the labeled var
  int choice[3]; // next value to be given
     
  int go_on;
  int flag;
  int done;
  
  int prev1;
  int prev2;
  int fast_dir; /// if -1 no fast domain possible (use normal domain enumeration), if >=0 apply fast in_domain
  int fast_dir_ct=0;
  int fast_choice1,fast_choice2,fast_choice3;

  /// base cases     
  if (lev<1) {printf("ERROR: labeling called with %d\n",lev);return;}


  if (SEARCH_DBG) printf("Level %d\n",lev);
  
  
  if (lev>n)
  {
         //// consistent leaf: handling ....         
         double temp=calc_energy_real(real_positions);
         if (best_energy>temp) 
           {
//         for (int i=0;i<n;i++)
//          printf("%d: %f %f %f\n",i,real_positions[i][0],real_positions[i][1],real_positions[i][2]);   
             
             for (int i=0;i<n;i++)
             for (int z=0;z<3;z++)
               best_real_positions[i][z]=real_positions[i][z];
               
             best_energy=temp;
             allvar_fill_from(best_sol,STATE);
             printf("Best new minimum: %f. Leaves %ld, Nodes %ld\n",best_energy,leaves,expanded_nodes);
             search_print_result_best_real(0);
             leaves++;
           }
       return;
  }
  
  /// inductive step
       // set up the current level 
       trailtop = trailstack->count;

       /// var_selection
       variable = var_on_lev[lev] = search_variable_selection(lev,STATE); //look in the current status (in last explored level)

       if (SEARCH_DBG) allvar_print_stat(STATE);
       if (SEARCH_DBG) printf("next var %d\n",variable);
       
       memcpy(llimit,STATE->variables[variable].l,sizeof(int)*3);
       memcpy(hlimit,STATE->variables[variable].h,sizeof(int)*3);
       memcpy(choice,STATE->variables[variable].l,sizeof(int)*3);

//////////////////////////////////////////
//// check if it's possible to start a fast indomain (only 6 values tested)
       fast_dir=-1;
       prev1=-1;
       
       // when two vars on left are labelled
       if (variable-2>=0 &&
           STATE->variables[variable-1].labelled &&
           STATE->variables[variable-2].labelled &&
           chain_code[variable-1] && chain_code[variable] &&
           chain_code[variable-2] && chain_code[variable]
           )
             {prev1=variable-1; prev2=variable-2;}
       // two vars on right are labelled
       if (variable+2<n &&
           STATE->variables[variable+1].labelled &&
           STATE->variables[variable+2].labelled &&
           chain_code[variable+1] && chain_code[variable] &&
           chain_code[variable+2] && chain_code[variable])
           { prev1=variable+1; prev2=variable+2;}
           
       // prepare the data for fast indomain
       if (prev1!=-1)    
       {
          //direct indomain         
          int v1,v2,v3;
          v1=STATE->variables[prev1].l[0]-
             STATE->variables[prev2].l[0];
          v2=STATE->variables[prev1].l[1]-
             STATE->variables[prev2].l[1];
          v3=STATE->variables[prev1].l[2]-
             STATE->variables[prev2].l[2];
          // retrieve the index for incoming direction
          for (int k=0;k<12;k++)
            if (v1==directions[k][0] &&
                v2==directions[k][1] &&
                v3==directions[k][2])
                fast_dir=k;
          done=0;
          while (!done)
	      {
            fast_choice1=STATE->variables[prev1].l[0]+directions[direct_indomain[fast_dir][fast_dir_ct]][0];
            fast_choice2=STATE->variables[prev1].l[1]+directions[direct_indomain[fast_dir][fast_dir_ct]][1];
            fast_choice3=STATE->variables[prev1].l[2]+directions[direct_indomain[fast_dir][fast_dir_ct]][2];
                           
            /// intersect with domain on var...
            if (llimit[0]<=fast_choice1 &&
                hlimit[0]>=fast_choice1 &&
                llimit[1]<=fast_choice2 &&
                hlimit[1]>=fast_choice2 &&
                llimit[2]<=fast_choice3 &&
                hlimit[2]>=fast_choice3)
	              done = 1;  /// fast_dir_ct generates an ok point
	       else
	       {
	         fast_dir_ct++;
	         if (fast_dir_ct>=6)
	           done = 1;
	       }
	      }
       }       
//////////////////////////////////////////
//// prepare data for normal indomain
       else    
       {       
        // ensure correct value
        done=0;
        while (!done)
	    {
	    if ( (choice[0]+choice[1]+choice[2]) % 2 == 0)
	      done = 1;
	    else
	      {
	      choice[0]++;
	      if (choice[0] > hlimit[0])
	        {choice[0] = llimit[0]; choice[1]++;}
	      if (choice[1] > hlimit[1])
	        {choice[1] = llimit[1]; choice[2]++;}
	      if (choice[2] > hlimit[2])
	        {choice[0] = -1;done = 1;}
	      }
	    }
       } 
       //allvar_print_stat(STATE);
       
//////////////////////////////////////////
//// assign every point in the domain and open branches
       go_on=1;
       while(go_on)  // copy new level and sets variable value
       {
         if (fast_dir<0)    
      /// normal indomain	     
	     {
          if (SEARCH_DBG) printf("normal\n");
	      if (choice[0] == -1)
	        go_on = 0;
	      else
	      {
	        var_init_point(STATE->variables+variable,choice[0],choice[1],choice[2]);
	        real_positions[variable][0]=choice[0];
	        real_positions[variable][1]=choice[1];
	        real_positions[variable][2]=choice[2];
	        if (SEARCH_DBG) printf("\t Lev%d: Trying value %d %d %d for var%d\n",lev,choice[0],choice[1],choice[2],variable);
  	        //if (SEARCH_DBG) allvar_print_stat(STATE);
	        STATE->variables[variable].labelled = 1;
 	        done = 0;
 	        //move to next value in the choice point
 	        while (!done)
	        {
		      choice[0]++;
		      if (choice[0] > hlimit[0])
		        {choice[0] = llimit[0];choice[1]++;}
  		      if (choice[1] > hlimit[1])
	            {choice[1] = llimit[1];choice[2]++;}
		      if (choice[2] > hlimit[2])
		        {choice[0] = -1;done = 1;}
		      else
		      {
               if ( (choice[0]+choice[1]+choice[2])%2 == 0)
		         done = 1;
              }
	        }
          } 
	     }
	     else 
      /// use fast indomain
	     {
          if (SEARCH_DBG) printf("fast\n");
             if (fast_dir_ct>=6)   /// no more directions to explore
	          go_on = 0;                                
             else
             {
              //assign
	           var_init_point(STATE->variables+variable,fast_choice1,fast_choice2,fast_choice3);
	        real_positions[variable][0]=fast_choice1;
	        real_positions[variable][1]=fast_choice2;
	        real_positions[variable][2]=fast_choice3;
	           if (SEARCH_DBG) printf("\t Lev%d: FAST%d: Trying value %d %d %d for var%d\n",lev,fast_dir_ct,fast_choice1,fast_choice2,fast_choice3,variable);
  	           //if (SEARCH_DBG) allvar_print_stat(STATE);
	           STATE->variables[variable].labelled = 1;
               done=0;
               while (!done)
	           {
                  fast_dir_ct++;
      	          if (fast_dir_ct>=6)
      	            done = 1;
    	          else
                  {   
                    fast_choice1=STATE->variables[prev1].l[0]+directions[direct_indomain[fast_dir][fast_dir_ct]][0];
                    fast_choice2=STATE->variables[prev1].l[1]+directions[direct_indomain[fast_dir][fast_dir_ct]][1];
                    fast_choice3=STATE->variables[prev1].l[2]+directions[direct_indomain[fast_dir][fast_dir_ct]][2];
                    /// intersect with domain on var...
                    if (llimit[0]<=fast_choice1 &&
                        hlimit[0]>=fast_choice1 &&
                        llimit[1]<=fast_choice2 &&
                        hlimit[1]>=fast_choice2 &&
                        llimit[2]<=fast_choice3 &&
                        hlimit[2]>=fast_choice3)
      	                  done = 1;  /// fast_dir_ct generates an ok point
      	          }
               } 
             }
         } /// the new domain has been assigned
	     
	     if (go_on)
	     {
           int select_type_indomain=0;  // 0 normal next var, 1 label helix, 2 label strand
           
	       expanded_nodes++;
	       flag=cstore_consistent(STATE,var_on_lev[lev]);
	       if (flag) // check consistency
	       {
              if (SEARCH_DBG) printf("consistent\n");
	         flag=cstore_propagate(STATE,var_on_lev[lev],trailtop);
		     if (flag)
		     {
           ////// try a fast pattern indomain
              if (SEARCH_DBG) printf("prop ok\n");
                if (pattern_code[variable]>=0)
                {  
                int beg,end;
                int ct=0;   
                // =================================================================================                    
                // == rigid block ==================================================================                    
                 
                  beg=pattern_extension[pattern_code[variable]][0];
                  end=pattern_extension[pattern_code[variable]][1];
                  for (int i=beg;i<=end;i++)
                    if (STATE->variables[i].labelled==1) ct++;
                  if (ct==1) /// first time the block is labelled
                  {
                    //allvar_print_stat(STATE);
                    if (SEARCH_DBG) printf("Pattern %d Beg: %d end %d, Pos%d\n",pattern_code[variable],beg,end,variable);
                    int n_var=end-beg+1;     
                    /// for each block placement, try to assign, test consistency and propagate
                    for (int h=0;h<24;h++)
//                    int h=0;
                    {
                      /// store current state
                      allvar_fill_from(temp_nodes+lev,STATE);
                      /// assign domain       
                      int sh[3]; /// position of var (ground) as offset from correct position in block
                      sh[0]=STATE->variables[variable].l[0];
                      sh[1]=STATE->variables[variable].l[1];
                      sh[2]=STATE->variables[variable].l[2];
       
                    if (SEARCH_DBG) printf("Rot %d; SH%d %d %d\n",h,sh[0],sh[1],sh[2]);
                      int pt_sh;   /// compute pattern shift (w.r.t. labelled var)
       
                      pt_sh=(variable-beg);   /// compute pattern shift
                      //printf("sh%d of%d\n",pt_sh,pt_ofs);
                      /// subtract the block absolute position (correct traslation to overlap block in point "var")
                      sh[0]-=pattern[pattern_code[variable]][h][pt_sh][0];
                      sh[1]-=pattern[pattern_code[variable]][h][pt_sh][1];
                      sh[2]-=pattern[pattern_code[variable]][h][pt_sh][2];
         
                      int p1,p2,p3;
                      int flag1=1;
                      for (int i=beg;i<=end && flag1;i++)
                      {
                        pt_sh=i-beg;
                        //if (SEARCH_DBG) printf("i:%d var%d: pos%d\n",i,variable,pt_sh);
                        p1=sh[0]+pattern[pattern_code[variable]][h][pt_sh][0];
                        p2=sh[1]+pattern[pattern_code[variable]][h][pt_sh][1];
                        p3=sh[2]+pattern[pattern_code[variable]][h][pt_sh][2];
                        if (STATE->variables[i].l[0]>p1 ||
                            STATE->variables[i].l[1]>p2 ||
                            STATE->variables[i].l[2]>p3 ||
                            STATE->variables[i].h[0]<p1 ||
                            STATE->variables[i].h[1]<p2 ||
                            STATE->variables[i].h[2]<p3)
                              flag1=0;
                    if (SEARCH_DBG) 
                    printf("point %d, sh%d val %d %d %d pattern %d %d %d h%d\n",
                           i,pt_sh,p1,p2,p3,
                           pattern[pattern_code[variable]][h][pt_sh][0],
                           pattern[pattern_code[variable]][h][pt_sh][1],
                           pattern[pattern_code[variable]][h][pt_sh][2],h);
                        /// and assign the variable
                        var_init_point(STATE->variables+i,p1,p2,p3);
                        /// set the flag for labeling
                        STATE->variables[i].labelled=1;
	        real_positions[i][0]=sh[0]+pattern_real[pattern_code[variable]][h][pt_sh][0];
	        real_positions[i][1]=sh[1]+pattern_real[pattern_code[variable]][h][pt_sh][1];
	        real_positions[i][2]=sh[2]+pattern_real[pattern_code[variable]][h][pt_sh][2];
                      }
                    //if (flag1) printf("Cons\n");
                      for (int i=beg;i<=end && flag1;i++) /// consistency for all
                      if (i!=variable)
                      {
                        flag1=cstore_consistent(STATE,i); // check consistency
                        if (!flag1) fail_cons++;//printf("Cons Var:%d=%d\n",i,flag);
                      }       
                      
                      cstore_reset_var_changed();
                      for (int i=beg;i<=end && flag1;i++) /// propagate ground->non ground
                      if (i!=variable)
                      {
                        flag1=cstore_propagate_g_ng(STATE,i,trailtop);
                        if (!flag1) fail_prop++;
                        //if (!flag1) printf("Prop Var:%d=%d\n",i,flag);
                      }  
                      if (flag1 && cstore_ac(STATE,trailtop)) /// arc consistency on non ground vars
                      {                               
               //           printf("AC ok: jump on %d\n",lev+n_var);
               //           for (int i=0;i<n;i++)
               //            printf("%d",nodes[lev+n_var-1].variables[i].labelled);
               //            printf("\n");           
                          search_best(lev+n_var);         /// proceed in tree exploration
                      }
                      /// At the end of current helix try, restore the original state
                      allvar_fill_from(STATE,temp_nodes+lev);
                    }/// for end        
                  } 
                }
                else
                /// normal (apply next level)                
                // == NORMAL ============================================================================                    
                  search_best(lev+1);		 




             } 
	       }
	       
	     }
	     backtrack(lev,trailtop,STATE);
       } /// loop while
       
       STATE->variables[variable].labelled = 0;
       memcpy(STATE->variables[variable].l,llimit,sizeof(int)*3);
       memcpy(STATE->variables[variable].h,hlimit,sizeof(int)*3);
       if (SEARCH_DBG) printf("Backtrack lev %d\n",lev);
       if (SEARCH_DBG) printf("\t RESTORE bounds for var %d to %d %d %d  - %d %d %d\n",var_on_lev[lev],
       	      STATE->variables[variable].l[0],
              STATE->variables[variable].l[1],
              STATE->variables[variable].l[2],
              STATE->variables[variable].h[0],
              STATE->variables[variable].h[1],
              STATE->variables[variable].h[2]);
        //if (SEARCH_DBG) allvar_print_stat(STATE);
    
     if (lev==1) 
      {printf("End of search\n");
      }
}

