
#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include <fstream>
#include <math.h>
#include "Pattern.h"
#include "load.h"
#include "Utils.h"
#include "Search.h"

extern int n;

int npattern=0;                                                /// how many patterns
int pattern_len[MAXNPATTERNS];                               /// length of each pattern
int pattern_extension[MAXNPATTERNS][2];                      /// associated start and end variables (included)
int pattern[MAXNPATTERNS][24][MAXPATTERNPOINTS][3];          /// for each rotation list all points (on FCC)
float pattern_real[MAXNPATTERNS][24][MAXPATTERNPOINTS][3];   /// for each rotation list all points (real)

int* pattern_code;                                           /// for each variable, set -1 if no pattern, othrw belonging pattern number
int* chain_code;                                           /// for each variable, set -1 if no pattern, othrw belonging pattern number
int minPattern;    /// stores the first aa involved in some pattern (used to compute a better FF strategy)
int maxPattern;    /// stores the last aa involved in some pattern 

int rot[12][3][3];   /// rotation matrices...

int nssbond=0;
int ssbond[100][2];

int nchains=0;
int chains[100][2];


extern double table[256][256];  // fast version: indexed directely by char code
extern char primary[1000]; // sequence


void init_pattern()
{
///// pattern handling
    
    pattern_code=(int*)calloc(n,sizeof(int));
    chain_code=(int*)calloc(n,sizeof(int));
    
    minPattern=n-1;
    maxPattern=0;
    
    for (int i=0;i<n;i++)
      pattern_code[i]=-1;

    for (int i=0;i<n;i++)
      chain_code[i]=0;

   for (int i=0;i<npattern;i++)
   {
     if (minPattern>pattern_extension[i][0]) minPattern=pattern_extension[i][0];
     if (maxPattern<pattern_extension[i][1]) maxPattern=pattern_extension[i][1];
   }
   
   if (minPattern==n-1) /// no patterns
   {
      minPattern=0;
      maxPattern=n-1;
   }
      

    printf("%d patterns loaded\n",npattern);
//    for (int i=0;i<npattern;i++)
//      printf("%d: %d %d\n",i,pattern_extension[i][0],pattern_extension[i][1]);
    printf("npatterns loaded %d, min max %d %d\n",npattern,minPattern,maxPattern);

   for (int i=0;i<nchains;i++)
    for (int j=chains[i][0];j<=chains[i][1];j++)
     chain_code[j]=i;

   for (int i=0;i<npattern;i++)
   {
//       printf("i%d\n",i);
   for (int j=pattern_extension[i][0];j<=pattern_extension[i][1];j++)
   {
//       printf("pat %d: %d\n",j,pattern_code[j]);
   if (pattern_code[j]<0)
     pattern_code[j]=i;
   else
   {
       printf("Error: pattern %d overlaps pattern %d!\n",pattern_code[j],i);
       system("PAUSE");
       exit(0);
   }
   }
}

   for (int i=0;i<n;i++)
   {
     if (i%10==0) printf("%2d: ",i/10);
     printf("%2d ",pattern_code[i]);
     if (i%10==9) printf("\n");
   }
   printf("\n");
   
   for (int i=0;i<n;i++)
   {
     if (i%10==0) printf("%2d: ",i/10);
     printf("%2d ",chain_code[i]);
     if (i%10==9) printf("\n");
   }
   printf("\n");

   setup_rotation_matr();
   
   /// rotate each pattern in 24 (FCC dependent) orientations
   /// first 180 deg along 1,0,0 direction
   int coef=1;
   for (int k=0;k<npattern;k++)   
   for (int p=0;p<pattern_len[k];p++)
   for (int z=0;z<3;z++)
   {
       
       if (z==0) coef=1;
       else
       coef=-1;
       pattern[k][1][p][z]=coef*pattern[k][0][p][z];
       pattern_real[k][1][p][z]=coef*pattern_real[k][0][p][z];
   }

   for (int k=0;k<npattern;k++)   
   for (int i=2;i<24;i++)
   for (int p=0;p<pattern_len[k];p++)
   for (int z=0;z<3;z++)
   {
    pattern[k][i][p][z]=0;
    pattern_real[k][i][p][z]=0;
   }
   
   /// then 12 different matrices
   for (int k=0;k<npattern;k++)   
   for (int i=1;i<12;i++)
   for (int z=0;z<3;z++)
   for (int l=0;l<3;l++)
   for (int b=0;b<2;b++)
   {
    // pattern points
    for (int p=0;p<pattern_len[k];p++)
    {
      pattern[k][2*i+b][p][z]+=rot[i][z][l]*pattern[k][b][p][l];
      pattern_real[k][2*i+b][p][z]+=rot[i][z][l]*pattern_real[k][b][p][l];
    }
   }
}

void setup_rotation_matr()
{
   int temp[3][3]; // temp matrix
   
   /// init first 4 rot matrices
   for (int i=0;i<12;i++) 
   for (int j=0;j<3;j++) 
   for (int k=0;k<3;k++) 
     rot[i][j][k]=0;

   for (int i=0;i<3;i++) 
   for (int j=0;j<3;j++) 
     temp[i][j]=0;
   
   
   rot[0][0][0]=1;rot[0][1][1]=1;rot[0][2][2]=1; // identity
   rot[1][0][1]=-1;rot[1][1][0]=1;rot[1][2][2]=1;
   rot[2][0][0]=-1;rot[2][1][1]=-1;rot[2][2][2]=1;
   rot[3][0][1]=1;rot[3][1][0]=-1;rot[3][2][2]=1;
   
   /// rotate the base plane 90 deg plane xz
   temp[0][2]=-1; temp[1][1]=1;temp[2][0]=1;   
   for (int i=0;i<4;i++)
   for (int j=0;j<3;j++)
   for (int k=0;k<3;k++)
   for (int l=0;l<3;l++)
   {   // i index, matrix[i][j]
    rot[4+i][j][k]+=temp[j][l]*rot[i][l][k];
   }
   /// rotate the base plane 90 deg plane yz
   temp[0][2]=0; temp[1][1]=0;temp[2][0]=0;   
   temp[0][0]=1; temp[2][1]=1;temp[1][2]=-1;   
   for (int i=0;i<4;i++)
   for (int j=0;j<3;j++)
   for (int k=0;k<3;k++)
   for (int l=0;l<3;l++)
   {   // i index, matrix[i][j]
    rot[8+i][j][k]+=temp[j][l]*rot[i][l][k];
   }
}


void pattern_load_helix(int v1,int v2)
{
  //printf("add pattern %d: %d %d\n",npattern,v1,v2);
  pattern_extension[npattern][0]=v1;
  pattern_extension[npattern][1]=v2;
  pattern_len[npattern]=v2-v1+1;
 
  pattern[npattern][0][0][0]=0;pattern[npattern][0][0][1]=0;pattern[npattern][0][0][2]=0;
  pattern[npattern][0][1][0]=1;pattern[npattern][0][1][1]=0;pattern[npattern][0][1][2]=1;
  pattern[npattern][0][2][0]=2;pattern[npattern][0][2][1]=0;pattern[npattern][0][2][2]=0;
  pattern[npattern][0][3][0]=2;pattern[npattern][0][3][1]=1;pattern[npattern][0][3][2]=-1;

  for (int i=4;i<pattern_len[npattern];i++) // if helix if longer than 3 add (the current axis is 2,2,0)
  {
    pattern[npattern][0][i][0]=pattern[npattern][0][i%4][0]+2*(i/4);
    pattern[npattern][0][i][1]=pattern[npattern][0][i%4][1]+2*(i/4);
    pattern[npattern][0][i][2]=pattern[npattern][0][i%4][2]+0*(i/4);
  }
  
  for (int i=0;i<pattern_len[npattern];i++)
  for (int z=0;z<3;z++)
    pattern_real[npattern][0][i][z]=pattern[npattern][0][i][z];
  
  npattern++;    
}

void pattern_load_strand(int v1,int v2)
{
  //printf("add pattern %d: %d %d\n",npattern,v1,v2);
  pattern_extension[npattern][0]=v1;
  pattern_extension[npattern][1]=v2;
  pattern_len[npattern]=v2-v1+1;

  pattern[npattern][0][0][0]=0;pattern[npattern][0][0][1]=0;pattern[npattern][0][0][2]=0;
  pattern[npattern][0][1][0]=1;pattern[npattern][0][1][1]=1;pattern[npattern][0][1][2]=0;

  for (int i=2;i<pattern_len[npattern];i++) // if strand is longer than 1 add (the current axis is 2,0,0)
  {
    pattern[npattern][0][i][0]=pattern[npattern][0][i%2][0]+2*(i/2);
    pattern[npattern][0][i][1]=pattern[npattern][0][i%2][1]+0*(i/2);
    pattern[npattern][0][i][2]=pattern[npattern][0][i%2][2]+0*(i/2);
  }

  for (int i=0;i<pattern_len[npattern];i++)
  for (int z=0;z<3;z++)
    pattern_real[npattern][0][i][z]=pattern[npattern][0][i][z];

  npattern++;    
}

void pattern_load(int v1,int v2, char* fn)
{
  pattern_load(v1,v2, 0,v2-v1, fn);
}
void pattern_load(int v1,int v2, int s1, int s2, char* fn)
{
    extern float tempter[10000][3];
    extern char temppri[10000][4];
    extern int tempn;
    extern int temphelix[10][2];
    extern int tempsheet[10][2];
    extern int tempss[10][2];
    extern char tempid[4];  
    extern char tempprotid[10];
    extern int tempnhelix;
    extern int tempnsheet;
    extern int tempnss;
    extern int tempnaa;
    extern char tempprin[10000][5];
    extern int tempdelta;


  printf("add pattern %d: %d %d\n",npattern,v1,v2);
  pattern_extension[npattern][0]=v1;
  pattern_extension[npattern][1]=v2;
  pattern_len[npattern]=v2-v1+1;

  if (load(fn)!=0)
   {
    printf("ERROR: pattern %d (%s) not found!\n",npattern,fn);
    system("PAUSE");
    exit(1);
   } 

  if (tempnaa<pattern_len[npattern])
    {
      printf("ERROR: pattern %d has declared length %d, but pdb file contains %d aa\n",npattern,pattern_len[npattern],tempnaa);
    system("PAUSE");
      exit(1);
    }
    
    for (int i=0;i<pattern_len[npattern];i++)
    {
//      printf("%d: ",i);
    for (int z=0;z<3;z++)
    {    
//    printf("%f (%f) ",tempter[i+s1][z]-tempter[s1][z],round(tempter[i+s1][z]-tempter[s1][z]));
    pattern_real[npattern][0][i][z]=tempter[i+s1][z]-tempter[s1][z];
    }
    /// the discretized pattern has to be on FCC!, add 1 on z coordinate if the point was not on fcc
    
    int temp[3];
    for (int z=0;z<3;z++)
     temp[z]=floor(tempter[i+s1][z]-tempter[s1][z]);
    // look for best fcc approximation
    int pos[3];
    pos[0]=0;
    pos[1]=0;
    pos[2]=0;
    double best=4;
    for (int i1=0;i1<2;i1++)
    for (int j1=0;j1<2;j1++)
    for (int k1=0;k1<2;k1++)
    {
        double curr=0;
        curr+=(tempter[i+s1][0]-tempter[s1][0]-temp[0]-i1)*(tempter[i+s1][0]-tempter[s1][0]-temp[0]-i1);
        curr+=(tempter[i+s1][1]-tempter[s1][1]-temp[1]-j1)*(tempter[i+s1][1]-tempter[s1][1]-temp[1]-j1);
        curr+=(tempter[i+s1][2]-tempter[s1][2]-temp[2]-k1)*(tempter[i+s1][2]-tempter[s1][2]-temp[2]-k1);
/*
        printf("%d %d %d: %f, %f %f %f . %d %d %d\n",i1,j1,k1,curr,
                                                     tempter[i+s1][0]-tempter[s1][0]-temp[0],
                                                     tempter[i+s1][1]-tempter[s1][1]-temp[1],
                                                     tempter[i+s1][2]-tempter[s1][2]-temp[2],
                                                     temp[0],
                                                     temp[1],
                                                     temp[2]
                                                     ); 
*/
        if (curr<best &&
            (temp[0]+i1+temp[1]+j1+temp[2]+k1)%2==0)
          {
//            printf("*\n");
            pos[0]=temp[0]+i1;
            pos[1]=temp[1]+j1;
            pos[2]=temp[2]+k1;
            best=curr;
          }
    }
    
    for (int z=0;z<3;z++)
    pattern[npattern][0][i][z]=pos[z];
    
/*    printf("%d:",i+s1);
    for (int z=0;z<3;z++)
      printf("%d ",pattern[npattern][0][i][z]);
    for (int z=0;z<3;z++)
      printf("%f ",pattern_real[npattern][0][i][z]);
    for (int z=0;z<3;z++)
      printf("%f ",tempter[i+s1][z]);
    printf("\n");
    
     printf("%c",cv31(tempprin[i+s1]));
//    printf("\n");
*/     
    }    
   printf("\n");
  npattern++;    
}