// Definire una classe Vagone che ha come campi identificativo e posti disponibili.
// Definire una classe base Treno che come campi ha un numero identificativo ed una velocità massima con i relativi getter. Ciascun Treno contiene un array lungo numero_vagoni di oggetti di classe Vagone, numerati da 1 ad numero_vagoni e ciascuno con una capienza k, che permettono di inizializzare il campo che tiene conto dei posti disponibili.
// Definire poi due classi derivate, TrenoRegionale e TrenoAltaVelocita, che aggiungano i dati specifici dei rispettivi tipi di treno
// Il numero di fermate per i treni regionali
// L'elenco delle stazioni in cui può fermare un treno ad alta velocità
// Creare un main dove vengono inizializzati due treni e, tramite l’operatore <<, ridefinito nelle opportune classi, stampare i campi di ciascuno.

#include <iostream>
#include <string>

using namespace std;

class Vagone
{
private:
    int id;
    int posti_disponibili;

public:
    Vagone(){} // costruttore di default

    Vagone(int id, int posti_disponibili)
    {
        this->id = id;
        this->posti_disponibili = posti_disponibili;
    }
    int getId()
    {
        return id;
    }
    int getPostiDisponibili()
    {
        return posti_disponibili;
    }
};

class Treno
{
private:
    int id;
    int velocita_massima;
    Vagone *vagoni;
    int numero_vagoni;

public:
    Treno(int id, int velocita_massima, int numero_vagoni, int k)
    {
        this->id = id;
        this->velocita_massima = velocita_massima;
        this->numero_vagoni = numero_vagoni;
        vagoni = new Vagone[numero_vagoni];
        for (int i = 0; i < numero_vagoni; i++)
        {
            vagoni[i] = Vagone(i + 1, k);
        }
    }
    int getId()
    {
        return id;
    }
    int getVelocitaMassima()
    {
        return velocita_massima;
    }
    Vagone *getVagoni()
    {
        return vagoni;
    }
    int getNumero_vagoni()
    {
        return numero_vagoni;
    }
};

ostream &operator<<(ostream &os, Treno &treno)
{
    os << "Treno " << treno.getId() << " con velocità massima di " << treno.getVelocitaMassima() << " km/h" << endl;
    int posti_disponibili = 0;
    for (int i = 0; i < treno.getNumero_vagoni(); i++)
    {
        posti_disponibili += treno.getVagoni()[i].getPostiDisponibili();
        os << "Vagone " << treno.getVagoni()[i].getId() << " con " << treno.getVagoni()[i].getPostiDisponibili() << " posti disponibili" << endl;
    }
    os << "Posti totali disponibili: " << posti_disponibili << endl;
    return os;
}

class TrenoRegionale : public Treno
{
private:
    int numero_fermate;
public:
    TrenoRegionale(int id, int velocita_massima, int numero_vagoni, int k, int numero_fermate) : Treno(id, velocita_massima, numero_vagoni, k)
    {
        this->numero_fermate = numero_fermate;
    }
    int getNumero_fermate()
    {
        return numero_fermate;
    }
};

ostream &operator<<(ostream &os, TrenoRegionale &treno)
{
    os << "Treno " << treno.getId() << " con velocità massima di " << treno.getVelocitaMassima() << " km/h" << endl;
    int posti_disponibili = 0;
    for (int i = 0; i < treno.getNumero_vagoni(); i++)
    {
        posti_disponibili += treno.getVagoni()[i].getPostiDisponibili();
        os << "Vagone " << treno.getVagoni()[i].getId() << " con " << treno.getVagoni()[i].getPostiDisponibili() << " posti disponibili" << endl;
    }
    os << "Posti totali disponibili: " << posti_disponibili << endl;
    os << "Numero fermate: " << treno.getNumero_fermate() << endl;
    return os;
}

class TrenoAltaVelocita : public Treno
{
private:
    string *stazioni;
public:
    TrenoAltaVelocita(int id, int velocita_massima, int numero_vagoni, int k, string *stazioni, int numero_stazioni) : Treno(id, velocita_massima, numero_vagoni, k)
    {
        this->stazioni = new string[numero_stazioni];
        for (int i = 0; i < numero_stazioni; i++)
        {
            this->stazioni[i] = stazioni[i];
        }
    }
    string *getStazioni()
    {
        return stazioni;
    }
};


ostream &operator<<(ostream &os, TrenoAltaVelocita &treno)
{
    os << "Treno " << treno.getId() << " con velocità massima di " << treno.getVelocitaMassima() << " km/h" << endl;
    int posti_disponibili = 0;
    for (int i = 0; i < treno.getNumero_vagoni(); i++)
    {
        posti_disponibili += treno.getVagoni()[i].getPostiDisponibili();
        os << "Vagone " << treno.getVagoni()[i].getId() << " con " << treno.getVagoni()[i].getPostiDisponibili() << " posti disponibili" << endl;
    }
    os << "Posti totali disponibili: " << posti_disponibili << endl;
    os << "Stazioni: ";
    for (int i = 0; i < 3; i++)
    {
        os << treno.getStazioni()[i] << " ";
    }
    os << endl;
    return os;
}

int main()
{
    TrenoRegionale treno1(1, 100, 5, 100, 10);
    string stazioni[3] = {"Milano", "Roma", "Napoli"};
    TrenoAltaVelocita treno2(2, 300, 10, 100, stazioni, 3);
    cout << treno1 << endl;
    cout << treno2 << endl;
    return 0;
}