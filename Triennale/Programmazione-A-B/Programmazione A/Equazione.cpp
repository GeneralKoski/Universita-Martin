//Data l’equazione ax + b = 0, scrivere un programma in C++ per determinare il valore di x, se esiste, che risolve l'equazione (a e b devono essere inseriti dall'utente)

#include <iostream>

using namespace std;

int main() {
	float a, b, x;
	cout << "Inserisci il valori di A e B nell'equazione di ax + b = 0 " << endl;
	cin >> a >> b;
	if (a == 0)
	{
		cout << "Impossibile determinare la x " << endl;
	}
	else
	{
		x = -b/a;
		cout << "Il valore della x e' pari a " <<  x << endl;
	}
	
	return 0;
}
