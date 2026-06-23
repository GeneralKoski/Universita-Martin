#include<stdio.h>

__managed__ int lock= 0, x=0; 

__global__ void kernel() {

// if (  threadIdx.x%32 == 0 )  // sincronismo tra wrap 
if (  threadIdx.x == 0 )        // sincronismo tra blocchi 
 {
    do {} while(atomicCAS(&lock, 0, 1));    // spin
    printf("Block %d thread %d entering critical section \n", blockIdx.x, threadIdx.x); 
    x+=1;  
   atomicExch(&lock, 0); // release lock
   } 
 }


int main(){

kernel<<<2,512>>>(); 
cudaDeviceSynchronize();

printf("finito: %d \n", x);
}

