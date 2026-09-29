#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include "Utils.h"

float tempter[MAXATOM][3];
char temppri[MAXATOM][4];
int tempn;
int temphelix[10][2];
int tempsheet[10][2];
int tempss[10][2];
char tempid[4];  
char tempprotid[10];
int tempnhelix=0;
int tempnsheet=0;
int tempnss=0;
int tempnaa;
char tempprin[MAXATOM][5];
int tempdelta;

//OK!
void read_atom_pdb(char *buf, char *at_rec, int *p_n_at_pdb,
   char *at_name, char *alt_loc, char *res_name, char *chain,
   int *p_n_res, char *res_ins, float *p_x, float *p_y, float *p_z,
   float *p_occ, float *p_temp_f, int *p_foo_num) {


        char tok[10];


        strncpy(tok,buf,5);
        tok[5] = '\0';
        sscanf(tok,"%s", at_rec);


        strncpy(tok,buf + 6,6);
        tok[6] = '\0';
        sscanf(tok,"%i",p_n_at_pdb);


        strncpy(tok,buf + 12,5);
        tok[5] = '\0';
        sscanf(tok,"%s", at_name);


        strncpy(tok,buf + 16,1);
        tok[1] = '\0';
        if(sscanf(tok,"%s", alt_loc) == -1) strcpy(alt_loc," ");


        strncpy(tok,buf + 17,3);
        tok[3] = '\0';
        sscanf(tok,"%s", res_name);


        strncpy(tok,buf + 21,1);
        tok[1] = '\0';
        if(sscanf(tok,"%s", chain) == EOF) strcpy(chain," ");


        strncpy(tok,buf + 22,5);
        tok[5] = '\0';
        sscanf(tok,"%i", p_n_res);


        strncpy(tok,buf + 26,1);
        tok[1] = '\0';
        if (sscanf(tok,"%s", res_ins) == EOF) strcpy(res_ins," ");


        strncpy(tok,buf + 30,8);
        tok[8] = '\0';
        sscanf(tok,"%f", p_x);
        
        strncpy(tok,buf + 38,8);
        tok[8] = '\0';
        sscanf(tok,"%f", p_y);
        
        strncpy(tok,buf + 46,8);
        tok[8] = '\0';
        sscanf(tok,"%f", p_z);


        strncpy(tok,buf + 54,6);
        tok[6] = '\0';
        sscanf(tok,"%f", p_occ);


        strncpy(tok,buf + 60,6);
        tok[6] = '\0';
        sscanf(tok,"%f", p_temp_f);


        strncpy(tok,buf + 67,3);
        tok[3] = '\0';
        sscanf(tok,"%i", p_foo_num);


}



int load(char* fn)
{
	
    FILE* fi;
	 fi=fopen(fn,"r");

    if (fi==NULL) 
    {
     printf("File error!\n");	
     return -1;
    }
    tempnaa=0;
    

  	 tempn=0;
	 tempnhelix=0;
	 tempnsheet=0;
	 tempnss=0;
      char buf[121];
      char tok[10];
      char at_rec[5], at_name[6], alt_loc[2], res_name[4],
           chain[2], res_ins[2];
      int n_at_pdb, n_res, foo_num;
      float x, y, z, temp_f, occ;
     float r12[3];

      tempdelta=-1;

int flag=0;
int stop=0;
tempn=0;

while(!flag  && fgets(buf,120,fi) != NULL &&  stop<2)
{
      if(!strncmp("DBREF",buf,5)) 
      {
	      
        strncpy(tok,buf + 7,4);
        tok[4] = '\0';
        sscanf(tok,"%s",tempprotid);
//        printf("ID:%s",tempprotid);
	      
	   }
      else
      if(!strncmp("SHEET",buf,5)) 
      {
//	      printf("Sheet: ");      
        strncpy(tok,buf + 23,3);
        tok[3] = '\0';
        sscanf(tok,"%d",&tempsheet[tempnsheet][0]);
        
        strncpy(tok,buf + 34,3);
        tok[3] = '\0';
        sscanf(tok,"%d",&tempsheet[tempnsheet][1]);        
        
//        printf("[%d,%d]\n",tempsheet[tempnsheet][0],tempsheet[tempnsheet][1]);
	      
	      tempnsheet++;	      
	   }else
      if(!strncmp("HELIX",buf,5)) 
      {
//	      printf("Helix: ");	      
        strncpy(tok,buf + 22,3);
        tok[3] = '\0';
        sscanf(tok,"%d",&temphelix[tempnhelix][0]);
        
        strncpy(tok,buf + 34,3);
        tok[3] = '\0';
        sscanf(tok,"%d",&temphelix[tempnhelix][1]);        
        
//        printf("[%d,%d]\n",temphelix[tempnhelix][0],temphelix[tempnhelix][1]);
         tempnhelix++;	      
	   }else
      if(!strncmp("SSBOND",buf,6)) 
      {	      
	     strncpy(tok,buf + 18,3);
        tok[3] = '\0';
        sscanf(tok,"%d",&tempss[tempnss][0]);
        
        strncpy(tok,buf + 32,3);
        tok[3] = '\0';
        sscanf(tok,"%d",&tempss[tempnss][1]);                
//        printf("ssbond(%d,%d)\n",tempss[tempnss][0],tempss[tempnss][1]);
         
	      tempnss++;	      
	   }
	   else      
      if (!strncmp("ANISOU",buf,6))
      {
	      int i=1;
	   }else      
	   
      if((!strncmp("ATOM",buf,4) ||
          !strncmp("HETATM",buf,6))
         && stop<2) 
       {stop=1;

               read_atom_pdb(buf, at_rec, &n_at_pdb, at_name, alt_loc,
                       res_name, chain, &n_res, res_ins, &x, &y, &z, 
                       &occ, &temp_f, &foo_num);
                       

               
             if (strcmp(at_name,"CA")==0 &&
                 (strcmp(alt_loc,"A")==0 ||
                  strcmp(alt_loc," ")==0)
                 )
             {
//        printf("%s\n",alt_loc);
//               printf("%s\n",buf);

/*
         	   printf("%d: %s %c ",tempn,res_name, cv(res_name));
               printf("%d %f ",tempn,x);
         	   printf("%f ",y);	  
         	   printf("%f \n",z);
               //printf("%c",cv31(res_name));
*/

         		if (tempdelta==-1) tempdelta=n_res-1;
         		
         		tempter[tempn][0]=x/3.81*sqrt(2);
         		tempter[tempn][1]=y/3.81*sqrt(2);
         		tempter[tempn][2]=z/3.81*sqrt(2);

                   if (tempn>0)
                   {
/*
                 	 r12[0]=tempter[tempn][0]-tempter[tempn-1][0]; 
                	 r12[1]=tempter[tempn][1]-tempter[tempn-1][1];
                	 r12[2]=tempter[tempn][2]-tempter[tempn-1][2];
                    if (len(r12)>4) flag=1;
*/                   }
      
         		strcpy(tempprin[tempn],res_name); 	 
 		 	  
         		tempn++; 	   
              }
	   }
     else
       	      if (stop==1) stop=2;
	    
}
	 strcpy(tempprin[tempn],"END");
	 strcpy(tempprin[tempn+1],"END");
	 strcpy(tempprin[tempn+2],"END");
   tempnaa=tempn;
   //printf("%d read\n",tempnaa);
   fclose(fi);
   return 0;
}
