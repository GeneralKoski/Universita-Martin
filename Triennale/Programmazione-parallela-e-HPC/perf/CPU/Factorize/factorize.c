/* gcc factorize.c -o factorize   -lcrypto -lm */

/*
Generare il modulo (ad esempio di 68 bit) utilizzando genrsa di openssl: 
openssl genrsa -out rsa_key.pem 68
openssl rsa -in rsa_key.pem -modulus -noout

time ./factorize -m B81915BC0A2222F4B  -a 4    # modulus 68 bit - prime 34 bit (4 addr + 30 block) 
*/

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/bn.h>
#include <time.h>
#include <math.h>

#define BILLION  1000000000L;

void status() {}
void options(int argc, char * argv[]) ;
void usage(char * argv[]);
int block_factorize (unsigned long int);

BIGNUM *P, *Q, *M, *F, *ZERO,  *ONE, *TWO, *BLOCK_DIM_SIZE, *BLOCK_DIM_BIT ;
BN_CTX *ctx;
int block_idx=0, found=0, skip=0;
unsigned long int  modulus_bit, prime_bit, block_addr_bit,  block_addr_size ,  block_dim_bit , block_dim_size; 
char m[256];  // modulus


int main(int argc, char *argv[])
{

//double t1, t2; // timer

    P = BN_new();     // prime number
    Q = BN_new();     // prime number
    M = BN_new();     // modulw = p x q
    F = BN_new();     // found number

    ZERO           = BN_new();  //  0
    BN_set_word(ZERO,0);
    ONE            = BN_new();  //  1
    BN_set_word(ONE,1);
    TWO            = BN_new();  //  2
    BN_set_word(TWO,2);
    BLOCK_DIM_BIT  = BN_new();  // quanti bit per blocco
    BLOCK_DIM_SIZE = BN_new();  // dimensione blocco
    ctx = BN_CTX_new();

//    modulus_bit=64; // init modulus bits
    block_addr_bit  = 4;

    options(argc, argv);
    if (argc < 3) { usage(argv); exit (1); } // Modulus is mandatory

    modulus_bit     = strlen(m)*4;
    BN_hex2bn(&M, m);

    block_addr_size = pow(2,block_addr_bit);
    prime_bit       = modulus_bit/2;

    block_dim_bit   = prime_bit - block_addr_bit;    // bits per block
    BN_set_word(BLOCK_DIM_BIT,block_dim_bit);            
//    BN_print_fp(stdout,BLOCK_DIM_BIT);

    block_dim_size  = pow(2,block_dim_bit);           // block size
    BN_exp(BLOCK_DIM_SIZE, TWO , BLOCK_DIM_BIT,ctx);
      
    printf("\n# Modulus: ");
    BN_print_fp(stdout,M);

    printf(" %d bits - prime: address %d bit, block %d bit \n\n", modulus_bit, block_addr_bit, block_dim_bit );

    for (block_idx=block_addr_size-1; block_idx > -1 ; block_idx--)
         block_factorize (block_idx);

    printf("FOUND: ");
    BN_print_fp(stdout,F);
    printf("\n");
    return (0);
}


int block_factorize (unsigned long int block_addr)
{

           struct timespec start, stop;
           double time;

              BIGNUM *R, *X, *Y, *BLOCK_IDX, *BLOCK_ADDR;
              BN_CTX *ctx2;
              ctx2 = BN_CTX_new();
              R       = BN_new();  // resto della divisione
              X       = BN_new();  // indice del  blocco
              Y       = BN_new();  // ultimo numero del  blocco
              BLOCK_IDX       = BN_new();  // ultimo numero del  blocco
              BLOCK_ADDR      = BN_new();  // Block Address

              BN_set_word(R,0);
              BN_set_word(X,1);
              BN_set_word(Y,1);
              BN_set_word(BLOCK_ADDR, block_addr);
              BN_mul(X, BLOCK_ADDR, BLOCK_DIM_SIZE,ctx2);   // x = i  block_size
              BN_add(X,X,ONE);                             // x = x+1 
              BN_add(Y,X,BLOCK_DIM_SIZE);                      // y = x + block_size
              BN_sub(Y,Y,TWO);                             // y = y - 2
              BLOCK_IDX=BN_dup(X);

              printf("Processing block %d \n", block_addr);

             clock_gettime( CLOCK_REALTIME ,          &start) ;

              while ( ! skip  && BN_cmp(BLOCK_IDX,Y))
                {
                BN_add(BLOCK_IDX,BLOCK_IDX,TWO);
                BN_mod(R,M,BLOCK_IDX, ctx2);
                if ( BN_is_zero(R) ) 
                  { 
                    F=BN_dup(BLOCK_IDX);
                    found=1;
                    skip=1;
                  }  
               }
              clock_gettime( CLOCK_REALTIME ,          &stop) ;

             time = (double) ( stop.tv_sec - start.tv_sec )
                 + (double) ( stop.tv_nsec - start.tv_nsec ) / BILLION; 


              printf(" Blk:");
              BN_print_fp(stdout,BLOCK_ADDR);
              printf(" ");
              BN_print_fp(stdout, X);
              printf("-");
              BN_print_fp(stdout, Y);
                printf(" %.2f sec.  ", time);
             if (found) {  printf (" FOUND \n");  found=0;}
              else if (skip)  printf (" skip \n"); 
              else printf (" not found \n");

              return (0);
             
}

/************************************************/
  
void options(int argc, char * argv[])
{
  int i;
   while ( (i = getopt(argc, argv, "a:m:h")) != -1) {
        switch (i)
        {
        case 'a':  block_addr_bit = strtol(optarg, NULL, 10);  break;
        case 'm':  strcpy(m,optarg);  break;
        case 'h':  usage(argv); exit(1);
        case '?':  usage(argv); exit(1);
        default:   usage(argv); exit(1);
        }
    }
}

/***************************************/

void usage(char * argv[])
{
  printf ("\n%s -m modulus [-a block_addr_bit] [-h]\n",argv[0]);

  printf ("\n Per generare il modulo:"); 
  printf ("\n openssl genrsa -out rsa_key.pem 68");
  printf ("\n openssl rsa -in rsa_key.pem -modulus -noout"); 
  printf ("\n Esempio: ./factorize -m 9FAEEDA86CC433891 \n"); 
  printf ("\n");	
}
