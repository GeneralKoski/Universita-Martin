/*
mpi_heat.h
*/


/***********************************/
/* JACOBI ITERATION FUNCTION - CPU */
/***********************************/
void Jacobi_Iterator_CPU(float * __restrict T, float * __restrict T_new, const int NX, const int NY)
{
    int i,j;

    // --- Only update "interior" (not boundary) node points
    for(j=1; j<NY-1; j++)
        for(i=1; i<NX-1; i++) {
            float T_E = T[(i+1) + NX*j];
            float T_W = T[(i-1) + NX*j];
            float T_N = T[i + NX*(j+1)];
            float T_S = T[i + NX*(j-1)];
            T_new[NX*j + i] = 0.25*(T_E + T_W + T_N + T_S);
        }
}

/***********************************/
/* JACOBI ITERATION ITERNAL FUNCTION - CPU */
/***********************************/
void Jacobi_Iterator_CPU_internal(float * __restrict T, float * __restrict T_new, const int NX, const int NY)
{
    int i,j;

    // --- Righe dalla 2 alla penultima
    for(j=2; j<NY-2; j++)
        for(i=1; i<NX-1; i++) {
            float T_E = T[(i+1) + NX*j];
            float T_W = T[(i-1) + NX*j];
            float T_N = T[i + NX*(j+1)];
            float T_S = T[i + NX*(j-1)];
            T_new[NX*j + i] = 0.25*(T_E + T_W + T_N + T_S);
        }
}

/***********************************/
/* JACOBI ITERATION ITERNAL FUNCTION - CPU */
/***********************************/
void Jacobi_Iterator_CPU_external(float * __restrict T, float * __restrict T_new, const int NX, const int NY)
{
    int i,j;

    j=1;  // prima riga
    for(i=1; i<NX-1; i++) {
        float T_E = T[(i+1) + NX*j];
        float T_W = T[(i-1) + NX*j];
        float T_N = T[i + NX*(j+1)];
        float T_S = T[i + NX*(j-1)];
        T_new[NX*j + i] = 0.25*(T_E + T_W + T_N + T_S);
    }

    j=NY-2;  // ultima riga
    for(i=1; i<NX-1; i++) {
        float T_E = T[(i+1) + NX*j];
        float T_W = T[(i-1) + NX*j];
        float T_N = T[i + NX*(j+1)];
        float T_S = T[i + NX*(j-1)];
        T_new[NX*j + i] = 0.25*(T_E + T_W + T_N + T_S);
    }
}

/********************************/
/* TEMPERATURE INITIALIZATION : */
/* parte centrale della griglia */
/********************************/
void Init_center(float * __restrict h_T, const int NX, const int NY)
{
    int i,j;
    int startx=NX/2-NX/10;
    int endx=NX/2+NX/10;
    int starty=NY/2-NY/10;
    int endy=NY/2+NY/10;
//    int starty=NY/4;
//    int endy=NY-NY/4;
    for(i=startx; i<endx; i++)
        for(j=starty; j<endy; j++)
            h_T[NX*j + i] = 1.0;
}


/********************************/
/* TEMPERATURE INITIALIZATION : */
/* bordo sinistro               */
/********************************/
void Init_left(float * __restrict h_T, const int NX, const int NY)
{
    int i,j;
    int startx=1;
    int endx=2;
    int starty=0;
    int endy=NY-1;
    for(i=startx; i<endx; i++)
        for(j=starty; j<endy; j++)
            h_T[NX*j + i] = 1.0;
}

/********************************/
/* TEMPERATURE INITIALIZATION : */
/* bordo alto                   */
/********************************/
void Init_top(float * __restrict h_T, const int NX, const int NY)
{
    int i,j;
    int startx=0;
    int endx=NX-1;
    for(i=startx; i<endx; i++)
        h_T[NX + i] = 1.0;
}

/********************************/
/* Periodic boundary conditions */
/* COPY BORDER: COLS            */
/********************************/
void copy_cols (float * __restrict h_T, const int NX, const int NY)
{

    int i;

    // copy cols
    for (i = 1; i < NY-1; ++i) {
        h_T[NX*i+0]    = h_T[NX*i+NX-2];
        h_T[NX*i+NX-1] = h_T[NX*i+1];
    }
}


/********************************/
/* Periodic boundary conditions */
/* COPY BOREDER: ROWS           */
/********************************/
void copy_rows (float * __restrict h_T, const int NX, const int NY)
{

    memcpy(&(h_T[NX*0])      ,&(h_T[NX*(NY-2)]), NX*sizeof(float) );
    memcpy(&(h_T[NX*(NY-1)]) ,&(h_T[NX*1]),      NX*sizeof(float) );
}


/******************************************/
/* print color map                        */
/******************************************/

void print_colormap(float * __restrict h_T, int NX, int NY)
{
    int i,j;

    for (j=0; j<NY; j++){
        for (i=0; i<NX; i++) {
            printf("%2.2f ",h_T[NX*j + i]);
        }
        printf("\n");
    }
}

/******************************************/
/* save color map  to file                */
/******************************************/

void save_colormap(float * __restrict h_T,  const int NX, const int NY)
{
    int i,j;
    FILE *fp;
    fp=fopen("colormap.dat","wb");

    for (j=0; j<NY; j++) {
        for (i=0; i<NX; i++)
            fprintf(fp,"%f ",h_T[NX*j + i]);
        fprintf(fp, "\n");
    }
    fclose (fp);
    return;
}

/******************************************/
/* Load color map  from file              */
/******************************************/

void load_colormap(float * __restrict h_T,  const int NX, const int NY)
{
    int i,j;
    FILE *fp;
    fp=fopen("colormap.dat","r");

    for (j=0; j<NY; j++) {
        for (i=0; i<NX; i++) {
            fscanf(fp, "%f ", &h_T[NX*j + i]);
        }
    }

    fclose (fp);
    return;
}

/******************************************/
/* options management                     */
/******************************************/
void options(int argc, char * argv[]) {

    int i;
    while ( (i = getopt(argc, argv, "c:r:s:hlw")) != -1) {
        switch (i) {
            case 'c':  WNX       = strtol(optarg, NULL, 10);  break;
            case 'r':  WNY       = strtol(optarg, NULL, 10);  break;
            case 's':  MAX_ITER = strtol(optarg, NULL, 10);  break;
            case 'h':
            default:  printf ("\n%s [-c ncols] [-r nrows] [-s nsteps] [-l load] [-w write] [-h]\n",argv[0]); exit(1);
        }
    }
}
