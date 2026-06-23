#include <iostream>
#include <cstring>

using namespace std;

int main() {
	char str[31];
	cin.getline(str, 31);
	
	int len = strlen(str);
	bool isPalindroma = true;
	
	for(int i = 0; i < len; i++)
		if(str[i] != str[len-1-i]) {
			isPalindroma = false;
			break;
		}
	cout << "La stringa " << (isPalindroma ? "" : "non ") << "e' palindroma" << endl;
	return 0;
}

