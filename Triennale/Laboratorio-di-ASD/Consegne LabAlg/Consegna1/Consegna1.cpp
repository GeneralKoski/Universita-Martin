/* 
Trajkovski Martin 335566
Montinaro Davide 331881
*/

#include <fstream>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <vector>
using namespace std;

int ct_swap = 0;
int ct_cmp = 0;
int ct_read = 0;

int max_dim = 0; 
int ntests = 100;
int ndiv = 1;
int details = 0;
int graph = 0;

int n = 0;

void print_array(int *A, int dim) {
    for (int j = 0; j < dim; j++) {
        printf("%d ", A[j]);
    }
    printf("\n");
}

void swap(int &a, int &b) {
    int tmp = a;
    a = b;
    b = tmp;
    ct_swap++;
}

void shellSort(int* arr, int length) {
    for (int gap = length / 2; gap > 0; gap /= 2)
    {
        for (int i = gap; i < length; i++)
        {
            int temp = arr[i];
			ct_read++;
            int j;

            for (j = i; j >= gap && arr[j - gap] > temp; j -= gap)
            {
                swap(arr[j], arr[j - gap]); 
				ct_read+=3; 
            }
            arr[j] = temp;
        }
    }
}

int parse_cmd(int argc, char **argv) {


    max_dim = 1000;

    for (int i = 1; i < argc; i++) {
        if (argv[i][1] == 'd')
            ndiv = atoi(argv[i] + 3);
        if (argv[i][1] == 't')
            ntests = atoi(argv[i] + 3);
        if (argv[i][1] == 'v')
            details = 1;
        if (argv[i][1] == 'g') {
            graph = 1;
            ndiv = 1;
            ntests = 1;
        }
    }

    return 0;
}

int main(int argc, char **argv)
{
    int i, test;
    int *A;
	
	cout << argv[1] << endl;

    if (parse_cmd(argc, argv)) 
        return 1;
   
    A = new int[max_dim];
    n = max_dim;

    ifstream input_data;
    input_data.open("data.txt"); 
	
	if (!input_data.is_open())
	{
		cerr << "Errore nell'apertura del file di input." << endl;
		return 1;
	}
	
	ofstream output_file;
	output_file.open("Consegna1.txt");
	
	if (!output_file.is_open())
	{
		cerr << "Errore nell'apertura del file di output." << endl;
		return 1;
	}

    int read_min = -1;
    int read_max = -1;
    long read_avg = 0;

    for (test = 0; test < ntests; test++)
	{
        for (i = 0; i < n; i++)
		{
            char comma;
            input_data >> A[i];
            input_data >> comma;
        }

        if (details)
		{
            printf("caricato array di dimensione %d\n", n);
            print_array(A, n);
        }

        ct_swap = 0;
        ct_cmp = 0;
        ct_read = 0; 

        shellSort(A,n); 
		
        if (details) 
		{
            printf("Output:\n");
            print_array(A, n);
        }
       
        read_avg += ct_read; 
        if (read_min < 0 || ct_read < read_min) 
            read_min = ct_read;
        if (read_max < 0 || ct_read > read_max) 
            read_max = ct_read;
		
        printf("Test %d %d\n", test, ct_read);
		output_file << "Test " << test << " " << ct_read << endl;
    }
           
    printf("Letture - Caso migliore: %d \n", read_min);
	printf("Letture - Caso medio: %.1f \n", (0.0 + read_avg) / ntests); 
	printf("Letture - Caso peggiore: %d \n", read_max);
	
	output_file << "Letture - Caso migliore: " << read_min << endl;
	output_file << "Letture - Caso medio: " << (0.0 + read_avg) / ntests << endl;
	output_file << "Letture - Caso peggiore: " << read_max << endl;
	
	cout << endl;
	
    delete[] A;
	output_file.close();
	
    return 0;
}
