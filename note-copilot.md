# Revisione delle infografiche sulla modellistica e la qualità dell’aria

**Data della revisione:** 2026-11-09  
**Ambito:** coerenza con il rapporto *Air quality modelling for air quality policy*, accuratezza tecnico-normativa, efficacia grafica e manutenzione del repository.

## 1. Valutazione generale

Il progetto è nel complesso coerente con il rapporto di riferimento. Le 17 infografiche seguono la struttura dei capitoli 1-6 e coprono quasi tutti i principali messaggi operativi.

La base progettuale è solida:

- stile grafico coerente e riconoscibile;
- contenuti in italiano e inglese;
- output vettoriali;
- separazione tra testi e geometrie;
- attenzione all’accessibilità;
- schede delle fonti dettagliate.

Prima di completare l’intera serie, conviene consolidare alcuni aspetti scientifici, normativi, grafici e infrastrutturali. La criticità principale non riguarda lo stile, già convincente, ma il rischio di concentrare troppe precisazioni tecniche e normative in una singola slide.

## 2. Correzioni tecnico-normative per slide

### Slide 1 - Il ruolo della modellistica nella AAQD

- Integrare i riferimenti agli articoli **8(7b), 17(4) e 23(5)**.
- Precisare che i modelli diventano obbligatori **due anni dopo l’adozione** dell’atto di esecuzione previsto dall’art. 8(7a), non immediatamente dopo.
- Nel percorso del superamento, rendere graficamente evidente anche il controllo finale del rispetto dei limiti nell’intera zona, non soltanto nelle stazioni.

### Slide 2 - Anatomia di un sistema modellistico

Aggiungere due elementi rilevanti del rapporto:

- la speciazione chimica delle emissioni;
- il rischio di doppio conteggio nelle catene multiscala.

### Slide 4 - MQI e MQO

- Precisare che il denominatore dell’MQI combina quadraticamente le incertezze di misura e di modello.
- Aggiungere che, con meno di circa **10 stazioni**, la raccomandazione FAIRMODE è verificare **MQI ≤ 1 in tutte le stazioni**, senza applicare il 90° percentile.
- Per recuperare spazio, questa informazione può sostituire il dettaglio «R: correlazione · SD: ampiezza», meno importante per il messaggio principale.

#### Uso del target plot

La normalizzazione storica del target plot FAIRMODE non coincide necessariamente con la formula MQI introdotta nella nuova AAQD.

**Intervento suggerito:**

- evitare, finché l’equivalenza non è verificata, l’affermazione «distanza dal centro = MQI»;
- in alternativa, presentare il target plot come rappresentazione concettuale;
- verificare l’equivalenza con la documentazione FAIRMODE/DELTA aggiornata prima della pubblicazione.

### Slide 6 - Progettazione della rete

- Esplicitare le tre condizioni previste dall’art. 9(3).
- Chiarire che la riduzione fino al **50% delle stazioni fisse** riguarda le zone sopra la soglia di valutazione, ma non sopra i valori limite o i valori obiettivo.

### Slide 8 - Indicatori delle situazioni di superamento

- Precisare che l’indicatore relativo a vegetazione ed ecosistemi si applica agli standard per la protezione della vegetazione.
- Precisare che la lunghezza stradale è pertinente quando il superamento è attribuibile al traffico.

### Slide 12 - Inquinamento transfrontaliero e prodotti UE

Separare più chiaramente i prodotti: la riduzione del **15%** riguarda il prodotto CAMS *Country & city impact evaluation*, non SHERPA in generale.

### Slide 14 - I sette scenari emissivi

La differenza tra scenario di riferimento e scenario a zero emissioni non rappresenta necessariamente, in modo direttamente additivo, la quota attribuibile alle emissioni della zona. La cautela è particolarmente importante per l’ozono e il particolato secondario, a causa delle non linearità chimiche.

**Testo suggerito:**

> La differenza rispetto allo scenario a zero emissioni indica l’effetto della rimozione delle emissioni della zona nello specifico scenario modellato.

### Slide 15 - Proiezioni

Il rapporto presenta **quattro opzioni meteorologiche**, non tre. La quarta riguarda l’impiego di dati meteorologici statisticamente rappresentativi per modelli gaussiani o CFD.

### Slide 17 - La previsione come innesco dei piani a breve termine

Aggiungere che:

- la preparazione del piano richiede l’analisi degli episodi su un periodo di **3-5 anni**;
- possono servire strumenti diversi dal modello previsionale;
- il modello previsionale può non essere adatto al source apportionment.

## 3. Verifiche normative da chiudere

Prima della prima release pubblica occorre risolvere gli elementi ancora contrassegnati con `◐` o `✖` nei file `sources.md`, in particolare per l’infografica sulla rappresentatività spaziale:

- data di applicazione della decisione di esecuzione;
- valore minimo di tolleranza per il PM10;
- numerazione e contenuto degli articoli richiamati;
- formulazione italiana ufficiale della definizione;
- periodicità della revisione.

La release dovrebbe distinguere chiaramente tra:

1. contenuti verificati sul testo normativo vigente;
2. contenuti derivati da bozze o fonti secondarie;
3. aspetti ancora in attesa di verifica.

## 4. Miglioramenti grafici ed editoriali

### 4.1 Ridurre la densità testuale

Le slide **2, 4, 11, 14 e 17** presentano il maggiore rischio di sovraccarico. Anche le infografiche su fitness-for-purpose, ESI e scenari emissivi contengono pannelli più vicini a schede tecniche che a infografiche.

**Interventi suggeriti:**

- mantenere quattro pannelli per slide;
- assegnare a ogni pannello un solo messaggio principale;
- ridurre il testo visibile di circa il **25-30%**;
- trasferire precisazioni, eccezioni e riferimenti completi nelle note, in `sources.md` o in un documento tecnico di accompagnamento.

### 4.2 Variare gli archetipi grafici

La ripetizione di pannelli bianchi, frecce e fascia finale garantisce coerenza, ma può diventare monotona in una serie di 17 slide.

Si suggeriscono almeno tre archetipi riutilizzabili:

1. **Processo**, per sequenze operative e roadmap.
2. **Confronto**, per metodi, scenari e alternative.
3. **Mappa o sistema**, per assessment, rete, esposizione e scale modellistiche.

Palette, tipografia e fascia conclusiva possono restare comuni a tutta la serie.

### 4.3 Alleggerire il pannello ESI

Nella slide ESI, il pannello con i cinque passaggi è informativo ma visivamente dominante, soprattutto per la lunghezza dei dettagli sulla vegetazione.

In slide è sufficiente mantenere la sequenza:

> area di superamento → superficie → popolazione → strade → vegetazione

Le esclusioni dettagliate dell’Allegato IV possono essere spostate nelle note o in `sources.md`.

### 4.4 Estendere il layout mobile

Attualmente solo l’infografica sulla rappresentatività spaziale dispone di una versione verticale.

**Interventi suggeriti:**

- rendere il layout mobile un requisito comune;
- mantenere come soglia minima indicativa un corpo del testo pari ad almeno il **2,4% della larghezza della tela**, come già indicato nel README;
- per le nuove infografiche, valutare un approccio mobile-first e derivare successivamente la versione 16:9.

## 5. Struttura e manutenzione del repository

### 5.1 Uniformare i nomi delle cartelle

La struttura attuale alterna un nome descrittivo, come `01-rappresentativita-spaziale`, a cartelle identificate soltanto da numeri.

**Convenzione suggerita:**

```text
01-rappresentativita-spaziale/
02-mqi-mqo/
03-fitness-for-purpose/
04-indicatori-superamento/
05-scenari-emissivi/
```

Ogni cartella dovrebbe contenere una struttura uniforme:

```text
build.py
strings/
├── it.yaml
└── en.yaml
sources.md
out/
```

### 5.2 Escludere i metadati Git dagli archivi

Gli archivi distribuiti non dovrebbero contenere `.git/`, hook di esempio, oggetti o log locali.

Per creare uno ZIP a partire dall’ultimo commit del branch corrente:

```bash
git archive --format=zip \
  --prefix=infographics-aaqd/ \
  -o latest.zip HEAD
```

Il comando include soltanto i file tracciati e già registrati nel commit. I file generati in `out/` vengono inclusi solo se sono tracciati da Git.

Verifica del contenuto:

```bash
unzip -l latest.zip
```

### 5.3 Aggiornare il README

Il README descrive principalmente l’infografica 01 e non riflette ancora lo stato complessivo della serie.

Aggiungere una tabella con tutte le 17 infografiche e i relativi stati:

- prevista;
- in sviluppo;
- graficamente completa;
- verificata sul rapporto tecnico;
- verificata sul testo normativo vigente;
- disponibile in italiano e inglese;
- disponibile nei formati wide e mobile.

### 5.4 Aggiungere controlli automatici

Una pipeline, per esempio basata su GitHub Actions, dovrebbe verificare:

- build di tutte le versioni italiane e inglesi;
- validità sintattica dei file YAML;
- presenza delle chiavi obbligatorie;
- corretta generazione di SVG, PNG e PDF;
- presenza di testi fuori pannello o oltre la larghezza disponibile;
- presenza di `sources.md` per ogni infografica;
- presenza di elementi ancora marcati `◐` o `✖`;
- confronto visivo delle immagini con una baseline approvata.

### 5.5 Separare versione normativa e versione grafica

È utile distinguere l’aggiornamento del contenuto giuridico dalla versione grafica del progetto.

**Metadati suggeriti:**

```yaml
graphic_version: 0.2.0
legal_review_date: 2026-11-09
directive: EU 2024/2881
implementing_acts:
  - EU 2026/1208
source_document: Air quality modelling for air quality policy, 2025
```

Questi dati potrebbero alimentare automaticamente:

- i sottotitoli delle infografiche;
- `CITATION.cff`;
- il README;
- le schede delle fonti.

## 6. Modello di riferimento per la serie

L’infografica sulla rappresentatività spaziale costituisce attualmente il riferimento più completo perché combina:

- progressione narrativa chiara;
- esempi numerici leggibili;
- distinzione esplicita tra dati reali e sintetici;
- versioni italiana e inglese;
- layout wide e mobile;
- fonti associate ai singoli elementi;
- SVG accessibile e modificabile.

Questo modello dovrebbe essere generalizzato senza imporre la medesima composizione grafica a tutti gli argomenti.

## 7. Ordine operativo suggerito

1. Correggere i punti scientifici delle slide MQI/MQO e scenari emissivi.
2. Chiudere le verifiche normative ancora aperte nei file `sources.md`.
3. Definire la struttura standard delle cartelle e uno schema YAML comune.
4. Aggiornare il README e `CITATION.cff`.
5. Introdurre i controlli automatici di build e impaginazione.
6. Definire i tre archetipi grafici della serie.
7. Proseguire con le nuove infografiche applicando il modello consolidato.

## 8. Sintesi conclusiva

La serie risulterà più efficace se ogni infografica privilegerà un messaggio visivo centrale e affiderà alle note e alle schede delle fonti le eccezioni, i riferimenti normativi e il dettaglio metodologico. La priorità immediata è consolidare l’accuratezza scientifica e normativa delle slide già sviluppate, quindi uniformare la struttura del repository prima di estendere il modello alle restanti infografiche.
