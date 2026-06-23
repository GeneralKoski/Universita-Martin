#include <iostream>
#include <windows.h>
using namespace std;

#define dimensione 1000

int main(){
    int numero=0;
    int variabili = 0;
    int c = dimensione - 1;
    bool esistente;
    int *A[dimensione];

    cout << "Inserisci una sequenza di numeri interi positivi (Per chiudere inserisci un numero negativo)" << endl;

    do {
        cout << "Inserisci un numero: ";
        cin >> numero;

        if (numero < 0) {
            break;
        }

        for (int i = dimensione - 1; i > c; i--) {
            if (*A[i] == numero) {
                esistente = true;
                break;
            }
        }

        if (!esistente) {
            A[variabili] = new int(numero);
            A[c] = A[variabili];
            variabili++;
        }else {
            for (int i = dimensione - 1; i > c; i--) {
                if (*A[i] == numero) {
                    A[c] = A[i];
                    break;
                }
            }
        }

        esistente = false;
        c--;

    } while(true);

    system("cls");
    
    if (variabili == 0)
    	cout << "Non sono state allocate variabili!" << endl;
    else if (variabili == 1) {
    	cout << "E' stata allocata " << variabili << " variabile" << endl;
		cout << "Sequenza: ";
	}
   	else {
    	cout << "Sono state allocate " << variabili << " variabili" << endl;
		cout << "Sequenza: ";
	}

    for (int j = dimensione - 1; j > c; j--)
        cout << *A[j] << " ";
    
	cout << endl;

    for (int j = 0; j < variabili; j++)
        delete A[j];
    
    cout << endl;
    return 0;
}
