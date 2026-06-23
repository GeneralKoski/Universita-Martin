#include <iostream>
using namespace std;

void inverti (int a[], int puntatore, int l) {
    if (puntatore < l) {
        int m = a[l - 1];
        a[l - 1] = a[puntatore];
        a[puntatore] = m;

        inverti(a, puntatore + 1, l - 1);
    }
}

int main() {
    int lunghezza = 0, n = 0;
    
	do {
    	cout << "Inserire la lunghezza: ";
    	cin >> lunghezza;
    	if (lunghezza <= 0)
    		cout << "L'array deve essere lungo almeno 1!!!" << endl;
	} while (lunghezza <= 0);	
	
	int numeri[lunghezza];
	
	cout << "Inserisci gli elementi:" << endl;
    for(int i = 0; i < lunghezza; i++) {
        cin >> n;
        numeri[i] = n;
    }
	
	cout << "I numeri sono: 		";
    for(int i = 0; i < lunghezza; i++)
   		 cout << numeri[i] << " ";
    cout << endl;
    
    inverti(numeri, 0, lunghezza);
	cout << "I numeri inveriti sono: ";
    for(int i = 0; i < lunghezza; i++)
    	cout << numeri[i] << " ";

    return 0;
}
