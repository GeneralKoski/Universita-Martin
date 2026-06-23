package esame;

public class Verbalizzazione {
	private final Studente studente;
	private final int esito;
	
	public Verbalizzazione(Studente studente, int esito) {
		this.studente = studente ;
		if (esito < 0 || esito > 30) 
			throw new RuntimeException();
		this.esito = esito;
	}
	
	public Studente getStudente() { 
		return studente ; 
	}
	
	public int getEsito() { 
		return esito;
	}
	
	@Override 
	public String toString() {
		return studente.toString() + " Esito : " + esito ;
	}
	
	@Override
	public boolean equals ( Object obj ) {
		if (this==obj) 
			return true;
		if (obj == null) 
			return false;
		if (this.getClass() != obj.getClass()) 
			return false;
		
		Verbalizzazione other = (Verbalizzazione)obj;
		return other.esito == esito && other.studente.equals(studente);
	}

	@Override 
	public int hashCode() { 
		return studente.hashCode() + 31 * esito;
	}
}

