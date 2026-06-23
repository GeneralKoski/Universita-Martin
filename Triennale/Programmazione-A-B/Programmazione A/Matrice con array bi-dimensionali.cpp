#include <iostream>

using namespace std;

int main() {
	int m, n;
	
	cout << "Inserire il numero di righe: ";
	cin >> m;
	
	cout << "Inserire il numero di colonne: ";
	cin >> n;

	int x[m][n];
	
	for (int i = 0; i < m; i++)
		for (int j = 0; j < n; j++)
			{
				cout << "inserisci il valore della cella in posizione " << i << "-" << j << ": ";
				cin >> x[i][j];
			}
			
	for (int i = 0; i < m; i++)
	{
		for (int j = 0; j < n; j++)
			cout << x[i][j];
		cout << endl;
	}
	


	return 0;
}

