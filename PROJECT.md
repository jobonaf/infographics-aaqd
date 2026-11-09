# Progetto delle infografiche sulla modellistica e la qualità dell’aria

**Data di consolidamento:** 2026-11-09  
**Formato previsto:** 17 infografiche in slide 16:9, con possibile versione mobile  
**Lingue:** italiano e inglese  
**Riferimento principale:** *Air quality modelling for air quality policy*

## 1. Obiettivo

Il progetto prevede una serie coordinata di **17 infografiche** dedicate al ruolo della modellistica nell’applicazione della direttiva sulla qualità dell’aria, nella valutazione, nella progettazione delle reti, nel source apportionment, nei piani e nei sistemi di previsione.

La serie è articolata in **6 capitoli**. Ogni slide sviluppa un tema attraverso più pannelli coordinati e deve poter essere utilizzata in presentazioni, attività formative, gruppi tecnici e pubblicazioni.

## 2. Struttura generale

| Capitolo | Tema | Slide |
|---:|---|---:|
| 1 | Quadro e qualità | 1-4 |
| 2 | Rete di monitoraggio | 5-6 |
| 3 | Valutazione | 7-9 |
| 4 | Source apportionment | 10-12 |
| 5 | Piani e roadmap | 13-15 |
| 6 | Previsioni | 16-17 |

---

# Capitolo 1 - Quadro e qualità

## 1. Il ruolo della modellistica nella AAQD

**Riferimento:** §1.3

### Contenuti

1. **I cinque ambiti applicativi**
   - rete di monitoraggio;
   - valutazione;
   - source apportionment;
   - piani;
   - previsioni.

2. **Il percorso di un superamento**
   - osservazione;
   - indicatori della situazione di superamento, ESI;
   - source apportionment;
   - piano;
   - ritorno del source apportionment alla valutazione.

3. **Atti di esecuzione e scadenze**
   - riferimenti agli articoli 8(7a), 16(4) e 18(5);
   - dopo l’adozione degli atti previsti, modelli o misure indicative diventano obbligatori sopra i valori limite, secondo le scadenze applicabili.

### Impostazione grafica suggerita

Schema dei cinque ambiti applicativi affiancato da un percorso circolare o a flusso che rappresenti il trattamento di un superamento.

## 2. Anatomia di un sistema modellistico

**Riferimento:** §1.4

### Contenuti

1. **Famiglie di modelli**
   - modelli deterministici;
   - modelli data-driven.

2. **Risoluzione**
   - temporale: valori annuali, percentili e altre metriche;
   - spaziale: capacità di riprodurre la variabilità attesa;
   - confronto esemplificativo tra NO₂ e PM2,5.

3. **Input principali**
   - emissioni: griglia, quota, profilo temporale e speciazione;
   - meteorologia;
   - condizioni al contorno o concentrazioni di fondo.

4. **Catene modellistiche per scala**
   - regionale: 50-1 km;
   - urbana: 3 km-100 m;
   - locale: 100-10 m;
   - microscala.

### Impostazione grafica suggerita

Sezione esplosa di un sistema modellistico, con input a sinistra, processi al centro e scale di applicazione a destra.

## 3. Fitness-for-purpose

**Riferimento:** §1.5

### Contenuti

1. **I sei criteri**
   - risoluzione;
   - processi;
   - sorgenti;
   - meteorologia;
   - validazione e MQO;
   - documentazione.

2. **QA/QC degli input**
   - controllo prima di ogni simulazione;
   - pre-processing semiautomatico;
   - tracciabilità e riproducibilità.

3. **Applicazione nei cinque ambiti**
   - rete;
   - valutazione;
   - source apportionment;
   - piani;
   - previsioni.

4. **Oltre l’MQO**
   - l’MQO è necessario ma non sufficiente;
   - DELTA Tool e checklist FAIRMODE;
   - standard CEN in preparazione.

### Impostazione grafica suggerita

Tre pannelli: criteri e input, declinazione nei cinque ambiti, strumenti che completano l’MQO.

## 4. MQI e MQO

**Riferimento:** §3.4

### Contenuti

1. **MQI**
   - errore RMSE rapportato all’incertezza ammessa di misura e modello;
   - nel lungo termine l’indicatore è ricondotto al bias.

2. **Incertezza ammessa**
   - `U_O,fix` specifica per inquinante;
   - rapporto β;
   - andamento a tratti rispetto al valore limite.

3. **MQO**
   - MQI al 90° percentile ≤ 1;
   - verifica a breve e lungo termine;
   - circa 10 stazioni come numero minimo raccomandato da FAIRMODE;
   - con meno stazioni, verifica in tutte le stazioni.

4. **Validazione indipendente**
   - necessaria con data fusion o assimilazione;
   - leave-one-out in sei passaggi;
   - alternativa: sottoinsieme di stazioni riservato alla validazione.

### Impostazione grafica suggerita

Formula semplificata, andamento dell’incertezza, verifica dell’MQO e sequenza leave-one-out. L’eventuale target plot deve essere presentato con cautela, verificandone la coerenza con la formulazione AAQD.

---

# Capitolo 2 - Rete di monitoraggio

## 5. Rappresentatività spaziale

**Stato:** già sviluppata; da armonizzare con il capitolo 2 durante la revisione finale della serie.

### Contenuti

Mantenere i pannelli della versione esistente, inclusi:

- definizione dell’area di rappresentatività;
- confronto tra punti di campionamento;
- trattamento delle aree escluse;
- esempi numerici e cartografici;
- distinzione tra dati reali e dati sintetici.

### Formati

- versione wide 16:9;
- versione mobile verticale.

## 6. Progettazione della rete

**Riferimento:** §2.3

### Contenuti

1. **Hotspot**
   - modello ad alta risoluzione;
   - criteri di localizzazione dell’Allegato IV;
   - esclusione dei luoghi non valutabili;
   - campagne parallele.

2. **Fondo**
   - aree prossime all’esposizione media;
   - siti non dominati da una singola sorgente.

3. **Riduzione delle stazioni fisse**
   - fino al 50% in meno ai sensi dell’art. 9(3);
   - esplicitazione delle tre condizioni applicabili.

4. **Revisione periodica**
   - almeno ogni cinque anni;
   - supportata da modelli o misure indicative.

### Impostazione grafica suggerita

Confronto hotspot/fondo, seguito da uno schema decisionale per la riduzione delle stazioni e la revisione della rete.

---

# Capitolo 3 - Valutazione

## 7. Modellistica di assessment, sorgenti naturali e sabbiatura/salatura

**Riferimenti:** §§3.1-3.3 e 3.7

### Contenuti

1. **Ruolo nella valutazione**
   - quando il modello è obbligatorio;
   - impieghi nella valutazione della qualità dell’aria.

2. **Sorgenti naturali**
   - art. 16;
   - sottrazione dei superamenti attribuibili alle sorgenti naturali.

3. **Strumenti disponibili**
   - CAMS per incendi, polveri e sale marino;
   - SDS-WAS per le polveri desertiche.

4. **Sabbiatura e salatura invernale**
   - art. 17;
   - modellistica non ancora raccomandata per l’erraticità dei fattori di emissione.

### Impostazione grafica suggerita

Percorso di assessment con un ramo per le sorgenti naturali e uno per sabbiatura e salatura.

## 8. Indicatori delle situazioni di superamento, ESI

**Riferimento:** §3.5

### Contenuti

1. **Indicatori e GIS**
   - superficie;
   - popolazione;
   - vegetazione ed ecosistemi;
   - lunghezza delle strade;
   - elaborazione GIS.

2. **Stima passo dopo passo**
   - estensione del superamento;
   - superficie;
   - popolazione;
   - strade;
   - vegetazione;
   - esclusioni previste dall’Allegato IV.

3. **Fattori che modificano il risultato**
   - risoluzione della popolazione, almeno 0,5 km² o più fine;
   - canyon stradali;
   - popolazione statica o dinamica;
   - rete stradale utilizzata.

4. **Due livelli di stima**
   - stima iniziale con le aree di rappresentatività per il reporting annuale;
   - stima completa nel piano;
   - rischio di sovrastima o sottostima.

### Impostazione grafica suggerita

Sequenza GIS: area di superamento → superficie → popolazione → strade → vegetazione.

## 9. Esposizione della popolazione e impatto sanitario

**Riferimento:** §3.6

### Contenuti

1. **Perché andare oltre gli ESI**
   - gli effetti sanitari si verificano anche sotto i valori limite.

2. **Metodo**
   - sovrapposizione tra popolazione e concentrazioni;
   - funzioni concentrazione-risposta OMS 2021;
   - risoluzione indicativa di 1 km² in area urbana e 5-10 km² in area rurale.

3. **Cautele**
   - doppio conteggio degli effetti di PM2,5 e NO₂;
   - gruppi vulnerabili;
   - contributi distinti per sorgente e scala.

4. **Questioni aperte**
   - alta risoluzione;
   - canyon stradali;
   - popolazione dinamica.

### Impostazione grafica suggerita

Sovrapposizione di tre livelli: concentrazione, popolazione e funzione concentrazione-risposta, con output sanitario finale.

---

# Capitolo 4 - Source apportionment

## 10. Source apportionment: definizioni e metodi

**Riferimenti:** §§4.1-4.2

### Contenuti

1. **Finalità**
   - requisito dell’Allegato VIII;
   - distinzione tra sorgenti naturali e antropiche.

2. **Famiglie di metodi**
   - modelli orientati alla sorgente;
   - modelli orientati al recettore, applicabili al particolato.

3. **Tipi di risultato**
   - impatti potenziali per la pianificazione;
   - contributi;
   - incrementi per la valutazione.

4. **Aspetti metodologici**
   - linearità per gli inquinanti non reattivi;
   - non linearità per quelli reattivi;
   - dettaglio emissivo per combustibile, tecnologia e processo.

### Impostazione grafica suggerita

Confronto tra metodi a sorgente e a recettore, collegato ai tre tipi di risultato.

## 11. I sei passi del source apportionment

**Riferimento:** §4.3

### Contenuti

1. **Passo 1: scelta del metodo**
   - tabelle verde, arancio e grigio;
   - scelta per inquinante e finalità.

2. **Passo 2: scelta degli strumenti**
   - prodotti UE;
   - modelli orientati alla sorgente;
   - modelli orientati al recettore.

3. **Passi 3-4: qualità e reporting**
   - QA/QC della simulazione di riferimento;
   - reporting.

4. **Passi 5-6: valutazione e interpretazione**
   - assenza di osservazioni dirette dei contributi;
   - uso dei traccianti;
   - interpretazione dei risultati.

### Impostazione grafica suggerita

Roadmap in sei passi, raggruppata in quattro pannelli per evitare sovraccarico.

## 12. Inquinamento transfrontaliero e prodotti UE

**Riferimento:** §4.4

### Contenuti

1. **Finalità**
   - coordinamento tra paesi;
   - limiti dei soli piani nazionali.

2. **Scelta del metodo**
   - source apportionment geografico;
   - tagging per i contributi;
   - impatti per valutare misure estere;
   - ozono e verifica della linearità.

3. **Limiti delle condizioni al contorno**
   - non distinguono la categoria emissiva;
   - non rappresentano direttamente le riduzioni.

4. **Prodotti europei per lo screening**
   - CAMS;
   - SHERPA;
   - contributi per paese;
   - valutazioni d’impatto con riduzioni emissive;
   - disponibilità limitata a un sottoinsieme di città per alcuni prodotti.

### Impostazione grafica suggerita

Mappa transfrontaliera con flussi tra paesi, affiancata da un confronto tra prodotti e risultati disponibili.

---

# Capitolo 5 - Piani e roadmap

## 13. Dalla valutazione al piano

**Riferimenti:** §§5.1-5.2

### Contenuti

1. **Piani e roadmap**
   - art. 19;
   - art. 18.

2. **Tempistica**
   - piano entro due anni dall’anno del superamento;
   - durata non superiore a quattro anni;
   - aggiornamento al terzo anno;
   - roadmap entro il 31 dicembre 2028 per la proroga.

3. **Continuità con la valutazione**
   - il modello deve collegare emissioni e concentrazioni;
   - la sola fusione dei dati non è sufficiente.

4. **Dallo screening alle misure**
   - screening con impatti potenziali;
   - catalogo delle misure;
   - vincoli legali e finanziari;
   - accettazione delle misure.

### Impostazione grafica suggerita

Linea temporale normativa associata a un percorso valutazione → screening → misure → piano.

## 14. I sette scenari emissivi

**Riferimento:** §5.2.4

### Contenuti

1. **Reference e baseline**
   - scenario di riferimento;
   - baseline con misure già adottate;
   - collegamento alla NECD.

2. **Scenari di riduzione**
   - riduzione massima fattibile;
   - riduzioni necessarie per il rispetto dei limiti.

3. **Zero emissioni e misure**
   - scenario a zero emissioni con possibili non linearità;
   - misure singole;
   - pacchetti di misure.

4. **AEI e sensitività**
   - media di tre anni confrontata con i tre anni di dieci anni prima;
   - scenari best/worst;
   - possibile riduzione operativa a due scenari.

### Impostazione grafica suggerita

Sette scenari disposti in sequenza o matrice, con evidenza degli scenari obbligatori, esplorativi e di sensitività.

## 15. Proiezioni

**Riferimento:** §5.3

### Contenuti

1. **Fondo e trend**
   - scenari IIASA 2025-2050;
   - prodotti CAMS.

2. **Meteorologia**
   - anno di riferimento;
   - periodo di 3-5 anni con condizioni medie, migliori e peggiori;
   - anno rappresentativo;
   - dati statisticamente rappresentativi per modelli gaussiani o CFD.

3. **Correzione del bias**
   - cause del bias;
   - correzione assoluta;
   - correzione relativa;
   - correzione combinata;
   - nessuna correzione;
   - mappa del bias.

4. **Valutazione dinamica**
   - uso di scenari storici secondo §5.4.3.

### Impostazione grafica suggerita

Catena di proiezione con tre blocchi principali: fondo e trend, meteorologia, correzione del bias.

---

# Capitolo 6 - Previsioni

## 16. Sistemi di previsione

**Riferimenti:** §§6.1-6.3

### Contenuti

1. **Obblighi informativi**
   - soglie di informazione e allarme per SO₂, NO₂, PM2,5, PM10 e O₃.

2. **CAMS**
   - ensemble di 11 modelli;
   - orizzonte di 96 ore;
   - risoluzione di circa 10 km;
   - prodotti statistici per le grandi città;
   - downscaling nazionale.

3. **Sistema nazionale o locale**
   - modello;
   - input;
   - dominio;
   - condizioni al contorno;
   - output.

4. **Incertezza e validazione**
   - MQIf e MQOf;
   - confronto con il modello di persistenza;
   - verifica giornaliera;
   - verifica di lungo periodo.

### Impostazione grafica suggerita

Architettura a livelli: CAMS → downscaling nazionale → sistema locale → prodotti previsionali e verifica.

## 17. La previsione come innesco dei piani a breve termine

**Riferimenti:** §§6.4-6.5

### Contenuti

1. **Procedura per un sistema robusto**
   - definizione dello scopo;
   - scelta del fornitore;
   - regione target;
   - configurazione e verifica del sistema.

2. **Operatività quotidiana**
   - affidabilità delle catene;
   - tempestività dei dati;
   - manutenzione;
   - continuità del servizio;
   - comunicazione dell’incertezza.

3. **Piani a breve termine**
   - art. 20;
   - rischio di superamento della soglia di allarme;
   - preparazione e attuazione con responsabilità separate.

4. **Casi particolari**
   - ozono: piano non richiesto se il potenziale di riduzione è trascurabile;
   - particolato: possibili misure limitate all’informazione sui comportamenti.

### Impostazione grafica suggerita

Catena previsionale → soglia decisionale → attivazione del piano, con un ramo specifico per ozono e particolato.

---

# 3. Principi comuni di progettazione

## Contenuto

- Un messaggio principale per pannello.
- Quattro pannelli come riferimento, adattabili alla natura del tema.
- Dettagli normativi, eccezioni e fonti estese in `sources.md` o nelle note.
- Distinzione esplicita tra dati osservati, dati modellati e dati sintetici.
- Verifica tecnico-scientifica e normativa prima della pubblicazione.

## Stile grafico

La coerenza della serie è affidata a:

- palette comune;
- tipografia comune;
- numerazione uniforme;
- fascia conclusiva o messaggio chiave;
- componenti SVG condivisi.

Per evitare monotonia, sono previsti tre archetipi:

1. **Processo**, per sequenze, procedure e roadmap.
2. **Confronto**, per metodi, alternative e scenari.
3. **Mappa o sistema**, per reti, scale, esposizione e catene modellistiche.

## Formati

- wide: 1920 × 1080, rapporto 16:9;
- mobile: 1200 × 1960, quando previsto;
- SVG come formato sorgente modificabile;
- PNG e PDF come esportazioni opzionali.

## Lingue e accessibilità

- testi separati in `strings/it.yaml` e `strings/en.yaml`;
- geometria condivisa tra le lingue;
- titolo e descrizione alternativa negli SVG;
- testi vivi e gruppi grafici identificabili;
- contrasto e palette compatibili con le principali alterazioni della visione dei colori.

# 4. Stato iniziale del progetto

Al momento del consolidamento del progetto risultano sviluppate:

| # | Infografica | Stato sintetico |
|---:|---|---|
| 03 | Fitness-for-purpose | sviluppata, revisione editoriale pendente |
| 04 | MQI e MQO | sviluppata, revisione scientifica pendente |
| 05 | Rappresentatività spaziale | sviluppata in wide e mobile, revisione normativa pendente |
| 08 | Indicatori ESI | sviluppata, revisione editoriale pendente |
| 14 | Scenari emissivi | sviluppata, revisione scientifica pendente |

Le altre dodici infografiche sono previste dal progetto e saranno sviluppate secondo la numerazione definitiva indicata in questo documento.
