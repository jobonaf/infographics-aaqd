AAQD - PACCHETTO PER LA SERIE DI INFOGRAFICHE - LEGGIMI PER PRIMO
Generato il 2026-11-14 (aggiornato con instructions_12, 14, 15, 16 e 17). Tutti i percorsi qui sotto sono RELATIVI a questo zip (una volta scompattato) o alla radice del tuo repository.

CHE COSA CONTIENE (due parti indipendenti)
==========================================
PARTE A - repo/       da COPIARE nel tuo repository (le cartelle vanno accanto a common/, README.md, scripts/ ...)
PARTE B - session-kit/  file da ALLEGARE alle sessioni pulite (non vanno nel repository)

PARTE A - COSA COPIARE NEL REPOSITORY
=====================================
  repo/common/layout.py                         -> <repo>/common/layout.py           (helper condivisi di layout, nuovo)
  repo/common/test_layout.py                    -> <repo>/common/test_layout.py      (pagina di prova di layout.py, facoltativo)
  repo/13-from-assessment-to-plan/              -> <repo>/13-from-assessment-to-plan/   (slide 13, versione 2 «linea dei tempi»)
  repo/15-projections/                          -> <repo>/15-projections/               (slide 15, versione attuale)
Ogni cartella di slide contiene: build.py, sources.md, strings/it.yaml, strings/en.yaml, out/ (SVG, PNG, PDF in italiano e inglese).
Altre modifiche da fare a mano:
  1) requirements.txt: aggiungi una riga "pillow" (serve a layout.py per misurare la larghezza del testo).
  2) README.md: aggiorna nella tabella dello stato le righe 13 e 15.
  3) Lancia: python scripts/validate_repository.py   -> atteso: 0 errori; restano avvisi sulle voci ancora aperte (◐ e ✖) nelle sources.md.
Verificato: con le cartelle 13 e 15 aggiunte a una copia del repo, lo script di validazione ha dato 0 errori e 15 avvisi (solo voci aperte).
Le slide 03, 04, 05, 08, 14 sono gia' nel tuo repo e questo pacchetto NON le modifica.

PARTE B - COME USARE session-kit/ (una sessione pulita per slide)
=================================================================
Prima di tutto: chat NUOVA, senza memoria (incognito o memoria disattivata), con esecuzione di codice e creazione di file attive.
Allega alla chat questi file, tutti nel primo messaggio:
  - session-kit/methods.txt                      (metodo comune, uguale per tutte le slide)
  - session-kit/instructions_NN.txt              (una sola: quella della slide da fare)
  - il PDF del documento tecnico UE (Air quality modelling for air quality policy, aprile 2025)
  - session-kit/layout.py                        (helper di layout; serve se non e' ancora committato nel repo)
  - (facoltativo, vedi tabella) uno dei modelli in session-kit/optional/
Primo messaggio da incollare (sostituisci NN):
  "Allego methods.txt, instructions_NN.txt, il PDF del report UE e layout.py. Esegui lo STEP 1 per la slide NN come descritto
   in methods.txt (sezione 9): leggi solo le pagine indicate e fermati alla proposta, senza scrivere codice."
Dopo la proposta rispondi, ad esempio: "ok, procedi" oppure indica le correzioni. La sessione eseguira' STEP 2 e STEP 3.
A fine lavoro la sessione ti consegna UNO ZIP, NN-english-name.zip, con la cartella della slide e l'alberatura completa:
scompattalo nella radice del tuo repository (la cartella NN-english-name/ va accanto a common/), poi lancia lo script di validazione.

Quale file allegare per ciascuna slide:
  Slide  File di istruzioni        Modello facoltativo da allegare             Note
  01     instructions_01.txt       -                                            nuova
  02     instructions_02.txt       -                                            nuova
  03     instructions_03.txt       -                                            rifacimento (la cartella 03-fitness-for-purpose esiste gia')
  04     instructions_04.txt       optional/template_chart_build.py             sfoltimento del testo (04-model-quality-mqi-mqo esiste gia')
  06     instructions_06.txt       optional/template_map_layers_build.py        nuova
  07     instructions_07.txt       -                                            nuova
  08     instructions_08.txt       optional/template_map_layers_build.py        rifacimento (08-exceedance-situation-indicators esiste gia')
  09     instructions_09.txt       optional/template_chart_build.py             nuova
  10     instructions_10.txt       -                                            nuova
  11     instructions_11.txt       -                                            nuova
  12     instructions_12.txt       optional/template_map_layers_build.py        nuova
  14     instructions_14.txt       optional/template_chart_build.py             sfoltimento (14-emission-scenarios esiste gia' nel repo)
  15     instructions_15.txt       optional/template_chart_build.py             rifacimento (repo/15-projections dello zip e' la versione vecchia: non e' ancora nel repo)
  16     instructions_16.txt       -                                            nuova
  17     instructions_17.txt       optional/template_timeline_build.py          nuova
  Le slide 05 e 13 non hanno istruzioni (sono gia' a posto). Nessun'altra slide e' in attesa di istruzioni.
  Il modello optional/template_timeline_build.py e' consigliato per la slide 17 (e riprende l'impostazione della 13).
Le slide sono indipendenti: puoi lanciarne piu' di una in sessioni diverse. Non servono altri file: il codice del repo
(common/svgkit.py) viene scaricato dalla sessione con "git clone" dal tuo repository pubblico.

NOTE
====
- Se una sessione viene interrotta dai limiti del piano, ti lascia comunque lo stato corrente: apri una nuova chat con gli stessi
  allegati piu' i file parziali e scrivi "riprendi da qui".
- Le cartelle pack/ e istruzioni/ del precedente scambio NON servono piu': vale questo zip.

ALBERATURA DELLO ZIP
====================
  repo/13-from-assessment-to-plan/build.py
  repo/13-from-assessment-to-plan/out/from_assessment_to_plan_en.pdf
  repo/13-from-assessment-to-plan/out/from_assessment_to_plan_en.png
  repo/13-from-assessment-to-plan/out/from_assessment_to_plan_en.svg
  repo/13-from-assessment-to-plan/out/from_assessment_to_plan_it.pdf
  repo/13-from-assessment-to-plan/out/from_assessment_to_plan_it.png
  repo/13-from-assessment-to-plan/out/from_assessment_to_plan_it.svg
  repo/13-from-assessment-to-plan/sources.md
  repo/13-from-assessment-to-plan/strings/en.yaml
  repo/13-from-assessment-to-plan/strings/it.yaml
  repo/15-projections/build.py
  repo/15-projections/out/projections_en.pdf
  repo/15-projections/out/projections_en.png
  repo/15-projections/out/projections_en.svg
  repo/15-projections/out/projections_it.pdf
  repo/15-projections/out/projections_it.png
  repo/15-projections/out/projections_it.svg
  repo/15-projections/sources.md
  repo/15-projections/strings/en.yaml
  repo/15-projections/strings/it.yaml
  repo/common/layout.py
  repo/common/test_layout.py
  session-kit/instructions_01.txt
  session-kit/instructions_02.txt
  session-kit/instructions_03.txt
  session-kit/instructions_04.txt
  session-kit/instructions_06.txt
  session-kit/instructions_07.txt
  session-kit/instructions_08.txt
  session-kit/instructions_09.txt
  session-kit/instructions_10.txt
  session-kit/instructions_11.txt
  session-kit/instructions_12.txt
  session-kit/instructions_14.txt
  session-kit/instructions_15.txt
  session-kit/instructions_16.txt
  session-kit/instructions_17.txt
  session-kit/layout.py
  session-kit/methods.txt
  session-kit/optional/template_chart_build.py
  session-kit/optional/template_map_layers_build.py
  session-kit/optional/template_timeline_build.py
  README_FIRST.txt
