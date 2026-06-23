#include <iostream>
#include <cstring>

using namespace std;
#define MAX_LENGTH 100

int main() {
	char a[MAX_LENGTH];
	char b[MAX_LENGTH];
	int continuo = 1;
	
	cout << "Scrivi $ per chiudere il programma" << endl;
	
	do {	
		cout << "Inserisci la stringa a: ";
		cin.getline(a, MAX_LENGTH + 1);
		if (a[0] == '$')
			break;
		cout << "Inserisci la stringa b: ";
		cin.getline(b, MAX_LENGTH + 1);
		if (b[0] == '$')
			break;
		
		if (strcmp(a, b) == 0) {
			cout << "Reverse: ";
			for (int i = strlen(a) - 1; i >= 0; i--)
				cout << a[i];
			cout << endl;
		}
			
		if (strcmp(a, b) < 0)
			cout << "La parola " << a << " e' prefisso di " << b << endl;
		
		if (strcmp(a, b) > 0)
			cout << "La parola " << b << " e' prefisso di " << a << endl;	

	} while (continuo == 1);
	
	return 0;
}

