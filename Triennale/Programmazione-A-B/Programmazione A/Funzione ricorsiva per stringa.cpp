#include <iostream>
#include <cmath>
using namespace std;

int len(char* str) {
	if (*str == '\0')
		return 0;
	else
		return 1 + len(str + 1);
}

bool contains(int arr[], int l, int elem) {
	if (l <= 0)
		return false;
	else if (arr[l - 1] == elem)
		return true;
	else
		return contains(arr, l - 1, elem);
}

int main() {
	int x[] = {17, 23, 41, -24, 21, 54, 5, 8, 1};
	char str[] = "helloworld";
	cout << len(str) << endl;
	cout << contains(x, 9, 16) << endl; //(array, quanti numeri controllare, che numero trovare)
	return 0;
}

