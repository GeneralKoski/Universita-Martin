#include "AllVariables.h"

#ifndef _CONSTR_
#define _CONSTR_

#define CONSTR_DIST_LEQ 0/// only propagation
                         /// Semantics: the distance of v2 is bounded to be at MOST distance from v1 in all coordinates (norm 1)
#define CONSTR_EUCL 1    /// the constraint propagates its approximated version like CONSTR_DIST
                         /// it performs a consistency check based on the correct formula
                         /// Semantics: the distance of v2 from v1 in norm 2 is bounded to be EQUAL to "distance"
                         /// NOTE: the distance has to be specified already squared!!!!
#define CONSTR_EUCL_LEQ 2/// the constraint propagates its approximated version like CONSTR_DIST (actually it invokes the
                         /// same propagator as in constr_eucl
                         /// it performs a consistency check based on the correct formula
                         /// Semantics: the distance of v2 from v1 in norm 2 is bounded to be LESS or EQUAL to "distance"
                         /// NOTE: the distance has to be specified already squared!!!!
#define CONSTR_EUCL_GEQ 3/// only consistency check
                         /// Semantics: the distance of v2 from v1 is bounded to be GREATER or EQUAL to distance 
                         /// NOTE: the distance has to be specified already squared!!!!

#define CONSTR_REMOVED -1    /// when the constraint is removed (due to simplifications)

// distance constraint is modeled as directional: distance(V1, V2) does not imply distance(V2, V1)
// this is explicitly duplicated when adding the constraint in the constraint store
// The second variable is the one to be modified upon propagation

typedef struct {
       int dbg;
       int type;
       int var1;
       int var2;
       int distance;
       int distance_approx; /// used by eucl distance, when propagating 
} Constraint;

// Main routines for propagation and consistency
int  constr_propagate(Constraint* c, AllVariables* allvar,int trailtop);
int  constr_consistency(Constraint* c, AllVariables* allvar);

// Specific constraint propagations
int  constr_propagate_eucl_distance(Constraint* c, AllVariables* allvar,int trailtop);
int  constr_propagate_distance(Constraint* c, AllVariables* allvar,int trailtop);

// Specific constraint consistencies
int  constr_consistency_eucl_distance(Constraint* c, AllVariables* allvar);
int  constr_consistency_eucl_leq_distance(Constraint* c, AllVariables* allvar);
int  constr_consistency_eucl_geq_distance(Constraint* c, AllVariables* allvar);

int  constr_is_unary(int type);  // query arity of type
void constr_print(Constraint* c);

// Methods for addition of constraints in the constraint store
void constr_set(Constraint* c, int n_type, int n_var1, int n_var2);
void constr_set(Constraint* c, int n_type, int n_var1, int n_var2, int n_dist);

#endif












