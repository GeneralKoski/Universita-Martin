# Quanto testo legge bge-m3 attraverso Ollama

**Domanda.** La sezione 7.1 della tesi dà per scontato che il testo intero di
un atto di Crispiano, fra 5 e 13 mila caratteri, stia nel contesto di `bge-m3`,
8.192 token. Ma Koskidex chiede i vettori a Ollama senza dire quanto contesto
usare, e Ollama ha un contesto predefinito suo. Fino a quanti token del testo
arriva davvero il vettore, quanti atti ne restano tagliati, e basta chiedere a
Ollama un contesto più grande?

**Dichiarato.** Preparando le misure sulle known-item umane ho fatto una prova
di sviluppo, non archiviata: testi lunghi con lo stesso inizio e code diverse.
Fino a circa 1.500 token i vettori differiscono; da circa 2.000 token in su
sono identici, e Ollama riporta al più 2.048 token letti. Le previsioni qui
sotto sono scritte dopo quella prova, e quelle sul troncamento a 2.048 ne
dipendono: sono una conferma formale, non un'ipotesi. Le altre (il contesto
più grande, quanti atti superano la soglia) non le ho misurate.

## Metodo

`misura.py`, che parla con Ollama direttamente (non passa da Koskidex), sul
corpus esportato da Documentale (`beir-full`, che per i 563 atti di Crispiano
ha il testo intero e per gli altri la scheda):

1. **Dove taglia.** Un testo lungo fatto dei testi interi di Crispiano uno
   dopo l'altro; per ogni lunghezza del prefisso (da 1.000 a 40.000 caratteri)
   due richieste con lo stesso prefisso e due code diverse. Se i due vettori
   coincidono, la coda non è stata letta. Si registra la differenza massima
   fra le componenti e i token che Ollama dice di aver letto
   (`prompt_eval_count`). Con il contesto predefinito e con `num_ctx` 8.192.
2. **Quanti atti.** Per ciascuno dei 563 testi interi e per ogni scheda, i
   token letti da Ollama con `num_ctx` 8.192, una richiesta per testo: quanti
   superano 2.048 token, quanti arrivano a 8.192 (e quindi sono tagliati anche
   così). Lo stesso per i documenti di SciFact e NFCorpus (aggiunto sotto).

Modello `bge-m3`, con l'impronta registrata nel file di esito.

## Prima di misurare

1. **Con il contesto predefinito Ollama legge al più 2.048 token**: da lì in
   su i due vettori coincidono (differenza massima 0), sotto no.
2. **Con `num_ctx` 8.192 legge fino a 8.192 token**: i vettori differiscono
   fino a quella lunghezza e coincidono oltre.
3. **Fra il 30% e il 70% dei 563 testi interi supera 2.048 token**: 5-13 mila
   caratteri di italiano amministrativo sono dell'ordine di 1.500-4.000 token.
4. **Meno del 5% dei testi interi arriva a 8.192 token.**
5. **Nessuna scheda supera 2.048 token** (la più lunga ha 1.409 caratteri):
   nessun vettore misurato finora nella tesi, tutti su schede o su abstract,
   è stato tagliato. Per SciFact e NFCorpus la misura non si fa qui.

Se la 5 cade, i numeri del capitolo 7 vanno rimisurati.

**Aggiunto dopo le previsioni, prima di misurare.** La guardia della 5 vale
solo se copre tutte le collezioni del capitolo 7: `misura.py` conta i token
anche dei documenti di SciFact e NFCorpus, titolo e testo in un campo come in
valutazione. Previsione, nello stesso spirito:

6. **Meno dell'1% dei documenti di SciFact e di NFCorpus supera 2.048 token**,
   e i numeri del capitolo 7 cambiano al più in modo trascurabile.
