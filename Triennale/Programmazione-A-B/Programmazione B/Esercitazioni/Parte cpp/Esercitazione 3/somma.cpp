// Scrivere una funzione template chiamata "somma" che prende in input un array di elementi di tipo generico e la sua lunghezza, e restituisce la somma di tutti gli elementi dell'array.
// Scrivere un main che testi la funzione

#include <iostream>
using namespace std;

template <typename T>
T somma(const T array[], const int lunghezza)
{
    T risultato = 0;
    for (int i = 0; i < lunghezza; i++)
    {
        risultato += array[i];
    }
    return risultato;
}

int main()
{
    int arrayInt[] = {1, 2, 3, 4, 5};
    cout << "La somma di 1, 2, 3, 4, 5 è: ";
    cout << somma(arrayInt, 5) << endl;
    double arrayDouble[] = {1.1, 2.2, 3.3, 4.4, 5.5};
    cout << "La somma di 1.1, 2.2, 3.3, 4.4, 5.5 è: ";
    cout << somma(arrayDouble, 5) << endl;
    return 0;
}