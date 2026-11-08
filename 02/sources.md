# 02 · MQI e MQO: fonti e stato di verifica

Scheda redatta il 2026-11-07. **Non sostituisce la lettura del testo vigente.** Stato: ✔ letto nel testo · ◐ da fonte secondaria o da riassunto · ✖ da verificare.

Fonti principali
- Documentazione FAIRMODE/DELTA sul *target plot* (Thunis et al., 2012-2013; presentazioni DELTA 2014; atti Harmo): **solo per il pannello 3**. Il documento tecnico della Commissione nomina il target diagram soltanto per le previsioni (§6.3), non per la valutazione
- Commissione europea, DG Ambiente, *Air quality modelling for air quality policy: a technical support document* (2025), cap. 3, §3.4 (documento caricato in conversazione)
- Direttiva (UE) 2024/2881, Allegato V, punto A, tabelle 1 e 2 (CELEX 32024L2881): **non riletta direttamente**; i valori sono presi dalla tabella `T_DATA_QUALITY` di AQ Framework SNPA (trascrizione dell'Allegato V) e confrontati con il documento tecnico

| Elemento nella figura | Fonte | Stato | Nota |
|---|---|---|---|
| MQI = RMSE / √(U_O² + U_M²); a lungo termine |BIAS| al posto dell'RMSE | Doc. tecnico §3.4.1, p. 36 | ✔ | Formula riportata come nel documento |
| U_M = β · U_O,fix (modello = misure fisse × rapporto massimo β) | Doc. tecnico §3.4.1, p. 36 | ✔ | |
| U_O,fix(O) costante (= U_Ø = U_O,fix(VL)) fino al VL, poi proporzionale | Doc. tecnico §3.4.1, p. 36 e fig. 3-2 | ✔ | Per il PM10 annuo la curva del documento vale 4 fino a 20 µg/m³ e 14 a 70 µg/m³: coincide con la formula usata nel codice |
| PM10 annuo: VL = 20 µg/m³, U_O,fix(VL) = 4,0 µg/m³ (20 %) | Doc. tecnico fig. 3-2; AQ Framework SNPA `T_DATA_QUALITY` | ✔ doc. · ◐ Allegato V | Confrontare con la tabella 1 dell'Allegato V nella Gazzetta Ufficiale |
| β a lungo termine: PM2,5 1,7 · PM10 1,3 · NO2 1,4 | AQ Framework SNPA `T_DATA_QUALITY` | ◐ | **Da confrontare con l'Allegato V, tabella 1**; il documento tecnico rimanda alla stessa tabella senza ripetere i valori nel testo letto |
| MQO soddisfatto se MQI ≤ 1 in almeno il 90 % delle stazioni, a breve e a lungo termine (fascia in basso e intestazione del pannello 3) | Doc. tecnico §3.4; FAIRMODE (guidance MQO e DELTA) | ◐ | Il criterio del 90 % è confermato da fonti FAIRMODE; verificare formulazione e pagina nel documento |
| Target plot: assi = CRMSE e bias normalizzati; distanza dal centro = MQI; cerchio MQI = 1 (MQO) e cerchio 0,5 (modello entro l'incertezza di misura) | FAIRMODE/DELTA (Thunis et al.; atti Harmo) | ◐ | Normalizzazione nella figura: denominatore dell'MQI del documento tecnico (√(U_O² + U_M²)); nelle fonti FAIRMODE storiche è 2·RMSU. La distanza dal centro è comunque l'MQI |
| Zone del target plot: bias + in alto, bias − in basso; a sinistra prevale l'errore di correlazione (R), a destra quello di ampiezza (SD) | FAIRMODE/DELTA | ◐ | Convenzione di segno di CRMSE (positivo se σ_modello > σ_osservato) da verificare sulla guida DELTA in uso |
| Il target plot si riferisce all'MQI a breve termine (RMSE); a lungo termine l'MQI usa solo il |bias| | Doc. tecnico §3.4.1, p. 36 | ✔ | |
| «circa 10 stazioni come minimo», raccomandazione FAIRMODE non presente nella direttiva | Doc. tecnico §3.4 | ◐ | Verificare formulazione e numero esatti |
| Con data fusion o assimilazione serve validazione indipendente; leave-one-out; sottoinsieme riservato | Doc. tecnico §1.4.6 e §3.4 | ◐ | La figura semplifica la procedura in 4 passi; il documento ne descrive 6. Verificare i passi e la citazione di 4D-Var e filtri di Kalman |
| «condizione necessaria ma non sufficiente» (fitness-for-purpose) | Doc. tecnico §1.5 e §3.4 | ◐ | Verificare formulazione |
| Dati delle serie (pannello 1) e dei 12 valori MQI (pannello 3) | — | n/a | Inventati, dichiarati nella figura. MQI90 = 0,97 è calcolato in `build.py` dai 12 valori sintetici |

Elementi volutamente **non** rappresentati: regola «con meno di 10 stazioni, MQI ≤ 1 in tutte» (tolta per spazio dopo il passaggio al target plot, da riprendere in una slide di approfondimento), incertezze a breve termine (24 h, 8 h, orarie; tabella 2 dell'Allegato V), valori per le misure indicative, aggiustamenti dell'MQI per l'incertezza dovuta al campionamento casuale.

Dopo la verifica sull'Allegato V: aggiornare gli stati qui sopra e la versione in `CITATION.cff`.
