#include <iostream>
using namespace std;

template <class T>
class vett {
	private:
		T* A;
		int dim;
	public:
		vett() {
			A = new T[0];
			dim = 0;
		}
		vett(int n) {
			A = new T[n];
			dim = n;
		}
		vett(int n, T v) {
			A = new T[n];
			dim = n;
			for (int i = 0; i < n; i++)
				A[i] = v;
		}
		
		vett(const vett<T>& other) {
			A = new T[other.dim];
			dim = other.dim;
			
			for (int i = 0; i < dim; i++)
				A[i] = other.A[i];
		}
				
		~vett() {
			delete[] A;	
		}
		
		const vett<T>& operator=(const vett<T>& other) {
			if (this == &other)
				return *this;
			int d;
			if(dim <= other.dim)
				d=dim;
			else
				d=other.dim;
			for (int i = 0; i < d; i++)
				A[i] = other.A[i];
			return *this;
		}
		
		bool operator==(const vett<T>& other) {
			if (dim != other.dim)
				return false;
			for (int i = 0; i < dim; i++)
				if (A[i] != other.A[i])
					return false;
			return true;
		}
		
		T operator[](int i) {
			if (i < 0 || i >= dim)
				throw string("Out of range!");
			return A[i];
		}
		
		void stampa(ostream& dest) {
			for (int i = 0; i < dim; i++)
				dest << A[i] << " ";
		}
		
		void leggi (istream& sorg) {
			for ( int i = 0; i< dim; i++)
				sorg >> A[i];
		}
		
};

template<class T>
istream& operator>>(istream& sorg, vett<T>& r) {
	r.leggi(sorg);
	return sorg;
}

template<class T>
ostream& operator<<(ostream& dest, const vett<T>& r) {
	r.stampa(dest);
	return dest;
}

operator<<();

int main() {
	
}

