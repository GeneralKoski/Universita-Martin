#ifndef _VARIABLE_
#define _VARIABLE_

#define MAXVAL 255

typedef struct {
        int dbg;      // if set to 1, prints every modifications to the variable during search
        int ID;       // the id code of the variable
        int labelled; // flag for processed variables (and inserted as nodes in the search tree)
        int ground;   // flag for ground variables
        int failed;   // flag for failed variables
        int changed;  // used during propagation to tell if the propagator modified the domain
        int l[3];     // low domain corner
        int h[3];     // high domain corner
        long size;    // volume included (product of sides' lengths)    
        int lasttrailed;  // info for stack handling     
} Variable;


void var_init(Variable* v);                                  /// general init (0..MAXVAL for each coordinate)
void var_init_bounds(Variable* v,int newl[3], int newh[3]);  /// load the variable domain from an interval
void var_init_point(Variable* v,int newp[3]);                /// load the variable domain from a point
void var_init_point(Variable* v,int x, int y, int z);        /// load the variable domain from a point
void var_test_ground(Variable* v);                           /// test if the current variable is ground (store result in flag)
void var_test_failed(Variable* v);                           /// test if the current variable is failed (store result in flag)
long var_size(Variable* v);                                  /// computes the volume of the domain
void var_intersect(Variable* v,Variable* other);             /// intersection of variables
void var_intersect(Variable* v, int otherl[],int otherh[]);  /// intersection with a specified domain
void var_fail(Variable* v);                                  // impose a failed domain
void var_copy(Variable* v, Variable* other);                 // copy the variable info from other to v
void var_print_domain(Variable* v);                          // printf of variable domain

#endif
