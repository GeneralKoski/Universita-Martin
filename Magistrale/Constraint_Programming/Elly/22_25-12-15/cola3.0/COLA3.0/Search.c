#include <stdio.h>
#include <iostream>
#include <fstream>
#include <math.h>
#include "Search.h"
#include "SearchComplete.h"
#include "SearchBest.h"
#include "SearchSimple.h"
#include "SearchBestHeurBBF.h"
#include "TrailStack.h"
#include "Utils.h"
#include "Pattern.h"

#if !(defined(_WIN32) || defined(__WIN32__) || defined(WIN32))
#include <sys/time.h>
#endif

#define SEARCH_DBG 0

using namespace std;

long fail_cons=0;
long fail_prop=0;

TStack trailstack;
extern int *var_changed;

extern char prot_name[10];
extern int n; // number of variables
extern char primary[1000]; // sequence

AllVariables* nodes; /// nodes of the tree (array of variables)
double** real_positions;   /// real values (patterns as loaded from files)
double** best_real_positions;   /// real values (patterns as loaded from files)
AllVariables* temp_nodes; /// temp store for search_best_guided
ofstream* out;

extern int npattern;                                                /// how many patterns
extern int pattern_extension[MAXNPATTERNS][2];                      /// associated start and end variables (included)

///////// BBF parameters
int block_size;
double* block_thr;  /// for each block, threshold (number of allowed failures on block)
double* block_failed_ct;  /// count how many blocks are failed for each block level
int* block_failed;  /// flag to detect the failure of a block
int n_blocks;

///////// TREE STRUCTURE indexes
int* var_on_lev;  /// for each node, stores the variable currently labelled
long leaves;       // leaves visited
long expanded_nodes;       // nodes expanded
long pruned_nodes;       // nodes pruned

int variable_selection_type;
int search_type;

#if (defined(_WIN32) || defined(__WIN32__) || defined(WIN32))
clock_t global_time;
#else
struct timeval global_t1,global_t2;
#endif

// rigid blocks variables
int directions[12][3]; // codes every lattice direction 
int direct_indomain[12][6];  /// for each direction, lists the 6 possible neighbors
int inv_directions[3][3][3]; // for each direction, gives the correct directions code (sum+1 to indexes)
                             // ex: p = -1 1 0 --> directions[inv_directions[0][2][1]]=[-1,1,0]

int direct_indomain_2_2[12][6][6];  /// _2 is the second depending on the first (=-1 if no dir associated)
int direct_indomain_2_1[12][6];     /// directions for 2 vars at once: _1 is the first

int pattern_h[24][4][3];   /// precompute the periodic pattern for helix
int pattern_h_dir[24][3];   /// for each pattern, specfies the patterns direction

int pattern_s[24][2][3];   /// precompute the periodic pattern for strand
int pattern_s_dir[24][3];   /// for each pattern, specfies the patterns direction

int pattern_z[12][2][1000][3];   /// first two are along directions[12], 2 rotations around that axis
                                 /// array of max 1000 points and 3 coordinates
                                   
//// cost function variables
double best_energy;
AllVariables* best_sol;
double* best_potlist;  // n x n matrix with contributions


int search_variable_selection(int i, AllVariables* vars)
{  

extern int* pattern_code;                                           /// for each variable, set -1 if no pattern, othrw belonging pattern number
extern int minPattern;    /// stores the first aa involved in some pattern (used to compute a better FF strategy)
extern int maxPattern;    /// stores the last aa involved in some pattern 


   switch(variable_selection_type)
   {
      case(SEARCH_LEFTMOST):
         // simple leftmost strategy
         // variable selection (return index) for labeling level i
         // take variable i-1
         return i-1;
      break;
      
      case(SEARCH_FF):
        {
        // search for smaller domain among vars
        // in case of same domain size, prefers variables involved in a sse
        int best=-1;
        long vol=-1;
        ///// search first inside core (between extremes wrapping SSEs)
        for (int j=minPattern;j<=maxPattern;j++)
        {
           if (!vars->variables[j].labelled)
            {
                long s=var_size(vars->variables+j);
                                
                if (s>0 && 
                    (best==-1 || 
                     s<vol ||
                     (s<=vol && (pattern_code[j]>=0)))) // the var is involved in a block
                  {
                     best=j;
                     vol=s;
                  }
            }   
        }

        if (best==-1) /// no more choices inside core
        {
        // look in tails
        for (int j=0;j<minPattern;j++)
        {
           if (!vars->variables[j].labelled)
            {
                long s=var_size(vars->variables+j);
                if (s>0 && (best==-1 || s<vol))
                  {
                     best=j;
                     vol=s;
                  }
            }   
        }
        for (int j=maxPattern+1;j<n;j++)
        {
           if (!vars->variables[j].labelled)
            {
                long s=var_size(vars->variables+j);
                if (s>0 && (best==-1 || s<vol))
                  {
                     best=j;
                     vol=s;
                  }
            }   
        }                      
        }        
        return best;
        }
      break;

   }


   if (SEARCH_DBG) printf("Selected var %d on lev %d\n",var_on_lev[i],i);
}



void search_print_result(AllVariables* vars)
{

    //vars->print_stat();
     printf("HEADER: \n");
     for (int i=0;i<n;i++)
      printf("ATOM  %5d  CA  %s %5d    %8.3f%8.3f%8.3f  1.00  0.00\n",i,cv(primary[i]),i,vars->variables[i].l[0]*2.69,
                                                                                vars->variables[i].l[1]*2.69,
                                                                                vars->variables[i].l[2]*2.69);
     for (int i=0;i<n;i++)
      printf("ATOM  %5d  CA  %s %5d    %8.3f%8.3f%8.3f  1.00  0.00\n",i,cv(primary[i]),i,
                                                                                (double)vars->variables[i].l[0],
                                                                                (double)vars->variables[i].l[1],
                                                                                (double)vars->variables[i].l[2]);
}

void search_print_result_best(AllVariables* vars, float sec)
{
/*
    //vars->print_stat();
     printf("HEADER: \n");
     printf("REMARK: Time: %3.3f\n",sec);
     printf("REMARK: Energy: %6.0f\n",best_energy);
     for (int i=0;i<n;i++)
      printf("ATOM  %5d  CA  %s %5d    %8.3f%8.3f%8.3f  1.00  0.00\n",i,cv(primary[i]),i,vars->variables[i].l[0]*2.69,
                                                                                vars->variables[i].l[1]*2.69,
                                                                                vars->variables[i].l[2]*2.69);
*/                                                                                
     FILE* of;
     char fn[100];
     strcpy(fn,prot_name);
     strcat(fn,"-out.pdb");     
     of=fopen(fn,"w+");
     if (of==NULL) printf("FILE ERROR\n");
     else
     {
     fprintf(of,"HEADER: \n");
     fprintf(of,"REMARK: Time: %3.3f\n",sec);
     fprintf(of,"REMARK: Contact Energy: %6.0f\n",calc_energy(vars));
//     fprintf(of,"REMARK: Real    Energy: %6.2f\n",calc_energy_real(vars));
     fprintf(of,"REMARK: Search ");
     if (search_type == SEARCH_BEST) fprintf(of,"Best");    
     if (search_type == SEARCH_BEST_HEUR_BBF) 
       fprintf(of,"Best: contact pruning and BBF (Bl. size %d, Thr b %3.0f, Thr e %3.0f)",block_size,block_thr[0],block_thr[n_blocks-1]);
     
     fprintf(of,"\n");
     
     for (int i=0;i<n;i++)
      fprintf(of,"ATOM  %5d  CA  %s %5d    %8.3f%8.3f%8.3f  1.00  0.00\n",i,cv(primary[i]),i,vars->variables[i].l[0]*2.69,
                                                                                vars->variables[i].l[1]*2.69,
                                                                                vars->variables[i].l[2]*2.69);
     
     fclose(of);
     }
}

void search_print_result_best_real(float sec)
{
     FILE* of;
     char fn[100];
     strcpy(fn,prot_name);
     strcat(fn,"-out.pdb");
//     printf("writing file %s\n",fn);     
     of=fopen(fn,"w+");
     if (of==NULL) printf("FILE ERROR\n");
     else
     {
     fprintf(of,"HEADER: \n");
     fprintf(of,"REMARK: Time: %3.3f\n",sec);
     fprintf(of,"REMARK: Real    Energy: %6.2f\n",calc_energy_real(best_real_positions));
     fprintf(of,"REMARK: Search ");
     if (search_type == SEARCH_BEST) fprintf(of,"Best");    
     if (search_type == SEARCH_BEST_HEUR_BBF) 
       fprintf(of,"Best: contact pruning and BBF (Bl. size %d, Thr b %3.0f, Thr e %3.0f)",block_size,block_thr[0],block_thr[n_blocks-1]);
     
     fprintf(of,"\n");
     
     
     for (int i=0;i<n;i++)
     {
       double x,y,z;
       x=best_real_positions[i][0]/sqrt(2)*3.81;
       y=best_real_positions[i][1]/sqrt(2)*3.81;
       z=best_real_positions[i][2]/sqrt(2)*3.81;
      fprintf(of,"ATOM  %5d  CA  %s %5d    %8.3f%8.3f%8.3f  1.00  0.00\n",i,cv(primary[i]),i,x,y,z);
//      printf("ATOM  %5d  CA  %s %5d    %8.3f%8.3f%8.3f  1.00  0.00\n",i,cv(primary[i]),i,x,y,z);
     }
      
     fclose(of);
     }
     printf("Written protein: file %s\n",fn);
}

void init_directions()
{
     /// init lattice directions, for faster labeling
     directions[ 0][0]= 0;directions[ 0][1]= 1;directions[ 0][2]= 1;
     directions[ 1][0]= 0;directions[ 1][1]= 1;directions[ 1][2]=-1;
     directions[ 2][0]= 0;directions[ 2][1]=-1;directions[ 2][2]= 1;
     directions[ 3][0]= 0;directions[ 3][1]=-1;directions[ 3][2]=-1;
     directions[ 4][1]= 0;directions[ 4][0]= 1;directions[ 4][2]= 1;
     directions[ 5][1]= 0;directions[ 5][0]= 1;directions[ 5][2]=-1;
     directions[ 6][1]= 0;directions[ 6][0]=-1;directions[ 6][2]= 1;
     directions[ 7][1]= 0;directions[ 7][0]=-1;directions[ 7][2]=-1;
     directions[ 8][2]= 0;directions[ 8][0]= 1;directions[ 8][1]= 1;
     directions[ 9][2]= 0;directions[ 9][0]= 1;directions[ 9][1]=-1;
     directions[10][2]= 0;directions[10][0]=-1;directions[10][1]= 1;
     directions[11][2]= 0;directions[11][0]=-1;directions[11][1]=-1;
     
     for (int i=0;i<3;i++)
     for (int j=0;j<3;j++)
     for (int k=0;k<3;k++)
       inv_directions[i][j][k]=-1;
       
     for (int i=0;i<12;i++)
     {
       inv_directions[directions[i][0]+1][directions[i][1]+1][directions[i][2]+1]=i;
     }
       
     
     /// load for each direction, the 6 directions allowed (according to lattice and constraints)
     for (int i=0;i<12;i++)
     {
      int ct=0;
      for (int j=0;j<12;j++)
      {
        int prodscal=directions[i][0]*directions[j][0]+
                     directions[i][1]*directions[j][1]+
                     directions[i][2]*directions[j][2];
        if (prodscal>=0 && prodscal!=2)
          direct_indomain[i][ct++]=j;
      }     
     }            
          
     for (int i=0;i<12;i++)
     {
      for (int j=0;j<12;j++)
      for (int k=0;k<12;k++)
          direct_indomain_2_2[i][j][k]=-1;

      int ct1=0;
      for (int j=0;j<12;j++)
      {
        int ct2=0;
        int prodscal=directions[i][0]*directions[j][0]+
                     directions[i][1]*directions[j][1]+
                     directions[i][2]*directions[j][2];
        // first point is selected              
        if (prodscal>=0 && prodscal!=2)
        {
         direct_indomain_2_1[i][ct1]=j;
         for (int k=0;k<12;k++)
         {
          int prodscal1=directions[j][0]*directions[k][0]+
                        directions[j][1]*directions[k][1]+
                        directions[j][2]*directions[k][2];
          int v1,v2,v3;
          v1=directions[i][0]+directions[j][0]+directions[k][0];
          v2=directions[i][1]+directions[j][1]+directions[k][1];
          v3=directions[i][2]+directions[j][2]+directions[k][2];
          // also check that the directions don't create a sqrt(2) distance (2 cases among 36)
          if (prodscal1>=0 && prodscal1!=2 && v1*v1+v2*v2+v3*v3>2)
          {
            direct_indomain_2_2[i][ct1][ct2]=k;
            ct2++;
          }
         }        
         ct1++;
         }
      }     
     }
}

void prod_vett(int* a, double* b, double* c)
{
  c[0] = a[1]*b[2] - b[1]*a[2];
  c[1] = a[2]*b[0] - b[2]*a[0];
  c[2] = a[0]*b[1] - b[0]*a[1];

}

void prod_vett_d(double* a, double* b, double* c)
{
  c[0] = a[1]*b[2] - b[1]*a[2];
  c[1] = a[2]*b[0] - b[2]*a[0];
  c[2] = a[0]*b[1] - b[0]*a[1];

}

double prod_scal(double* a, int* b)
{
  return a[0]*b[0]+a[1]*b[1]+a[2]*b[2];
}


void search_start_search()
{
     printf("Init search\n");
     switch (variable_selection_type)
     {
         case SEARCH_FF:
            printf("Using FF\n");
         break;
         case SEARCH_LEFTMOST:
            printf("Using LEFTMOST\n");
         break;
     }
     

     leaves=0;
     expanded_nodes=0;
     pruned_nodes=0;
          
     memset(var_changed,0,(sizeof(int)*n)); 

#if (defined(_WIN32) || defined(__WIN32__) || defined(WIN32))
     global_time=clock();
#else
     gettimeofday(&global_t1,NULL);
#endif
     
     //propagate 
     //cstore_propagate(nodes);    
     if (SEARCH_DBG) allvar_print_stat(nodes);
     
     switch (search_type)
     {
         case SEARCH_COMPLETE:
            printf("Launching Complete Search\n");
            search_complete(1);
         break;
         case SEARCH_SIMPLE:
            printf("Launching Simple Search\n");
            search_simple(1);
         break;
         case SEARCH_BEST:
            printf("Launching Best Solution Search\n");
            search_best(1);
            break;
         case SEARCH_BEST_HEUR_BBF:
            printf("Launching Best Solution Search BBF and BB\n");
            search_best_heur_bbf(1);
            break;
     }
     
#if (defined(_WIN32) || defined(__WIN32__) || defined(WIN32))
     clock_t final=clock()-global_time;
#else
     gettimeofday(&global_t2,NULL);
#endif
     printf("Labeling found %ld leaves\n",leaves);
     printf("Labeling expanded %ld nodes\n",expanded_nodes);
     printf("Labeling pruned %ld nodes\n",pruned_nodes);
#if (defined(_WIN32) || defined(__WIN32__) || defined(WIN32))
     printf("Time: %1.3f s\n",((float)final/CLK_TCK));
#else
     printf("\t\tEXECUTION TIME IS %f\n", (0.0+global_t2.tv_sec+global_t2.tv_usec/1000000.0) - (0.0+global_t1.tv_sec+global_t1.tv_usec/1000000.0));
#endif
     
//     if (search_type == SEARCH_BEST)
#if (defined(_WIN32) || defined(__WIN32__) || defined(WIN32))
     search_print_result_best_real(((float)final/CLK_TCK));
#else
     search_print_result_best_real((global_t2.tv_sec+global_t2.tv_usec/1000000.0) - (global_t1.tv_sec+global_t1.tv_usec/1000000.0));
#endif

     printf("N. FAILS %ld %ld\n",fail_cons,fail_prop);
    
     if (search_type!= SEARCH_SIMPLE)
     {     
     printf("Contact energy: %f\n",calc_energy(best_sol));
     printf("Real    energy: %f\n",calc_energy_real(best_real_positions));
     }
}


void search(AllVariables* init_vars, int init_search_type, int var_selection, int b_size,float thr_b, float thr_e)
{
     block_size=b_size;
     variable_selection_type=var_selection;
     search_type=init_search_type;

     // initialize the array of nodes
     nodes=(AllVariables*)calloc(n+1,sizeof(AllVariables));
     real_positions=(double**)calloc(n+1,sizeof(double*));
     for (int i=0;i<n+1;i++)
     real_positions[i]=(double*)calloc(n+1,sizeof(double)*3);
     best_real_positions=(double**)calloc(n+1,sizeof(double*));
     for (int i=0;i<n+1;i++)
     best_real_positions[i]=(double*)calloc(n+1,sizeof(double)*3);
     
     for (int i=0;i<n+1;i++)
        allvar_init(nodes+i);
     
     temp_nodes=(AllVariables*)calloc(n+1,sizeof(AllVariables));
     for (int i=0;i<n+1;i++)
        allvar_init(temp_nodes+i);

     best_sol=(AllVariables*)malloc(sizeof(AllVariables));
     allvar_init(best_sol);
     
     best_energy=123456; // a big number

     trailstack = new_tstack(2*n);
     
     /// init best potential matrix     
     best_potlist=(double*)calloc(n*n,sizeof(double));
     for (int i=0;i<n;i++)
     for (int j=0;j<n;j++)
         best_potlist[i+j*n]=0;

     // init arrays for bbf     
     block_failed_ct=(double*)calloc(n,sizeof(double));
     block_failed=(int*)calloc(n,sizeof(int));
     block_thr=(double*)calloc(n,sizeof(double));
     
     // set the thresholds for BBF
     if (search_type==SEARCH_BEST_HEUR_BBF)
     {
//      float thr_b=100;
//      float thr_e=10;
      
      n_blocks=n/b_size+1;
      for (int i=0;i<n_blocks;i++)
      {
          block_failed_ct[i]=0;          
          block_failed[i]=0;          
          float ind=(1-(float)i/(n_blocks-1));
          float ind1=pow(ind,1);
          block_thr[i]=thr_b*ind1+thr_e*(1-ind1);
      }
      printf("Blocks thr: ");
      for (int i=0;i<n_blocks;i++)
          printf("%2.0f ",block_thr[i]);
      printf("\n");
      printf("Block size: %d\n",block_size); 
     }

     // init lattice directions
     init_directions();

     //init variables (-1)
     var_on_lev=(int*)calloc(n+1,sizeof(int));
     for (int i=0;i<n+1;i++)
         var_on_lev[i]=-1;   

     // copies in first node the original status
     allvar_fill_from(nodes+0,init_vars);

     //// call to the constraint store, 
     //// in order to prepare the data structures for AC3... 
     //// and to simplify the constraint store
     //// assuming that no new constraints are added after this point     
     if (!cstore_before_start())
      printf("No solution!\n");
     else          
      search_start_search();     
}

void search(AllVariables* init_vars, int init_search_type, int var_selection)
{
    search(init_vars, init_search_type,var_selection,0,0,0);     
}

void search(AllVariables* init_vars, int search_type)
{
    search(init_vars, search_type,SEARCH_LEFTMOST,0,0,0);
}
