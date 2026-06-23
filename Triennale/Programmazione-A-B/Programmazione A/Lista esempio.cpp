#include <iostream>

using namespace std;

struct elemento{
	int numero;
	elemento* next;
};

int main() {
	elemento* primo = new elemento;
	primo->numero = 21;
	primo->next = 0;
	
	elemento* temp = new elemento;
	temp->numero = 22;
	temp->next = 0;
	primo->next = temp;
	
	temp = new elemento;
	temp->numero = 23;
	temp->next = 0;
	primo->next->next = temp;

	temp = primo;
	while (temp>0) {
		cout << " Numero: " << temp->numero << endl;;
		temp = temp->next;
	}
	return 0;
}

