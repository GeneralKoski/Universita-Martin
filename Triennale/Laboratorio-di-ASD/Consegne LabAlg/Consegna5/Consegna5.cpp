/*
Trajkovski Martin 335566
Montinaro Davide 331881
*/

#include <iostream>
#include <vector>
#include <queue>
#include <limits>

using namespace std;

// Struttura per rappresentare un nodo nel grafo
struct Edge {
    int v; // Vertice di destinazione
    int weight;
};

// Funzione per creare un nuovo grafo con n vertici
vector<vector<Edge>> createGraph(int n) {
    vector<vector<Edge>> graph(n);
    return graph;
}

// Funzione per aggiungere un nodo ad un gafo non orientato
void addEdge(vector<vector<Edge>>& graph, int u, int v, int weight) {
    graph[u].push_back({v, weight});
    graph[v].push_back({u, weight}); // Per grafi non orientati
}

// Funzione per implementare l'algoritmo di Prim per trovare l'MST
vector<Edge> primMST(const vector<vector<Edge>>& graph, int start) {
    int n = graph.size();

    // Array per memorizzare i valori chiave, i puntatori padre e i nodi dell'albero di spanning minimo
    vector<int> key(n, numeric_limits<int>::max());
    vector<int> parent(n, -1);
    vector<Edge> mst;

    // Creare una coda di priorità per memorizzare i nodi in base ai valori chiave
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;

    // Inizializzare la chiave per il vertice iniziale e inserirlo nella coda
    key[start] = 0;
    pq.push({0, start});

    // Elaborare tutti i nodi finché la coda non è vuota
    while (!pq.empty()) {
        int u = pq.top().second; // Estrarre il nodo con la chiave minima
        pq.pop();

        mst.push_back({parent[u], u}); // Aggiungere il nodo all'MST (se il padre non è -1)

        // Per tutti i nodi adiacenti al nodo elaborato
        for (const Edge& e : graph[u]) {
            int v = e.v;

            // Se il nodo non è ancora incluso nell'MST e il peso del nodo è inferiore alla chiave corrente del nodo
            if (key[v] > e.weight) {
                // Aggiornare il valore chiave e il puntatore padre
                key[v] = e.weight;
                parent[v] = u;

                // Aggiornare la priorità nella coda se necessario (diminuire la chiave)
                pq.push({key[v], v});
            }
        }
    }

    return mst;
}

// Funzione per stampare i nodi dell'MST memorizzati in padre
void printMST(const vector<Edge>& mst) {
    for (const Edge& e : mst) {
        cout << e.v << " - " << e.weight << endl;
    }
}

int main() {
    // Richiedere all'utente il numero di vertici (n)
    cout << "Enter the number of vertices (n): ";
    int n;
    cin >> n;

    // Richiedere all'utente il numero di archi (m)
    cout << "Enter the number of edges (m): ";
    int m;
    cin >> m;

    // Creare un grafo vuoto con n vertici
    vector<vector<Edge>> graph = createGraph(n);

    // Richiedere all'utente di inserire gli archi (u, v, peso)
    cout << "Enter the edges in the format (u v weight):\n";
    for (int i = 0; i < m; i++) {
        int u, v, weight;
        cin >> u >> v >> weight;
        addEdge(graph, u, v, weight);
    }

    // Richiedere all'utente il vertice iniziale per l'MST
    cout << "Enter the starting vertex for MST: ";
    int start;
    cin >> start;

    // Calcolare e stampare l'albero di spanning minimo
    vector<Edge> mst = primMST(graph, start);

    cout << "Minimum Spanning Tree Edges (with weights):\n";
    printMST(mst);

    return 0;
}

