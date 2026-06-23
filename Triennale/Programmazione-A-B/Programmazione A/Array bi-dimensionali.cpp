#include <iostream>

using namespace std;

int main() {
	int x[5][2] = {{3,2}, {-2,5}, {-1,7}, {9,4}, {8,1}};
	
	for (int i = 0; i < 5; i++)
		for (int j = 0; j < 2; j++)
			cout << x[i][j] << " ";
	cout << endl;
		
	for (int i = 0; i < 5; i++)
		x[i][1]++;
		
	for (int i = 0; i < 5; i++)
		for (int j = 0; j < 2; j++)
			cout << x[i][j] << " ";

	return 0;
}

