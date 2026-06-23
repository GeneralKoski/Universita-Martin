#include <iostream>
using namespace std;

class Data {
	protected:
		int g;
		int m;
		int a;
	private:
		bool controllaData(int g, int m, int a) {
			if (g <= 0)
				return false;
			else if (m <= 0 || m > 12)
				return false;
			else if (a < 0)
				return false;
			// TODO: completare
			return true;
		}
	public:
		Data() {
			g = 1;
			m = 1;
			a = 1970;
		}

		Data(int g, int m, int a) {
			if (!controllaData(g, m, a))
				throw "Data errata";
			this->g = g;
			this->m = m;
			this->a = a;
		}

		bool operator==(Data other) const {
			return a == other.a && m == other.m && g == other.g; 
		}

		void stampa(ostream& dest) const {
			dest << g << "/" << m << "/" << a;
			return;
		}
};

class DataConOrario : public Data {
	private:
		int sec;
	public:
		DataConOrario() {
			this->sec = 0;
		}

		DataConOrario(int g, int m, int a) : Data(g, m, a) {
			this->sec = 0;
		}

		DataConOrario(int g, int m, int a, int sec) : Data(g, m, a) {
			this->sec = sec;
		}

		DataConOrario(int g, int m, int a, int h, int min, int sec) : Data(g, m, a) {
			this->sec = h * 3600 + min * 60 + sec;
		}

		int getOre() const {
			return sec / 3600;
		}

		int getMinuti() const {
			return (sec % 3600) / 60;
		}

		int getSecondi() const {
			return sec % 60;
		}

		void stampa(ostream& dest) const {
			Data::stampa(dest);
			dest << "h" << getOre() << ":" << getMinuti() << ":" << getSecondi() << endl;
		}

		bool operator==(DataConOrario other) {
			return Data::operator==(other) && sec == other.sec;
		}
};

