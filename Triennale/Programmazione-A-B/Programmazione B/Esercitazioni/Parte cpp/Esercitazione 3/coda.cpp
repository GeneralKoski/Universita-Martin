// Implementare una classe coda templatica che supporti i seguenti metodi:
// enqueue(T element): aggiunge un elemento alla fine della coda
// dequeue(): rimuove e restituisce l'elemento in testa alla coda
// front(): restituisce l'elemento in testa alla coda senza rimuoverlo
// size(): restituisce il numero di elementi presenti nella coda
// isEmpty(): restituisce true se la coda è vuota, altrimenti false
// La classe deve essere implementata senza l'uso di costrutti della STL

#include <iostream>
using namespace std;

template <typename T>
class Queue {
private:
    struct Node {
        T element;
        Node* next;
    };
    Node* head;
    Node* tail;
    int count;
public:
    Queue() {
        head = NULL;
        tail = NULL;
        count = 0;
    }
    ~Queue() {
        while (head != NULL) {
            Node* temp = head;
            head = head->next;
            delete temp;
        }
    }
    void enqueue(T element) {
        Node* newNode = new Node;
        newNode->element = element;
        newNode->next = NULL;
        if (head == NULL) {
            head = newNode;
            tail = newNode;
        } else {
            tail->next = newNode;
            tail = newNode;
        }
        count++;
    }
    T dequeue() {
        if (head == NULL) {
            throw "Queue is empty";
        }
        Node* temp = head;
        T element = temp->element;
        head = head->next;
        delete temp;
        count--;
        return element;
    }
    T front() {
        if (head == NULL) {
            throw "Queue is empty";
        }
        return head->element;
    }
    int size() {
        return count;
    }
    bool isEmpty() {
        return count == 0;
    }
};

int main(){
    Queue<int> q;
    for (int i = 0; i < 10; i++) {
        q.enqueue(i);
    }
    cout << "Size: " << q.size() << endl;
    cout << "Front: " << q.front() << endl;
    cout << "Dequeue: " << q.dequeue() << endl;
    cout << "Front: " << q.front() << endl;

    while (!q.isEmpty()) {
        cout << q.dequeue() << endl;
    }
    cout << endl;
    return 0;
}
