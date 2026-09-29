#include <stdio.h>
#include <stdlib.h>


int clause_count(int n){
  int p=n + 2*n*n*(n-1)/2;
  for(int i=0; i < n; i++)
    for(int j=0; j < n; j++)
      for(int k=1; k < n; k++){
	if (i+k < n && j+k < n)p++;
	if(i+k < n && j-k >=0)p++;
      }
  return p;
}

int main ( int arg, char* args[] ){

  if (arg!=2) {
    printf("Usage: %s number_of_queens\n",args[0]);
    printf("Ouput: cnf formula for number_of_queens problem\n");
    return 1;
  }

  int n = atoi(args[1]);
  int vars=n*n;
  int clauses=clause_count(n);

  printf("c SAT encoding of the %d queens problem\n",n);
  printf("c To uderstand variable meaning, just write 1..%d in the top row, %d+1 ..2*%d in the second and so on\n",n,n,n);
  printf("p cnf %d %d\n", vars, clauses);

  printf("c at least one in a row is true \n");

  for(int i=0; i < n; i++){
    for(int j=0; j < n; j++)
      printf("%d ",n*i+j+1);
    printf(" 0 \n");
        }

  printf("c At most one in a row \n");

  for(int i=0; i < n; i++)
    for(int j=0; j < n-1; j++)
        for(int k=j+1; k < n; k++)
	  printf("%d %d 0 \n",-(n*i+j+1),-(n*i+k+1));

  printf("c At most one in a column \n");

  for(int i=0; i < n; i++)
    for(int j=0; j < n-1; j++)
        for(int k=j+1; k < n; k++)
	  printf("%d %d 0 \n",-(n*j+i+1),-(n*k+i+1));


  printf("c No two queens in the same diagonal \n");


  for(int i=0; i < n; i++)
    for(int j=0; j < n; j++)
      for(int k=1; k < n; k++){
	// starting=n*i+j+1
        // attacked=n*(i+k)+(j+/-k)+1
	if(i+k < n && j+k < n)
	  printf("%d %d 0 \n",-(n*i+j+1),-(n*(i+k)+j+k+1));
	if(i+k < n && j-k >=0)
	  printf("%d %d 0 \n",-(n*i+j+1),-(n*(i+k)+j-k+1));
      }

  return 1;
}
