#include <iostream>
using namespace std;

template <class T>
const T& maxValue(const T& x, const T& y) {
	return x > y ? x : y;
}

int main() {
	char x = 'a', y = 'A';
	cout << maxValue(x, y) << endl;
	return 0;
}
