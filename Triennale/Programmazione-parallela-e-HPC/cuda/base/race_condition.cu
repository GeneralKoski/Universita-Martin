#include<stdio.h>

__global__ void increment(int *a_d) {
*a_d +=1; 
//atomicAdd(a_d, 1); 
}

int main(){

int a=0, *a_d;  
cudaMalloc((void**)&a_d, sizeof(int));
cudaMemcpy(a_d, &a, sizeof(int), cudaMemcpyHostToDevice); 
float elapsedTime; 

cudaEvent_t start , stop; 
cudaEventCreate(&start);
cudaEventCreate(&stop);
cudaEventRecord( start , 0 ); 
increment<<<100,100>>>(a_d);
cudaEventRecord( stop, 0 ); 
cudaEventSynchronize( stop );
cudaEventElapsedTime( &elapsedTime , start , stop ); 
cudaEventDestroy( start ); 
cudaEventDestroy( stop ); 

 printf("GPUTime elapsed: %f seconds\n", elapsedTime/1000.0); 
 cudaMemcpy(&a, a_d, sizeof(int), cudaMemcpyDeviceToHost); 
 printf("a=%d\n", a);
 cudaFree(a_d); 
}

