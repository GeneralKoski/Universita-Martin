#include <iostream>
using namespace std;


class Tris {
	private:
		char matrix[3][3];
		int winner;

		void initialize() {
			for (int i = 0; i < 3; i++)
				for (int j = 0; j < 3; j++)
					matrix[i][j] = '-';
			winner = -1;
		}

		bool playerWon(char c) {
			if (matrix[0][0] == c && matrix[0][1] == c && matrix[0][2] == c)
				return true;
			if (matrix[0][0] == c && matrix[1][0] == c && matrix[2][0] == c)
				return true;
			if (matrix[0][0] == c && matrix[1][1] == c && matrix[2][2] == c)
				return true;
			if (matrix[2][0] == c && matrix[1][1] == c && matrix[0][2] == c)
				return true;
			if (matrix[2][0] == c && matrix[2][1] == c && matrix[2][2] == c)
				return true;
			if (matrix[0][2] == c && matrix[1][2] == c && matrix[2][2] == c)
				return true;
			if (matrix[1][0] == c && matrix[1][1] == c && matrix[1][2] == c)
				return true;
			if (matrix[0][1] == c && matrix[1][1] == c && matrix[2][1] == c)
				return true;
			return false;
		}

	public:
		Tris() {
			initialize();
		} 

		// X
		void movePlayer1(int row, int col) {
			if (row < 0 || row > 2 || col < 0 || col > 2)
				throw string("Posizione non valida");
			else if (isFull())
				throw string("Gioco terminato");
			else if (matrix[row][col] != '-')
				throw string("Cella occupata");

			matrix[row][col] = 'X';
			if (player1Won())
				winner = 1;
		}

		// O
		void movePlayer2(int row, int col) {
			if (row < 0 || row > 2 || col < 0 || col > 2)
				throw string("Posizione non valida");
			else if (isFull())
				throw string("Gioco terminato");
			else if (matrix[row][col] != '-')
				throw string("Cella occupata");

			matrix[row][col] = 'O';
			if (player2Won())
				winner = 2;
		}

		bool player1Won() {
			return playerWon('X');
		}

		bool player2Won() {
			return playerWon('O');
		}		

		int getWinner() {
			return winner;
		}

		bool someoneWon() {
			return winner != -1;
		}

		bool isFull() {
			for (int i = 0; i < 3; i++)
				for (int j = 0; j < 3; j++)
					if (matrix[i][j] == '-')
						return false;
			return true;
		}

		void print() {
			for (int i = 0; i < 3; i++) {
				for (int j = 0; j < 3; j++)
					cout << matrix[i][j] << " ";
				cout << endl;
			}
		}
};


int main() {
	Tris game;
	bool player = false;

	do {
		int row, col;

		try {
			game.print();
			if (!player) {
				// Giocatore 1
				cout << "Giocatore 1: "; 
				cin >> row >> col;
				game.movePlayer1(row, col);
			} else {
				// Giocatore 2
				cout << "Giocatore 2: ";
				cin >> row >> col;
				game.movePlayer2(row, col);
			}
		} catch (const string& e) {
			cout << "Mossa non valida: " << e << endl;
			continue;
		}

		player = !player;
	} while (!game.someoneWon() && !game.isFull());

	game.print();

	if (game.getWinner() == -1)
		cout << "Patta!" << endl;
	else
		cout << "Vincitore: Giocatore " << game.getWinner() << endl;
	return 0;
}