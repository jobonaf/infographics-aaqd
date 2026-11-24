# 03 – Fitness-for-purpose (versione 3, archetipo G «hub»)

Fonte: «Air quality modelling for air quality policy: a technical support document», Commissione europea, aprile 2025. Pagine = pagine FISICHE del PDF. La Direttiva (UE) 2024/2881 NON è stata riletta direttamente.
Stati: ✔ letto nel testo · ◐ sintesi, resa redazionale, schema o esempio · ✖ da verificare.

| Elemento | Fonte (sezione / pagina) | Stato | Nota |
|---|---|---|---|
| Titolo: un modello non è buono o cattivo in assoluto, è adatto o no allo scopo | §3.3, p. 45 | ✔ | «there are no good or bad models»; qualità relativa all'applicazione |
| Sei criteri (risoluzione, processi, sorgenti, meteorologia, validazione e MQO, documentazione) | §1.5, p. 24 (da Denby et al., EEA 2011) | ✔ | Etichette abbreviate a 2-3 parole: ◐ |
| Gli input vanno controllati prima di ogni simulazione | §1.5, p. 24 | ✔ | «before any single model run»; non solo in fase di sviluppo |
| MQO necessario ma non sufficiente | §3.4.5, p. 51; §3.3, p. 46 | ✔ | Nelle istruzioni indicato come §3.4.4: nel PDF è §3.4.5. P. 46: la fitness-for-purpose è «più che superare l'MQO» |
| Spiegazione di «MQO» in figura («obiettivo di qualità della modellistica; soglia per lo scarto tra modello e misure») | §3.3, p. 45 (indicatori statistici contro le misure; MQO dice se la qualità è sufficiente) | ◐ | Resa redazionale; la definizione formale (§3.4.2) non è tra le pagine lette |
| Esempio «NO₂ urbano: strade e canyon» | §3.3, p. 46 | ✔ | Sintesi: il modello deve riprodurre fondo urbano e stazioni da traffico (moduli per strade aperte e canyon stradali) |
| Stessa domanda, criteri diversi per ambito | §1.5, p. 24-25; §3.3, p. 46 | ◐ | P. 25: i criteri saranno raffinati per i vari domini; p. 46: i principi valgono anche per piani, previsioni e SA |
| Cinque ambiti di applicazione (rete di monitoraggio, valutazione, attribuzione delle sorgenti, piani e roadmap, previsioni); in inglese «application», non «domain» (ambiguo con il dominio geografico) | §1.6, p. 25 (capitoli 2-6) | ◐ | Nomi e icone redazionali; l'MQO non è citato nella riga perché vale solo per la valutazione (§3.4.5, p. 51) |
| Riga «processi pertinenti»: adatti a scala, applicazione e inquinante | §1.5, p. 24 | ✔ | Sintesi del secondo criterio |
| Riga «sorgenti»: es. previsioni, il riscaldamento domestico varia con la temperatura | §1.4.3, p. 21 | ✔ | Previsioni richiedono emissioni dinamiche per settori legati alla meteorologia, come il riscaldamento residenziale |
| Riga «meteorologia»: risoluzione simile a quella del modello di qualità dell'aria | §1.4.4, p. 21 | ✔ | Per dati da modello meteorologico; altrimenti verificare che catturi i processi che guidano gli inquinanti |
| Riga «documentazione»: sistema e validazione descritti per l'applicazione | §1.5, p. 24 | ✔ | Il riferimento al calcolo dell'MQO da riportare (§3.4.5, p. 51) vale solo per la valutazione: non usato |
| Icone | – | ◐ | Set di common/layout.py; «wave» ripetuto per meteorologia e previsioni |

Nessun valore numerico né esempio inventato nella figura.

## Elementi volutamente non rappresentati
- Secondo criterio, variante per i modelli data-driven (dati di addestramento sufficienti e rappresentativi, §1.5, p. 24).
- Condizioni «più severe» per source apportionment e piani (suggerite dalle istruzioni): non trovate nelle p. 45-46; il testo dice che i principi valgono per tutti gli ambiti, con la condizione severa sulla risoluzione riferita alla valutazione (§3.3, p. 46). ✖ se si vuole usarle, cercarle nei capitoli 4 e 5.
- Tabella 1-1 (§1.4.2, p. 19-20): risoluzioni spaziali indicative (≤ 2 500 m urbano, ≤ 10 000 m rurale), non riportate per non allungare l'esempio sulla risoluzione.
- Strumenti pre-processing semiautomatici, tracciabilità e riproducibilità degli input (§1.5, p. 24).
- Strumenti, checklist e schema di reporting FAIRMODE, norma CEN (§3.4.5, p. 51); DELTA Tool omesso (la nota 11 del PDF lo dà non allineato, la regola 5.10 oggi allineato).
- Collaborazione tra modellisti, gestori delle reti ed esperti di emissioni (§1.5, p. 24).
- Tier, MoNET, codici colore SA, emulatori, tabella per ambito.
