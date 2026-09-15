# Wochenroutine SEO / AI-Search — AthenaRun

Kurzfassung dessen, was in diesem Repo eingerichtet ist, was der geplante Trigger tun
würde und was davon Menschenarbeit bleibt.

**Stand:** Skill und Workspace sind committet und gepusht auf
`claude/weekly-seo-routine-lfm87m`. Der wöchentliche Trigger ist **noch nicht
angelegt** — die Routine läuft derzeit nur manuell.

---

## 1. Was installiert ist

| Pfad | Inhalt |
| --- | --- |
| `.claude/skills/weekly-seo/SKILL.md` | Die Routine selbst — sechs Schritte, Produktfakten, Leitplanken |
| `.claude/skills/weekly-seo/references/keywords.md` | Keyword-Familien, Wettbewerber-Set, deutscher Track |
| `.claude/skills/weekly-seo/references/content-spec.md` | Checkliste, die jede Seite erfüllen muss |
| `.claude/skills/weekly-seo/references/outreach.md` | Mail-Vorlage für „Best of"-Listen, Community-Regeln |
| `.claude/skills/weekly-seo/references/page-template.html` | Seitenvorlage im Homepage-Stil (dunkel, Inter, `#FF5533`) |
| `seo/keywords.csv` | Alle Keywords mit Status `candidate` → `picked` → `keep` / `drop` |
| `seo/tracking.csv` | Eine Zeile pro Keyword pro Woche: zitiert oder nicht, und wer stattdessen |
| `seo/runs/<datum>/` | Wochenlog, YouTube-Skript, Kapitelliste |
| `seo/outbox/` | Entwürfe für Mails und Community-Antworten — **verschickt ein Mensch** |

Manuell starten: `/weekly-seo` in Claude Code oder „führe die Wochenroutine aus".

---

## 2. Was der Trigger tun würde

Ein Cron-Job auf Anthropic-Seite, `0 6 * * 1` — jeden **Montag 06:00 UTC**
(08:00 Berlin im Sommer, 07:00 im Winter; Cron rechnet in UTC, deshalb die
Verschiebung zur Zeitumstellung).

Bei jedem Feuern:

1. **Neue Session.** Frischer Container, Repo neu geklont, keine Erinnerung an
   vorherige Läufe — deshalb steht die vollständige Anweisung im Trigger-Prompt und
   die eigentliche Logik im Repo.
2. **Skill lesen und abarbeiten.** Die Session liest `.claude/skills/weekly-seo/SKILL.md`
   und geht die sechs Schritte der Reihe nach durch (siehe unten).
3. **Committen und pushen** auf einen Branch `seo/week-<datum>`. Kein Pull Request,
   kein Push auf `main`.
4. **Push-Benachrichtigung** mit der To-do-Liste: welches Video aufzunehmen ist,
   welche Listen anzuschreiben sind, welche Threads zu beantworten sind, welche
   Fakten gefehlt haben.

Laufende Kosten: eine Agent-Session pro Woche.

---

## 3. Die sechs Schritte

| # | Schritt | Zeit | Ergebnis |
| --- | --- | --- | --- |
| 1 | Kauf-Keywords wählen (nicht „was ist …", sondern „best …", „… alternative", „… pricing") | 20 min | 1 Pillar + 3 Kauf-Keywords in `keywords.csv` |
| 2 | Ein Pillar-Artikel und drei Kauf-Posts schreiben | 2 h | Vier Seiten in `content/`, jede mit einem **zitierfähigen Satz** |
| 3 | Interne Links setzen — Servicepage runter zu den Posts, Posts hoch zur Servicepage, Ankertext = Suchphrase | 15 min | Verlinkung in beide Richtungen |
| 4 | YouTube-Video zum selben Keyword: 8–12 Minuten, Kapitel ab `0:00`, Titel = exakte Suchphrase | 45 min | Skript + Kapitelliste in `seo/runs/<datum>/` |
| 5 | „Best of"-Listen anschreiben, Community-Fragen beantworten | 45 min | Entwürfe in `seo/outbox/` |
| 6 | Prüfen, welche Suchen uns zitiert haben; Gewinner behalten, Nieten streichen | 10 min | Zeilen in `tracking.csv` |

Der zitierfähige Satz aus Schritt 2 ist der Kern: ein vollständiger, wahrer Satz ohne
Rückbezug, der ohne Kontext in einer AI-Antwort stehen kann. Ein Punkt, den man erst
nach drei Absätzen versteht, wird nie zitiert.

---

## 4. Leitplanken

Im Skill fest verdrahtet, nicht optional:

- **Keine erfundenen Zahlen.** Preise, Kundenzahlen, Case Studies, Logos, Benchmarks —
  fehlt ein Fakt, landet er als `TODO(human): …` auf der Seite und unter „Blocked on
  facts" im Wochenlog. Betrifft aktuell vor allem Pricing-Keywords, weil auf der Seite
  kein Preis steht.
- **Nichts wird verschickt oder veröffentlicht.** Keine Mail, kein Post, kein Upload,
  kein Push auf `main`. Alles bleibt Entwurf in `seo/outbox/`.
- **Nutzbare Fakten** sind die von der Homepage: live in unter 5 Minuten, 99,9 %
  Uptime, null Entwickler, 3 Monate → 1 Tag, −95 % Entwicklungskosten, Frankfurt,
  DSGVO, self-hosted.
- **Wettbewerber ehrlich behandeln.** Erst schreiben, was Retool, Power Apps oder
  Bubble wirklich gut können, dann der Fall, in dem „Ziel rein, App raus" gewinnt. Ein
  Vergleich, der den Wettbewerber schlechtredet, wird nicht zitiert.
- **Zitierquellen jede Woche neu prüfen.** Welche Plattformen AI-Antworten zitieren,
  verschiebt sich — die Seed-Listen sind Startpunkt, nicht Wahrheit.

---

## 5. Menschenarbeit bleibt

Der Agent liefert Text, Skripte und Entwürfe. Nicht automatisierbar ist:

- Video aufnehmen und hochladen
- Outreach-Mails tatsächlich verschicken
- Community-Antworten aus einem echten Account posten
- Search Console lesen (Query-Filter Regex: `(?i)^(who|what|why|how|which|is|are|can|does)\b`)
- Seiten deployen — das Repo enthält statisches HTML, kein CMS

Genau diese Liste steht am Ende jedes `seo/runs/<datum>/log.md`.

---

## 6. Trigger anlegen, ändern, löschen

Anlegen: „leg den wöchentlichen Trigger an" — optional mit anderer Uhrzeit.
Ändern oder abschalten: über `list_triggers` / `update_trigger` / `delete_trigger`,
oder schlicht danach fragen. Ein Trigger ändert nichts am Repo; der Skill funktioniert
auch ohne ihn.
