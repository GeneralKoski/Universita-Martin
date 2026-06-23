#include <stdio.h>
#include <iostream.h>
#include <fstream.h>
#include <math.h>
#include "TrailStack.h"
#include "Search.h"

#define SEARCH_DBG 0

//#define USE_LOWER_BOUND   /// if uncommented, uses the lower bound information to prune the search

extern char prot_name[10];
extern int n; // number of variables
extern char primary[1000]; // sequence

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

int max_energy=-123456;  /// a big uninstantiated val

double contrib_hp(int dx, int dy, int dz, int i, int j)
{
       
   //contact
   /// energy contribution    
   if (primary[i]=='h' &&
       primary[j]=='h' &&
       dx*dx+dy*dy+dz*dz==1)
    return -1;
   else
    return 0;       

}

double estimate_hp(AllVariables* vars)
{
       /// hp model
       double temp=0;

    int sure=0;
    int poss=0;

    int tempMin, tempMax;
       for (int i=0;i<n-1;i++)  //// use only upper right half matrix
       {
        int max_contribs=2;         /// max possible contribs (lowered when additional ground contacts are found)
        if (i==0) max_contribs=3;                      
        int possible=0;             /// limited by max_contrib at the end of line
        int known_contribs=1;       /// refer to line  (1 refers to i and i+1, already known)
        int avail_spots=0;          /// n. of effective 
        for (int j=i+3;j<n;j++)
        if (i%2 != j%2)
        {
          avail_spots++;
        if (vars->variables[i].labelled==1 &&
            vars->variables[j].labelled==1)
            {
             int dx,dy,dz;          
          dx=(int)vars->variables[i].l[0]-vars->variables[j].l[0];
          dy=(int)vars->variables[i].l[1]-vars->variables[j].l[1];
          dz=(int)vars->variables[i].l[2]-vars->variables[j].l[2];
          if (contrib_hp(dx,dy,dz,i,j)!=0)
            {
               known_contribs++;
               max_contribs--;
            }
            }
            else
            {

                //// check if i and j can generate a contact
                /// intersect axis x
                tempMin=(int)vars->variables[i].l[0]-1;
                if (tempMin<(int)vars->variables[j].l[0])
                    tempMin=(int)vars->variables[j].l[0];
                tempMax=(int)vars->variables[i].h[0]+1;
                if (tempMax>(int)vars->variables[j].h[0])
                    tempMax=(int)vars->variables[j].h[0];               
                /// intersect axis y
                if (tempMin<=tempMax)
                {
                tempMin=(int)vars->variables[i].l[1]-1;
                if (tempMin<(int)vars->variables[j].l[1])
                    tempMin=(int)vars->variables[j].l[1];
                tempMax=(int)vars->variables[i].h[1]+1;
                if (tempMax>(int)vars->variables[j].h[1])
                    tempMax=(int)vars->variables[j].h[1];                    
                /// intersect axis z
                if (tempMin<=tempMax)
                {
                tempMin=(int)vars->variables[i].l[2]-1;
                if (tempMin<(int)vars->variables[j].l[2])
                    tempMin=(int)vars->variables[j].l[2];
                tempMax=(int)vars->variables[i].h[2]+1;
                if (tempMax>(int)vars->variables[j].h[2])
                    tempMax=(int)vars->variables[j].h[2];
                if (tempMin<=tempMax)
                   /// finally -> they can intersect -> 
                   possible++;
                }                     
                }
            }
        } // for j
        
        if (avail_spots<max_contribs)  /// limit max_contribs to effective place
          max_contribs=avail_spots;
          
        if (possible>max_contribs)     /// limit possible to max_contribs
          possible=max_contribs;

        sure+=known_contribs;
        poss+=possible;          
      }  //for i
    
    if (SEARCH_DBG)
       printf("Estimate: p%d s%d est%d best%f\n",poss,sure,-(poss+sure),best_energy);
    /// best contacts available for each aa
    if (-(sure+poss) > best_energy)
         return 0;
    return 1;       
}

double calc_energy_hp(AllVariables* vars)
{
       /// hp model
       double temp=0;
       for (int i=0;i<n;i++)
       for (int j=i+1;j<n;j++)
       {
          int dx,dy,dz;          
          dx=(int)vars->variables[i].l[0]-vars->variables[j].l[0];
          dy=(int)vars->variables[i].l[1]-vars->variables[j].l[1];
          dz=(int)vars->variables[i].l[2]-vars->variables[j].l[2];
          temp+=contrib_hp(dx,dy,dz,i,j);
       }
       
   return temp;
       
}


void search_best_HP(int lev)
{
     /// implements simple search with backtrack
     /// assume that constraint propagation is applied on level 0 (initial state)

  // keep choice point info in the C stack
  int trailtop;  // top of trail at the start
  int variable;  // variable picked for labeling
  int llimit[3]; // original lower limit for labeled var
  int hlimit[3]; // original higher limit for the labeled var
  int choice[3]; // next value to be given
  int oldc[3];    // for sphere domains
  long oldr;
     
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
     ///init
     {
           int l=(int)ceil(sqrt(n));
      int temp;
      temp=n-(l-1)*(l-1);
      max_energy=-(l-2)*(l-2);  /// base contacts in a full square
      if (temp>0 && temp<=l-1)
        max_energy-=temp-1;
      if (temp>l-1)
        max_energy-=temp-2;
      max_energy-=n-1;         ///consecutive contacts
        printf("Min energy %d\n",max_energy);
     }

  if (SEARCH_DBG) printf("Level %d\n",lev);
  
  
  if (lev>n)
  {
         //// consistent leaf: handling ...         
         //double temp=calc_energy(STATE);
         //Calcolo dell'energia per i cbeta
         double temp=calc_energy_hp(STATE);
         if (best_energy>temp)
           {
             best_energy=temp;
             allvar_fill_from(best_sol,STATE);
             printf("Best new minimum: %f. Leaves %ld, Nodes %ld\n",best_energy,leaves,expanded_nodes);
             search_print_result_best(best_sol,0);
         //allvar_print_stat(STATE);
           }
         leaves++;
       return;
  }
    
  /// inductive step
       // set up the current level 
       trailtop = trailstack->count;

       /// var_selection
       variable = var_on_lev[lev] = search_variable_selection(lev,STATE); //look in the current status (in last explored level)

       if (SEARCH_DBG) printf("Selected var %d\n",variable);       

       memcpy(llimit,STATE->variables[variable].l,sizeof(int)*3);
       memcpy(hlimit,STATE->variables[variable].h,sizeof(int)*3);
       memcpy(choice,STATE->variables[variable].l,sizeof(int)*3);

if (SEARCH_DBG) printf("Normal indom\n");
        // ensure correct value
        done=0;
        while (!done)
	    {
	    if ( (choice[0]+choice[1]+choice[2]) % 2 == variable %2 /// even vars on even points! 2D square property
        )
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
       //allvar_print_stat(STATE);
       
//////////////////////////////////////////
//// assign every point in the domain and open branches
       go_on=1;
       while(go_on)  // copy new level and sets variable value
       {
      /// normal indomain	     
	      if (choice[0] == -1)
	        go_on = 0;
	      else
	      {
	        var_init_point(STATE->variables+variable,choice[0],choice[1],choice[2]);
	        if (SEARCH_DBG) printf("\t Lev%d: Trying value %d %d %d for var%d\n",lev,choice[0],choice[1],choice[2],variable);
  	        if (SEARCH_DBG) allvar_print_stat(STATE);
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
              if ( (choice[0]+choice[1]+choice[2])%2 == variable %2 /// even vars on even points! 2D square property
                )
		        done = 1;
	        }
          } 
	     
	     if (go_on)
	     {
	       expanded_nodes++;
	       flag=cstore_consistent(STATE,var_on_lev[lev]);
	       if (SEARCH_DBG) printf("Consistent %d\n",flag);
	       if (flag) // check consistency
	       {
	         flag=cstore_propagate(STATE,var_on_lev[lev],trailtop);
	         if (SEARCH_DBG) printf("Prop %d\n",flag);
		     if (flag 
                 && (lev<n-2 || estimate_hp(STATE))
#ifdef USE_LOWER_BOUND
                 && (best_energy>max_energy)   /// lower bound test (if reached conclude the search!)
#endif                 
                 )
                  search_best_HP(lev+1);		 
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
     if (lev==1) 
      {printf("End of search\n");
      }
}







