package esame;
import java.util.HashSet;
import java.util.Set;

public class Esame {
	private final Set<Studente> studentiIscritti;
	private final Set<Verbalizzazione> verbalizzazioni;

	public Esame() {
		this.studentiIscritti = new HashSet<Studente>();
		this.verbalizzazioni = new HashSet<Verbalizzazione>();
	}

	public void iscrivi(Studente studente) throws StudenteGiaIscrittoException {
		if (studentiIscritti.contains(studente))
			throw new StudenteGiaIscrittoException();

		studentiIscritti.add(studente);
	}

	public void verbalizza(Studente st, int voto) throws StudenteGiaVerbalizzatoException, StudenteNonIscrittoException  {   

		if (!studentiIscritti.contains(st))
			throw new StudenteNonIscrittoException();

		Verbalizzazione verb = new Verbalizzazione(st, voto);

		for (Verbalizzazione v : verbalizzazioni)
			if (v.getStudente().equals(st))
				throw new StudenteGiaVerbalizzatoException();
		
		verbalizzazioni.add(verb);
	}
}

