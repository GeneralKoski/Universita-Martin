#include <iostream>

using namespace std;

int main() {
	int a[1000];
	int i=0;
	for (int i; i<1000; i++) {
		cin>>a[i];
		if (a[i]<0)
			break;
		cout << a[i];
	}	
	
	return 0;
}

