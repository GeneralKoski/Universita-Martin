#include <iostream>

using namespace std;

struct node{
	int dato;
	node* next;	
};

void concat (node* l1, node* l2) {
	if (l2 == NULL)
		return;
	else if (l1 == NULL) {
		l1 = l2;
		return;
	} else {
		node* cursor = l1;
		while (cursor->next !=NULL) {
			cursor = cursor->next;
		}
		cursor->next = l2;
		return;
	}
}

int main() {
	return 0;
}
