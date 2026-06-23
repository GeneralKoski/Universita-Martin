#include <iostream>
#include <cmath>

using namespace std;

int main() {
  int nBit, num, scelta;
  do{
    cout << "Inserisci il numero di bit della rappresentazione: ";
    cin >> nBit;
    if (nBit < 2)
      cout << "Errore, numero non valido!" << endl;
  } while (nBit < 2);
  
  int x[nBit];
  
  for (int i = nBit - 1; i >= 0; i--)
  {
    cout << "Inserisci il bit nella posizione " << i << ": ";
    cin >> num;
    
    if (num == 0 || num == 1)
    {
      x[i] = num;
    }
    else
    {
      cout << "Puoi inserire solo 0 o 1 nel numero binario!" << endl;
      i++;
    }
  }
  
  do {
  cout << "Scegli un'operazione: " << endl;
  cout << "-1: Chiudi programma" << endl;
  cout << "0: Stampa a video del numero binario" << endl;
  cout << "1: Stampa a video del decimale corrispondente al numero binario inserito" << endl;
  cout << "2: Stampa a video dell opposto del numero binario" << endl;
  cin >> scelta;
  if (scelta < -1 || scelta > 2)
    cout << "Errore!" << endl;
  } while (scelta < -1 || scelta > 2);
  
  int sum = 0;
  int i = nBit - 1;
  
  switch (scelta) {
    case -1:
      break;
    case 0:
      for (i; i >= 0; i--)
        cout << x[i];
      break;
    case 1:
      for (i; i >= 0; i--)
		do {
			sum += pow(2, i) * x[i];
			i--;
		} while (i >= 0);
        cout << sum;
      break;
    case 2:
      if (x[i] == 1)
      {
      	cout << "Overflow!" << endl;
	  }
	  else
	  {
	  	x[i] = 1;
	  	int j = 0;
	  	while (x[j] == 0)
		{
	  		x[j] = 0;
	  		j++;
		}
		
	  }
      break;
  }
  
  
  return 0;
}
