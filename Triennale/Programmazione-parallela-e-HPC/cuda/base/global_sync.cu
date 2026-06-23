#include<stdio.h>

__managed__ unsigned int lock; 

__global__ void kernel() {

printf("Block %d thread %d entering global sync \n", blockIdx.x, threadIdx.x); 

__syncthreads(); 
// syncblocks

printf("Block %d thread %d exiting global sync \n", blockIdx.x, threadIdx.x); 
 }


int main(){

int grid_size=8;
int block_size=8;

 
kernel<<<grid_size,block_size>>>(); 
cudaDeviceSynchronize();

printf("finito lock:%d \n", lock);
}

