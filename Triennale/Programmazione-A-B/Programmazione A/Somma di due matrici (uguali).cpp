#include <iostream>

using namespace std;

int main() {
	int m, n;
	
	cout << "Inserire il numero di righe: ";
	cin >> m;
	
	cout << "Inserire il numero di colonne: ";
	cin >> n;

	int a[m][n];
	int b[m][n];
	
	for (int i = 0; i < m; i++)
		for (int j = 0; j < n; j++) {
				cout << "Matrice a: inserisci il valore della cella in posizione " << i << "-" << j << ": ";
				cin >> a[i][j];
			}
	
	for (int i = 0; i < m; i++)
		for (int j = 0; j < n; j++) {
				cout << "Matrice b: inserisci il valore della cella in posizione " << i << "-" << j << ": ";
				cin >> b[i][j];
			}
			
	int r[m][n];
	
	
	for (int i = 0; i < m; i++) {
		for (int j = 0; j < n; j++){
			r[i][j] = a[i][j] + b[i][j];
			cout << r[i][j];
		}
		cout << endl;
	}
	
	return 0;
}

