 
//l'array float a[16] viene copiato sulla GPU che somma gli elementi e ritorna il risultato in c 
   

#include<stdio.h>
#define MAX 16


__global__ void sum(float *a_d, float *c_d) {

__shared__ float a_s[MAX];  // shared 
a_s[threadIdx.x]=a_d[threadIdx.x]; 
 
//c_d += a_s[threadIdx.x]; //?? 

 int i = MAX/2;
   while (i != 0) {
         if (threadIdx.x < i)
         a_s[threadIdx.x] += a_s[threadIdx.x + i];
         __syncthreads();
         i /= 2;
   }

if  (threadIdx.x==0) for (int i=0; i<MAX; i++) printf ("a_s:%.1f ", a_s[i]); printf("\n"); 

  *c_d=a_s[0];
}

int main(){

float a[MAX], c; 
float *a_d, *c_d;   
for (int i=0; i<MAX; i++) a[i]=1000; 
cudaMalloc((void**)&a_d, MAX * sizeof(float));  // global
cudaMalloc((void**)&c_d,       sizeof(float));  // global
cudaMemcpy(a_d, a, sizeof(float)*MAX , cudaMemcpyHostToDevice); 

sum<<<1,MAX>>>(a_d, c_d);

 cudaMemcpy(&c, c_d, sizeof(float), cudaMemcpyDeviceToHost); 
 printf("c=%.1f\n", c);

 cudaFree(a_d); 
 cudaFree(c_d); 
}

