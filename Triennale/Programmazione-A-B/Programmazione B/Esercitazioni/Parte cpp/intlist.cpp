#include <iostream>
using namespace std;


struct node {
	int data;
	node* next;
};

class int_list {
	private:
		struct node {
			int data;
			node* next;
		};

		node* l;
		int n;

	public:

		int_list() {
			l = NULL;
			n = 0;
		}

		~int_list() {
			if (l != NULL) {
				node* prev;

				do {
					prev = l;
					l = l->next;
					delete prev;
				} while(l != NULL)
			}
		}

		void addFirst(int x) {
			node* t = new node;
			t->data = x;
			t->next = this->l;
			this->l = t;
			n++;
		}

		void removeFirst() {
			if (l == NULL)
				throw string("Lista vuota!");

			node* cpy = l;
			l = l->next;
			delete cpy;
			n--;
		}


};