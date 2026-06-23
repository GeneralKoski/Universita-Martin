#include <time.h>
#include <fstream>
#include "AllVariables.h"
#include "ConstraintStore.h"


#ifndef _SEARCH_
#define _SEARCH_

#define SEARCH_COMPLETE          0        /// complete enumeration
#define SEARCH_SIMPLE            1        /// simple enumeration for GENERIC constraints
#define SEARCH_BEST              3        /// enumeration keeping the best folding
#define SEARCH_BEST_HEUR_BBF     13        /// enumeration with new heuristic BBF

#define SEARCH_LEFTMOST   100
#define SEARCH_FF         101

       //// Structure of search tree:
       //// nodes: 0 1 .. n
       //// 0 represents the root = variables status as defined by user (apply consistency)
       //// i>0, represents the level i \in [1..n], where the variable selected for the i-th level
       ////      has been assigned. The node i contains the ground assignment to the variable and consistency
       ////      caused by that choice       
       //// The node i, labels the variable var_on_lev[i]. The value of that variable is selected
       //// following the codification given by domain_selection. The values are taken from 
       //// the same variable on node i-1. For each assignment in node i, the choiches[i] index
       //// is updated and the consistency applied.

/// variable selection (leftmost/first fail)
int search_variable_selection(int i, AllVariables* vars);

/// search predicates, with different types of calls
void search(AllVariables* init_vars, int init_search_type, int var_selection, int b_size,float thr_b, float thr_e);
void search(AllVariables* init_vars, int init_search_type, int var_selection);
void search(AllVariables* init_vars, int search_type);

/// protein structure prediction energy handling
double calc_energy(AllVariables* vars);
double calc_energy_real(double** pos);
double contrib(int dx, int dy, int dz, int i, int j);

/// utils
void search_print_result(AllVariables* vars);
void search_print_result_best(AllVariables* vars, float sec);   /// print on video and file, with time
void search_print_result_best_real(float sec);

void load_table();

#endif
