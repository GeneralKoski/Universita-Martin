#include "Search.h"
#include "TrailStack.h"
#include <fstream>
#include <iostream>
#include <stdio.h>

#define SEARCH_DBG 0

extern char prot_name[10];
extern int n;              // number of variables
extern char primary[1000]; // sequence

extern long leaves;         // leaves visited
extern long expanded_nodes; // nodes expanded
extern long pruned_nodes;   // nodes pruned

extern int *var_on_lev;          /// for each node, stores the variable currently labelled
extern AllVariables *nodes;      /// nodes of the tree (array of variables)
extern AllVariables *temp_nodes; /// temp store for search_best_guided

extern TStack trailstack;

extern long fail_cons;
extern long fail_prop;

void search_simple(int lev) {
    /// implements simple search with backtrack
    /// assume that constraint propagation is applied on level 0 (initial state)

    // keep choice point info in the C stack
    int trailtop;  // top of trail at the start
    int variable;  // variable picked for labeling
    int llimit[3]; // original lower limit for labeled var
    int hlimit[3]; // original higher limit for the labeled var
    int choice[3]; // next value to be given
    int oldc[3];   // for sphere domains
    long oldr;

    int go_on;
    int flag;
    int done;

    int prev1;
    int prev2;
    int fast_dir; /// if -1 no fast domain possible (use normal domain enumeration), if >=0 apply fast in_domain
    int fast_dir_ct = 0;
    int fast_choice1, fast_choice2, fast_choice3;

    /// base cases
    if (lev < 1) {
        printf("ERROR: labeling called with %d\n", lev);
        return;
    }

    if (lev == 1)
        allvar_print_stat(STATE);

    if (SEARCH_DBG)
        printf("Level %d\n", lev);

    if (lev > n) {
        /// print first solution
        if (leaves == 0) {
            printf("Solution: %d\n", leaves);
            allvar_print_stat(STATE);
        }
        leaves++;
        return;
    }

    //  allvar_print_stat(STATE);

    /// inductive step
    // set up the current level
    trailtop = trailstack->count;

    /// var_selection
    variable = var_on_lev[lev] = search_variable_selection(lev, STATE); // look in the current status (in last explored level)
    if (SEARCH_DBG)
        printf("Selected var %d\n", variable);
    memcpy(llimit, STATE->variables[variable].l, sizeof(int) * 3);
    memcpy(hlimit, STATE->variables[variable].h, sizeof(int) * 3);
    memcpy(choice, STATE->variables[variable].l, sizeof(int) * 3);
    if (SEARCH_DBG)
        printf("%d\n", STATE->variables[variable].l[0]);
    if (SEARCH_DBG)
        printf("Normal indom\n");

    //////////////////////////////////////////
    //// assign every point in the domain and open branches
    go_on = 1;
    while (go_on) // copy new level and sets variable value
    {
        /// normal indomain
        if (choice[0] == -1)
            go_on = 0;
        else {
            var_init_point(STATE->variables + variable, choice[0], choice[1], choice[2]);
            if (SEARCH_DBG)
                printf("\t Lev%d: Trying value %d %d %d for var%d\n", lev, choice[0], choice[1], choice[2], variable);
            if (SEARCH_DBG)
                allvar_print_stat(STATE);
            if (SEARCH_DBG)
                system("PAUSE");
            STATE->variables[variable].labelled = 1;
            done = 0;
            // move to next value in the choice point
            while (!done) {
                choice[0]++;
                if (choice[0] > hlimit[0]) {
                    choice[0] = llimit[0];
                    choice[1]++;
                }
                if (choice[1] > hlimit[1]) {
                    choice[1] = llimit[1];
                    choice[2]++;
                }
                if (choice[2] > hlimit[2]) {
                    choice[0] = -1;
                    done = 1;
                }
                done = 1;
            }
        }
        if (go_on) {
            int select_type_indomain = 0; // 0 normal next var, 1 label helix, 2 label strand

            expanded_nodes++;
            flag = cstore_consistent(STATE, var_on_lev[lev]);
            if (SEARCH_DBG)
                printf("Consistent %d\n", flag);
            if (flag) // check consistency
            {
                flag = cstore_propagate(STATE, var_on_lev[lev], trailtop);
                if (SEARCH_DBG)
                    printf("Prop %d\n", flag);
                if (flag)
                    search_simple(lev + 1);
            }
        }
        backtrack(lev, trailtop, STATE);
    } /// loop while

    STATE->variables[variable].labelled = 0;
    memcpy(STATE->variables[variable].l, llimit, sizeof(int) * 3);
    memcpy(STATE->variables[variable].h, hlimit, sizeof(int) * 3);
    if (SEARCH_DBG)
        printf("Backtrack lev %d\n", lev);
    if (SEARCH_DBG)
        printf("\t RESTORE bounds for var %d to %d %d %d  - %d %d %d\n", var_on_lev[lev],
               STATE->variables[variable].l[0],
               STATE->variables[variable].l[1],
               STATE->variables[variable].l[2],
               STATE->variables[variable].h[0],
               STATE->variables[variable].h[1],
               STATE->variables[variable].h[2]);
    // if (SEARCH_DBG) allvar_print_stat(STATE);
    if (lev == 1) {
        printf("End of search\n");
    }
}
