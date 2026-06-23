/*
Trajkovski Martin 335566
Montinaro Davide 331881
*/

#include <fstream>
#include <iostream>
#include <cstdlib>
#include <ctime>
using namespace std;

#define INFINITO 1000000

int details = 0;
int graph = 1;

// file di output per grafo
ofstream output_grafo;
int conteggio_operazioni = 0; /// contatore di operazioni per visualizzare i vari step


typedef struct Node // Struttura che rappresenta i nodi di un albero
{
    int val; // Contiene un valore in base al contesto
    float w; // peso dell'arco
    struct Node *next; // Fa riferimento al prossimo nodo
} Node_t;


typedef struct List  // Rappresenta una lista collegata di nodi (del TIPO Node)
{
    Node *head; // Restituisce un ELEMENTO Node perchè list->next restituisce un PUNTATORE al primo elemento della LISTA
} List_t;


struct nodeData // La struttura nodeData è progettata per contenere informazioni specifiche legate ai nodi di un grafo
{
    int prev = -1;    // inizialmente non c'e' precedente
    int dist = INFINITO; // distanza dal nodo in questione al nodo SORGENTE, inizialmente impostata su "INFINITO"
    int visitato = 0; // Flag che indica se un nodo è stato visitato o meno, inizialmente impostato su MAI VISITATO
    int nodeNumber; // Questo campo è un INTERO che serve per IDENTIFICARE UNIVOCAMENTE un NODO
};

// Archiconnessi è una matrice di liste di adiacenza
List_t** Archiconnessi; // Archiconnessi' una variabile di tipo puntatore a puntatore di List_t, utilizzata per creare una matrice dinamica di liste collegate, ogni nodi contiene un puntatore a *List_t che rappresenta la lista di adiacenza del nodo, ovvero i nodi a quel nodo adiacenti
int num_nodi; // Tiene il conto del numero totale di nodi del grafo
List_t* puntatore_globale = NULL; // Serve come riferimento iniziale per la costruzione di liste di adiacenza. 


void print_node(int n, nodeData* &nodes, int* order)
{
    // calcolo massima distanza (eccetto infinito)
    float max_d = 0;
    for (int i = 0; i < num_nodi; i++)
	{
		if (max_d < nodes[order[i]].dist && nodes[order[i]].dist < INFINITO)
		{
			max_d = nodes[order[i]].dist;
		}
	}

    output_grafo << "node_" << nodes[n].nodeNumber << "_" << conteggio_operazioni << endl;
    output_grafo << "[ shape = oval; ";

    if (nodes[n].visitato == 1)
	{
		output_grafo << "penwidth = 4; ";
	}

    float col = nodes[n].dist / max_d; // distanza in scala 0..1
    output_grafo << "fillcolor = \"0.0 0.0 " << col / 2 + 0.5 << "\"; style=filled; ";
	
    if (nodes[n].dist < INFINITO)
	{
		output_grafo << "label = "
                     << "\"Idx: " << nodes[n].nodeNumber << ", dist: " << nodes[n].dist << "\" ];\n";
	}
    else
	{
		output_grafo << "label = "
                     << "\"Idx: " << nodes[n].nodeNumber << ", dist: INF\" ];\n";
	}

    Node_t* elem = Archiconnessi[nodes[n].nodeNumber]->head;
    while (elem != NULL) 
	{
		// disegno arco
        output_grafo << "node_" << nodes[n].nodeNumber << "_" << conteggio_operazioni << " -> ";
        output_grafo << "node_" << elem->val << "_" << conteggio_operazioni << " [ label=\"" << elem->w << "\", len=" << elem->w / 100 * 10 << " ]\n";
        elem = elem->next;
    }

    if (nodes[n].prev != -1)
	{ 
		// se c'e' un nodo precedente visitato -> disegno arco

        float len = 0;

        len = 1;
        output_grafo << "node_" << nodes[n].nodeNumber << "_" << conteggio_operazioni << " -> ";
        output_grafo << "node_" << nodes[n].prev << "_" << conteggio_operazioni << " [ color=blue, penwidth=5, len=" << len / 100 * 10 << " ]\n";
    }
}

void print_graph(nodeData* &nodes, int* order)
{
	for (int i = 0; i < num_nodi; i++)
	{
		print_node(order[i], nodes, order);
	}
    conteggio_operazioni++;
}

List_t* crea_lista(void)
{
    List_t* lista = new List_t;
    if (details)
	{
        printf("Lista creata\n");
    }

    lista->head = NULL;
    if (details)
	{
        printf("Imposto a NULL head\n");
    }

    return lista;
}

void print_list(List_t* lista)
{
    if (lista->head == NULL) // Se vero significa che la lista di adiacenza è vuota, cioè il nodo non è connesso ad alcun altro nodo
    {
        cout << "Lista vuota" << endl;
    }
    else
    {
        Node_t* corrente = lista->head; // corrente prende il primo nodo della lista di adiacenza
        while (corrente != NULL)
        {
            cout << corrente->val << ", ";
            corrente = corrente->next;
        }
        cout << endl;
    }
}

void inserisci_in_testa(List_t* lista, int elem, float peso) // Crea un NUOVO NODO che verrà aggiunto in TESTA alla LISTA
{
    /// inserisce un elemento all'inizio della lista
    Node_t* nuovo_nodo = new Node_t;
    nuovo_nodo->next = NULL;

    nuovo_nodo->val = elem;
    nuovo_nodo->w = peso;

    nuovo_nodo->next = lista->head; // Il PUNTATORE del nuovo nodo punta alla TESTA(inizio) della LISTA

    lista->head = nuovo_nodo; // La TESTA(inizio) della LISTA punta al NUOVO NODO creato, in questo modo il primo elemento ora sarà il NODO appena creato
}

void swap(nodeData* &node1, nodeData* &node2) // Scambia le INFORMAZIONI di 2 NODI, quindi ne SCAMBIA anche la POSIZIONE(dato che vengono scambiati i PUNTATORI ai 2 NODI)
{
    nodeData* temp = node1;
    node1 = node2;
    node2 = temp;
}

void adjustIndex(nodeData* nodes, int* order, int a, int b) // Questa funzione serve per aggiornare l'ARRAY "order", che tiene traccia dell'ORDINE CORRETTO dei NODI in un MIN-HEAP
{
    order[nodes[a].nodeNumber] = a;
    order[nodes[b].nodeNumber] = b;
}

void minHeapify(nodeData* &nodes, int q_size, int current, int* order)
{
	// nodes --> un puntatore alla struttura dati nodeData
	// q_size --> Indica la DIMENSIONE corrente della CODA del MIN-HEAP
	// current --> indica l'indice(valore intero) del nodo corrente all'interno del MIN-HEAP
	// order --> Array che tiene traccia dell'ordine dei nodi nel MIN-HEAP
	 
    int smallest = current; // smallest viene inizializzato all'INDICE del NODO CORRENTE
    int left = 2 * current + 1; // Calcolo indici figlio sinistro
    int right = 2 * current + 2; // Calcolo indici figlio destro
	
    if (left < q_size && nodes[left].dist < nodes[smallest].dist) // Se l'INDICE del FIGLIO SINISTRO è minore della DIMENSIONE della CODA e se la DISTANZA del nodo SINISTRO rispetto al NODO di ORIGINE è MINORE della DISTANZA tra NODO di ORIGINE e NODO più PICCOLO(nel senso di DISTANZA) allora
	{
		smallest = left; // Aggiorno l'indice del nodo più PICCOLO(in termini di distanza) con il valore dell'INDICE nuovo
	}
        
    if (left < q_size && nodes[right].dist < nodes[smallest].dist) // Se l'INDICE del FIGLIO SINISTRO è minore della DIMENSIONE della CODA e se la DISTANZA del nodo DESTRO rispetto al NODO di ORIGINE è MINORE della DISTANZA tra NODO di ORIGINE e NODO più PICCOLO(nel senso di DISTANZA) allora
    {
		smallest = right; // Aggiorno l'indice del nodo più PICCOLO(in termini di distanza) con il valore dell'INDICE nuovo
	}
	
    if (smallest != current) // Se l'INDICE del NODO con la distanza minore è DIVERSO dall'INDICE del NODO CORRENTE allora
	{
        swap(nodes[current], nodes[smallest]); // Scambio il NODO corrente con il NODO più piccolo(ovvero quello con la DISTANZA MINORE dall'ORIGINE)
        adjustIndex(nodes, order, current, smallest); // Aggiusta l'INDICE dei NODI nel MIN-HEAP
		
        if (smallest == current) // Quando il nodo corrente corrisponderà a quello con la DISTANZA minore dall'ORIGIINE allora termina l'ESECUZIONE di questo METODO
		{
			return;
		}
		else
		{
			minHeapify(nodes, q_size, smallest, order); // Richiama la FUNZIONE RICORSIVAMENTE, cambiando solo il valore 
		}   
    }
}

// Questa funzione diminuisce la DISTANZA di un nodo specifico all'interno di un min-heap rappresentato dalla struttura 'nodeData'
void decreaseDistance(nodeData* &nodes, int q_size, int current, int* order)
{
	// nodes --> un puntatore alla struttura dati nodeData
	// q_size --> Indica la DIMENSIONE corrente della CODA del MIN-HEAP
	// current --> indica l'indice(valore intero) del nodo corrente all'interno del MIN-HEAP
	// order --> Array che tiene traccia dell'ordine dei nodi nel MIN-HEAP
	
    // Se l'indice corrente è inferiore a zero, viene impostato a zero per evitare valori negativi
    if (current < 0)
	{
        current = 0;
    }
    
    // Inizialmente, si assume che il nodo corrente sia il più piccolo
    int smallest = current;
    
    // Calcola gli indici dei figli sinistro e destro del nodo corrente all'interno dell'heap
    int left = 2 * current + 1;
    int right = 2 * current + 2;

    // Controlla se il figlio sinistro esiste ed è minore del nodo più piccolo corrente
    if (left < q_size && nodes[left].dist < nodes[smallest].dist)
	{
		smallest = left;
	}
        
    // Controlla se il figlio destro esiste ed è minore del nodo più piccolo corrente
    if (left < q_size && nodes[right].dist < nodes[smallest].dist)
	{
		smallest = right;
	}
        
    // Se il nodo più piccolo è diverso dal nodo corrente, scambia i valori dei due nodi e aggiorna gli indici nel min-heap
    if (smallest != current)
	{
        swap(nodes[current], nodes[smallest]);
        adjustIndex(nodes, order, current, smallest);
        // Richiama ricorsivamente la funzione 'decreaseDistance' sul genitore del nodo corrente per mantenere l'ordinamento dell'heap
        decreaseDistance(nodes, q_size, (smallest-1) / 2, order);
    }
}


void minHeapRootDelete (nodeData* &nodes, int q_size, int current, int* order)
{
	// nodes --> un puntatore alla struttura dati nodeData
	// q_size --> Indica la DIMENSIONE corrente della CODA del MIN-HEAP
	// current --> indica l'indice(valore intero) del nodo corrente all'interno del MIN-HEAP
	// order --> Array che tiene traccia dell'ordine dei nodi nel MIN-HEAP
	
    // Scambio il nodo radice con l'ultimo nodo dell'heap e poi applico minHeapify alla radice
    swap(nodes[0], nodes[q_size - 1]);  // Scambio il primo nodo (radice) con l'ultimo nodo
    adjustIndex(nodes, order, 0, q_size - 1);  // Aggiorno gli indici dopo lo scambio, solitamente è sempre così dopo uno SWAP c'è ADJUSTINDEX
    minHeapify(nodes, q_size - 1, current, order);  // Eseguo minHeapify sulla radice
}


void shortest_path(int n, nodeData* &nodes, int* order)
{
	// n --> Indica l'INDICE del NODO di PARTENZA da cui calcolare il PERCORSO più breve
    nodes[n].dist = 0;  // Imposta la distanza del nodo di partenza a 0

    // Garantita la presenza di un heap minimo poiché gli altri nodi hanno distanza infinita
    swap(nodes[n], nodes[0]);  // Scambia il nodo di partenza con la radice dell'heap
    adjustIndex(nodes, order, n, 0);  // Aggiorna gli indici dei nodi dopo lo scambio

    int q_size = num_nodi;  // Contatore degli elementi in coda

    while (q_size != 0)  // Continua finché ci sono nodi in coda
	{
        print_graph(nodes, order);  // Stampa lo stato attuale del grafo

        // Trova il minimo in coda (che in un heap minimo è il nodo di indice 0)
        // Riduce la dimensione della coda per eseguire correttamente la cancellazione
        if (nodes[0].dist < INFINITO)  // Controlla se la distanza del nodo corrente è finita
		{
            nodes[0].visitato = 1;  // Imposta il nodo corrente come visitato
            int u = nodes[0].nodeNumber;  // Ottiene l'indice del nodo corrente
            int current = 0;  // Imposta l'indice corrente a 0
            minHeapRootDelete(nodes, q_size, current, order);  // Esegue la cancellazione della radice dall'heap minimo
            q_size--;  // Riduce la dimensione della coda

            // Itera attraverso tutti i nodi adiacenti al nodo corrente
            Node_t* elem = Archiconnessi[u]->head;
            while (elem != NULL)
			{
                int v = elem->val;  // Ottiene l'indice del nodo adiacente
                int alt = nodes[order[u]].dist + elem->w;  // Calcola la distanza alternativa
                if (alt < nodes[order[v]].dist)  // Se la distanza alternativa è minore della distanza corrente
				{
                    nodes[order[v]].dist = alt;  // Aggiorna la distanza del nodo adiacente
                    // Indice per eseguire minHeapify sul solo nodo il cui valore di distanza viene modificato
                    nodes[order[v]].prev = u;  // Imposta il nodo corrente come nodo precedente
                    decreaseDistance(nodes, q_size, (order[v] - 1) / 2, order);  // Riduce la distanza del nodo e aggiorna l'heap
                }
                elem = elem->next;  // Passa all'elemento successivo
            }
        }
        else
		{  // Se la coda non è vuota e i nodi non sono raggiungibili, termina
            q_size = 0;
        }
    }
    print_graph(nodes, order);  // Stampa lo stato finale del grafo
}


int parse_cmd(int argc, char **argv)
{
    /// controllo argomenti
    int ok_parse = 0;
    for (int i = 1; i < argc; i++)
	{
        if (argv[i][1] == 'v')
		{
            details = 1;
            ok_parse = 1;
        }
		
        if (argv[i][1] == 'g')
		{
            graph = 1;
            ok_parse = 1;
        }
    }

    if (argc > 1 && !ok_parse)
	{
        printf("Usage: %s [Options]\n", argv[0]);
        printf("Options:\n");
        printf("  -verbose: Abilita stampe durante l'esecuzione dell'algoritmo\n");
        printf("  -graph: creazione file di dot con il grafo dell'esecuzione (forza d=1 t=1)\n");
        return 1;
    }

    return 0;
}

// L'algoritmo di Bellman-Ford calcola il percorso più breve da un nodo sorgente a tutti gli altri nodi nel grafo.
// La funzione riceve l'indice del nodo di partenza, un riferimento ai dati dei nodi e un ordine specificato.
// Inizializza la distanza del nodo di partenza a 0 e scambia il nodo di partenza con il primo elemento dell'array.
// Imposta l'indice del nodo di partenza nell'ordine specificato come primo elemento.

void bellmanFord(int n, nodeData* &nodes, int* order)
{
	// n --> Archiconnessi' l'INDICE del NODO di partenza da cui l'algoritmo di BELLMAN-FORD calcola il percorso più breve verso tutti i NODI del GRAFO
    nodes[n].dist = 0;
    swap(nodes[n], nodes[0]);
    adjustIndex(nodes, order, n, 0);

    // Esegue l'algoritmo di Bellman-Ford per calcolare il percorso più breve per ogni nodo nel grafo
    for (int u = 0; u < num_nodi; u++)
	{
        // Inutile ai fini dell'algoritmo, ma utile per evidenziare i cerchi visitati di nero
        nodes[order[u]].visitato = 1;
        Node_t* elem = Archiconnessi[u]->head;

        // Itera su tutti i nodi adiacenti al nodo corrente
        while (elem != NULL)
		{
            print_graph(nodes, order);

            int v = elem->val;
            // Se il percorso corrente è più corto del percorso precedentemente registrato, aggiorna la distanza e il nodo precedente
            if (nodes[order[u]].dist + elem->w < nodes[order[v]].dist)
			{
                nodes[order[v]].dist = nodes[order[u]].dist + elem->w;
                nodes[order[v]].prev = u;
            }
            elem = elem->next;
        }
    }

    // Stampa il grafo dopo ogni iterazione dell'algoritmo di Bellman-Ford
    print_graph(nodes, order);

    // Verifica se ci sono cicli di peso negativo nel grafo
    for (int u = 0; u < num_nodi; u++)
	{
        Node_t* elem = Archiconnessi[u]->head;
        while (elem != NULL)
		{
            int v = elem->val;
            // Se viene trovato un ciclo di peso negativo, stampa un messaggio di errore e interrompe il programma
            if (nodes[order[u]].dist + elem->w < nodes[order[v]].dist)
			{
                cout << "Il grafo ha un ciclo di peso negativo";
                exit(1);
            }
            elem = elem->next;
        }
    }
}


// Funzione principale del programma
int main(int argc, char **argv)
{
    // Verifica se sono presenti comandi e ne gestisce l'eventuale errore
    if (parse_cmd(argc, argv))
        return 1;

    // Verifica se è attiva l'opzione di stampa del grafo e, in caso affermativo, apre il file per il grafo
    if (graph)
    {
        output_grafo.open("graph.dot");
        output_grafo << "digraph g" << endl;
        output_grafo << "{ " << endl;
        output_grafo << "Node [shape=none]" << endl;
        output_grafo << "rankdir=\"LR\"" << endl;
    }

    // Inizializza il numero di nodi e la struttura dati nodes
    int N = 5;
    num_nodi = N;
    nodeData* nodes = new nodeData[N];

    // Inizializza i nodi con i rispettivi numeri
    for (int i = 0; i < num_nodi; i++)
    {
        nodes[i].nodeNumber = i;
    }

    // Inizializza la struttura dati per gli archi e l'array di ordine
    Archiconnessi = new List_t *[num_nodi];
    int order[num_nodi];

    // Inizializza l'array di ordine con gli indici corrispondenti
    for (int i = 0; i < num_nodi; i++)
    {
        order[i] = i;
    }

    // Costruisce il grafo e gli archi in base alle specifiche
    for (int i = 0; i < num_nodi; i++) 
    {
        Archiconnessi[i] = crea_lista();

        if (i == 0)
		{
			puntatore_globale = Archiconnessi[i];
		}
    }

    inserisci_in_testa(Archiconnessi[0], 1, 10);  // Arco positivo
    inserisci_in_testa(Archiconnessi[1], 2, 5);   // Arco positivo
    inserisci_in_testa(Archiconnessi[2], 3, -3);  // Arco negativo
    inserisci_in_testa(Archiconnessi[3], 4, 2);   // Arco positivo

    // Stampa il grafo iniziale con un arco negativo
    print_graph(nodes, order);

    // Esegue l'algoritmo per il percorso pi� breve (da implementare)
    shortest_path(0, nodes, order);

    // Creazione di un nuovo grafo con un ciclo di archi di peso tutti negativi
    for (int i = 0; i < num_nodi; i++)
    {
        Archiconnessi[i] = crea_lista();
    }

    inserisci_in_testa(Archiconnessi[0], 1, -1);
    inserisci_in_testa(Archiconnessi[1], 2, -1);
    inserisci_in_testa(Archiconnessi[2], 3, -1);
    inserisci_in_testa(Archiconnessi[3], 0, -1);  // Crea un ciclo di archi negativi

    // Stampa il grafo con un ciclo di archi negativi
    print_graph(nodes, order);

    // Se l'opzione di stampa del grafo � attiva, prepara il footer e chiude il file
    if (graph)
    {
        output_grafo << "}" << endl;
        output_grafo.close();
        cout << " File graph.dot scritto" << endl
             << "****** Creare il grafo con: neato graph.dot -Tpdf -o graph.pdf" << endl;
    }

    return 0;
}
