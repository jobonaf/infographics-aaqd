# 06 · Proiezioni: come stimare le concentrazioni future: fonti e stato di verifica

Scheda aggiornata il 2026-11-08 (seconda versione). Stato: ✔ letto nel testo · ◐ da sintesi, resa redazionale o schema · ✖ da verificare.
Fonte principale: Commissione europea, DG Ambiente, *Air quality modelling for air quality policy: a technical support document* (2025), §5.3 e §5.4 (documento caricato in conversazione). La direttiva (UE) 2024/2881 **non è stata riletta direttamente**: i riferimenti agli allegati sono quelli citati dal documento.
Nella slide: sigle spiegate (IIASA, CAMS, AEI, PM10), pochi termini inglesi in parentesi nella versione italiana (background, bias), esempio numerico inventato e dichiarato, nessuna SRA.

Scelte editoriali (su indicazione dell'autore)
- **Tolta la mappa con le stazioni** e la discussione su cosa «vedono» le stazioni. Resta una sola frase: «La proiezione riguarda l'intera zona».
- Il filo della slide è l'elenco delle **cinque incertezze da controllare** nei piani (§5.4.2): emissioni future, fondo, meteorologia, correzione del bias, sensibilità dinamica del modello. È nella fascia in basso.

| Elemento nella figura | Fonte | Stato | Nota |
|---|---|---|---|
| La proiezione riguarda l'intera zona | §5.3.1 (e indicazione dell'autore) | ✔ | Il documento dice anche che la valutazione è richiesta in ogni punto di campionamento in superamento (Allegato VIII, A, punto 7, lettera d); la frase della slide è stata semplificata su indicazione dell'autore |
| Cinque incertezze da controllare: emissioni future, selezione dei dati meteo, scelte sulla correzione del bias, scenari per trasporto a lunga distanza e fondo, sensibilità dinamica del modello; l'Allegato VIII, A, punto 8(f) chiede informazioni su queste incertezze, dove possibile | §5.4.2 | ✔ | |
| Emissioni future incerte (efficacia e attuazione delle misure, trend delle attività); caso migliore e peggiore | §5.4.2 e §5.2.4 | ✔ | La frase del riquadro è una sintesi redazionale |
| Fondo = concentrazioni da fuori dell'area modellata; cambia nel tempo con le politiche europee e nazionali | §5.3.2 | ✔ | |
| Dati già pronti: emissioni per paese 2025–2050 (IIASA); scenari europei CAMS | §5.3.2 | ✔ | IIASA = International Institute for Applied Systems Analysis; CAMS = Copernicus Atmosphere Monitoring Service (nomi estesi come nel documento) |
| **Non rappresentati** per spazio: dati giornalieri EMEP per 2030 e 2050 (3 scenari emissivi, anni meteo 2005 e 2015); coerenza con il programma nazionale di controllo dell'inquinamento (NAPCP) e rischio di doppio conteggio delle emissioni | §5.3.2 | ✔ | La prima versione della slide conteneva la frase su NAPCP; è stata tolta nella seconda |
| Sorgenti naturali: possono essere sottratte dai superamenti, se serve per rispettare il limite (esempi: incendi boschivi; il testo cita anche eruzioni, attività sismica e geotermica, eventi di vento forte, spruzzi marini, risospensione e trasporto di particelle naturali da regioni aride) | §5.3.4 e §3.7 | ✔ | Nella slide solo l'esempio degli incendi boschivi |
| Sale e sabbia sulle strade (solo PM10): sottraibili se si mostra che sono state prese misure ragionevoli; nelle proiezioni le loro emissioni restano quelle dell'anno di riferimento, se note, salvo riduzioni previste dal piano (allora si quantificano) | §5.3.4 | ✔ | |
| Meteo: non si prevede, si sceglie; quattro opzioni | §5.3.3 | ✔ | |
| Opzione 1 (anno di riferimento): consigliata per ridurre i calcoli e per collegare direttamente valutazione e correzione del bias; da verificare la rappresentatività | §5.3.3 | ✔ | |
| Opzione 2 (ultimi 3–5 anni: media, migliore, peggiore): più completa e robusta perché le misure devono valere in tutti gli anni; più calcoli | §5.3.3 | ✔ | |
| Opzione 3 (un anno rappresentativo, anche con i dati di misura): si perde il legame con l'anno di riferimento | §5.3.3 | ✔ | |
| Opzione 4 (dati meteo statistici, modelli su aree limitate): migliore e peggiore anno statistici | §5.3.3 | ✔ | «Modelli su aree piccole» è la resa breve di «models that cover limited areas» (es. fluidodinamici, gaussiani) |
| AEI: stessa meteorologia nell'anno di proiezione (es. 2030) e 10 anni prima (es. 2020), su 3 anni consecutivi; conta la variazione relativa | §5.3.3 | ✔ | |
| Cause del bias → metodi: differenza assoluta, relativa, combinata; si può anche non correggere | §5.3.5 | ✔ | Elenco delle cause (formulazione, impostazione concettuale, rappresentatività, meteorologia, emissioni, fonti mancanti, fondo) non riportato per ridondanza con i metodi |
| Esempio del grafico: il modello sottostima del 25 % (5 µg/m³) | §5.3.5, fig. 5-2 | ✔ | Stesso rapporto dell'esempio del documento |
| **Valori del grafico**: fondo 8 e fonte locale 7 (modello 15), misure 20; fondo −10 % e fonte locale −40 % a fine scenario (11,4 senza correzione); assoluta 16,4; relativa 15,2; combinata 15,6 (3 µg/m³ al fondo, 2 alla fonte locale) | — | n/a | **Inventati**, dichiarati nella figura; calcolati in `build.py`. Non sono risultati del documento |
| Provare la correzione sul passato: scenari di emissioni storici (es. il 2010 per correggere il 2020) per valutare la qualità dei metodi di correzione | §5.3.5 | ◐ | Resa sintetica; il documento descrive la valutazione dei metodi con scenari storici di emissioni, con gli anni riportati come esempio: verificare formulazione e anni |
| Sensibilità dinamica: andare bene oggi non garantisce di rispondere bene ai cambi di emissioni; si verifica con trend storici e con il modulo degli indicatori di pianificazione di DELTA (strumento FAIRMODE); confronto in condizioni diverse (notte/giorno, feriali/festivi) | §5.4.3 | ◐ | «Notte e giorno, feriali e festivi» riprende l'esempio del documento sulle condizioni diverse: verificare la formulazione esatta. «Chimica non lineare e particolato secondario» presenti nel testo ma tolti dalla slide |

Elementi volutamente **non** rappresentati: correzione del bias a livello di mappa; emulatori (§5.4.1, trattati nella slide 3); il numero di calcoli e gli scenari (slide 05); NAPCP ed EMEP; indicatori di estensione del superamento.
