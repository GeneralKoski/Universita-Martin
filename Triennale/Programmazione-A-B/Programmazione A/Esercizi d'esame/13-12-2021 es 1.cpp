#include <iostream>

using namespace std;

int coincide(int a1[], int a2[], int d1, int d2) {
	int c = 0;
	for (int i = 0; i <d1 && i < d2; i++)
		if (a1[i] == a2[i]) {
			c++;
		}
	return c;
}

int main() {
	int a1[] = {6, 7, 4, 5, 2, 5, 12};
	int a2[] = {6, 7, 4, 5, 2};
	cout << coincide(a1, a2, 7, 5) << endl;
	return 0;
}

