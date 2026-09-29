// Implementation of a generic stack
// Size given in constructor

#include <string.h>
#include <stdlib.h>
#include "AllVariables.h"

#ifndef __TSTACK

#define __TSTACK 1

#define ERROR(S)				\
  { \
    printf(S); \
    exit(0); \
  }

struct trailpoint
{
  Variable *var;
  int oldlow[3];
  int oldhigh[3];
  int previoustrail;
};

struct tstack {
  int size; // total size of stack
  int count; // current count of elements
  struct trailpoint *space; // array of element
};

typedef struct tstack *TStack;



//- macros

#define STATE (nodes+0)

//- operations

TStack new_tstack (int size);
void delete_tstack (TStack s);
void TPush(TStack s, struct trailpoint entry);
void TPop(TStack s);
struct trailpoint TTop(TStack s);
bool empty_tstack(TStack s);

void backtrack(int lev,int trailtop, AllVariables *s);
void trail(Variable *var,int l[], int h[],AllVariables *s,int trailtop);

#endif
