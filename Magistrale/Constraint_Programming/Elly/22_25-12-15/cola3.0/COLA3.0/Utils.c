#include "AllVariables.h"
#include "Pattern.h"
#include <fstream>
#include <iostream>
#include <math.h>
#include <stdio.h>

#include <string>

using namespace std;

extern int n;              // number of variables
extern char primary[1000]; // sequence
extern char prot_name[100];

extern int npattern;
extern int *pattern_code;                                  /// for each variable, set -1 if no pattern, othrw belonging pattern number
extern int pattern[MAXNPATTERNS][24][MAXPATTERNPOINTS][3]; /// for each rotation list all points (on FCC)
extern int pattern_len[MAXNPATTERNS];                      /// length of each pattern
extern int pattern_extension[MAXNPATTERNS][2];             /// associated start and end variables (included)
extern int nssbond;
extern int ssbond[100][2];

extern int nchains;
extern int chains[100][2];

double table[256][256];  // fast version: indexed directely by char code
int SEARCH_SKIP_VAR = 4; //// how many variables are skipped on primary sequence when considering energy contributions

// from file data.txt
int load_protein(char *id) {
    char a[1000];
    char c;
    int v1, v2;
    char name[10];
    int found = 0;

    strcpy(prot_name, id);
    ifstream in;
    in.open("data.txt", ifstream::in);

    strcpy(name, "ID=");
    strcat(name, id);

    while (!in.eof()) {
        in >> a;
        if (strcmp(name, a) == 0) {
            cout << "Loading: " << id << "..." << endl;
            in >> a;
            strcpy(primary, a);
            n = strlen(primary);
            do {
                in >> c;
                if (c == 'H' || c == 'S' || c == 'B' || c == 'C') {
                    in >> v1 >> v2;
                    v1--;
                    v2--;
                    printf("Load pattern %c %d %d\n", c, v1, v2);
                    if (c == 'H') {
                        pattern_load_helix(v1, v2);
                        // helix[nhelix][0]=v1;helix[nhelix++][1]=v2;
                    }
                    if (c == 'S') {
                        pattern_load_strand(v1, v2);
                        // strand[nstrand][0]=v1;strand[nstrand++][1]=v2;
                    }
                    if (c == 'B') {
                        ssbond[nssbond][0] = v1;
                        ssbond[nssbond++][1] = v2;
                    }
                    if (c == 'C') {
                        chains[nchains][0] = v1;
                        chains[nchains++][1] = v2;
                        printf("A chain starts from %d and ends in %d\n", v1 + 1, v2 + 1);
                    }
                }
                if (c == 'P') {
                    char fn[200];
                    in >> v1 >> v2;
                    v1--;
                    v2--;
                    in >> fn;
                    printf("Load pattern %d %d from |%s|\n", v1, v2, fn);
                    pattern_load(v1, v2, fn);
                }

                if (c == 'p') {
                    char fn[200];
                    in >> v1 >> v2;
                    v1--;
                    v2--;
                    int s1, s2;
                    in >> s1 >> s2;
                    s1--;
                    s2--;
                    in >> fn;
                    printf("Load pattern %d %d from |%s|, extracting pos in pdb %d %d\n", v1, v2, fn, s1, s2);
                    pattern_load(v1, v2, s1, s2, fn);
                }
            } while (c != 'E');
            found = 1;
        }
    }
    in.close();
    init_pattern(); // load patterns, given files
    return found;
}

void load_table() {
    char a, b;
    double temp;
    ifstream in;
    in.open("table.txt", ifstream::in);

    for (int i = 0; i < 256; i++)
        for (int j = 0; j < 256; j++)
            table[i][j] = 0;

    for (int i = 0; i < 400; i++) {
        in >> a >> b >> temp;
        table[a][b] = temp;
    }

    in.close();
}

double contrib(int dx, int dy, int dz, int i, int j) {
    // contact
    /// energy contribution
    if (dx * dx + dy * dy + dz * dz == 4) /////// eucl distance = 2
        return table[primary[i]][primary[j]];
    else
        return 0;

    /*
       double dist=(dx*dx+dy*dy+dz*dz)/4.0;
       if (dist<1) return 0;
       return table[primary[i]][primary[j]]/pow(dist,5);
    */
}

double calc_energy(AllVariables *vars) {
    //// compute the energy associated to the conformation
    /// assume that all variables are ground!

    double temp = 0;
    for (int i = 0; i < n; i++)
        for (int j = i + SEARCH_SKIP_VAR; j < n; j++) {
            int dx, dy, dz;

            dx = (int)vars->variables[i].l[0] - vars->variables[j].l[0];
            dy = (int)vars->variables[i].l[1] - vars->variables[j].l[1];
            dz = (int)vars->variables[i].l[2] - vars->variables[j].l[2];
            temp += contrib(dx, dy, dz, i, j);
        }

    return temp;
}

double calc_energy_real(double **pos) {
    //// compute the energy associated to the conformation
    /// assume that all variables are ground!

    double temp = 0;
    for (int i = 0; i < n; i++)
        for (int j = i + SEARCH_SKIP_VAR; j < n; j++) {
            double dx, dy, dz;
            dx = pos[i][0] - pos[j][0];
            dy = pos[i][1] - pos[j][1];
            dz = pos[i][2] - pos[j][2];
            double dist = (dx * dx + dy * dy + dz * dz);
            if (dist < 4)
                dist = 4;
            temp += table[primary[i]][primary[j]] * 4.0 / dist;
        }

    return temp;
}
/////////////////////////////// END OF PROTEIN ENERGY

///// conversion utilities
char *cv(char a) {
    if (a == 'a')
        return "ALA";
    if (a == 'r')
        return "ARG";
    if (a == 'n')
        return "ASN";
    if (a == 'd')
        return "ASP";
    if (a == 'c')
        return "CYS";
    if (a == 'q')
        return "GLN";
    if (a == 'e')
        return "GLU";
    if (a == 'g')
        return "GLY";
    if (a == 'h')
        return "HIS";
    if (a == 'i')
        return "ILE";
    if (a == 'l')
        return "LEU";
    if (a == 'k')
        return "LYS";
    if (a == 'm')
        return "MET";
    if (a == 'f')
        return "PHE";
    if (a == 'p')
        return "PRO";
    if (a == 's')
        return "SER";
    if (a == 't')
        return "THR";
    if (a == 'w')
        return "TRP";
    if (a == 'y')
        return "TYR";
    if (a == 'v')
        return "VAL";
}

char cv31(char *a) {
    if (strcmp("ALA", a) == 0)
        return 'a';
    if (strcmp("ARG", a) == 0)
        return 'r';
    if (strcmp("ASN", a) == 0)
        return 'n';
    if (strcmp("ASP", a) == 0)
        return 'd';
    if (strcmp("CYS", a) == 0)
        return 'c';
    if (strcmp("GLN", a) == 0)
        return 'q';
    if (strcmp("GLU", a) == 0)
        return 'e';
    if (strcmp("GLY", a) == 0)
        return 'g';
    if (strcmp("HIS", a) == 0)
        return 'h';
    if (strcmp("ILE", a) == 0)
        return 'i';
    if (strcmp("LEU", a) == 0)
        return 'l';
    if (strcmp("LYS", a) == 0)
        return 'k';
    if (strcmp("MET", a) == 0)
        return 'm';
    if (strcmp("PHE", a) == 0)
        return 'f';
    if (strcmp("PRO", a) == 0)
        return 'p';
    if (strcmp("SER", a) == 0)
        return 's';
    if (strcmp("THR", a) == 0)
        return 't';
    if (strcmp("TRP", a) == 0)
        return 'w';
    if (strcmp("TYR", a) == 0)
        return 'y';
    if (strcmp("VAL", a) == 0)
        return 'v';
    return '!';
}
