# Pitch Deck — Überarbeitung

## Datei

`AthenaRun_Pitch_Deck_15_Slides.pptx` — das vollständige Deck mit 15 Slides.
Die zwölf bestehenden Slides sind unverändert aus dem Keynote-Export
übernommen, die drei neuen sind an den richtigen Stellen eingesetzt.

| # | Slide | |
|---|---|---|
| 1 | Cover | |
| 2 | The Problem | |
| 3 | The Cost | |
| 4 | **The Solution** | neu |
| 5 | Platform Process 1/2 | |
| 6 | Platform Process 2/2 | |
| 7 | Builds | |
| 8 | Traction | |
| 9 | The Compounding Loop | |
| 10 | Competitive Map | |
| 11 | Market Size | |
| 12 | **Business Model** | neu |
| 13 | Team | |
| 14 | **The Ask & Use of Funds** | neu |
| 15 | Closing | |

## Wie die neuen Slides gebaut sind

Nicht nachgebaut, sondern **dupliziert**: „The Solution" und „The Ask" sind
Kopien der Traction-Slide (Vier-Spalten-Raster), „Business Model" ist eine
Kopie der Market-Size-Slide (Drei-Spalten-Raster). Getauscht wurden nur die
Texte und einzelne Positionen. Dadurch erben sie Schriften, Farben,
Hintergrundbild und Logo exakt aus dem Original.

Das Designsystem, wie es im Export tatsächlich steht:

| Element | Schrift | Größe | Farbe |
|---|---|---|---|
| Headline | Poppins Bold | 27 | `ECECEE`, zweiter Satz `9A9AA2` |
| Slide-Tag oben rechts | **Courier New** | 11 | `9A9AA2` |
| Sub-Zeile | Poppins | 18 | `9A9AA2`, Zeilenabstand 135 % |
| Sektions- und Spaltenlabel | **Courier New** | 9–10 | `9A9AA2` |
| Kartentitel | Poppins Bold | 17 | `ECECEE` |
| Große Zahl | Poppins Regular | 38 | `ECECEE`, Akzent `FF6B3D` |
| Beschreibung | Poppins | 11 | `9A9AA2`, Zeilenabstand 135 % |
| Trennlinien | | 1 pt | `2B2B2D` |
| Bar-Fläche | | | `161619` |
| Hintergrund | | | `0E0E11` |

Zwei Dinge, die im ersten Entwurf falsch waren: die Uppercase-Label sind
**Courier New**, nicht Poppins, und der Akzent ist **`FF6B3D`** (orange). Das
Rosé aus dem ersten Entwurf stammte aus einem JPEG-Vorschaubild und war
schlicht falsch gemessen.

## Noch einzutragen

Auf Slide 12: die drei Preisfelder (`[ Fixpreis ]`, `[ pro Monat ]`,
`[ pro Jahr ]`).
Auf Slide 14: `[ Instrument ]`, die Laufzeit `[ 00 ]` Monate und
`[ Meilenstein ]`. Die Aufteilung 40/25/25/10 ist ein Vorschlag.

## Offene Punkte im Deck

**Kontaktdaten.** Die Closing-Slide hat keine E-Mail, keine Website, keinen
nächsten Schritt.

**Ohne Quelle.** Die beiden stärksten Zahlen — 61 % ohne EBIT-Impact, 50 % der
Pilots — stehen ohne Beleg.

**Widerspruch.** Traction nennt 7 LOIs mit €150K Gesamtwert (≈ €21k pro
Kunde), die Markt-Slide rechnet mit $600k pro Kunde.

**Cover.** Gerades Apostroph in „Germany's" gegen typografische Apostrophe im
Rest. Die spitzen Klammern um „Software Implementation & Delivery
Infrastructure" prüfen.

**Poppins muss installiert sein**, sonst fällt das ganze Deck auf Helvetica
zurück — kostenlos bei Google Fonts.

## Prüfung

`validate.py` bestanden. Alle drei neuen Slides gegengelesen und mit einem
eigenen Renderer aus dem Slide-XML gegen die Originalslides verglichen
(LibreOffice Impress ist in dieser Umgebung nicht installiert). Dabei
gefunden und behoben: „€500k" kollidierte mit seinem Label, weil die erste
KPI-Kachel im Original für eine einstellige Zahl gebaut ist; der Bar-Text auf
Slide 12 lief über zwei Zeilen aus der Fläche; der Spaltenblock saß zu dicht
unter der Trennlinie. Vorschauen in `slides/`.
