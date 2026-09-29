#ifndef _UTLS_
#define _UTLS_
#include "AllVariables.h"

#define MAXATOM 10000

int load_protein(char *id);

void load_table();
double contrib(int dx, int dy, int dz, int i, int j);
double calc_energy(AllVariables *vars);
double calc_energy_real(double **pos);

char cv31(char *a);
char *cv(char a);

#endif