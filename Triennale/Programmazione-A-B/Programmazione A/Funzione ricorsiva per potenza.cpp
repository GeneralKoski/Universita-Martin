#include <iostream>
#include <cmath>
using namespace std;

int pow(int x, int y) {
	if (y == 0)
		return 1;
	else
		return x * pow(x, y-1);
}


int fact(int n) {
	return n * fact(n - 1);
}

int main() {
	cout << pow(3, 2) << endl;
	return 0;
}

