# 03 · Fitness-for-purpose: fonti e stato di verifica

Scheda aggiornata il 2026-11-07. Stato: ✔ letto nel testo · ◐ da fonte secondaria o da riassunto · ✖ da verificare.
Fonte principale: Commissione europea, DG Ambiente, *Air quality modelling for air quality policy: a technical support document* (2025). La direttiva (UE) 2024/2881 **non è stata riletta direttamente**.
Principio editoriale della slide: ogni termine tecnico è spiegato nella figura (Tier, MoNET, codice colore, emulatori, QA/QC, MQO, FAIRMODE), senza rimandi al documento originale.

| Elemento nella figura | Fonte | Stato | Nota |
|---|---|---|---|
| Sei criteri di fitness-for-purpose | Doc. tecnico §1.5, da Denby et al. (EEA, 2011) | ✔ | «o dati di addestramento adeguati» per i modelli data-driven è nel testo |
| Controllo degli input prima di *ogni* simulazione; pre-processing semiautomatico, tracciabile, riproducibile | Doc. tecnico §1.5 | ✔ | |
| Rete di monitoraggio: quattro livelli (Tier) di metodo per le aree di rappresentatività: 1 giudizio esperto, 2 dati proxy o campagne di misura, 3 modelli fit-for-purpose, 4 modelli + misure aggiuntive; consigliato almeno il 3 | Doc. tecnico §2.2.2 e §2.4 | ✔ | Il documento precisa che il Tier 3 da solo può non bastare per i criteri di area minima rappresentativa (Allegato IV, punto B); non rappresentato |
| MoNET: applicazione web FAIRMODE; raggruppamento gerarchico delle zone per regime di inquinamento (andamento temporale e concentrazioni del modello); segnala stazioni ridondanti, lacune, incoerenze di classificazione | Doc. tecnico §2.3 e §2.4 | ✔ | Sintesi in una riga; «incoerenze di classificazione» omesse per spazio |
| Valutazione: riprodurre tutte le concentrazioni osservate (fondo e traffico), nello spazio e nel tempo | Doc. tecnico §3.3 | ✔ | |
| Source apportionment: metodo scelto per scopo (valutazione o piano) e inquinante; verde = adatto, arancio = adatto solo a condizioni specifiche, grigio = non adatto; esempio: modello a recettore per NO2 | Doc. tecnico §4.3.1 (tab. 4-1, 4-2) | ✔ | L'esempio del recettore per NO2 è citato nel testo come caso di grigio «per limiti intrinseci della formulazione» |
| Piani: legare emissioni e concentrazioni per scenari futuri; scala del modello = scala del superamento (hotspot, area più ampia, regione) | Doc. tecnico §5.4.1 | ✔ | |
| Emulatori: metodi statistici o di machine learning che ricreano la relazione emissioni–concentrazioni di un modello esistente; vantaggio: velocità | Doc. tecnico §5.4.1 | ✔ | La figura dice «più veloci» |
| Previsioni: validazione con misure conformi agli obiettivi di qualità dei dati dell'Allegato V; orizzonte completo, n ≥ 3 giorni; giorno per giorno e lungo periodo | Doc. tecnico §6.3 | ✔ | Non rappresentato: il requisito minimo del solo giorno 1 |
| Source apportionment e piani: condizioni più severe, soprattutto su emissioni e condizioni al contorno (barra ocra) | Doc. tecnico §3.3, ultimo capoverso | ✔ | |
| MQO necessario ma non sufficiente; DELTA Tool (FAIRMODE) calcola MQI e MQO con diagrammi e report armonizzati | Doc. tecnico §3.4.4 | ✔ | Nota sull'allineamento di DELTA alla AAQD rimossa su indicazione dell'autore (versione aggiornata nel frattempo) |
| FAIRMODE: criteri QA/QC, checklist, schema di reporting (Thunis e Tarrason, 2020) | Doc. tecnico §3.4.4 | ✔ | «forum europeo di modellazione della qualità dell'aria» è una descrizione redazionale di FAIRMODE |
| Norma CEN/TC 264/WG43 sugli obiettivi di qualità dei modelli, in preparazione | Doc. tecnico §3.4.4 | ✔ | Verificare lo stato attuale della norma |
| La direttiva chiede di riportare descrizione dell'applicazione e calcolo dell'MQO | Doc. tecnico §3.4.4 (che cita la AAQD) | ◐ | Verificare il riferimento di articolo/allegato nella direttiva |
| Non esistono modelli «buoni» o «cattivi»; qualità relativa agli obiettivi dell'applicazione (fascia in basso) | Doc. tecnico §3.3 | ✔ | |

Scelte grafiche: la barra ocra a destra dei riquadri indica le condizioni più severe (SA e piani); i colori verde/arancio/grigio dei chip sono quelli del codice del documento.
Elementi volutamente **non** rappresentati: elenco completo degli strumenti FAIRMODE (§7.2), limiti del Tier 3 rispetto ai criteri di area minima, dettaglio dei criteri per i singoli ambiti.
