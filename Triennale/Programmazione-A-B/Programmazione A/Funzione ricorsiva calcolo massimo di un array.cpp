#include <iostream>
#include <cmath>
using namespace std;

int max(int arr[], int cursor, int l) {
	if (cursor == l - 1)
		return arr[cursor];
	else {
		int m = max(arr, cursor + 1, l);
		if (arr[cursor] > m)
			return arr[cursor];
		else
			return m;
	}
}

bool contains(int arr[], int cursor, int l, int elem) {
	if (cursor >= 1)
		return false;
	else if (arr[cursor] == elem)
		return true;
	else
		return contains (arr, cursor + 1, l, elem);
}

int main() {
	int x[] = {17, 23, 41, -24, 21, 54, 5, 8, 1};
	cout << max(x, 0, 9) << endl;
	cout << contains(x, 0, 9, 0) << endl;
	
	return 0;
}

