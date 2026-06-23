#ifndef _ALLVARIABLES_
#define _ALLVARIABLES_
#include "Variable.h"

#include <fstream>

/// this structure contains the whole set of variables


typedef struct {
        Variable* variables;  // array of variables
        
} AllVariables;


// initialize the container of n_vars variables
void allvar_init(AllVariables* allv);
// copy the set of variables from another set (other)
void allvar_fill_from(AllVariables* allv, AllVariables* other);
// print some stats
void allvar_print_stat(AllVariables* allv);
// print the each domain size
void allvar_print_delta(AllVariables* allv);

#endif
