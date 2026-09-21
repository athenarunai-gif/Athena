# Büro-Funnel: Ablage in der Cloud

Die Morgen-Routine „Morgen: Funnel" lief gegen den lokalen Ordner „Büro" auf
dem Mac und stand still, sobald der Rechner aus war. Die Ablage liegt jetzt in
Supabase, die Routine läuft geräteunabhängig.

## Warum Supabase und nicht Google Drive oder Claude Docs

Drei Anläufe, zwei Sackgassen:

1. **Google Drive** kann Dateien lesen und neu anlegen, aber den Inhalt
   bestehender Dateien nicht ersetzen (`update_file` ändert nur Titel und
   Ordner). Die Routine muss aber Verläufe fortschreiben.
2. **Claude Docs** ist für dieses Konto kein installierbarer Connector. Ein
   Diagnoselauf am 21.09.2026 hat es belegt: in der Routine-Sitzung standen
   Slack (27 Werkzeuge), Google Drive (11) und Supabase (26) bereit, für
   Claude Docs **null**. Der Eintrag in der Routine zeigt auf
   `api.anthropic.com/v1/pages/mcp` und führt im Lauf zu nichts. Das ist weder
   über Einstellungen noch über den Prompt zu beheben.
3. **Supabase** ist ein Standard-Connector, wird im Lauf sauber geladen und
   kann lesen und schreiben.

## Aufbau

Die Instanz ist geteilt und enthält in `public` die produktive App mit 85
Tabellen. Die Ablage liegt deshalb in einem eigenen Schema.

Projekt `zafbcpkfhtktohzjzkvj` (AthenaRun), Schema `buero`:

| Tabelle | Inhalt | Routine |
| --- | --- | --- |
| `eintraege` | ein Satz je Firma oder Investor, mit MEDDPICC und offenen Punkten | lesen, anlegen, ändern |
| `log` | ein Eintrag je Ereignis, mit Quelle | nur anhängen |
| `stand` | eine Zeile: letzter Lauf, bis wohin Slack gelesen ist | lesen, ändern |
| `gelernt` | Muster aus verlorenen Deals | nur lesen |
| `gelernt_gruende` | die sechs zulässigen Gründe | nur lesen |

Auf allen Tabellen ist RLS aktiv, `anon` und `authenticated` haben keine
Rechte, das Schema ist nicht über PostgREST freigegeben.

Google Drive bleibt als Lese-Ablage: Ordner „Büro"
(`1oK30eLw8IDxN_S-JxQm9n7UEnOtfnN19`) mit CLAUDE.md, PROMPTS.md und
`Vorlagen/` (`1MveaJ4XTVJyh1D-EgLy7debJ-mOGCCnJ`).

## Routinen

| Routine | ID | Zustand |
| --- | --- | --- |
| Morgen: Funnel (Supabase) | `trig_01NbZQDsyTTcimGHpkdbtHJL` | aktiv, `0 8 * * 1-5` |
| Morgen: Funnel (Büro-Ablage, abgelöst) | `trig_011Q6PGEWyiKZQVwcxUDF7rj` | abgeschaltet |

Die aktive Routine trägt Slack, Google Drive, Supabase und einen wirkungslosen
Claude-Docs-Eintrag. Connectors lassen sich nur in der Routinen-Oberfläche auf
claude.ai setzen — `create_trigger` lehnt den Parameter für diese Organisation
ab, `update_trigger` kennt ihn nicht.

## Stand am 21.09.2026

- Migration vom Mac gelaufen und geprüft: CLAUDE.md, PROMPTS.md und 7 Vorlagen
  als Markdown in Drive, lokaler Ordner unverändert.
- Erster echter Lauf auf Supabase: 7 Kunden, 4 Investoren, 18 Log-Zeilen.
  Kein DDL ausgeführt, `public` nicht angefasst (jüngste Migration in der
  Datenbank ist die eigene vom Schema-Aufbau).

## Offen

- Uhrzeit: `0 8 * * 1-5` ist UTC, also 10 Uhr deutscher Sommerzeit.
  `0 6 * * 1-5` wären 8 Uhr.
- Modell: die abgelöste Routine lief auf `claude-fable-5-1`, die neue auf dem
  Standardmodell. `create_trigger` kann kein Modell setzen.
- Terje (Boost4S) steht als Kunde in der Ablage, tauchte in einer früheren
  Slack-Auswertung aber unter Investoren auf. Zuordnung ist zu klären.
- Das Claude-Dokument „Büro – Funnel" ist nur noch eine Momentaufnahme vom
  21.09. und wird von der Routine nicht mehr gepflegt.
