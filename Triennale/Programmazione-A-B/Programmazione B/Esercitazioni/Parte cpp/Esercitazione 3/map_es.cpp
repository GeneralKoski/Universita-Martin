// Si vuole implementare un programma in C++ che utilizzi la classe map della STL 
// per gestire una mappa che associa il nome di uno studente al suo voto in un esame. 
// In particolare, il programma deve permettere all'utente di eseguire le seguenti operazioni:
//     Inserimento di un nuovo studente e del suo voto
//     Aggiornamento del voto di uno studente esistente
//     Cancellazione di uno studente e del suo voto
//     Ricerca del voto di uno studente (tramite il nome dello studente)
//     Stampa di tutti gli studenti e dei loro voti
// Il programma deve chiedere all'utente di scegliere l'operazione da eseguire e 
// poi eseguirla sulla mappa. Il programma deve terminare quando l'utente sceglie di uscire.

#include <iostream>
#include <map>
#include <string>
using namespace std;

int main(){
    map<string, int> voti;
    int scelta;
    do{
        cout << "********** MENU **********" << endl;
        cout << "1. Inserisci un nuovo studente e il suo voto" << endl;
        cout << "2. Aggiorna il voto di uno studente esistente" << endl;
        cout << "3. Cancella uno studente e il suo voto" << endl;
        cout << "4. Ricerca il voto di uno studente" << endl;
        cout << "5. Stampa tutti gli studenti e i loro voti" << endl;
        cout << "0. Esci" << endl;
        cout << "Scelta: ";
        cin >> scelta;
        cout << endl;

        switch(scelta){
            case 1:{
                string nome;
                int voto;
                cout << "Inserisci il nome dello studente: ";
                cin >> nome;
                cout << "Inserisci il voto dello studente: ";
                cin >> voto;
                voti[nome] = voto;
                break;
            }
            case 2:{
                string nome;
                int voto;
                cout << "Inserisci il nome dello studente: ";
                cin >> nome;
                if(voti.find(nome)==voti.end()){
                    cout << "Studente non trovato!" << endl;
                    break;
                }
                cout << "Inserisci il nuovo voto dello studente: ";
                cin >> voto;
                voti[nome] = voto;
                break;
            }
            case 3:{
                string nome;
                cout << "Inserisci il nome dello studente: ";
                cin >> nome;
                if(voti.find(nome)==voti.end()){
                    cout << "Studente non trovato!" << endl;
                    break;
                }
                voti.erase(nome);
                break;
            }
            case 4:{
                string nome;
                cout << "Inserisci il nome dello studente: ";
                cin >> nome;
                if(voti.find(nome)==voti.end()){
                    cout << "Studente non trovato!" << endl;
                    break;
                }
                cout << "Voto dello studente: " << voti[nome] << endl;
                break;
            }
            case 5:{
                for (auto elemento : voti)
                    cout << elemento.first << " " << elemento.second << endl;
                break;
            }
            case 0:{
                cout << "Arrivederci!" << endl;
                break;
            }
            default:{
                cout << "Scelta non valida!" << endl;
                break;
            }
        }
    }while(scelta!=0);
    return 0;
}