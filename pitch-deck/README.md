# Pitch Deck — Überarbeitung

## Dateien

| Datei | Inhalt |
|---|---|
| `AthenaRun_Pitch_Deck_reordered.key` | Das Original-Deck mit neuer Slide-Reihenfolge. Inhalte, Layouts und Bilder sind unverändert. |
| `neue-slides.html` | Vier fehlende Slides als Entwurf im Raster und in der Typografie des Decks. |

## Was an der .key-Datei geändert wurde

Ausschließlich die Slide-Reihenfolge. Technisch: in `Index/Document.iwa` die
geordnete Node-Liste des `KNSlideTreeArchive` (Objekt 6076, Feld 3) permutiert.
14 Bytes geändert, alle innerhalb dieser Liste. Alle 74 übrigen Dateien im
Keynote-Paket sind byteidentisch zum Original.

| # | Slide | vorher |
|---|---|---|
| 1 | Cover | 1 |
| 2 | The Problem | 3 |
| 3 | The Cost | 2 |
| 4 | Platform Process 1/2 | 4 |
| 5 | Platform Process 2/2 | 5 |
| 6 | Builds | 7 |
| 7 | Traction | 11 |
| 8 | The Compounding Loop | 6 |
| 9 | Competitive Map | 9 |
| 10 | Market Size | 8 |
| 11 | Team | 10 |
| 12 | Closing | 12 |

Begründung: Die Problem-Slide endet mit der Kausalkette „… → lost EBIT", die
Cost-Slide setzt genau dort an — vorher stand die Antwort vor der Frage.
Traction stand auf Position 11 von 12; die stärksten Belege (7 LOIs,
Channel-Partner, drei Programme) waren damit hinter dem Punkt, an dem die
meisten Leser aufhören. Der Compounding Loop liest sich als Moat-Argument
direkt vor der Competitive Map, weil er dort mit deren Schlusssatz
zusammenfällt.

## Offene Punkte

**Schriften.** Das Deck fordert an 47 Stellen Poppins an, aufgelöst wird
Helvetica — die Schrift ist nicht installiert. Dazu Altlasten aus dem
PPTX-Import: Arial (54 Stile), Courier New (15), Calibri (13). Poppins
installieren, die Theme-Stile für Tabellen und Diagramme angleichen, und für
die Einreichung als PDF exportieren (Keynote bettet keine Schriften ein).

**Fehlende Slides.** Solution (Pos. 4), Business Model (Pos. 12), The Ask &
Use of Funds (Pos. 14), Closing & Contact (Pos. 15). Entwürfe in
`neue-slides.html`, Platzhalter für Zahlen sind gelb markiert.

**Widerspruch in den Zahlen.** Traction nennt 7 LOIs mit €150K Gesamtwert
(≈ €21k pro Kunde), die Markt-Slide rechnet mit $600k pro Kunde. Faktor 28.

**Cover.** Gerades Apostroph in „Germany's" gegen typografische Apostrophe im
Rest des Decks. Die spitzen Klammern um „Software Implementation & Delivery
Infrastructure" prüfen — falls kein Stilmittel, entfernen. Außerdem liegen auf
dem Cover zwei Textboxen („The bottleneck has moved …", „We build the chain,
not the generator.") die in Keynotes eigenem Vorschaubild nicht erscheinen.

**Ohne Quelle.** Die beiden stärksten Zahlen im Deck — 61 % ohne EBIT-Impact,
50 % der Pilots — stehen ohne Beleg. Fußnote oder Appendix.
