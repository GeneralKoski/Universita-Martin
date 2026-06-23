#include <stdio.h>

#define N 32

__managed__  int  Vett[N];

__global__ void VecAdd(int *Vett, int a)
 { 
   Vett[threadIdx.x] =  Vett[threadIdx.x] * Vett[threadIdx.x]; 
 } 


int main() {
   for(int i=0; i<N; i++) Vett[i]=i; 
   VecAdd<<< 1, N >>>(Vett,  100);  
   cudaDeviceSynchronize(); 
   for(int i=0; i<N; i++)        printf("%d: Vett*Vett = %d\n", i, Vett[i]); 
   return  0;
 }
