#include "Constraint.h"

#include <vector>
#include <list>

#ifndef _CONSTRSTO_
#define _CONSTRSTO_

#define STORE_AC1 0
#define STORE_AC3 1

// initialization
void cstore_init(int ac);

// user available constraints
// syntactic sugar for inserting constraints for Protein Structure Prediction Problem (they call cstore_add internally)
void cstore_add_next(int v1,int v2);    // sugar for next definition for var1 ,var2 
void cstore_add_ang(int v1);            // sugar for angle constraint
void cstore_add_strand(int v1,int v2);  // sugar for strand definition from var1 to var2 included
void cstore_add_helix(int v1,int v2);   // sugar for helix definition from var1 to var2 included
void cstore_add_ssbond(int v1,int v2);  // sugar for ssbond

void cstore_add_alldifferent(int v1,int v2);        // sugar for alldifferent from var1 to var2 included
void cstore_add_alldistant(int v1,int v2, int d);   // sugar for alldistant from var1 to var2 included, min distance = sqrt(d)
                                                    // the constraints skips the neighbors of a var (to avoid inconsistency with next!)
void cstore_add_contiguous(int v1,int v2);          // sugar for contiguous
void cstore_add_saw(int v1,int v2);                 // sugar for saw from var1 to var2 included
void cstore_add_chain();                            // sugar for chain 

// insert constraint in the store
void cstore_add(int type, int v1, int v2,int d);
void cstore_add(int type, int v1, int v2);
void cstore_add(int type, int v1);

//// arc consistency routine
int cstore_ac1(AllVariables* vars,int trailtop);                      // AC 1
int cstore_ac3(AllVariables* vars,int trailtop);                      // AC 3

////  consistency routine
int cstore_consistent(AllVariables* vars, int varidx);   //launch consistency using the constraints in the constr store

void cstore_reset_var_changed();

//// propagation 
int cstore_propagate(AllVariables* vars);                    // special case (beginning)
int cstore_propagate(AllVariables* vars, int varidx,int trailtop);        // invoke propagation 
int cstore_propagate_g_ng(AllVariables* vars, int varidx,int trailtop);  // propagate from ground to non ground vars
int cstore_ac(AllVariables* vars,int trailtop);                           // invoke arc consistency

//// to be called after the CSP has been input
int cstore_before_start();                            // constriaint simplification and data str handling before starting the search

//// utils
void cstore_list();
void cstore_stat();
      
#endif












