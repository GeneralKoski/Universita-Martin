#include <stdio.h>
#include "Domain.h"

#define DBG 0

Domain::Domain()
{ // constructor: sets the initial bounds (all the volume)
        dbg=DBG;
        if (dbg) printf("Created new domain\n");
        for (int i=0;i<3;i++)
        {l[i]=0;h[i]=MAXVAL;
        } 
        test_ground();
        test_failed();
}

Domain::Domain(unsigned char newl[3], unsigned char newh[3])
{ // constructor: sets the specified bounds
        dbg=DBG;
        if (dbg) printf("Created new domain\n");
        set_domain(newl,newh);
}

Domain::Domain(unsigned char newp[3])
{ // constructor: sets the point
        dbg=DBG;
        if (dbg) printf("Created new domain\n");
        set_value(newp);
}

Domain::~Domain()
{
        printf("Destroying variable\n");
}

void Domain::test_ground()
{
   ground=1;
   for (int i=0;i<3;i++)
    if (l[i]!=h[i]) 
      ground=0;
}        

void Domain::test_failed()
{
   failed=0;
   for (int i=0;i<3;i++)
    if (l[i]>h[i]) 
      failed=1;
}        

int Domain::is_ground()
{
    return ground;
}

int Domain::is_failed()
{
    return failed;
}

long Domain::size()
{
    return ((long)h[0]-l[0]+1)*(h[1]-l[1]+1)*(h[2]-l[2]+1);
}

void Domain::intersect(Domain other)
{
     //// intersection of current bounds with the interval newl--newh
     for (int i=0;i<3;i++)
     {
       if (l[i]<other.l[i]) {l[i]=other.l[i];changed=1;}
       if (h[i]>other.h[i]) {h[i]=other.h[i];changed=1;}
     }     
     test_ground();
     test_failed();
}

void Domain::fail()
{
     l[0]=1;
     l[1]=1;
     l[2]=1;
     l[0]=0;
     l[1]=0;
     l[2]=0;
     test_ground();
     test_failed();
}

void Domain::intersect(unsigned char otherl[],unsigned char otherh[])
{
     //// intersection of current bounds with the interval newl--newh
     for (int i=0;i<3;i++)
     {
       if (l[i]<otherl[i]) {l[i]=otherl[i];changed=1;}
       if (h[i]>otherh[i]) {h[i]=otherh[i];changed=1;}
     }     
     test_ground();
     test_failed();
}

void Domain::set_value(unsigned char newp[])
{
    for (int z=0;z<3;z++)
        {
         l[z]=newp[z];
         h[z]=newp[z];
        }
    changed=1;
     test_ground();
     test_failed();
}

void Domain::set_domain(unsigned char newl[],unsigned char newh[])
{
    for (int z=0;z<3;z++)
        {
         l[z]=newl[z];
         h[z]=newh[z];
        }
    changed=1;
     test_ground();
     test_failed();
}

unsigned char* Domain::getl()
{
         return l;
}

unsigned char* Domain::geth()
{
         return h;
}

void Domain::copy_domain(Domain* other)
{
     for (int i=0;i<3;i++)
     {
         l[i]=other->l[i];
         h[i]=other->h[i];
     }
     test_ground();
     test_failed();
}

void Domain::before_change()
{
     changed=0;
}

int Domain::is_changed()
{
    return changed;
}

void Domain::print_domain()
{
     printf("Domain: ");
     print_point(l);
     printf(", ");
     print_point(h);
     printf("\n");
}

void Domain::print_point(unsigned char v[])
{
     for (int i=0;i<3;i++)
       printf("%d ",v[i]);
}
