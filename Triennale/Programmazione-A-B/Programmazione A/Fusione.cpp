#include <iostream>

using namespace std;

int main() {
	int na, nb, nc, k = 0, j = 0;

	cout << "Quanti numeri vuoi inserire nell'array a? -- ";
	cin >> na;
	
	cout << "e nell'array b? -- ";
	cin >> nb;
	
	nc = na + nb;
	
	int a[na];
	int b[nb];
	int c[nc];
	
	cout << "Inserisci i numeri nell'array a: " << endl;
	do {
		cin >> a[k];
		k++;
	} while (k != na);
	k = 0;
	cout << "Inserisci i numeri nell'array b: " << endl;
	do {
		cin >> b[k];
		k++;
	} while (k != nb);
	k = 0;
	for (int i = 0; i < na; i++)
		c[i] = a[i];
		
	for (int i = na; i < nc; i++) {
		c[i] = b[k];
		k++;
	}
	
	for (int j = 0; j < nc; j++) {
		int i = 0;
		for (i = 0; i <= nc; i++) {
			if (i == nc) {
				continue;
			} else if (c[i] > c[i + 1]) {
				k = c[i];
				c[i] = c[i + 1];
				c[i + 1] = k;
			}
		}
	}
				
		
	for (int i = 0; i < nc; i++)
		cout << c[i];
	
	return 0;
}

