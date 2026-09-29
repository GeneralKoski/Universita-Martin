#include <stdio.h>
#include "Variable.h"

#define VAR_DBG 0

void var_init(Variable* v)
{
        v->dbg=VAR_DBG;
        if (v->dbg) printf("Created new variable\n");
        v->labelled=0;     
        for (int i=0;i<3;i++)
        {v->l[i]=0;v->h[i]=MAXVAL;
        } 
        v->ground=0;
        v->failed=0;
	    v->lasttrailed = -1;
}

void var_init_bounds(Variable* v,int newl[3], int newh[3])
{ // constructor: sets the specified bounds
        v->dbg=VAR_DBG;
        if (v->dbg) printf("Created new variable\n");
        v->labelled=0;     
        v->ground=1;
        v->failed=0;
        v->changed=0;
       for (int z=0;z<3;z++)
        {
         if (v->l[z]!=newl[z]) v->changed=1;
         v->l[z]=newl[z];
         if (v->h[z]!=newh[z]) v->changed=1;
         v->h[z]=newh[z];
         if (v->l[z]>v->h[z]) 
           v->failed=1;
         if (v->l[z]!=v->h[z]) 
           v->ground=0;
        }
	v->lasttrailed = -1;
}

void var_init_point(Variable* v,int newp[3])
{ // constructor: sets the point
        v->dbg=VAR_DBG;
        if (v->dbg) printf("Created new variable\n");
        v->labelled=0;     
        v->ground=1;
        v->failed=0;
        v->changed=0;
       for (int z=0;z<3;z++)
        {
         if (v->l[z]!=newp[z]) v->changed=1;
         v->l[z]=newp[z];
         if (v->h[z]!=newp[z]) v->changed=1;
         v->h[z]=newp[z];
        }    
	v->lasttrailed = -1;
}

void var_init_point(Variable* v,int x, int y, int z)
{ // constructor: sets the point
        v->dbg=VAR_DBG;
        if (v->dbg) printf("Created new variable\n");
        v->labelled=0;     
        v->ground=1;
        v->failed=0;
        v->changed=0;
        if (v->l[0]!=x) v->changed=1;
        v->l[0]=x;
        if (v->h[0]!=x) v->changed=1;
        v->h[0]=x;
        if (v->l[1]!=y) v->changed=1;
        v->l[1]=y;
        if (v->h[1]!=y) v->changed=1;
        v->h[1]=y;
        if (v->l[2]!=z) v->changed=1;
        v->l[2]=z;
        if (v->h[2]!=z) v->changed=1;
        v->h[2]=z;
}

void var_test_ground(Variable* v)
{
   v->ground=1;
   for (int i=0;i<3;i++)
    if (v->l[i]!=v->h[i]) 
      v->ground=0;
}        

void var_test_failed(Variable* v)
{
   v->failed=0;
   for (int i=0;i<3;i++)
    if (v->l[i]>v->h[i]) 
      v->failed=1;
}        

long var_size(Variable* v)
{
    return ((long)v->h[0]-v->l[0]+1)*(v->h[1]-v->l[1]+1)*(v->h[2]-v->l[2]+1);
}

void var_intersect(Variable* v,Variable* other)
{
     //// intersection of current bounds of v with the domain in other
     for (int i=0;i<3;i++)
     {
       if (v->l[i]<other->l[i]) {v->l[i]=other->l[i];v->changed=1;}
       if (v->h[i]>other->h[i]) {v->h[i]=other->h[i];v->changed=1;}
     }     
     var_test_ground(v);
     var_test_failed(v);
}

void var_intersect(Variable* v, int otherl[],int otherh[])
{
     //// intersection of current bounds with the interval otherl--otherh
     for (int i=0;i<3;i++)
     {
       if (v->l[i]<otherl[i]) {v->l[i]=otherl[i];v->changed=1;}
       if (v->h[i]>otherh[i]) {v->h[i]=otherh[i];v->changed=1;}
     }     
     var_test_ground(v);
     var_test_failed(v);
}

void var_fail(Variable* v)
{/// set a failure domain
     v->l[0]=1;
     v->l[1]=1;
     v->l[2]=1;
     v->l[0]=0;
     v->l[1]=0;
     v->l[2]=0;
     v->ground=0;
     v->failed=1;
}


void var_copy(Variable* v, Variable* other)
{
     v->ID=other->ID;
     for (int i=0;i<3;i++)
     {
         v->l[i]=other->l[i];
         v->h[i]=other->h[i];
     }
     v->ground=other->ground;
     v->failed=other->failed;
     v->labelled=other->labelled;
     v->size=other->size;
}


void var_print_domain(Variable* v)
{
     printf("Domain of variable %3d: ",v->ID);
     for (int i=0;i<3;i++)
       printf("%3d ",v->l[i]);
     printf(", ");
     for (int i=0;i<3;i++)
       printf("%3d ",v->h[i]);
}

