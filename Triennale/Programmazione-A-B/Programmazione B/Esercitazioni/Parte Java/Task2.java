import java.util.Scanner;

public class Task2 {

	public static void main(String[] args) {
		int n;
		Scanner sc = new Scanner(System.in);

		do {
			System.out.println("Inserire un valore >= 0");
			n = sc.nextInt();
		} while (n <= 0);

		sc.close();
		
		int i = 0, j = 0;

		while (i < n){
			while (j < i + 1){
				System.out.print("* "); 
				j++;
			}
			j = 0;
			System.out.println(""); 
			i++;
		} 

		i -= 2;
		while (i >= 0){
			while (j < i + 1){
				System.out.print("* "); 
				j++;
			}
			j = 0;
			System.out.println(""); 
			i--;
		}   
	}
}
