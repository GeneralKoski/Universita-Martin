import java.util.Scanner;

public class Task1 {
	
	public static char convert(char c) {
		if (c < 97 || c > 122)
			return '?';
		else if (c >= 97 && c < 120)
			return (char) (c + 3);
		else 
			return (char) (((c + 3) % 122) + 97);
	}
	
	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		char x, y, z;
		
		// next() function returns the next token/word in the input 
		// as a string and charAt(0) function returns the first character in that string
		x = sc.next().charAt(0);
		y = sc.next().charAt(0);
		z = sc.next().charAt(0);
		sc.close();

		System.out.println(convert(x));
		System.out.println(convert(y));
		System.out.println(convert(z));
	}
}
