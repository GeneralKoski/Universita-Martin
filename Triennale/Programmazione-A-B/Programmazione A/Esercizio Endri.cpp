#include <iostream>
#include <cstring>
#include <cmath>

using namespace std;

int Funzione(int n, int k, int t) {
    int s = n/pow(10, k);
    t = t + n/pow(10, k);
    n = n - s * pow(10,k);
    k--;
    if (n >= 10) {
        Funzione(n, k, t);
    } else {
		t = t + n;
		return t;
	}
}

int main() {
    int n = 0, k = 0, t = 0;
    cout << "Inserisci il numero" << endl;
    cin >> n;
    int l = n;
    if (n >= 10) {
        while (l >= 10) {
            l = l/10;
            k++;
        }
    }
    cout << "il risultato e' " << Funzione(n, k, t) << endl;

    return 0;
}
