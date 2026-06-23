#include <iostream>

using namespace std;

int main() {
	int n, somma = 0, i = 0;
	do {
		cout << "Inserisci quanti numeri seguenti vuoi sommare" << endl;
		cin >> n;
	} while (n < 1);
	
	do {
		if (i <= n)
			somma = somma + i + (i - 1);
		i++;
	} while (i <= n);
	cout << "La somma dei numeri con il metodo Fibonacci e' " << somma << endl;

	return 0;
}

