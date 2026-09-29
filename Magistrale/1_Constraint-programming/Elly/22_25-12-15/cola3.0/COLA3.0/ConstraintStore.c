#include "ConstraintStore.h"

#define CSTORE_DBG 0
extern int n; // number of variables
extern int nchains;
extern int chains[100][2];
extern int* chain_code;

std::vector<int> clist;        // list of constraints to check (AC3)
int nclist;
int* temp_labelled;           // array for storing labeling information
int* clist_flags; ///used for implemeting ac3
       
       
std::vector<Constraint*> un_constr_array;    //store for unary constraints
std::vector<Constraint*> bi_constr_array;    //store for binary constraints

int n_un_constr_array=0;
int n_bi_constr_array=0;

/// adjancency list: for each variable V_i store an array of indexes of constr_array that
/// contains V_i (in first position)
       
std::vector<int>* un_adjacent; 
std::vector<int>* bi_adjacent;    

int arc_consistency;

long long nconsistency;
long long npropagate;

long ac_calls;
long ac_total_prop;

int* var_changed;

std::vector<int>::iterator theIterator;  // used to scan int vectors

void cstore_add(int type, int v1, int v2,int d)
{
     Constraint* c=(Constraint*)malloc(sizeof(Constraint));
     constr_set(c,type,v1,v2,d); 
   
     
     bi_adjacent[v1].push_back(n_bi_constr_array);       
     bi_constr_array.push_back(c);
     n_bi_constr_array++;
}

void cstore_add(int type, int v1, int v2)
{
     Constraint* c=(Constraint*)malloc(sizeof(Constraint));
     constr_set(c,type,v1,v2);      
    if (constr_is_unary(type))
    {
     un_adjacent[v1].push_back(n_un_constr_array);       
     un_constr_array.push_back(c);
     n_un_constr_array++;
    }
    else
    {
     bi_adjacent[v1].push_back(n_bi_constr_array);       
     bi_constr_array.push_back(c);
     n_bi_constr_array++;     
    }
    if (CSTORE_DBG) constr_print(c);
    if (CSTORE_DBG) printf("\n");
}

void cstore_add(int type, int v1)
{
     cstore_add(type, v1, 0);
}

/////////////// syntactic sugar
void cstore_add_next(int v1,int v2) // sugar for next definition for var1 ,var2 
{
     cstore_add(CONSTR_EUCL,v1,v2,2);
     cstore_add(CONSTR_EUCL,v2,v1,2);
}

void cstore_add_ang(int v1) // sugar for angle constraint
{

     if (v1>0 && v1<n-1)
       {
        cstore_add(CONSTR_EUCL_LEQ,v1-1,v1+1,7);
        cstore_add(CONSTR_EUCL_LEQ,v1+1,v1-1,7);
       }
}

void cstore_add_strand(int v1,int v2) // sugar for strand definition from var1 to var2 included
{
     if (v2-v1<2) printf("Strand is too short: %d %d. No constraints applied!\n",v1,v2);
     printf("Add strand: %d %d\n",v1,v2);
}

void cstore_add_helix(int v1,int v2) // sugar for helix definition from var1 to var2 included
{
     if (v2-v1<3) printf("Helix is too short: %d %d. No constraints applied!\n",v1,v2);
     printf("Add helix: %d %d\n",v1,v2);

////// can propagate some light information (useful pruning in case of ssbonds etc...)
     // global shape maintainance 
     for (int i=v1;i<=v2-4;i++)    //every 4 points the distance is 2,2,0 (to avoid 4,0,0 strand)
     {
       cstore_add(CONSTR_EUCL,i,i+4,8);
       cstore_add(CONSTR_EUCL,i+4,i,8);
     }
}


void cstore_add_ssbond(int v1,int v2) // sugar for ssbond
{
     int cube=2;
     if (n>50) cube=4;
     printf("Add ssbond: %d %d\n",v1,v2);
     cstore_add(CONSTR_DIST_LEQ,v1,v2,cube); // ssbond in the cube with side=2*cube
     cstore_add(CONSTR_DIST_LEQ,v2,v1,cube); // ssbond in the cube with side=2*cube
}

void cstore_add_alldifferent(int v1,int v2)   // sugar for alldifferent from var1 to var2 included
{
     for (int i=v1;i<=v2;i++)
     for (int j=i+1;j<=v2;j++)
     {
       cstore_add(CONSTR_EUCL_GEQ,i,j,1); 
       cstore_add(CONSTR_EUCL_GEQ,j,i,1); 
     }
}

void cstore_add_alldistant(int v1,int v2, int d)   // sugar for alldistant from var1 to var2 included, distance d
{
     for (int i=v1;i<=v2;i++)
     for (int j=i+2;j<=v2;j++)
     {
       cstore_add(CONSTR_EUCL_GEQ,i,j,d); 
       cstore_add(CONSTR_EUCL_GEQ,j,i,d); 
     }
}

void cstore_add_contiguous(int v1,int v2)   // sugar for contiguous
{
     for (int i=v1;i<v2;i++)
       cstore_add_next(i,i+1);      
}

void cstore_add_saw(int v1,int v2)   // sugar for self avoiding walk
{
     cstore_add_contiguous(v1,v2);
     cstore_add_alldifferent(v1,v2);
}

void cstore_add_chain()   // sugar for chain 
{
    // constraints:
    // all distant and contiguous (only outside a block)
    // angle (again outside a block) 
    
    // when a new chain starts, there is no next constraint!
    // if no chain information, the sequence is a single chain
     
    extern int* pattern_code;                                           /// for each variable, set -1 if no pattern, othrw belonging pattern number
    for (int i=0;i<n-1;i++)
    if (pattern_code[i]==-1 || 
        pattern_code[i+1]==-1 ||
        (pattern_code[i]!=pattern_code[i+1]))  // if inside a pattern cannot say anything!
      {
      if (chain_code[i]==chain_code[i+1])
        cstore_add_next(i,i+1);
      }

    /// angle between three consecutive amino acids
    for (int i=1;i<n-1;i++)
    if (pattern_code[i+1]==-1 && 
        pattern_code[i]==-1 && 
        pattern_code[i-1]==-1)// if inside a pattern cannot say anything!
          cstore_add_ang(i);

    /// non occupancy constraints
    for (int i=0;i<n;i++)
    for (int j=i+2;j<n;j++)
    {

    if (
        pattern_code[i]==-1 ||
        (
         pattern_code[i]!=-1 && 
//         pattern_code[j]!=-1 && 
         pattern_code[j]!=pattern_code[i]
        )
       )
       {
//       printf("geq %d %d\n",i,j);
         ////  no volume interaction 
        cstore_add(CONSTR_EUCL_GEQ,i,j,4);  ///  every pair of non next points (on primary), are at distance
        cstore_add(CONSTR_EUCL_GEQ,j,i,4);  /// greater than a lattice unit ( sqrt(4) is the first allowed eucl distance on lattice)
       }
     }
}


int cstore_consistent(AllVariables* vars, int varidx)
{
     /// check for consistency of assignment of variable varidx
     /// first unary constraints
     for( theIterator = un_adjacent[varidx].begin(); theIterator != un_adjacent[varidx].end(); theIterator++ )   
     {

        if (CSTORE_DBG){
           printf("Test un_constr: %d for var %d ",*(theIterator),varidx);
           constr_print(un_constr_array[*(theIterator)]);
           printf("\n");
           }

             nconsistency++;
        if (!constr_consistency(un_constr_array[*(theIterator)],vars))
          {
          return 0;
          }
     }     
     /// then binary constraints (only if other variable has been labelled!!!
     for( theIterator = bi_adjacent[varidx].begin(); theIterator != bi_adjacent[varidx].end(); theIterator++ )   
     {
           if (vars->variables[bi_constr_array[*(theIterator)]->var2].labelled)
            {
             nconsistency++;
             if (CSTORE_DBG) 
             {printf("Test bi_constr: %d for var %d ",*(theIterator),varidx);
              constr_print(bi_constr_array[*(theIterator)]);
              printf("\n");
              }
             if (!constr_consistency(bi_constr_array[*(theIterator)],vars))
              {
              if (CSTORE_DBG) printf("********   FAIL\n");              
              return 0;
              }
            }
     }     
    return 1;   
}


int cstore_before_start()
{  /// simplify constraints

   for (int i=0;i<n;i++)
   {
       for (int j=0;j<bi_adjacent[i].size();j++)
       for (int k=j+1;k<bi_adjacent[i].size();k++)
       if (bi_constr_array[bi_adjacent[i][j]]->var2 ==
           bi_constr_array[bi_adjacent[i][k]]->var2)           
       {
             /// for each pair of constraints
             int o1,o2;
             o1=bi_adjacent[i][j];
             o2=bi_adjacent[i][k];
             /// LEQ before GEQ
             if (bi_constr_array[o2]->type==CONSTR_EUCL_LEQ)
             {
                int temp=o1;
                o1=o2;o2=temp;
             }
             // EQ before every other
             if (bi_constr_array[o2]->type==CONSTR_EUCL)
             {
                int temp=o1;
                o1=o2;o2=temp;
             }
             
             /// = vs <=
             if (bi_constr_array[o1]->type==CONSTR_EUCL &&
                 (bi_constr_array[o2]->type==CONSTR_EUCL_LEQ)
                 )
                 {
                    if (bi_constr_array[o1]->distance>
                        bi_constr_array[o2]->distance)
                         return 0;  //inconsistent
                        else
                         {
                         //printf("Remove ");bi_constr_array[o2].print();printf("\n");
                         constr_set(bi_constr_array[o2],CONSTR_REMOVED,-1,1);
                         }
                 }

             /// = vs >=
             if (bi_constr_array[o1]->type==CONSTR_EUCL &&
                 (bi_constr_array[o2]->type==CONSTR_EUCL_GEQ)
                 )
                 {
                    if (bi_constr_array[o1]->distance<
                        bi_constr_array[o2]->distance)
                         return 0;  //inconsistent
                        else
                         {
                         //printf("Remove ");bi_constr_array[o2].print();printf("\n");
                         constr_set(bi_constr_array[o2],CONSTR_REMOVED,-1,1);
                         }
                 }
       }
   }   
   /// load adjacency lists (for binary constraints)
   for (int i=0;i<n;i++)
    bi_adjacent[i].clear();
   
   for (int i=0;i<n_bi_constr_array;i++)
   if (bi_constr_array[i]->type!=CONSTR_REMOVED)
   {
    int v1=bi_constr_array[i]->var1;
    int v2=bi_constr_array[i]->var2;
    bi_adjacent[v1].push_back(i);
   }  
   
   //cstore_list();
   nclist=0;
   
   for (int i=0;i<n_bi_constr_array;i++)
     clist.push_back(0);
   
   clist_flags=(int*)calloc(n_bi_constr_array,sizeof(int));
   printf("Alloc ok: %d\n",n_bi_constr_array);
   /////// initialize data structure for ac3  
   for (int i=0;i<n_bi_constr_array;i++)
     clist_flags[i]=0;
   return 1;
}

int cstore_ac1(AllVariables* vars,int trailtop)
{
     /// implement AC1, only for non-labelled variables
     /// note that the constraint (v_i,v_j) propagates
     /// on var v_j!
     /// here there is no domain support check (we do only interval propagation)
     
     
     ac_calls++;
     if (CSTORE_DBG) printf("AC1\n");
     int change;
     do{         
     change=0;
     if (CSTORE_DBG) printf("New iteration\n");
     /// for each non-labelled variable (i)     
     for (int i=0;i<n;i++){
     if (!vars->variables[i].labelled)
       {
        for( theIterator = bi_adjacent[i].begin(); theIterator != bi_adjacent[i].end(); theIterator++ )   
          if (!vars->variables[bi_constr_array[*(theIterator)]->var2].labelled)
             // if v1 and v2 not labelled
             // then propagate information from v1 to v2
             {
                if (CSTORE_DBG) {printf("AC on ");constr_print(bi_constr_array[*(theIterator)]);printf("\n");}
                npropagate++;
                ac_total_prop++;
                vars->variables[bi_constr_array[*(theIterator)]->var2].changed=0;
                if (!constr_propagate(bi_constr_array[*(theIterator)],vars,trailtop)) 
                {
                  return 0;
                }
                change=change || vars->variables[bi_constr_array[*(theIterator)]->var2].changed;
             }
     }
     }
     if (CSTORE_DBG) printf("End iteration: ch%d\n",change);
     }
     while (change);

     return 1;
}


int cstore_ac3(AllVariables* vars,int trailtop)
{
     /// implement AC3, only for non-labelled variables    

     /// the previous shrinking phase loaded in .changed
     /// the flag saying if the domain changed
     /// the propagation starts only for those
     /// vars that have been touched
     ac_calls++;
     
     long index_c;

     /// assume that flag_array is set 0 for each entry
     if (CSTORE_DBG) printf("AC3\n");
     /// load in the queue the constraints to be checked
     for (int i=0;i<n;i++)
       temp_labelled[i]=vars->variables[i].labelled;
       
     for (int i=0;i<n;i++)
         {
     if (!temp_labelled[i] && var_changed[i])
        for( theIterator = bi_adjacent[i].begin(); theIterator != bi_adjacent[i].end(); theIterator++ )   
        {
          index_c=*(theIterator);
          if (!temp_labelled[bi_constr_array[index_c]->var2])
             {
              clist[nclist++]=index_c;
              clist_flags[index_c]=1;
             }
         }
        }
     if (CSTORE_DBG) printf("Start iteration\n");
     
     while (nclist>0)
     {     
     ///fetch an element
     int current=clist[nclist-1];
     int currvar;     
     clist_flags[current]=0;
       nclist--;  // removes the constraint
     
     npropagate++;
     ac_total_prop++;

     currvar=bi_constr_array[current]->var2;
     vars->variables[currvar].changed=0;
     if (CSTORE_DBG) {printf("AC on ");constr_print(bi_constr_array[current]);printf("\n");}
     if (!constr_propagate(bi_constr_array[current],vars,trailtop)) 
       {
       return 0;
       }
     if (vars->variables[currvar].changed)
       {/// if the variable has been modified, include new arcs
          //if (CSTORE_DBG) printf("Changed: insert in queue\n");
          for( theIterator = bi_adjacent[currvar].begin(); theIterator != bi_adjacent[currvar].end(); theIterator++ )   
          {
             //by construction currvar not labelled
             // check that the arc is not the symmetric
             // and that the other var is actually not labelled
             int index_c=*(theIterator);
             int var2_c=bi_constr_array[index_c]->var2;
          //if (CSTORE_DBG) {printf("test ");constr_print(bi_constr_array[index_c]);printf("\n");}
             if (var2_c!=
                 bi_constr_array[current]->var1 &&
                 !temp_labelled[var2_c] &&
                 clist_flags[index_c]==0   /// not including a duplicate
                 )
              {
          //if (CSTORE_DBG) printf("          Add!!!\n");
                clist[nclist++]=index_c;
                clist_flags[index_c]=1;
              }
          //else
          //if (CSTORE_DBG) printf("Dont add\n");
          }
       }
     }
     if (CSTORE_DBG) printf("End AC3\n");
     return 1;
}

int cstore_propagate(AllVariables* vars, int varidx,int trailtop)
{
    cstore_reset_var_changed();
    if (cstore_propagate_g_ng(vars,varidx, trailtop))
      return cstore_ac(vars, trailtop);
    else
      return 0;
}

void cstore_reset_var_changed()
{
 memset(var_changed,0,(sizeof(int)*n));
}

int cstore_propagate_g_ng(AllVariables* vars, int varidx,int trailtop)
{
     /// varidx is the index of the last assigned var
     ///// based on Apt book    
     /////    domain shrinking: using propagators from labelled variables to non-labelled vars
     /////                      in order to reduce the domains of future vars
     /////                      Example (assuming [1..j] labelled [j+1..n] non-labelled
     /////                       (V_i,V_k) propagate, only if V_i in [1..j] and V_k in [j+1..n]
     /////                      
     /////                      For efficiency purposes, test each var non-labelled. The number 
     /////                      of constraints ending in the variable is bounded (k) non depending on n
     /////                      -> the test is O(kn) -> O(n)          
     //// phase 1.
     ////  --> using bound consistency
     /// for each non-labelled variable (i)
     /// apply consistency for constraints from labelled vars --> var_i
     //allvar_print_stat(vars);

     if (CSTORE_DBG) printf(" Shrinking\n");
     if (varidx==-1) return 1;
     int i=varidx;
     if (vars->variables[i].labelled)
       // retrieve set of binary constrains with second var == i
        for( theIterator = bi_adjacent[i].begin(); theIterator != bi_adjacent[i].end(); theIterator++ )   
          if (!vars->variables[bi_constr_array[*(theIterator)]->var2].labelled)
             // if v1 has been labelled
             // then propagate information from v1 to v2
             {
                npropagate++;
                if (CSTORE_DBG) {printf("SHR on ");constr_print(bi_constr_array[*(theIterator)]);}                
                vars->variables[bi_constr_array[*(theIterator)]->var2].changed=0;
                if (!constr_propagate(bi_constr_array[*(theIterator)],vars,trailtop))
                  {
                  return 0;
                  }
                // stores if var changed
                if (vars->variables[bi_constr_array[*(theIterator)]->var2].changed) 
                     var_changed[bi_constr_array[*(theIterator)]->var2]=1;
                if (CSTORE_DBG) {printf("ch:%d\n",vars->variables[bi_constr_array[*(theIterator)]->var2].changed);}
             }
    return 1;
}


int cstore_ac(AllVariables* vars,int trailtop)
{
     /////  ACX             : apply arc consistency on non-labelled vars (if phase 1 didnt failed)
     ///  --> again bound consistency     
     switch (arc_consistency)
     {
       case(STORE_AC1):
          return cstore_ac1(vars, trailtop);
       case(STORE_AC3):
          return cstore_ac3(vars, trailtop);
     }
}


int cstore_propagate(AllVariables* vars)
{
    cstore_propagate(vars,-1,0);
}

void cstore_init(int ac)
{
   nconsistency=0;
   npropagate=0;
   arc_consistency=ac;
   temp_labelled=(int*)calloc(n,sizeof(int));
   var_changed=(int*)calloc(n,sizeof(int));
   un_adjacent=new std::vector<int>[n];
   bi_adjacent=new std::vector<int>[n];
   ac_calls=0;
   ac_total_prop=0;
}

void cstore_list()
{
     printf("Unary:\n");
     for (int i=0;i<n;i++)
     {
         for (int j=0;j<un_adjacent[i].size();j++)
           {
           printf("Var %2d: index %3d ",i,un_adjacent[i][j]);
           constr_print(un_constr_array[un_adjacent[i][j]]);
           printf("\n");           
           }
     }
     printf("Binary:\n");
     for (int i=0;i<n;i++)
     {
         for (int j=0;j<bi_adjacent[i].size();j++)
          {
           printf("Var %2d: index %3d ",i,bi_adjacent[i][j]);
           constr_print(bi_constr_array[bi_adjacent[i][j]]);
           printf("\n");
           }
     }
}

void cstore_stat()
{
     printf("N. consistency checks %ld\n",nconsistency);
     printf("N. propagations %ld\n", npropagate);
     printf("Using AC%d\n",arc_consistency*2+1);
     printf("N. calls %ld\n",ac_calls);
     printf("N. prop %ld, avg %f\n",ac_total_prop, (float)ac_total_prop/ac_calls);
}