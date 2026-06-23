/*
module load gnu openmpi
mpicc mpi_factorize_todo.c   -lcrypto -lm

mpirun -n 1  a.out  -m B81915BC0A2222F4B   -a 4    # modulus 68 bit - prime 34 bit (4 addr + 28 block)
*/

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/bn.h>
#include <math.h>
#include <mpi.h>

void status() {}
void options(int argc, char * argv[]) ;
void usage(char * argv[]);
int block_factorize (unsigned long int);

BIGNUM *P, *Q, *M, *F, *ZERO,  *ONE, *TWO, *BLOCK_DIM_SIZE, *BLOCK_DIM_BIT ;
BN_CTX *ctx;
int block_idx=0, block_found;
unsigned long int  modulus_bit, prime_bit, block_addr_bit,  block_addr_size ,  block_dim_bit , block_dim_size;
char m[256];  // modulus


// variables required by MPI
int MPIrank=0, MPIsize=1;
int block_addr_size_global, flag;


int main(int argc, char *argv[])
{
    int i;
    float t1, t2, t3, t4;  // timer
    int received_msg;

// BN setting
    P = BN_new();     // prime number
    Q = BN_new();     // prime number
    M = BN_new();     // modulw = p x q
    F = BN_new();     // found number
    ZERO           = BN_new();  //  0
    ONE            = BN_new();  //  1
    TWO            = BN_new();  //  2
    BLOCK_DIM_BIT  = BN_new();  // quanti bit per blocco
    BLOCK_DIM_SIZE = BN_new();  // dimensione blocco
    ctx = BN_CTX_new();
    BN_set_word(ZERO,0);
    BN_set_word(ONE,1);
    BN_set_word(TWO,2);


// Default values
    modulus_bit=64; // init modulus bits
    block_addr_bit  = 4;

// Options management
    options(argc, argv);

// MPI init
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &MPIrank);
    MPI_Comm_size(MPI_COMM_WORLD, &MPIsize);
    MPI_Request request;
    MPI_Status status;


// Domain decomposition
    block_addr_size_global = pow(2,block_addr_bit);
    block_addr_size = block_addr_size_global/MPIsize;

    BN_hex2bn(&M, m);
    modulus_bit     = strlen(m)*4;
    prime_bit       = modulus_bit/2;
    block_dim_bit   = prime_bit - block_addr_bit;
    block_dim_size  = pow(2,block_dim_bit);

    BN_set_word(BLOCK_DIM_BIT,block_dim_bit);                 // bits per blocks
    BN_exp(BLOCK_DIM_SIZE, TWO , BLOCK_DIM_BIT,ctx);

    if (MPIrank==0)
    {
        printf("\n# Modulus: ");
        BN_print_fp(stdout,M);
        printf(" %d bits - prime %d bit: address %d bit, block %d bit \n\n", modulus_bit, prime_bit, block_addr_bit, block_dim_bit );
    }

    int lastBlock=block_addr_size*(MPIrank+1)-1;
    int firstBlock=block_addr_size*MPIrank;
    usleep(MPIrank*100);
    printf("Task %d/%d - block Address size %d, range %d-%d \n", MPIrank, MPIsize , block_addr_size, firstBlock, lastBlock );
    MPI_Barrier(MPI_COMM_WORLD);

// Attiva la Ricezione della comunicazione dagli altri rank
    MPI_Irecv(&received_msg, 1, MPI_INT, MPI_ANY_SOURCE, 0, MPI_COMM_WORLD, &request);

    t1=MPI_Wtime();

    for (block_idx=lastBlock; block_idx >= firstBlock ; block_idx--) {
// Verifica se  e' arrivato un messaggio. Se arrivato esci
        MPI_Test(&request, &flag, &status);
        if (flag)
            break; // Message received

        t2 = MPI_Wtime();
        printf("Task %d/%d - block %d processing  \n", MPIrank, MPIsize, block_idx);
        fflush(stdout);
        if (block_factorize(block_idx)) {

            // Invia un messaggio a tutti i task (TODO)
            // Send a message to all tasks
            for (int j = 0; j < MPIsize; ++j) {
                if(j != MPIrank)
                    MPI_Send(&block_idx, 1, MPI_INT, j, 0, MPI_COMM_WORLD);
            }


        t3 = MPI_Wtime();
        printf("Task %d/%d - block %d - FOUND: ", MPIrank, MPIsize, block_idx);
        BN_print_fp(stdout, F);
        printf(" %.1f sec. \n", t3 - t2);
        break;
    }else
        {
            t3=MPI_Wtime();
            printf("Task %d/%d - block %d - NOT found - %.1f sec.\n",  MPIrank, MPIsize, block_idx, t3-t2);
        }
    }

    t4=MPI_Wtime();
    printf("Task %d/%d  exiting,  time %.1f sec.  \n",  MPIrank, MPIsize, t4-t1);

    MPI_Finalize();
    return (0);
}


int block_factorize (unsigned long int block_addr)
{

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
    BN_mul(X, BLOCK_ADDR, BLOCK_DIM_SIZE,ctx2);  // x = i  block_size
    BN_add(X,X,ONE);                             // x = x+1
    BN_add(Y,X,BLOCK_DIM_SIZE);                  // y = x + block_size
    BN_sub(Y,Y,TWO);                             // y = y - 2
    BLOCK_IDX=BN_dup(X);

    while ( BN_cmp(BLOCK_IDX,Y) )
    {
        BN_add(BLOCK_IDX,BLOCK_IDX,TWO);
        BN_mod(R,M,BLOCK_IDX, ctx2);
        if ( BN_is_zero(R) )
        {
            F=BN_dup(BLOCK_IDX);
            return (1); // FOUND
        }
    }

    return (0);  // NOT FOUND
}

/************************************************/

void options(int argc, char * argv[])
{
    int i;
    while ( (i = getopt(argc, argv, "a:b:m:h")) != -1) {
        switch (i)
        {
            case 'a':  block_addr_bit = strtol(optarg, NULL, 10);  break;
            case 'b':  modulus_bit  = strtol(optarg, NULL, 10);  break;
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
    printf ("\n%s [-b modulus_bit] [-m modulus] [-a block_addr_bit] [-h]",argv[0]);
    printf ("\n");
}

