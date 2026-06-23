#ifndef _PATTERN_
#define _PATTERN_

#define MAXPATTERNPOINTS 1000      //// how many points supported by a pattern
#define MAXNPATTERNS 100          //// how many patterns

void init_pattern();
void setup_rotation_matr();

void pattern_load_helix(int v1,int v2);
void pattern_load_strand(int v1,int v2);
void pattern_load(int v1,int v2, char* fn);                  /// load pattern from an entire pdb file
void pattern_load(int v1,int v2, int s1, int s2, char* fn);  /// load pattern from an sub sequence in the pdb file
                                                             /// note that the internal coding in the PDB file is not used
                                                             /// we count starting from 1
#endif
