# Note di revisione di Claude sulle infografiche

**Data:** 2026-11-10  
**Ambito:** archetipi grafici, distribuzione degli archetipi sulle 17 slide e proposta di riprogettazione della slide 13.

## 1. Principio generale

Ogni slide dovrebbe essere costruita attorno a **un solo messaggio** e a **un elemento grafico dominante**, destinato ad almeno metà dello spazio disponibile.

Regole comuni:

- scegliere l’archetipo in funzione della struttura del contenuto, non per varietà decorativa;
- usare etichette brevi, idealmente di **2-6 parole**;
- evitare paragrafi nella slide;
- trasferire dettagli, eccezioni e riferimenti secondari in `sources.md`;
- mantenere palette, tipografia e componenti comuni, variando invece la struttura narrativa.

## 2. Archetipi grafici e casi d’uso

| Codice | Archetipo | Adatto quando il contenuto è… |
|:---:|---|---|
| **A** | **Linea dei tempi** | una sequenza scandita da anni, date o scadenze |
| **B** | **Flusso a tappe** | un processo con ingressi, uscite e passaggi successivi |
| **C** | **Mappa a strati** | un fenomeno spaziale composto da livelli sovrapposti |
| **D** | **Grafico protagonista** | un confronto quantitativo rappresentabile con un grande grafico e 2-3 annotazioni |
| **E** | **Matrice a pallini o colori** | più opzioni da confrontare rispetto a pochi criteri |
| **F** | **Albero decisionale** | una scelta basata su condizioni del tipo «se… allora…» |
| **G** | **Hub: centro e raggi** | un concetto centrale con 4-6 componenti indipendenti |
| **H** | **Anatomia con callout** | un oggetto o sistema da scomporre nelle sue parti |

## 3. Distribuzione proposta sulle 17 slide

| Slide | Tema sintetico | Archetipo proposto | Impostazione principale |
|---:|---|:---:|---|
| **1** | Ruolo della modellistica | **G** | i cinque ambiti attorno alla modellistica |
| **2** | Anatomia del sistema modellistico | **H** | sistema scomposto in input, processi, scale e output |
| **3** | Fitness-for-purpose | **G** | concetto centrale con i sei criteri |
| **4** | MQI e MQO | **D** | target plot come elemento dominante |
| **5** | Rappresentatività spaziale | **C** | mappa e aree sovrapposte |
| **6** | Progettazione della rete | **C** | mappa con hotspot, fondo e copertura della rete |
| **7** | Naturali, sabbiatura e salatura | **F** | decisione: sottrarre il contributo oppure no |
| **8** | Indicatori ESI | **C** | grande mappa con strati di popolazione, strade e vegetazione |
| **9** | Esposizione e impatto sanitario | **D** | grafico quantitativo dominante |
| **10** | Definizioni e metodi di SA | **E** | confronto dei metodi per inquinante e finalità |
| **11** | Sei passi del SA | **B** | processo sequenziale in sei tappe |
| **12** | Transfrontaliero e prodotti UE | **C** | mappa con flussi tra Stati |
| **13** | Dalla valutazione al piano | **A** | doppia linea temporale per piano e roadmap |
| **14** | Scenari emissivi | **D** | mantenere il grafico già dominante |
| **15** | Proiezioni | **E + D** | matrice per le quattro opzioni meteorologiche e grafico per il bias |
| **16** | Sistemi di previsione | **B** | catena operativa dalla previsione al prodotto |
| **17** | Previsione e piani a breve termine | **A** | sequenza temporale previsione → allarme → piano |

## 4. Slide da rivedere

### Revisione strutturale

Le slide **3, 8 e 15** risultano troppo testuali e richiedono una revisione basata su un elemento visivo dominante:

- **slide 3:** trasformare l’elenco dei criteri in un hub;
- **slide 8:** usare una mappa grande con strati GIS;
- **slide 15:** separare il confronto delle opzioni meteorologiche dal grafico della correzione del bias.

### Revisione editoriale

Le slide **4, 5 e 14** dispongono già di un grafico forte. L’intervento prioritario consiste nel ridurre il testo e lasciare al visual il ruolo principale.

## 5. Proposta dettagliata per la slide 13

### 5.1 Archetipo

**A. Linea dei tempi**, con un grafico protagonista a tutta larghezza e due binari orizzontali.

### 5.2 Binario 1: piano per la qualità dell’aria

Sequenza principale:

```text
Anno Y
superamento registrato
        →
Anno Y+2
piano adottato
        →
fine dell’anno Y+4
fine del superamento
```

Elementi complementari:

- freccia di ritorno: **«Se non basta: piano aggiornato»**;
- etichetta: **«Reporting entro 2 mesi»**;
- anni di esempio, in corpo ridotto: **2027 → 2029 → 2031**.

### 5.3 Binario 2: roadmap

Asse temporale **2026-2030** con:

- barra **2026-2029**: «Superamento previsto per i valori 2030»;
- bandierina al **31 dicembre 2028**: «Ultima data per chiedere la proroga»;
- traguardo finale: **2030**.

### 5.4 Percorso di costruzione del piano

Nella parte inferiore sinistra, rappresentare cinque tappe come frecce con icona. Ogni tappa risponde a una domanda breve:

1. **Valutazione:** «Dove e quanto?»
2. **Screening:** «Quali sorgenti contano?»
3. **Misure:** «Che cosa si può fare?»
4. **Scenari:** «Bastano? Quando?»
5. **Adozione:** «Adozione e reporting»

### 5.5 Contenuti minimi del piano

Nella parte inferiore destra, il blocco **«Il piano deve dire»** dovrebbe contenere sei icone con etichette di 2-3 parole:

- **dove**;
- **quanto**;
- **da quali sorgenti**;
- **quali misure**, con calendario e responsabili;
- **scenario di base**;
- **se non basta**, con il caso peggiore.

### 5.6 Obiettivo editoriale

Ridurre il testo complessivo a circa **100 parole**, rispetto alle circa **600 parole** dell’impostazione estesa.

## 6. Contenuti da eliminare o spostare nelle fonti

Dalla slide 13 si propone di togliere dal corpo principale:

- reporting supplementare, come costi e chilometri di strade;
- soglie di allarme;
- concentrazioni dei cinque anni precedenti;
- cataloghi di misure;
- nota sui dati assimilati.

La cooperazione tra Stati prevista dall’art. 21 potrebbe essere rimossa dalla slide per preservare la leggibilità, ma è una regola concreta e dovrebbe restare documentata in `sources.md` o nelle note di accompagnamento.

## 7. Indicazione conclusiva

La coerenza della serie non richiede che tutte le slide abbiano la stessa griglia. La coerenza dovrebbe derivare da palette, tipografia, gerarchia e trattamento delle fonti. L’archetipo deve invece cambiare in base alla logica del contenuto, privilegiando sempre un visual dominante e un numero ridotto di messaggi leggibili a colpo d’occhio.
