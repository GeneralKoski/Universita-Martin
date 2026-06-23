#include <iostream>
using namespace std;

template<class T> class Inventory {
private:
    int capacity;
    int dim;
    T* A;

    void enlarge(int amount){
        capacity += amount;
        T* B = A;
        A = new T[capacity];
        for(int i = 0; i < dim; i++){
            A[i] = B[i];
        }
        delete[] B;
    }

public:
    Inventory(){
        capacity = 10;
        dim = 0;
        A = new T[capacity];
    }

    Inventory(const Inventory<T>& other){
        capacity = other.capacity;
        dim = other.dim;
        A = new T[capacity];
        for(int i = 0; i < capacity; i++){
            A[i] = other.A[i];
        }
    }

    Inventory<T>& operator=(const Inventory<T>& other){
        if (this != &other){
            this->~Inventory();
            capacity = other.capacity;
            dim = other.dim;
            A = new T[capacity];
            for(int i = 0; i < dim; i++){
                A[i] = other.A[i];
            }
        }
        return *this;
    }

    void add(const T& object){
        if(dim == capacity) enlarge(10);
        A[dim] = object;
        dim++;
    }
    
    int count(const T& object) const{
        int counter = 0;
        for(int i = 0; i < dim; i++){
            if(A[i]==object){
                counter++;
            }
        }
        return counter;
    }

    T getMostCommon(){
        int max=0;
        T object;
        for(int i = 0; i < dim; i++){
            int c = this->count(A[i]);
            if(max<c){
                max = c;
                object = A[i];
            }
        }
        return object;
    }

    ~Inventory<T>(){
        delete[] A;
    }
};

int main() {
    Inventory<int> inv0;
    Inventory<string> inv1;
    inv0.add(1); 
    inv0.add(2); 
    inv0.add(1); 
    inv0.add(3);

    inv1.add("hello"); 
    inv1.add ("hello"); 
    inv1 .add ("ciao"); 
    inv1 .add ("hello");
    cout << inv0.count(7) << endl ; // output : 0
    cout << inv0.count(1) << endl ; // output : 2
    cout << inv1.count("ciao") << endl ; // output : 1
    cout << inv0.getMostCommon() << endl ; // output : 1
    return 0;
}
