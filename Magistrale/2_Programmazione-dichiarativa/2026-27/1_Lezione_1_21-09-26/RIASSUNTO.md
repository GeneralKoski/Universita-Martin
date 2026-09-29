# Lezione 1 - 21/09/2026: IA simbolica e programmazione dichiarativa

Fonte: `Slide.pdf` (5 lavagne scritte a mano, senza testo). Lezione introduttiva: dove sta la programmazione dichiarativa rispetto all'IA di oggi.

## Specifiche, sforzo e LLM
- Grafico con **sforzo** sull'asse x e **ottimizzazione delle specifiche** sull'asse y: la curva cresce lentamente e poi si impenna. Ottenere specifiche ottime (il punto rosso in cima) costa uno sforzo sempre maggiore.
- Accanto al grafico: **LLM che scrivono codice** e **human over the loop**, cioè l'umano che supervisiona il ciclo invece di scriverne ogni passo.
- La lavagna non dice esplicitamente cosa indichino le due frecce (rossa orizzontale e nera verticale): probabilmente il passaggio dallo sforzo di scrivere codice allo sforzo di scrivere specifiche. Da confermare con la registrazione o i propri appunti.

## Dov'è la comprensione/intelligenza nell'IA?
- Nell'IA attuale c'è **solo dataset + training + rete + contesto**.
- **IA sub-simbolica**: ML, e dentro di essa l'IA generativa (GEN).
- **IA simbolica**: l'altro ramo, quello su cui si basa il corso.

## Storia: due filoni
**Reti neurali - bottom-up**
- Crescita della **potenza di calcolo** (le **GPU**) → **LLM**.
- Risultato: modelli **generali**.

**Simbolico - top-down**
- **Dimostratori automatici** (theorem proving).
- **Knowledge Representation (KR)**.
- **Automated Reasoning (AR)**.
- Risultato: **applicazioni specialistiche**.

## Ragionamento ad alto livello
- Si parte da un **problema**, lo si scompone in alternative (alcune scartate) e si procede per **deduzioni** successive fino alla soluzione (**OK!**). Il cammino evidenziato va dal problema alla soluzione attraverso le deduzioni.
- La **conoscenza** che serve al ragionamento è **esplicita** e di tre tipi:
  - **common knowledge** (conoscenza comune);
  - **conoscenza specifica** del dominio;
  - **mancanza di conoscenza**: anche sapere cosa non si sa va rappresentato.

## Sub-simbolica vs simbolica

| | Sub-simbolica | Simbolica |
|---|---|---|
| Dati | tanti | pochi |
| Tipo di dato | poco significato | alto significato |
| Semantica dei dati | no | sì (posso interpretarli) |
| Velocità | alta | bassa |
| Affidabilità | no (~95%) | sì (100%) → **solver**, es. **SAT solver** |
| Interpretabile | no | sì |
| Black box | sì | no |

## Programmazione imperativa vs dichiarativa

**Imperativa**
- **Specifiche** informali (pre/post condizioni).
- **Modello algoritmico** e **implementazione**: li scrive il programmatore. Nel dichiarativo questa parte non c'è (il "NO" sull'implementazione).
- **Manutenzione**: **bug fixing** ed **evoluzione**.

**Dichiarativa**
- **Specifiche + KR**: le specifiche sono un **contratto matematico** e sono **eseguibili**, quindi **specifiche = programma**.
- Si pone un **goal** → il **solver** (basato su **automated reasoning**) → **risposta**.
- Il bug fixing si fa direttamente sulle specifiche, non su un'implementazione separata.

## Da ricordare
- Due filoni storici dell'IA: **reti neurali bottom-up** (→ GPU → LLM, generali) e **simbolico top-down** (theorem proving, KR, AR, applicazioni specialistiche).
- La tabella sub-simbolica vs simbolica: dati, significato, semantica, velocità, affidabilità (95% vs 100%), interpretabilità, black box.
- Nel paradigma dichiarativo **le specifiche sono il programma**: si scrivono specifiche + conoscenza, si pone un goal e il solver trova la risposta.
- La conoscenza esplicita comprende anche la **mancanza di conoscenza**.
- Testo di riferimento del corso: `../0_Introduzione/Dispensa Dovier-Formisano.pdf`.
