# 07 · Sorgenti naturali, sale e sabbia: fonti e stato di verifica

Scheda aggiornata il 2026-11-25. Stato: ✔ letto nel testo · ◐ da sintesi, resa grafica o esempio · ✖ da verificare.
Fonte principale: Commissione europea, DG Ambiente, *Air quality modelling for air quality policy: a technical support document* (2025), §3.7 (pagine fisiche 57-58) e §5.3.4 (p. 92, numero stampato 80) (documento caricato in conversazione). La direttiva (UE) 2024/2881 **non è stata riletta direttamente**: articoli e considerando sono quelli citati dal documento.
Archetipo F (albero decisionale), circa 94 parole in IT e 95 in EN (titolo, etichette e fascia; esclusi sottotitolo e testo alternativo), nessuna SRA, nessun valore numerico.

| Elemento nella figura | Fonte | Stato | Nota |
|---|---|---|---|
| Causa naturale → «si sottrae, se serve a rispettare il limite» | §5.3.4 (p. 92) | ✔ | Il testo dice che i contributi naturali si possono sottrarre se necessario per rispettare il limite |
| Esempi di sorgenti naturali: incendi boschivi, spruzzi marini, polvere da regioni aride, eruzioni | §5.3.4 (p. 92), §3.7 | ✔ | Il documento ne cita altri (risospensione e trasporto di particelle naturali, attività sismica e geotermica, vento forte): **ne sono mostrati 4 su più**, scelta redazionale; icone disegnate in `build.py` |
| Condizione «contributo determinato con sufficiente certezza» | §3.7 (p. 57), considerando 34 citato nel testo | ✔ | Il §5.3.4 parla anche di analisi adeguata del contributo. **Non** è formulato come obbligo esplicito di documentare: i dettagli di dimostrazione e sottrazione saranno fissati da un atto di esecuzione (art. 16(4)), non mostrato in figura |
| Sale e sabbia sulle strade: solo PM10 | §3.7, §5.3.4 | ✔ | «Polveri fini (PM10)» è la glossa redazionale della sigla |
| Sale/sabbia → «misure ragionevoli per ridurre le concentrazioni?» → sì: si sottrae; no: resta nel superamento | §5.3.4 (p. 92) | ◐ | Il «sì» è nel testo; il «no → resta nel superamento» è la lettura logica della condizione |
| Ramo «Altra causa → resta nel superamento» | — | ◐ | Deduzione logica: il documento non lo dice in modo esplicito. Il ramo completa l'albero |
| Nelle proiezioni: emissioni di sale e sabbia uguali a quelle dell'anno di riferimento (se note), salvo riduzioni previste dal piano, che si quantificano | §5.3.4 (p. 92) | ✔ | Le barre del riquadro sono **schematiche, senza valori**: la freccia indica il riporto dell'anno di riferimento alla proiezione, la terza barra più bassa le riduzioni del piano |
| «Modellistica non raccomandata: i fattori di emissione variano con pratiche locali e meteo» | §3.7 (p. 58) | ✔ | Il testo cita la guida del 2011, che non raccomanda la modellistica per sale e sabbia, e spiega che i fattori di emissione sono molto variabili. Formula scelta dall'utente tra due varianti |
| Fascia: «Sottrarre = escludere il contributo dal calcolo del superamento» | §3.7, §5.3.4 | ◐ | Definizione redazionale |
| Icone (fuoco, onde, polvere, eruzione, strada, sale) e colori dei terminali | — | ◐ | Resa grafica; fuoco, polvere, eruzione e sale sono definite in `build.py`, non in `layout.py` |

Elementi volutamente **non** rappresentati: metodi numerici per quantificare il contributo naturale o per sale e sabbia; elenco completo delle sorgenti naturali; prodotti CAMS e SDS-WAS; guida del 2011 per esteso; scadenza dell'atto di esecuzione (31 dicembre 2026).
✖ **Valori obiettivo**: nelle pagine lette non c'è nulla su eventuali condizioni specifiche per i valori obiettivo (il considerando cita solo valori limite e obblighi di riduzione dell'esposizione media). Non sono rappresentati; se serve, va riletta la direttiva.
