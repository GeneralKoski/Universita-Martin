package esame;

public class Studente implements Comparable<Studente> {
	private final String nome;
	private final String cognome;
	private final String matricola;
	
	public Studente(String nome, String cognome, String matricola) {
		this.nome = nome;
		this.cognome = cognome;
		this.matricola = matricola;
	}
	
	@Override
	public int hashCode() {
		return matricola.hashCode();
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		Studente other = (Studente) obj;
		return matricola.equals(other.matricola);

	}

	@Override
	public String toString() {
		return "Studente [nome=" + nome + ", cognome=" + cognome + ", matricola=" + matricola + "]";
	}

	@Override
	public int compareTo(Studente o) {
		return matricola.compareTo(o.matricola);
	}
}


