#include <iostream>
#include <cstring>

using namespace std;

struct rubrica {
	char nome [50];
	char cognome [50];
	char numero [11];
};

int main() {
	int i = 0, k = 0;
	char scelta;
	
	rubrica contatto[100];
	
	cout << "*** Rubrica ***" << endl;
	do {
		cout << "1 - Visualizza rubrica" << endl;
		cout << "2 - Inserisci contatto" << endl;
		cout << "3 - Cancella contatto" << endl;
		cout << "4 - Esci" << endl;
		cin >> scelta;
		
		if (scelta < '1' || scelta > '4')
			cout << "Errore!" << endl;
		else {
			cin.ignore();
			switch (scelta) {
				case '1':
					if (k == 0) {
						cout << "Rubrica vuota!" << endl;
					} else {
						for (i = 0; i < k; i++) {
							if (contatto[i].nome[0] == '\0' ) {
								continue;
							} else {
								cout << contatto[i].nome << " ";
								cout << contatto[i].cognome << " ";
								cout << contatto[i].numero << " " << endl;
							}
						}
					}
					break;
				case '2':
					cout << "Inserisci il nome del contatto da aggiungere: ";
					cin.getline(contatto[i].nome, 50);
					cout << "Inserisci il cognome del contatto da aggiungere: ";
					cin.getline(contatto[i].cognome, 50);
					
					do {	
						cout << "Inserisci il numero del contatto da aggiungere: ";
						cin.getline(contatto[i].numero, 11);
						
						if (strlen(contatto[i].numero) < 10)
							cout << "Il numero e' troppo corto, mettine uno italiano (da 10 numeri)!" << endl;
					} while (strlen(contatto[i].numero) < 10);
				
					cout << "Contatto aggiunto!" << endl;
					cout << endl;
					i++;
					k++;
					break;
				case '3':
					rubrica controllo[2];
					cout << "Inserisci il nome del contatto da cancellare: ";
					cin.getline(controllo[0].nome, 50);
					cout << "Inserisci il cognome del contatto da cancellare: ";
					cin.getline(controllo[0].cognome, 50);
					for (i = 0; i < k; i++) {
						if (strcmp(controllo[0].nome, contatto[i].nome) == 0 && strcmp(controllo[0].cognome, contatto[i].cognome) == 0) {
							contatto[i] = controllo[1];
							cout << "Contatto cancellato!" << endl;
						}
					}
					cout << endl;
					break;
				case '4':
					cout << "Addio!";
					break;
			}
		}
	} while (scelta != '4');
	return 0;
}

