#include <iostream>
#include <cmath>

using namespace std;

bool eq2 (float a, float b, float c, float& x1, float& x2) {
	float delta = pow(b, 2) - 4 * a * c;
	
	if (delta < 0)
		return false;
	else {
		float delta_sqrt = sqrt(delta);
		x1 = (-b + delta_sqrt) / (2 * a);
		x2 = (-b - delta_sqrt) / (2 * a);
		return true;
	}
}

int main() {
	float sol1;
	float sol2;
	int x, y, z;
	
	cout << "Inserisci i tre coefficienti: ";
	cout << endl;
	cin >> x >> y >> z;
	
	bool res = eq2(x, y, z, sol1, sol2);
	
	if (res) {
		cout << "x1: " << sol1 << endl;
		cout << "x2: " << sol2 << endl;
	} else {
		cout << "Il risultato e' negativo" << endl;
	}
	
	return 0;
}

