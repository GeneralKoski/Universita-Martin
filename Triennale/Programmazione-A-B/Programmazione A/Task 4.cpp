#include <iostream>
#include <cstring>

using namespace std;
#define MAX_LENGTH 100

int main() {
  char a[MAX_LENGTH];
  char b[MAX_LENGTH];
  
  cout << "Per chiudere il programma scrivere 'exit'" << endl;
  while (true) {
  	int C = 0;
    cout << "Inserisci la prima parola: ";
    cin.getline(a, MAX_LENGTH);
    if (a[0] == 'e' && a[1] == 'x' && a[2] == 'i' && a[3] == 't')
		break;
    cout << "Inserisci la seconda parola: ";
    cin.getline(b, MAX_LENGTH);
    if (b[0] == 'e' && b[1] == 'x' && b[2] == 'i' && b[3] == 't')
    	break;
    
    if (strcmp(a, b) == 0) {
    	cout << "Le due parole sono uguali." << endl;
    	cout << "Reverse: ";
    	for (int i = strlen(a) - 1; i >= 0; i--)
        cout << a[i];
    	cout << endl;
    } else if (strlen(a) < strlen(b)) {
	    	for (int i = 0; i < strlen(a); i++) 
	    		if (a[i] == b[i])
	        		C++;
	    	if (C == strlen(a))
	    	cout << "La parola " << a << " e' il prefisso della parola " << b << endl;
	      
	    	C = 0;
	    	int j = strlen(b) - 1;
	      
	    	for (int i = strlen(a) - 1; i >= 0; i--)
	    	if (a[i] == b[j]) {
	        	C++;
	        	j--;
	        }
	      
	    	if (C == strlen(a))
	        cout << "La parola " << a << " e' il suffisso della parola " << b << endl;
		} else if (strlen(a) > strlen (b)) {
			C = 0;
			for (int i = 0; i < strlen(b); i++) {
				if (a[i] == b[i])
					C++;
			}
			
			if (C == strlen(b))
				cout << "La parola " << b << " e' il prefisso della parola " << a << endl;
			C = 0;
			int j = strlen(a) - 1;
			
			for (int i = strlen(b) - 1; i >= 0; i--) 
				if (a[j] == b[i]) {
					C++;
					j--;
				}
			if (C == strlen(b))
				cout << "La parola " << b << " e' il suffisso della parola " << a << endl;
		}
    }
    cout << "Addio!" << endl;
    
    return 0;  
}
