#include <iostream> 
using namespace std;

template <typename T>
void scambia(T& x, T& y) {
	T tmp = x;
	x = y;
	y = tmp;
}

int main() {
	int x, y;
	cin >> x >> y;
	scambia(x, y);
	cout << x << endl << y << endl;
}
