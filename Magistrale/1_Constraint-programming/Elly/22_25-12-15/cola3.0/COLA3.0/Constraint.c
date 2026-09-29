#include "Constraint.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "TrailStack.h"

#define CONSTR_DBG 0

int constr_propagate_eucl_distance(Constraint* c, AllVariables* allvar, int trailtop)
{
     /// propagate from v1 to v2 and modify v2     
     int newl[3],newh[3];
     int ol[3],oh[3];
     if (CONSTR_DBG) printf("\nEucl_d %d->%d\n",c->var1,c->var2);
     if (CONSTR_DBG) {var_print_domain(allvar->variables+c->var2);printf("\n");}
     if (CONSTR_DBG) allvar_print_stat(allvar);

     /// original bounds (cannot touch, else modify directly)
     int* l=allvar->variables[c->var1].l;
     int* h=allvar->variables[c->var1].h;

     // apply eucl distance approximated semantics 
     // uses the box with size 2*distance_approx (approximates the sphere with radius sqrt(distance))
     for (int i=0;i<3;i++)
     {
         if (l[i]>=c->distance_approx)
             newl[i]=l[i]-c->distance_approx;
         else
             newl[i]=l[i];
             
         if (h[i]<=MAXVAL-c->distance_approx)
           newh[i]=h[i]+c->distance_approx;
         else
           newh[i]=h[i];
     }
     /// intersect with other volume
     memcpy(ol,(allvar->variables+c->var2)->l,sizeof(int)*3);
     memcpy(oh,(allvar->variables+c->var2)->h,sizeof(int)*3);
     var_intersect(allvar->variables+c->var2, newl,newh);
     
     if (CONSTR_DBG) var_print_domain(allvar->variables+c->var2);
     if ((allvar->variables+c->var2)->changed)
       {
	   trail((allvar->variables+c->var2),ol,oh,allvar,trailtop);
	   if (CONSTR_DBG) printf("New val ");
	   if (CONSTR_DBG)  var_print_domain(allvar->variables+c->var2);
	   if (CONSTR_DBG)  printf("\n");
       }
	 if (allvar->variables[c->var2].failed) return 0;     
  return 1;    
}

int constr_propagate_distance(Constraint* c, AllVariables* allvar, int trailtop)
{
     /// propagate from v1 to v2
     
     int newl[3],newh[3];
     int ol[3],oh[3];
     if (CONSTR_DBG) printf("\ndist %d->%d\n",c->var1,c->var2);
     if (CONSTR_DBG) {var_print_domain(allvar->variables+c->var2);printf("\n");}
     if (CONSTR_DBG) allvar_print_stat(allvar);
     /// original bounds (cannot touch, else modify directly)
     int* l=allvar->variables[c->var1].l;
     int* h=allvar->variables[c->var1].h;
     
     // apply distance semantics (expands borders by distance unit)
     for (int i=0;i<3;i++)
     {
         if (l[i]>=c->distance)
             newl[i]=l[i]-c->distance;
         else
             newl[i]=l[i];
             
         if (h[i]<=MAXVAL-c->distance)
           newh[i]=h[i]+c->distance;
         else
           newh[i]=h[i];
     }
     /// intersect with other volume
       memcpy(ol,(allvar->variables+c->var2)->l,sizeof(int)*3);
       memcpy(oh,(allvar->variables+c->var2)->h,sizeof(int)*3);
     var_intersect(allvar->variables+c->var2, newl,newh);

     if (CONSTR_DBG) allvar_print_stat(allvar);
     if (CONSTR_DBG) {var_print_domain(allvar->variables+c->var2);printf("\n");}

     if ((allvar->variables+c->var2)->changed)
  	  {
       trail((allvar->variables+c->var2),ol,oh,allvar,trailtop);
	   if (CONSTR_DBG) printf("New val ");
	   if (CONSTR_DBG) var_print_domain(allvar->variables+c->var2);
	   if (CONSTR_DBG) printf("\n");
      }
     
     if (allvar->variables[c->var2].failed) return 0;     
     if (CONSTR_DBG) var_print_domain(allvar->variables+c->var2);
  return 1;     
}



int constr_consistency_eucl_distance(Constraint* c, AllVariables* allvar)
{
   // test if v1 has the correct eucl distance from v2 (assuming that v2 is ground)
   // distance is already squared!  
      int* t1=allvar->variables[c->var1].l;
      int* t2=allvar->variables[c->var2].l;
      int va,vb,vc;
      va=(int)t2[0]-t1[0];
      vb=(int)t2[1]-t1[1];
      vc=(int)t2[2]-t1[2];
      if (va*va+vb*vb+vc*vc!=c->distance)  
      {
          var_fail(allvar->variables+c->var1);
          return 0;
      }
  return 1;
}

int constr_consistency_eucl_leq_distance(Constraint* c, AllVariables* allvar)
{
   // test if v1 has the correct eucl distance from v2 (assuming that v2 is ground)
   // distance is already squared!  
      int* t1=allvar->variables[c->var1].l;
      int* t2=allvar->variables[c->var2].l;
      int va,vb,vc;
      va=(int)t2[0]-t1[0];
      vb=(int)t2[1]-t1[1];
      vc=(int)t2[2]-t1[2];
      if (va*va+vb*vb+vc*vc>c->distance)  
      {
          var_fail(allvar->variables+c->var1);
          return 0;
      }
      
  return 1;
}

int constr_consistency_eucl_geq_distance(Constraint* c, AllVariables* allvar)
{
   // test if v1 has the correct eucl distance from v2 (assuming that v2 is ground)
   // distance is already squared!  
      int* t1=allvar->variables[c->var1].l;
      int* t2=allvar->variables[c->var2].l;
      int va,vb,vc;
      va=(int)t2[0]-t1[0];
      vb=(int)t2[1]-t1[1];
      vc=(int)t2[2]-t1[2];
      if (va*va+vb*vb+vc*vc<c->distance)  
      {
          var_fail(allvar->variables+c->var1);
          return 0;
      }
  return 1;
}



int constr_consistency(Constraint* c, AllVariables* allvar)
{    
     // var1 has been labelled
     // when dealing with var2,  assume that var2 has been labelled 

     switch(c->type){
     case CONSTR_DIST_LEQ :
     break;
     case CONSTR_EUCL :
           return constr_consistency_eucl_distance(c,allvar);
     break;
     case CONSTR_EUCL_LEQ :
           return constr_consistency_eucl_leq_distance(c,allvar);
     break;
     case CONSTR_EUCL_GEQ :
           return constr_consistency_eucl_geq_distance(c,allvar);
     break;
     case CONSTR_REMOVED :
     break;
     }
}

int constr_propagate(Constraint* c, AllVariables* allvar, int trailtop)
{
     switch(c->type){
     case CONSTR_DIST_LEQ :
           return constr_propagate_distance(c,allvar,trailtop);
     break;
     case CONSTR_EUCL :
           return constr_propagate_eucl_distance(c,allvar,trailtop);
     break;
     case CONSTR_EUCL_LEQ :
           return constr_propagate_eucl_distance(c,allvar,trailtop);  // use the same idea for approx propagation
     break;
     case CONSTR_EUCL_GEQ :
     break;
     case CONSTR_REMOVED :
     break;
     }
}

int constr_is_unary(int type)
/// return if the type of constraint is unary
{
    switch(type)
    {
       case (CONSTR_DIST_LEQ):
            return 0;
       case (CONSTR_EUCL):
            return 0;
       case (CONSTR_EUCL_LEQ):
            return 0;
       case (CONSTR_EUCL_GEQ):
            return 0;
    }
}
             


void constr_print(Constraint* c)
{
   switch(c->type)
   {
      case (CONSTR_DIST_LEQ):
           printf("DIST_LEQ(%d,%d)<=%d.",c->var1,c->var2,c->distance);
           break;
      case (CONSTR_EUCL):
           printf("EUCL_D(%d, %d)=%d.",c->var1,c->var2,c->distance);
           break;
      case (CONSTR_EUCL_LEQ):
           printf("EUCL_D_LEQ(%d, %d)<=%d.",c->var1,c->var2,c->distance);
           break;
      case (CONSTR_EUCL_GEQ):
           printf("EUCL_D_GEQ(%d, %d)>=%d.",c->var1,c->var2,c->distance);
           break;
     case CONSTR_REMOVED :
           printf("REMOVED\n");
     break;
   }
}

void constr_set(Constraint* c, int n_type, int n_var1, int n_var2)
{
     c->type=n_type;
     c->var1=n_var1;
     c->var2=n_var2;
}

void constr_set(Constraint* c, int n_type, int n_var1, int n_var2, int n_dist)
{
     c->type=n_type;
     c->var1=n_var1;
     c->var2=n_var2;
     c->distance=n_dist;
     if (c->type==CONSTR_EUCL || 
         c->type==CONSTR_EUCL_LEQ)
       c->distance_approx=(int)floor(sqrt(c->distance));
}
