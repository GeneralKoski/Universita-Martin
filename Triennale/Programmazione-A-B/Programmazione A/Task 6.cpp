#include <iostream>
#include <cstring>
#include <cctype>
using namespace std;

separa (char S[100], char alpha[100], char num[100], int &ca, int &cn) {
	for (int i = 0; S[i] != '\0'; i++) {
		if (isalpha(S[i])) {
			alpha[ca] = S[i];
			ca++;
		} else if (isdigit(S[i])) {
			num[cn] = S[i];
			cn++;
		}
	}	
}

int main() {
	char str[100], SAlpha[100], SNum[100];
	int ca = 0, cn = 0;
	cout << "Inserisci la stringa alfanumerica " << endl;
	cin.getline(str, 100);
	separa(str, SAlpha, SNum, ca, cn);
	cout << "Le lettere sono " << ca << ": ";
	if (ca == 0)
		cout << "Non ci sono lettere!";
	for (int i = 0; i < ca; i++)
		cout << SAlpha[i];
	cout << endl;
	cout << "I numeri sono " << cn << ": ";
	if (cn == 0)
			cout << "Non ci sono numeri!";
	for (int i = 0; i < cn; i++)
		cout << SNum[i];
			
	return 0;
}
