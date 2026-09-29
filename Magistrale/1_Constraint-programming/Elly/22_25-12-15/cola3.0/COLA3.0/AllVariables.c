#include <stdio.h>
#include <iostream>
#include "AllVariables.h"
#include "Search.h"

#define ALLVAR_DBG 0

void allvar_init(AllVariables* allv)
{
        extern int n; // number of variables
     
        allv->variables=(Variable*) calloc(n, sizeof(Variable));
        
        for (int i=0;i<n;i++)
        {
            allv->variables[i].ID=i;
            var_init(allv->variables+i);
            if (ALLVAR_DBG){
                    printf("Init var %d\n",i);
                    var_print_domain(allv->variables+i);
                    }
        }
        if (ALLVAR_DBG) printf("Created new variable store. Size %d\n",n);
}

void allvar_fill_from(AllVariables* allv, AllVariables* other)
{
  extern int n; // number of variables
  for (int i=0;i<n;i++)
   {
       if (ALLVAR_DBG) printf("Copying var %d\n",i);
       var_copy(allv->variables+i,other->variables+i);
   }                                                                        
}



void allvar_print_stat(AllVariables* allv)
{
     extern int n; // number of variables
     printf("Status of vars:\n");
     for (int i=0;i<n;i++)
         {
         var_print_domain(allv->variables+i);
         printf(" Size: %8d L%d\n",var_size(allv->variables+i),allv->variables[i].labelled);
         }
     printf("\n");
}

void allvar_print_delta(AllVariables* allv)
{
     extern int n; // number of variables
     for (int i=0;i<n-1;i++)
     {
         int* l1;
         int* l2;
         l1=(allv->variables+i)->l;
         l2=(allv->variables+i+1)->l;
         printf("%2d %2d %2d\n",l2[0]-l1[0],l2[1]-l1[1],l2[2]-l1[2]);         
     }
     printf("\n");     
}
