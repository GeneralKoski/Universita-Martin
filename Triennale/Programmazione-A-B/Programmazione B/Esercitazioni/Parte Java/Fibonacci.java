import java.util.Scanner;

/**
 * Si scriva una funzione ricorsiva che prende in input un intero n 
 * e calcola l’n-esimo numero della sequenza di Fibonacci.
 *
 * @author <a href="mailto:vincenzo.arceri@unipr.it">Vincenzo Arceri</a>
 */
public class Fibonacci {
	
	/**
	 * Questa funzione calcola l'{@code n}-esimo 
	 * numero della sequenza di Fibonacci.
	 * 
	 * @param n indice
	 * @return {@code n}-esimo numero della sequenza di Fibonacci
	 */
	public static int fib(int n) {
		if(n == 1 || n == 0) 
			return 1;
		else
			return fib(n-1) + fib(n-2);
	}
	
	/**
	 * Punto d'ingresso del programma
	 * 
	 * @param args parametri esterni
	 */
	public static void main(String[] args) {
		int n;
		Scanner sc = new Scanner(System.in);
		
		do {
			System.out.println("Inserire un valore: ");
			n = sc.nextInt();
		} while (n < 0);
		
		sc.close();
		System.out.println("Fibonacci: " + fib(n));
		
	}

}
