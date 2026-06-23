// Definire una classe base Dipendente che abbia come membri protetti il nome, l’età, lo stipendio ed un metodo calcolaBonus() che ritorna il 10% dello stipendio. 
// Definire poi le classi derivate Manager e Direttore che ereditino dalla classe base Dipendente.
// Il metodo calcolaBonus() per la classe Manager deve ritornare il 15% dello stipendio, mentre per la classe Direttore il 20%.
// Creare un main che crei un Dipendente, un Manager ed un Direttore e per ciascuno stampare il bonus.

#include <iostream>
#include <string>

using namespace std;

class Dipendente {
    protected:
        string nome;
        int eta;
        int stipendio;
    public:
        Dipendente(string nome, int eta, int stipendio) {
            this->nome = nome;
            this->eta = eta;
            this->stipendio = stipendio;
        }
        string getNome() {
            return nome;
        }
        int getEta() {
            return eta;
        }
        int getStipendio() {
            return stipendio;
        }
        int calcolaBonus() {
            return stipendio * 0.1;
        }
};

class Manager : public Dipendente {
    public:
        Manager(string nome, int eta, int stipendio) : Dipendente(nome, eta, stipendio) {}
        int calcolaBonus() {
            return stipendio * 0.15;
        }
};

class Direttore : public Dipendente {
    public:
        Direttore(string nome, int eta, int stipendio) : Dipendente(nome, eta, stipendio) {}
        int calcolaBonus() {
            return stipendio * 0.2;
        }
};

int main() {
    Dipendente dipendente("Mario Rossi", 30, 1000);
    Manager manager("Luigi Verdi", 40, 2000);
    Direttore direttore("Giovanni Bianchi", 50, 3000);
    cout << "Bonus dipendente: " << dipendente.calcolaBonus() << endl;
    cout << "Bonus manager: " << manager.calcolaBonus() << endl;
    cout << "Bonus direttore: " << direttore.calcolaBonus() << endl;
    return 0;
}