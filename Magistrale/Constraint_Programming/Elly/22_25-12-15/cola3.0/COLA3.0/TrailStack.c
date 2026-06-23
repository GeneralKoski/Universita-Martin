// implementation of a generic stack

#include "TrailStack.h"
#include <stdio.h>

#define TRAIL_DBG 0
//
extern TStack trailstack;

void backtrack(int lev, int trailtop, AllVariables *state) {
    int limit = trailtop;

    while (limit < trailstack->count) {
        struct trailpoint tp = TTop(trailstack);
        TPop(trailstack);
        tp.var->lasttrailed = tp.previoustrail;
        memcpy(tp.var->l, tp.oldlow, sizeof(int) * 3);
        memcpy(tp.var->h, tp.oldhigh, sizeof(int) * 3);

        if (TRAIL_DBG)
            printf("\t\t Untrailing variable %d -- position %d (%d,%d,%d - %d,%d,%d)\n", tp.var - state->variables, trailstack->count,
                   tp.var->l[0], tp.var->l[1], tp.var->l[2], tp.var->h[0], tp.var->h[1], tp.var->h[2]);
    }
}

void trail(Variable *var, int l[], int h[], AllVariables *state, int trailtop) {
    struct trailpoint nw;

    // check if we need to trail it; only if there are no
    // other trails for same variable after the last choice point
    if (var->lasttrailed >= trailtop)
        return;

    nw.var = var;

    memcpy(nw.oldlow, l, sizeof(int) * 3);
    memcpy(nw.oldhigh, h, sizeof(int) * 3);
    nw.previoustrail = var->lasttrailed;
    var->lasttrailed = trailstack->count;
    if (TRAIL_DBG)
        printf("\t\t Trail variable %d (%d,%d,%d - %d,%d,%d)\n", var - state->variables, l[0], l[1], l[2], h[0], h[1], h[2]);
    TPush(trailstack, nw);
}

TStack new_tstack(int size) {
    TStack n;

    n = (TStack)malloc(sizeof(struct tstack));
    if (n == NULL) {
        ERROR("unable to allocate stack\n");
    }
    n->space = (struct trailpoint *)malloc(sizeof(struct trailpoint) * size);
    if (n->space == NULL) {
        ERROR("unable to allocate stack\n");
    }
    n->size = size;
    n->count = 0;
    return n;
}

void delete_tstack(TStack s) {
    free(s->space);
    free(s);
}

void TPush(TStack s, struct trailpoint entry) {
    if (s->count == s->size) {
        struct trailpoint *ne;

        ne = (struct trailpoint *)malloc(sizeof(struct trailpoint) * (2 * s->size));
        if (ne == NULL) {
            ERROR("unable to extend stack\n");
        }
        memcpy(ne, s->space, sizeof(struct trailpoint) * (s->size));
        s->space = ne;
        s->size = 2 * s->size;
    }
    s->space[s->count] = entry;
    (s->count)++;
}

struct trailpoint TTop(TStack s) {
    return s->space[s->count - 1];
}

void TPop(TStack s) {

    if (s->count == 0)
        ERROR("cannot pop an empty stack\n");

    (s->count)--;
}

bool empty_tstack(TStack s) {
    return (s->count == 0);
}
