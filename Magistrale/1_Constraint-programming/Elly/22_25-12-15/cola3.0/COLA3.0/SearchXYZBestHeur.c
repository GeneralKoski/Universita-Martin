#include <stdio.h>
#include <iostream.h>
#include <fstream.h>
#include "TrailStack.h"
#include "Search.h"

#define SEARCH_DBG 0

extern char prot_name[10];
extern int n; // number of variables
extern char primary[1000]; // sequence

extern int ter[2][1000][3];
extern int len[2];
extern int leny; ///// length of coil y in xyz


extern long leaves;       // leaves visited
extern long expanded_nodes;       // nodes expanded
extern long pruned_nodes;       // nodes pruned

extern int* var_on_lev;  /// for each node, stores the variable currently labelled
extern AllVariables* nodes; /// nodes of the tree (array of variables)
extern AllVariables* temp_nodes; /// temp store for search_best_guided

extern TStack trailstack;

extern double best_energy;
extern AllVariables* best_sol;


extern long fail_cons;
extern long fail_prop;


extern int directions[12][3]; // codes every lattice direction 
extern int direct_indomain[12][6];  /// for each direction, lists the 6 possible neighbors
extern int pattern_h[24][4][3];   /// precompute the periodic pattern for helix
extern int pattern_h_dir[24][3];   /// for each pattern, specfies the patterns direction
extern int pattern_s[24][2][3];   /// precompute the periodic pattern for strand
extern int pattern_s_dir[24][3];   /// for each pattern, specfies the patterns direction
extern int* code_helix; // for each aa, sets a code: 0= no sec structure, n= number of belonging helix
extern int* code_strand; // for each aa, sets a code: 0= no sec structure, n= number of belonging strand
extern int nhelix;
extern int nstrand;
extern int helix[100][2];
extern int strand[100][2];


extern int pattern_z[12][2][1000][3];   /// first two are along directions[12], max [4] rotations around that axis
                                        /// array of max 1000 points and 3 coordinates


extern int current_MIN_CONTACTS;
extern int current_TEST_FROM_LEAF;

extern int* n_contacts_stack;
extern double* contrib_stack;

void search_xyz_best_heur(int lev)
{
     /// implements simple search with backtrack
     /// assume that constraint propagation is applied on level 0 (initial state)

  // keep choice point info in the C stack
  int trailtop;  // top of trail at the start
  int variable;  // variable picked for labeling
  int llimit[3]; // original lower limit for labeled var
  int hlimit[3]; // original higher limit for the labeled var
  int choice[3]; // next value to be given
  int n_contacts;
  double contrib;
     
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
  
  if (lev==1) 
   {
     /// first call -> set current_MIN_CONTACTS
     current_MIN_CONTACTS=0;//n/4;   // a very low low starting requirement
     current_TEST_FROM_LEAF=current_MIN_CONTACTS/3;

     // init stack for fast computation of energy
     n_contacts_stack=(int*)calloc((n+1)*n,sizeof(int));
     contrib_stack=(double*)calloc((n+1)*n,sizeof(double));
   }
  
  if (SEARCH_DBG) 
    printf("Level %d\n",lev);


  if (lev>n)
  {
         //// consistent leaf: handling ....         
         int leaf_n_cont=0;
         double leaf_energy=0;
         for (int i=0;i<n;i++)
          {
           leaf_n_cont+=STATE->variables[i].n_contacts;             
           leaf_energy+=STATE->variables[i].contrib;
          }             
          leaf_energy/=2.0;
          
         // =calc_energy(STATE);
         if (best_energy>leaf_energy) 
           {
             best_energy=leaf_energy;
             allvar_fill_from(best_sol,STATE);
             printf("Best new minimum: %f, contacts %d. Req%d,lim%d, leaves%d\n",best_energy,leaf_n_cont,current_MIN_CONTACTS,n-current_TEST_FROM_LEAF,leaves);
//             for (int i=0;i<n;i++)
//             if (STATE->variables[i].n_contacts>0)
//              printf("Var%d: %d %f. stack n ct%d c%f\n",i,STATE->variables[i].n_contacts,STATE->variables[i].contrib,leaf_n_cont,leaf_energy);
             search_print_result_best(best_sol,0);

/*
             // set new min contact
             if (current_MIN_CONTACTS<leaf_n_cont-4)
              {
                current_MIN_CONTACTS=leaf_n_cont-4;// use a small threshold to allow some tolerance to get some conformations with lesser but stronger contacts
                current_TEST_FROM_LEAF=current_MIN_CONTACTS/3;
              }
             printf("new %d\n",current_MIN_CONTACTS);
*/
           }
              
//         printf("leaf%d\n",leaves);
         leaves++;
         
       return;
  }

  
/*
  if (lev>=n-current_TEST_FROM_LEAF)
  {
   int flag=0;
   for (int i=0;i<n;i++)
     flag+=STATE->variables[i].n_contacts;             
      if (flag<current_MIN_CONTACTS)
        return;
  }
*/

  /// inductive step
  // set up the current level 
       trailtop = trailstack->count;

       /// var_selection
       variable = var_on_lev[lev] = search_variable_selection(lev,STATE); //look in the current status (in last explored level)
       
       llimit[0]=STATE->variables[variable].l[0];
       llimit[1]=STATE->variables[variable].l[1];
       llimit[2]=STATE->variables[variable].l[2];
       hlimit[0]=STATE->variables[variable].h[0];
       hlimit[1]=STATE->variables[variable].h[1];
       hlimit[2]=STATE->variables[variable].h[2];
       choice[0]=STATE->variables[variable].l[0];
       choice[1]=STATE->variables[variable].l[1];
       choice[2]=STATE->variables[variable].l[2];       
       for (int i=0;i<n;i++)
        {
          n_contacts_stack[i+lev*n]=STATE->variables[i].n_contacts;
          contrib_stack[i+lev*n]=STATE->variables[i].contrib;          
        }
       
       //printf("Lev %d var %d: push %d %f\n",lev,variable,n_contacts,contrib);
       

//////////////////////////////////////////
//// check if it's possible to start a fast indomain (only 6 values tested)
       fast_dir=-1;
       prev1=-1;
       
       // when two vars on left are labelled
       if (variable-2>=0 &&
           STATE->variables[variable-1].labelled &&
           STATE->variables[variable-2].labelled)
             {prev1=variable-1; prev2=variable-2;}
       // two vars on right are labelled
       if (variable+2<n &&
           STATE->variables[variable+1].labelled &&
           STATE->variables[variable+2].labelled)
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
	      if (choice[0] == -1)
	        go_on = 0;
	      else
	      {
	        var_init_point(STATE->variables+variable,choice[0],choice[1],choice[2]);
	        if (SEARCH_DBG) printf("\t Lev%d: Trying value %d %d %d for var%d\n",lev,choice[0],choice[1],choice[2],variable);
  	        //if (SEARCH_DBG) allvar_print_stat(STATE);
	        STATE->variables[variable].labelled = 1;
	        allvar_update_contacts(STATE,variable);
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
              if ( (choice[0]+choice[1]+choice[2])%2 == 0)
		        done = 1;
	        }
          } 
	     }
	     else 
      /// use fast indomain
	     {
             if (fast_dir_ct>=6)   /// no more directions to explore
	          go_on = 0;                                
             else
             {
              //assign
	           var_init_point(STATE->variables+variable,fast_choice1,fast_choice2,fast_choice3);
	           if (SEARCH_DBG) printf("\t Lev%d: FAST%d: Trying value %d %d %d for var%d\n",lev,fast_dir_ct,fast_choice1,fast_choice2,fast_choice3,variable);
  	           //if (SEARCH_DBG) allvar_print_stat(STATE);
	           STATE->variables[variable].labelled = 1;
	           allvar_update_contacts(STATE,variable);
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

//////////// propagation         
	     if (go_on)
	     {
           int select_type_indomain=0;  // 0 normal next var, 1 label helix, 2 label strand
           
	       expanded_nodes++;
	       flag=cstore_consistent(STATE,var_on_lev[lev]);
	       if (flag) // check consistency
	       {
	         flag=cstore_propagate(STATE,var_on_lev[lev],trailtop);
		     if (flag)
		     {
                      
                //////// if first aa of Z in XYZ -> direct labeling
                if (var_on_lev[lev]==len[0]+leny)
                {
                   select_type_indomain=1;
                   //allvar_print_stat(STATE);                   
                   
                    int n_var=len[1];     
                    for (int r=0;r<12;r++)
                    for (int q=0;q<2;q++)
                    {
                      /// store current state
                      allvar_fill_from(temp_nodes+lev,STATE);
                      /// assign domain       
                      int sh[3]; /// position of var (ground) as offset from correct position in helix (pattern, pattern_shift)
                      sh[0]=STATE->variables[variable].l[0];
                      sh[1]=STATE->variables[variable].l[1];
                      sh[2]=STATE->variables[variable].l[2];
       
                      int p1,p2,p3;
                      int flag1=1;
                      for (int i=len[0]+leny+1;i<n && flag1;i++)
                      {
                        p1=sh[0]+pattern_z[r][q][i-len[0]-leny][0];
                        p2=sh[1]+pattern_z[r][q][i-len[0]-leny][1];
                        p3=sh[2]+pattern_z[r][q][i-len[0]-leny][2];
                        if (STATE->variables[i].l[0]>p1 ||
                            STATE->variables[i].l[1]>p2 ||
                            STATE->variables[i].l[2]>p3 ||
                            STATE->variables[i].h[0]<p1 ||
                            STATE->variables[i].h[1]<p2 ||
                            STATE->variables[i].h[2]<p3)
                              flag1=0;
                        /// and assign the variable
//                        printf("ass %d: %d %d %d\n",i,p1,p2,p3);
                        var_init_point(STATE->variables+i,p1,p2,p3);
                        /// set the flag for labeling
                        STATE->variables[i].labelled=1;
                        if (i!=var_on_lev[lev]) allvar_update_contacts(STATE,i);
                      }
                    //if (flag1) printf("Cons\n");
                      for (int i=len[0]+leny+1;i<n && flag1;i++) /// consistency for all
                      if (i!=variable)
                      {
                        flag1=cstore_consistent(STATE,i); // check consistency
                        if (!flag1) fail_cons++;//printf("Cons Var:%d=%d\n",i,flag);
                      }       
                      if (flag1)
                          search_xyz_best_heur(lev+n_var);         /// proceed in tree exploration
                      /// At the end of current helix try, restore the original state
                      allvar_fill_from(STATE,temp_nodes+lev);
                    }/// for end        
                  }/// fast case
                      
                /// normal (apply next level)                
                // == NORMAL ============================================================================                    
		        if (select_type_indomain==0) 
                  search_xyz_best_heur(lev+1);		 
             } 
	       }
	       
         for (int i=0;i<n;i++)
         {
          STATE->variables[i].n_contacts=n_contacts_stack[i+lev*n];
          STATE->variables[i].contrib=contrib_stack[i+lev*n];          
         }

	     }
	     backtrack(lev,trailtop,STATE);
       } /// loop while
       
       STATE->variables[variable].labelled = 0;
       memcpy(STATE->variables[variable].l,llimit,sizeof(int)*3);
       memcpy(STATE->variables[variable].h,hlimit,sizeof(int)*3);
       for (int i=0;i<n;i++)
        {
          STATE->variables[i].n_contacts=n_contacts_stack[i+lev*n];
          STATE->variables[i].contrib=contrib_stack[i+lev*n];          
        }
       //printf("Lev %d var %d: pop %d %f\n",lev,variable,n_contacts,contrib);
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

