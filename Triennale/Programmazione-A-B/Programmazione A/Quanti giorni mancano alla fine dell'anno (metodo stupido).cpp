#include <iostream>

using namespace std;

int main() {
	int giorno, mese, resto, anno = 365;
	do {
		cout << "Inserisci il giorno del mese" << endl;
		cin >> giorno;
	} while (giorno < 1 || giorno > 31);
	do {
		cout << "Inserisci il mese dell'anno" << endl;
		cin >> mese;
	} while (mese < 1 || mese > 12);
	
	switch (mese) {
		case 1:
			resto = anno - giorno;
			cout << "Rimangono " << resto << " giorni alla fine dell'anno";
			break;
		case 2:
			resto = anno - giorno - 31;
			cout << "Rimangono " << resto << " giorni alla fine dell'anno";
			break;
		case 3:
			resto = anno - giorno - 31 - 28;
			cout << "Rimangono " << resto << " giorni alla fine dell'anno";
			break;
		case 4:
			resto = anno - giorno - 31 - 28- 31;
			cout << "Rimangono " << resto << " giorni alla fine dell'anno";
			break;
		case 5:
			resto = anno - giorno - 31 - 28- 31 - 30;
			cout << "Rimangono " << resto << " giorni alla fine dell'anno";
			break;
		case 6:
			resto = anno - giorno - 31 - 28- 31 - 30 - 31;
			cout << "Rimangono " << resto << " giorni alla fine dell'anno";
			break;
		case 7:
			resto = anno - giorno - 31 - 28- 31 - 30 - 31 -30;
			cout << "Rimangono " << resto << " giorni alla fine dell'anno";
			break;
		case 8:
			resto = anno - giorno - 31 - 28- 31 - 30 - 31 -30 - 31;
			cout << "Rimangono " << resto << " giorni alla fine dell'anno";
			break;
		case 9:
			resto = anno - giorno - 31 - 28- 31 - 30 - 31 -30 - 31 - 31;
			cout << "Rimangono " << resto << " giorni alla fine dell'anno";
			break;
		case 10:
			resto = anno - giorno - 31 - 28- 31 - 30 - 31 -30 - 31 - 31 - 30;
			cout << "Rimangono " << resto << " giorni alla fine dell'anno";
			break;
		case 11:
			resto = anno - giorno - 31 - 28- 31 - 30 - 31 -30 - 31 - 31 - 30 - 31;
			cout << "Rimangono " << resto << " giorni alla fine dell'anno";
			break;
		case 12:
			resto = anno - giorno - 31 - 28- 31 - 30 - 31 -30 - 31 - 31 - 30 - 31 - 30;
			cout << "Rimangono " << resto << " giorni alla fine dell'anno";
			break;
	}
	
	return 0;
}
