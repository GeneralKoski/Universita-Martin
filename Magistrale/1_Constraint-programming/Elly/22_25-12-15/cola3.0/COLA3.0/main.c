/*
COnstraint solver for LAttices COLA: v. 3.0

Written by Alessandro Dal Palu' (University of Parma)
Contributions of Enrico Pontelli (New Mexico State University)
Contributions of Agostino Dovier (University of Udine)

Mail: alessandro.dalpalu AT unipr.it
Web:  www2.unipr.it/~dalpalu

Usage:
      
(1)   launch the executable with a protein name contained in data.txt 
      for ab initio / rigid block folding, using contact energy contributions in table.txt
      
      Ex: > COLA 1ZDD [0.13]
      
      Optional Compact factor (see below)

(2)   launch the executable with a protein name in data.txt for ab initio / rigid block folding
      and the following parameters for heuristics search:
          * X: dimension of BBF blocks (0 set a default = (n/12)+1, with n= protein length)
          * Tm TM: thresholds for fails for first and last blocks
          * Compact_factor:
             0 for default compact factor
             -1 for no compact factor
             >0 for a user-selected compact factor
          
      Ex: COLA prot X Tm TM Compact_factor
          COLA 1ZDD 5 50 10 0.16
          
          
Protein definitions in data.txt (see there for syntax)
Energy contributions in table.txt                

*/

#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include <fstream>
#include <math.h>
#include "AllVariables.h"
#include "ConstraintStore.h"
#include "Search.h"
#include "load.h"
#include "Utils.h"
#include "Pattern.h"

char prot_name[100];
int n; // number of variables
char primary[1000]; // sequence
AllVariables* vars; // problem variables

extern int nssbond;
extern int ssbond[100][2];

extern int nchains;
extern int chains[100][2];

extern int npattern;
extern int* pattern_code;                                           /// for each variable, set -1 if no pattern, othrw belonging pattern number
extern int pattern[MAXNPATTERNS][24][MAXPATTERNPOINTS][3];          /// for each rotation list all points (on FCC)
extern int pattern_len[MAXNPATTERNS];                               /// length of each pattern
extern int pattern_extension[MAXNPATTERNS][2];                      /// associated start and end variables (included)

double compact_factor=0;  // compact factor
    /// 0  for default compact factor
    /// -1 for no compact factor
    /// >0 for a specific cf

/// add constraints for a generic protein
void protein()
{
    /// add the chain constraint   
   cstore_add_chain();
   
   /// is ssbonds defined, add constraint                 
   for (int i=0;i<nssbond;i++)
    cstore_add_ssbond(ssbond[i][0],ssbond[i][1]);

   /// compact factor
   double cf;
   if (compact_factor==0) 
    cf= (4.4*pow(n,0.38));
   else
    cf=compact_factor*n;
    
   if (compact_factor!=-1) 
   {
   printf("CF: %f = %d\n",cf/n,(int)ceil(cf));
   for (int i=0;i<n;i+=3)
   for (int j=i+3;j<n;j+=4)
   {
       cstore_add(CONSTR_DIST_LEQ,i,j,(int)ceil(cf));
       cstore_add(CONSTR_DIST_LEQ,j,i,(int)ceil(cf));
   }
   }
   else
   printf("No CF\n");

   /// fixing the first points
    int var=-1;
    /// scan secondary structure for best placement (beginning of longest sse)
    int bestb=-1;    
    int beste=-1;    
    for (int i=0;i<npattern;i++)
      if (bestb==-1 ||
          beste-bestb<pattern_extension[i][1]-pattern_extension[i][0])
        {bestb=pattern_extension[i][0];beste=pattern_extension[i][1];
        }
        
    if (bestb==-1) var=0;  // if no patterns --> start from the first variable
    else
    var=bestb;             // else start from the beginning of longest sse

    printf("Assigning from %d\n",var);
    
    /// impose the placement of 3 aminoacids (avoid symmetries)
    
    if (bestb==-1) // no patterns
    {
    int point[3];
    int point2[3];
    point[0]=128;
    point[1]=128;
    point[2]=128;    
    var_init_point(vars->variables+var,point);
    point[0]=129;
    point[1]=129;
    point[2]=128;    
    var_init_point(vars->variables+var+1,point);

    point[0]=130;point2[0]=130;
    point[1]=128;point2[1]=130;  /// NOTE:: there are choices on the interval left!!
    point[2]=127;point2[2]=129;    
    var_init_bounds(vars->variables+var+2,point,point2);    
    }
    else
    {
        // if pattern, impose the first rotation! (3 points)
    int point[3];
    int point2[3];
    point[0]=128+pattern[pattern_code[bestb]][0][0][0];
    point[1]=128+pattern[pattern_code[bestb]][0][0][1];
    point[2]=128+pattern[pattern_code[bestb]][0][0][2];
    var_init_point(vars->variables+var,point);
    point[0]=128+pattern[pattern_code[bestb]][0][1][0];
    point[1]=128+pattern[pattern_code[bestb]][0][1][1];
    point[2]=128+pattern[pattern_code[bestb]][0][1][2];
    var_init_point(vars->variables+var+1,point);
    point[0]=128+pattern[pattern_code[bestb]][0][2][0];
    point[1]=128+pattern[pattern_code[bestb]][0][2][1];
    point[2]=128+pattern[pattern_code[bestb]][0][2][2];
    var_init_point(vars->variables+var+2,point);    
    }
}

int main(int argc, char *argv[])
{    
   
 if (argc!=2 && argc!=3 && argc!=6)
      {
      printf("Usage: %s protein-name  (Best solution search)\n",argv[0]);
      printf("Usage: %s protein-name compact_factor (Best solution search)\n",argv[0]);
      printf("Usage: %s protein-name block_size thr_b thr_e compact_factor (search with heuristics)\n",argv[0]);
      #if (defined(_WIN32) || defined(__WIN32__) || defined(WIN32))
      system("PAUSE");
      #endif
      return 1;
      }
    printf("Constraint solver for Lattice\n");

     /// load energy table
     load_table();    

    // load protein
    if (!load_protein(argv[1])){
      printf("Protein unknown!\n");
    return 1;
    }    

    vars=(AllVariables*)malloc(sizeof(AllVariables));    
    allvar_init(vars);
    
    printf("Primary: %s\n",primary);
    printf("Length: %d\n",n);       

    //init constraint store  
    cstore_init(STORE_AC3);
   
    if (argc==2)
      compact_factor=0;   
    if (argc==3)
      compact_factor=atof(argv[2]);   
    if (argc==6)
      compact_factor=atof(argv[5]);
    
    protein();  // constrain the protein 
    //cstore_list();

  /// launch search
    if (argc==2 || argc==3)
      //search(vars,SEARCH_COMPLETE, SEARCH_FF);         /////// this is the call for a complete search
      search(vars,SEARCH_BEST, SEARCH_FF);
    if (argc==6)
      if (atoi(argv[2])!=0)
        search(vars,SEARCH_BEST_HEUR_BBF, SEARCH_FF,atoi(argv[2]),atoi(argv[3]),atoi(argv[4]));     /// block size, thr initial, the end
      else
        search(vars,SEARCH_BEST_HEUR_BBF, SEARCH_FF,(n/12)+1,atoi(argv[3]),atoi(argv[4]));     /// block size, thr initial, the end

    cstore_stat(); 
#if (defined(_WIN32) || defined(__WIN32__) || defined(WIN32))
    system("PAUSE");
#endif
    return 0;
}
