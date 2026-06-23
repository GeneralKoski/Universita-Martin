/*
 Esercizio – classe Orario
 implementare in c++ una classe di nome Orario che realizza il tipo di dato
 astratto ora del giorno così definito:
 valori:
     - terne <h,m, s>, con hh, mm, s numeri interi e
       0 <= h <= 23 e 0 <= m,s <= 59, che rappresentano,
       rispettivamente, le ore, i minuti e i secondi;

 operazioni su orari:
     - confronto tra due orari: operatore ==(vero se i due orari sono uguali);
     - operatore < (vero se il primo orario precede il secondo);
     - lettura e scrittura (con overloading degli operatori e <<>>) di un orario
       da/su stream nel formato h:m:s;
     - “getter” per gli attributi h, m, s;
        funzioni get_ora(), get_minuti(), get_secondi();
     - funzione di conversione da orario <h,m,s> a equivalente numero di:
       funzione to_second (); ad esempio, se a contiene l’orario <9:42:10 >>,
       a.to_seconds() restituisce 3493034930;
     - somma tra un orario e un dato numero di secondi: operatore ++; ad esempio, se a
       contiene l’orario 9:42:10 >>, a + 5221 restituisce il nuovo orario 11:9:11 >>.

 la classe fornisce anche un costruttore con tre parametri di tipo
 intero che rappresentano rispettivamente ore, minuti e secondi,
 e un costruttore con un parametro di tipo intero che rappresenta l’equivalente in secondi dell’orario.

 n.b. la funzione di lettura e i costruttori devono (obbligatoriamente) controllare che l’orario fornito sia corretto;
 in caso contrario, viene stampato un opportuno messaggio di errore e l’orario viene forzato al valore 0:0: 00.

 note di implementazione.
    - definire una funzione propria privata controlla_orario() che controlla
    la correttezza dell’orario.

 main di prova.
    la classe realizzata deve essere utilizzata dal main di prova messo a disposizione
    su ‘elly’ insieme al testo dell’esercizio (file orario _main.cpp cpp).
    l’esecuzione del main, completato con la classe orarioorario, deve dare i risultati riportati di seguito al main stesso. non è ammesso apportare modifiche al main.
    n.b. e' vietato: usare dichiarazioni friend, usare goto, usare variabili globali non motivate, definire public tutti i campi di una classe, usare ereditarietà a sproposito.
*/

#include <iostream>

using namespace std;

class Orario{
    private:
        int h;
        int m;
        int s;

        bool valida() const
        {
            bool check_h = (0 <= this->h) && (this->h < 24);
            bool check_m = (0 <= this->m) && (this->m < 60);
            bool check_s = (0 <= this->s) && (this->s < 60);
            return check_h && check_m && check_s;
        }

        void correggi()
        {
            if (!(this->valida()))
            {
                this->h = 0;
                this->m = 0;
                this->s = 0;
            }
            return;
        }
public:

    Orario()
    {
        this->h = 0;
        this->m = 0;
        this->s = 0;
    }
    Orario(int hours, int minutes, int seconds)
    {
        this->h = hours;
        this->m = minutes;
        this->s = seconds;
        this->correggi();
    } // end constuctor three parameters

    Orario(int seconds)
    {
        this->h = seconds / (60 * 60);
        seconds = seconds % (60 * 60);
        this->m = seconds / 60;
        this->s = seconds % 60;
        this->correggi();
    }// end constructor one parameter

    int get_hours() const
    {
        return this->h;
    }
    int get_minutes() const
    {
        return this->m;
    }
    int get_seconds() const
    {
        return this->s;
    }


    void set_hours(int hours)
    {
        if((0 <= hours) && (hours < 24))
            this->h = hours;
        return ;
    }
    void set_minutes(int minutes)
    {
        if((0 <= minutes) && (minutes < 60))
            this->m = minutes;
        return;
    }
    void set_seconds(int seconds)
    {
        if((0 <= seconds) && (seconds < 60))
            this->s = seconds;
        return;
    }

    ostream& stampa(ostream& os) const
    {
        os<< this->h << ':' << this->m << ':' << this->s;
        return os;
    }

    istream& read(istream& is)
    {
         char sep;
         is >> this->h >> sep >> this->m >> sep >> this->s;
         correggi();
         return is;
    }

    bool equals(const Orario& o) const
    {
             return (this->h == o.h) &&
                    (this->m == o.m) &&
                    (this->s == o.s);
    }

    bool less(const Orario& o) const
    {
            return (this->h <  o.h) ||
                  ((this->h == o.h) && (this->m < o.m)) ||
                  ((this->m == o.m) && (this->s < o.s));
    }

    int to_seconds() const
    {
        return this->h * 60 * 60 +
               this->m * 60 +
               this->s;
    }

    Orario add(int seconds) const
    {
        return Orario(seconds + this->to_seconds());
    }

};// end Orario class

ostream& operator<<(ostream& os, const Orario& o)
{
    return o.stampa(os);
}

istream& operator>>(istream& is, Orario& o)
{
    return o.read(is);
}

bool operator==(const Orario& o1,const Orario& o2)
{
    return o1.equals(o2);
}

bool operator< (const Orario& o1, const Orario& o2 )
{
    return o1.less(o2);
}

Orario operator+(const Orario& o1,const int seconds)
{
    return o1.add(seconds);
}
int main()
{
    Orario o1(23,45,36);
    Orario o2;
    cout << o2 << endl; //expected 0:0:0
    cin >> o2 ;
    cout << o2 << endl;
    Orario o3 = o1 + 24;
    cout << o3 << endl; // expected 23:46:0
    cout << (o3 < o2); // expected 0

    return 0;
}
