# Infografiche sulla Direttiva (UE) 2024/2881 (AAQD) e atti di esecuzione

Serie di infografiche **vettoriali (SVG)**, bilingui (IT/EN), generate da codice a partire da file di stringhe.
Destinate a slide riutilizzabili, formazione, gruppi tecnici (SNPA, FAIRMODE) e, se serve, a pubblicazioni.

| # | Infografica | Stato |
|---|---|---|
| 01 | Rappresentatività spaziale di un punto di campionamento | v0.1 – da verificare sul testo vigente (vedi `01-rappresentativita-spaziale/sources.md`) |

## Cosa c'è in ogni cartella

```
common/svgkit.py              palette, font, primitive SVG condivise dalla serie
NN-nome/build.py              genera SVG, PDF e PNG; geometrie e numeri sono calcolati qui
NN-nome/strings/it.yaml       tutti i testi italiani (liste = righe già spezzate)
NN-nome/strings/en.yaml       tutti i testi inglesi
NN-nome/out/                  uscite per ogni lingua e layout: *.svg (sorgente vettoriale), *.pdf, *.png
NN-nome/sources.md            scheda delle fonti normative e stato di verifica di ogni elemento
```

## Come si genera

```bash
pip install -r requirements.txt
cd 01-rappresentativita-spaziale
python build.py              # IT + EN, entrambi i layout
python build.py en mobile    # esempio: solo inglese, solo layout verticale
```

Font: **Source Sans 3** (licenza SIL OFL). L'SVG la richiama per nome con fallback su Helvetica/Arial: per vederlo
come progettato installala sul sistema. PDF e PNG la includono già. Il simbolo "≤" usa DejaVu Sans come fallback.

## Due layout dalla stessa sorgente

| Layout | File | Tela | Uso |
|---|---|---|---|
| `wide` | `spatrep_it.*`, `spatrep_en.*` | 1920×1080 (16:9), PNG 3840×2160 | slide, schermi grandi |
| `mobile` | `spatrep_it_mobile.*`, `spatrep_en_mobile.*` | 1200×1960 (verticale), PNG 2400×3920 | smartphone, messaggistica, pagina di rivista |

Il layout `mobile` rispetta una regola di leggibilità: **testo minimo 29 px su 1200, cioè ≥ 2,4 % della larghezza**, così resta
leggibile anche su uno schermo di 390 px. Nel layout `wide` il testo minimo è ~1,1 % della larghezza: va bene a schermo intero, non su un telefono.
Per le nuove infografiche conviene progettare prima il layout `mobile`.

## Convenzioni

- **Una sola fonte per lingua**: nessun testo è scritto nel codice. Le due versioni condividono la stessa geometria,
  quindi non possono divergere. Separatore decimale: virgola in IT, punto in EN.
- **Numeri esatti**: le barre delle scale sono calcolate dai valori (17–23 e 8–12 su una scala 0–30), non disegnate a mano.
- **Dati della mappa sintetici**: i campi di concentrazione e la forma della zona sono inventati e dichiarati come tali nella figura.
- **SVG modificabile**: testo vivo; gruppi con id (`panel1`, `panel2`, `panel3`, `cells`, `road`, `zone`, `expert-patch`,
  `definition`, `background`). Per fondo trasparente (slide) elimina l'elemento `background`.
- **Accessibilità**: `title` e `desc` nell'SVG come testo alternativo; palette verificata per daltonismo (verde-acqua/ocra).
- **Stile**: palette e motivo a punti ispirati al logo del pacchetto R *spatrep*.

## Aggiungere una nuova infografica

Copia la cartella `01-…`, cambia `strings/*.yaml` e le funzioni `panelN()` in `build.py`, riusa `common/svgkit.py`.
Compila `sources.md`: ogni affermazione nella figura deve avere fonte (CELEX/ELI), data di consultazione e stato.

## Pubblicazione su GitHub + Zenodo (DOI)

1. Crea il repository su GitHub e carica questa cartella.
2. Su <https://zenodo.org> accedi con GitHub, vai in *Account → GitHub* e **attiva il repository prima di creare la release**.
3. Crea una release su GitHub con tag `v0.1.0`: Zenodo archivia lo snapshot e assegna un **DOI di versione** e un **DOI "concept"**
   (quest'ultimo rimanda sempre all'ultima versione; è quello da citare in generale).
4. Aggiungi il DOI al `CITATION.cff` e il badge Zenodo al README, poi pubblica le versioni successive con nuove release.
5. Se cambia la norma, rilascia una nuova versione e indica nella scheda delle fonti la data di verifica: il DOI di versione permette di
   citare esattamente quale testo era valido.

### Prima della prima release (decisioni aperte)

- **Licenza**: proposta CC BY 4.0 per figure e testi, licenza permissiva (es. MIT) per il codice; aggiungi i file `LICENSE` con i testi ufficiali.
  Verifica la policy di ARPA FVG sulla diffusione. Zenodo copia la licenza nei metadati del record.
- **Licenze applicate in questo repository**: codice sotto `LICENSE` (MIT); figure, testi e asset grafici sotto `LICENSE-CC-BY-4.0` (CC BY 4.0).
- **Affiliazione e loghi**: se compaiono nomi o loghi istituzionali (ARPA FVG, SNPA, FAIRMODE), concorda prima l'autorizzazione.
- **Verifica normativa**: chiudi i punti "da verificare" in `01-rappresentativita-spaziale/sources.md`.
