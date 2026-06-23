// Scrivere un programma che legga in input degli interi positivi 
// (negativo per smettere) li inserisca in un set. Successivamente, il programma 
// dovrebbe stampare il numero di elementi distinti presenti nel set e gli elementi stessi.

#include <iostream>
#include <set>
using namespace std;

int main(){
    set<int> s;
    int n;
    cout << "Inserisci un numero intero positivo (negativo per smettere): ";
    cin >> n;
    while(n>=0){
        s.insert(n);
        cout << "Inserisci un numero intero positivo (negativo per smettere): ";
        cin >> n;
    }
    cout << "Il numero di elementi distinti presenti nel set è: " << s.size() << endl;
    cout << "Gli elementi distinti presenti nel set sono: ";
    for(auto i : s)
        cout << i << " ";
    cout << endl;
    return 0;
}