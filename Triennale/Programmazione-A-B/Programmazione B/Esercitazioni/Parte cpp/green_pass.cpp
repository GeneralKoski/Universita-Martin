/*Si implementi una classe GreenPass che contenga il codice fiscale di una persona 
e la data di scadenza.
Si implementi poi una classe GreenPassVaccino che rappresenta un green pass 
ottenuto tramite vaccino. 
La classe deve contenere l’informazione sul tipo di vaccino effettuato
Si implementi poi una classe ￼GreenPassTampone che rappresenta un green pass ottenuto tramite tampone. 
La classe deve contenere l’informazione sul tipo di tampone effettuato
Si implementi poi una classe GreeenPassGuarigione che rappresenta poi un green pass ottenuto per guarigione.
*/

#include<iostream>
using namespace std;

#include "date.cpp"

class GreenPass {
	protected:
		string cf;
		Data dataGenerazione;
	public:
		GreenPass(string cf, Data dataGenerazione) {
			this->cf = cf;
			this->dataGenerazione = dataGenerazione;
		}

		void stampa(ostream& dest) const {
			dest << "Data generazione: ";
			dataGenerazione.stampa(dest);
			dest << endl;
			dest << "Codice fiscale: " << cf;
		}

		string getCodiceFiscale() const {
			return cf;
		}
};

class GreenPassVaccino : public GreenPass {
	private:
		int tipoVaccino;
	public:
		const static int ASTRAZENECA = 0;
		const static int MODERNA = 1;
		const static int PFIZER = 2;

		GreenPassVaccino(string cf, 
						Data dataGenerazione, 
						int tipoVaccino) : GreenPass(cf, dataGenerazione) {
			if (tipoVaccino < ASTRAZENECA || tipoVaccino > PFIZER)
				throw "Vaccino non ancora rinosciuto!";
			this->tipoVaccino = tipoVaccino;
		}

		void stampa(ostream& dest) const {
			GreenPass::stampa(dest);
			dest << endl << "Vaccino: ";
			switch(tipoVaccino) {
				case ASTRAZENECA: dest << "Astrazeneca"; break;
				case MODERNA: dest << "Moderna"; break;
				case PFIZER: dest << "Pfizer"; break;
				default:
					throw "Vaccino non ancora rinosciuto!";
			}
		}
};

class GreenPassTampone : public GreenPass {
	private:
		int tipoTampone;
	public:
		const static int SIEROLOGICO = 0;
		const static int MOLECOLARE = 1;

		GreenPassTampone(string cf, 
						Data dataGenerazione, 
						int tipoTampone) : GreenPass(cf, dataGenerazione) {
			if (tipoTampone != SIEROLOGICO && tipoTampone != MOLECOLARE)
				throw "Tampone non riconosciuto!";
			this->tipoTampone = tipoTampone;
		}

		void stampa(ostream& dest) const {
			GreenPass::stampa(dest);
			dest << endl << "Tipo tampone: ";
			switch(tipoTampone) {
				case SIEROLOGICO: dest << "tampone sierologico"; break;
				case MOLECOLARE: dest << "tampone molecolare"; break;
				default:
					throw "Tampone non rinosciuto!";
			}
		}
};

class GreenPassGuarigione : public GreenPass {
	private:
		int variante;
	public:
		const static int ALFA = 0;
		const static int DELTA = 1;
		const static int OMICRON = 2;

		GreenPassGuarigione(string cf, 
							Data dataGenerazione, 
							int variante) : GreenPass(cf, dataGenerazione){
			this->variante = variante;
		}

		void stampa(ostream& dest) const {
			dest << "Data guarigione: ";
			dataGenerazione.stampa(dest);
			dest << endl << "Codice fiscale: " << cf;

			dest << endl << "Variante: ";
			switch(variante) {
				case ALFA: dest << "Alfa"; break;
				case DELTA: dest << "Delta"; break;
				case OMICRON: dest << "Omicron"; break;
				default: dest << "Variante non identificata";
			}
		}
};

class PersonaConGreenPass {
	private:
		string cf;
		GreenPass* gp;
	public:
		PersonaConGreenPass(string cf) {
			this->cf = cf;
			this->gp = NULL;
		}

		void addGreenPass(GreenPass gp) {
			if (gp.getCodiceFiscale() != cf)
				throw "Errore - Codici fiscali non uguali";
			this->gp = &gp;
		}

		bool hasGreenPass() const {
			return gp != NULL;
		}

		void stampa(ostream& dest) const {
			if (hasGreenPass()) 
				dest << "Persona con green pass";
			else
				dest << "Persona senza green pass";
		}
};


int main() {
	GreenPassVaccino gpv("ABC123", Data(6,5, 2022), GreenPassVaccino::ASTRAZENECA);
	gpv.stampa(cout);
	cout << endl << endl;

	GreenPassTampone gpt("DEF123", Data(3,4, 2022), GreenPassTampone::SIEROLOGICO);
	gpt.stampa(cout);
	cout << endl << endl;


	GreenPassGuarigione gpg("GHI542", Data(3,4, 2022), GreenPassGuarigione::DELTA);
	gpg.stampa(cout);
	cout << endl << endl;

	PersonaConGreenPass p("ABC123");
	p.stampa(cout);
	cout << endl;

	try {
		p.addGreenPass(gpt);
	} catch (const char* e) {
		cout << e << endl;
	}

	p.stampa(cout);
	cout << endl;
	p.addGreenPass(gpv);
	cout << endl;

	p.stampa(cout);
	cout << endl;
	return 0;
}