// Definire una classe MaterialeBibliotecario, che contiene i seguenti attributi: titolo, autore e anno.
// Dalla classe MaterialeBibliotecario devono essere derivate tre classi: Libro, Rivista e DVD. 
// Si implementi la classe Biblioteca, caratterizzata dagli attributi: un array di MaterialeBibliotecario contenente tutto il materiale presente nella biblioteca ed un intero che indica il numero di elementi presenti nell'array.
// La classe dovrà fornire i metodi aggiungiMateriale e rinuoviMateriale che lavorano su oggetti di tipo MaterialeBibliotecario, ed il metodo visualizzaMateriale che stampa tutti i materiali presenti nella blibioteca.
// Creare un main in cui si creano un libro, una rivista ed un dvd e aggiungerli alla biblioteca, stampare il contenuto, rimuovere il dvd e stampare nuovamente

#include <iostream>
#include <string>

using namespace std;

class MaterialeBibliotecario {
    protected:
        string titolo;
        string autore;
        int anno;
    public:
        MaterialeBibliotecario() {} // costruttore di default
        MaterialeBibliotecario(string titolo, string autore, int anno) {
            this->titolo = titolo;
            this->autore = autore;
            this->anno = anno;
        }
        string getTitolo() {
            return titolo;
        }
        string getAutore() {
            return autore;
        }
        int getAnno() {
            return anno;
        }
};

class Libro : public MaterialeBibliotecario {
    private:
        int numero_pagine;
    public:
        Libro(string titolo, string autore, int anno, int numero_pagine) : MaterialeBibliotecario(titolo, autore, anno) {
            this->numero_pagine = numero_pagine;
        }
        int getNumeroPagine() {
            return numero_pagine;
        }
};

class Rivista : public MaterialeBibliotecario {
    private:
        int numero_articoli;
    public:
        Rivista(string titolo, string autore, int anno, int numero_articoli) : MaterialeBibliotecario(titolo, autore, anno) {
            this->numero_articoli = numero_articoli;
        }
        int getNumeroArticoli() {
            return numero_articoli;
        }
};

class DVD : public MaterialeBibliotecario {
    private:
        int durata;
    public:
        DVD(string titolo, string autore, int anno, int durata) : MaterialeBibliotecario(titolo, autore, anno) {
            this->durata = durata;
        }
        int getDurata() {
            return durata;
        }
};

class Biblioteca {
    private:
        MaterialeBibliotecario *materiali;
        int n;
    public:
        Biblioteca() {
            materiali = new MaterialeBibliotecario[0];
            n = 0;
        }
        void aggiungiMateriale(MaterialeBibliotecario materiale) {
            MaterialeBibliotecario *tmp = new MaterialeBibliotecario[n+1];
            for (int i = 0; i < n; i++) {
                tmp[i] = materiali[i];
            }
            tmp[n] = materiale;
            n++;
            materiali = tmp;
        }
        void rimuoviMateriale(MaterialeBibliotecario materiale) {
            MaterialeBibliotecario *tmp = new MaterialeBibliotecario[n-1];
            int j = 0;
            for (int i = 0; i < n; i++) {
                if (materiali[i].getTitolo() != materiale.getTitolo()) {
                    tmp[j] = materiali[i];
                    j++;
                }
            }
            n--;
            materiali = tmp;
        }
        void visualizzaMateriali() {
            for (int i = 0; i < n; i++) {
                cout << materiali[i].getTitolo() << " " << materiali[i].getAutore() << " " << materiali[i].getAnno() << endl;
            }
        }
};

int main() {
    Biblioteca biblioteca;
    Libro libro("Il signore degli anelli", "Tolkien", 1954, 1000);
    Rivista rivista("Focus", "De Agostini", 1992, 10);
    DVD dvd("Titanic", "Cameron", 1997, 180);
    biblioteca.aggiungiMateriale(libro);
    biblioteca.aggiungiMateriale(rivista);
    biblioteca.aggiungiMateriale(dvd);
    cout << "Materiali presenti nella biblioteca:" << endl;
    biblioteca.visualizzaMateriali();
    biblioteca.rimuoviMateriale(dvd);
    cout << "Materiali presenti nella biblioteca:" << endl;
    biblioteca.visualizzaMateriali();
    return 0;
}
