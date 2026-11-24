# Fonti e verifica - 02 Anatomia di un sistema modellistico

Fonte: «Air quality modelling for air quality policy: a technical support document», Commissione europea, DG Ambiente (aprile 2025), §1.4 (pagine fisiche del PDF 17-23; pagina stampata + 12). Il testo vigente della Dir. (UE) 2024/2881 non è stato riletto direttamente.
Stati: ✔ letto nel testo · ◐ sintesi, resa redazionale, schema · ✖ da verificare.

| Elemento | Fonte | Stato | Nota |
|---|---|---|---|
| Modello deterministico = equazioni di fisica e chimica dell'atmosfera | §1.4, p. 17 | ✔ | Il documento elenca anche CTM, plume, street box, CFD: non rappresentati |
| Modello data-driven = relazioni empiriche (interpolazione, statistica, AI/ML) | §1.4, p. 17 | ✔ | Titolo e glossa ridotti a «relazioni empiriche, machine learning» |
| Ingressi: emissioni, meteorologia, condizioni al contorno o di fondo | §1.4.3-1.4.5, pp. 20-22 | ✔ | |
| Condizioni al contorno = inquinanti che entrano nel dominio | §1.4.5, p. 22 | ✔ | Parafrasi della definizione del documento |
| A scala urbana/locale le condizioni al contorno sono spesso sostituite da concentrazioni di fondo | §1.4.5, p. 22 | ✔ | Resa solo con «o di fondo» nell'etichetta |
| Le misure rientrano tramite data fusion / assimilazione | §1.4.6, pp. 22-23 | ✔ | |
| Data fusion = correzione a posteriori (offline); assimilazione = durante il calcolo (online) | §1.4.6, p. 22 | ◐ | Il documento chiama «data fusion» anche l'assimilazione offline (post-processing) e riserva «on-line» ai metodi con modello inverso o ensemble. La distinzione in figura è una semplificazione editoriale concordata |
| Scale: globale/regionale 50-1 km; urbana 3 km-100 m; locale 100-10 m; micro scala: metri | §1.4.7, p. 23 | ✔ | Nota 6 del documento: intervalli indicativi. «Globale/regionale» come nel testo, anche se 50 km è un limite basso per un modello globale |
| Nessun modello copre tutte le scale; alcune applicazioni combinano due o più modelli in una catena | §1.4.7, p. 23 | ✔ | Il documento non afferma che ogni scala abbia una catena propria: una catena può includere modelli a scale diverse |
| Ogni modello della catena fornisce le condizioni al contorno al successivo (globale → regionale → urbano) | §1.4.5, p. 22; §1.4.7, p. 23 | ◐ | Il testo descrive la cascata (globale, europeo, regionale, fondo urbano) per le concentrazioni di fondo a scala urbana; la formulazione generale è una resa redazionale |
| Forma a riquadri annidati (matrioska) | - | ◐ | Rappresentazione grafica; il documento non ha una figura delle scale |
| NO₂ vicino alle strade: risoluzione massima ≤ 100 m (canyon stradali) | Tab. 1-1, pp. 19-20 (stampate 7-8) | ✔ | Nota 2: 100 m è il massimo lungo l'asse della strada; in direzione perpendicolare va risolta la larghezza del canyon |
| PM₂,₅ di fondo regionale: ≤ 10 000 m (contesto rurale, «regional patterns») | Tab. 1-1, p. 20 | ✔ | Nel contesto urbano la stessa tabella indica ≤ 2 500 m |
| Perché la risoluzione conta: variabilità spaziale di NO₂ più marcata di quella di PM₂,₅ in ambiente urbano | §1.4.2, p. 18 | ✔ | Resa con i due valori di Tab. 1-1, senza frase |
| «Dimensione massima delle celle» | §1.4.2, p. 19 | ✔ | Il documento: «maximum model grid size» (e dettaglio dell'inventario delle emissioni) |
| Griglia di punti di «Concentrazioni» | - | ◐ | Schema illustrativo, campo liscio calcolato in build.py, senza valori né unità |
| Fascia: il modello è il cuore del sistema modellistico, che comprende anche dati in ingresso e scala; più modelli in catena | §1.4, pp. 17-23 | ◐ | Sintesi del messaggio della slide; la distinzione modello / sistema modellistico è editoriale |
| Icone per livello della matrioska (area, people, road, canyon) | - | ◐ | Scelte grafiche; nessuna numerazione dei blocchi |
| Icone e frecce | - | ◐ | Scelte grafiche |

Valori inventati: nessuno (tutti i numeri sono del documento).

## Elementi volutamente non rappresentati
- Elenchi di nomi di modelli e dei metodi di assimilazione (§1.4, §1.4.6).
- Requisiti di dettaglio sulle emissioni (griglia, quota di rilascio, profili temporali, speciazione chimica) e requisiti per area applicativa (§1.4.3).
- Risoluzione temporale, medie annuali e percentili (§1.4.1).
- Righe industria e riscaldamento domestico della Tab. 1-1; altri inquinanti.
- Meteorologia: osservazioni contro modello, anno medio o peggiore (§1.4.4).
- Doppio conteggio nelle catene modellistiche (§1.4.7).
- Natura ibrida di molti sistemi (§1.4).
- Validazione dei risultati con fusione/assimilazione (§1.4.6): argomento della slide 03.
