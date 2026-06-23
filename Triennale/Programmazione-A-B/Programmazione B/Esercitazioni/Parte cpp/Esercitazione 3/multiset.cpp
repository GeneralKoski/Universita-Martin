// Implementare una classe multiset templatica che supporti i seguenti metodi:
// insert(T element): aggiunge un elemento al multiset
// erase(T element): rimuove tutte le occorrenze di un elemento dal multiset
// count(T element): restituisce il numero di occorrenze di un elemento nel multiset
// size(): restituisce il numero di elementi presenti nel multiset
// isEmpty(): restituisce true se il multiset è vuoto, altrimenti false
// La classe deve essere implementata senza l'uso di costrutti della STL

#include <iostream>
using namespace std;

template <typename T>
class Multiset {
private:
    struct Node {
        T element;
        Node* next;
    };
    Node* head;
    int size;
public:
    Multiset() {
        head = nullptr;
        size = 0;
    }
    ~Multiset() {
        while (head != nullptr) {
            Node* temp = head;
            head = head->next;
            delete temp;
        }
    }
    void insert(T element) {
        Node* newNode = new Node;
        newNode->element = element;
        newNode->next = head;
        head = newNode;
        size++;
    }
    void erase(T element) {
        Node* temp = head;
        Node* prev = nullptr;
        while (temp != nullptr) {
            if (temp->element == element) {
                if (prev == nullptr) {
                    head = head->next;
                } else {
                    prev->next = temp->next;
                }
                delete temp;
                size--;
                temp = prev;
            }
            prev = temp;
            temp = temp->next;
        }
    }
    int count(T element) {
        int count = 0;
        Node* temp = head;
        while (temp != nullptr) {
            if (temp->element == element) {
                count++;
            }
            temp = temp->next;
        }
        return count;
    }
    int getSize() {
        return size;
    }
    bool isEmpty() {
        return size == 0;
    }
};

int main(){
    Multiset<int> m;
    // Ogni elemento i è inserito i volte
    for (int i = 1; i <= 3; i++) {
        for (int j = 0; j < i; j++) {
            m.insert(i);
        }
    }
    cout << "Size: " << m.getSize() << endl;
    cout << "Count 1: " << m.count(1) << endl;
    cout << "Count 2: " << m.count(2) << endl;
    cout << "Count 3: " << m.count(3) << endl;
    m.erase(2);
    cout << "Size: " << m.getSize() << endl;
    cout << "Count 1: " << m.count(1) << endl;
    cout << "Count 2: " << m.count(2) << endl;
    cout << "Count 3: " << m.count(3) << endl;
    return 0;
}