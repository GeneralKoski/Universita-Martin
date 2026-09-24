# La ricerca per numero d'atto

**Domanda.** In un documentale si cerca spesso un atto di cui si sa il numero.
Dove finisce l'atto giusto?

**Metodo.** Due atti di Crispiano, `doc-0001` (*Ordinanza N. 187*) e `doc-0002`
(*Determina N. 1223*). Elasticsearch interrogato con la query di produzione di
Documentale e con due varianti che isolano le cause; Koskidex letto da un
rapporto di `scripts/compare` già archiviato. Script: `posizioni.py`.

## Risultato

| Motore e configurazione | `ordinanza 187` | `determina 1223` |
|---|---|---|
| **Elasticsearch, produzione** | **12° su 85** | **5° su 8** |
| Elasticsearch senza refusi | 1° su 1 | 1° su 1 |
| Elasticsearch senza il campo `name` | 1° su 84 | 5° su 8 |
| Koskidex di oggi (and + euristico) | 1° su 1 | 1° su 52 |
| Koskidex or + euristico | 1° su 1.150 | 1° su 6.051 |
| Koskidex or + BM25 | 3° su 1.150 | 5° su 6.051 |

**La causa è la tolleranza ai refusi sui numeri.** Per Elasticsearch `187` è
una parola di tre caratteri e ammette un refuso: combacia con `18`, `17`, `137`,
`186`. Spenti i refusi, l'atto giusto è primo e unico in tutti e due i casi.

**`pathinfo()` la aggrava.** Il nome dell'atto giusto dentro Elasticsearch perde
il numero; e l'atto che vince si chiama *"ORDINANZA N. 18.2026"*, che
`pathinfo()` riduce a *"ORDINANZA N. 18"* prendendo `.2026` per un'estensione:
nel campo `name^5` combacia con `187` per un refuso. Togliendo `name`, per
l'ordinanza l'atto giusto torna primo; per la determina no, perché lì la
concorrenza sta nel riassunto.

**Da spiegare: BM25 peggiora la ricerca per numero in Koskidex** (3° e 5°
contro il 1° dell'euristico, a parità di recupero disgiuntivo). Non ancora
indagato.

Onestà sul confronto: Koskidex ha il nome intero, non quello troncato, e le sue
soglie non ammettono refusi su tre caratteri. Su `1223` le soglie coincidono
(un refuso per quattro caratteri) e Koskidex di oggi è comunque primo.

File d'esito: `2026-09-24T105848Z_esito.json`.
