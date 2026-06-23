import java.util.Scanner;

public class Task7 {

	public static void inverti(int[] array, int init, int end) {
		if (init >= end) 
			return;
		else {
			int tmp = array[init];
			array[init] = array[end];
			array[end] = tmp;
			inverti(array, init + 1, end -1);
		}
	}
	
	public static void printArray(int[] array, int len) {
		for (int i = 0; i < len; i++)
			System.out.print(array[i] + " ");
		System.out.println();
	}
	
	public static void main(String[] args) {
		int l;
		Scanner sc = new Scanner(System.in);
		System.out.println("Quanti elementi vuoi inserire?");
		l = sc.nextInt();

		int[] a = new int[l];
		for (int i = 0; i < l; i++) {
			System.out.print("Inserire elemento: ");
			a[i] = sc.nextInt();
		}
		sc.close();
		printArray(a, l);
		inverti(a, 0, l-1);
		printArray(a, l);
	}
}
