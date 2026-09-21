# Büro-Funnel: Umzug der Ablage in die Cloud

Die Morgen-Routine „Morgen: Funnel" lief bisher gegen den lokalen Ordner „Büro"
auf dem Mac. Der Auslöser feuert zwar serverseitig, der Ordner ist aber nur
erreichbar, solange Claude Desktop auf dem Mac läuft. Ziel: die Ablage liegt in
der Cloud, die Routine läuft geräteunabhängig.

## Warum die Ablage geteilt ist

Der Google-Drive-Connector kann Dateien lesen und neu anlegen, aber den Inhalt
bestehender Dateien nicht ersetzen (`update_file` ändert nur Titel und Ordner).
Die Routine muss aber an Verläufe anhängen und den Zeitstempel überschreiben.
Deshalb:

| Ort | Inhalt | Zugriff der Routine |
| --- | --- | --- |
| Claude Doc „Büro – Funnel" | Stand, Kunden, Investoren | lesen und ergänzen |
| Claude Doc „Büro – Funnel" | Gelernt | nur lesen, Einträge vorschlagen |
| Drive-Ordner „Büro" | CLAUDE.md, PROMPTS.md, Vorlagen/ | nur lesen |
| Slack | #sales-update, #meeting-notes | lesen, DM an Patrick |

## Feste IDs

- Doc „Büro – Funnel": `d6e60a64-a58c-4a3e-9201-cc8b07c409ca`
- Drive-Ordner „Büro": `1oK30eLw8IDxN_S-JxQm9n7UEnOtfnN19`
- Drive-Ordner „Büro/Vorlagen": `1MveaJ4XTVJyh1D-EgLy7debJ-mOGCCnJ`
- Drive-Ordner „Büro/Archiv": `1rYVhkQgclu4DjkICQHs6z8-7TP8EASze`
- Routine alt (Mac): `trig_011Q6PGEWyiKZQVwcxUDF7rj`, aktiv
- Routine neu (Cloud): `trig_01NbZQDsyTTcimGHpkdbtHJL`, deaktiviert

## Stand

Erledigt:

- Doc „Büro – Funnel" angelegt, Abschnitte Stand, Kunden, Investoren, Gelernt
  und der Arbeitsvertrag mit der Routine.
- Drive-Ordner „Büro" mit Vorlagen/ und Archiv/ angelegt.
- Neue Routine mit dem Cloud-Prompt angelegt, Zeitplan `0 8 * * 1-5`, deaktiviert.

Offen:

1. Migration vom Mac: `migration-prompt.md` einmal in Claude Desktop auf dem Mac
   ausführen, solange der Ordner „Büro" verbunden ist.
2. Connectors an der neuen Routine: Slack, Google Drive und Claude Docs in der
   Routinen-Oberfläche auf claude.ai ergänzen. Über die MCP-Werkzeuge geht das
   nicht — `create_trigger` lehnt den Parameter für diese Organisation ab, und
   `update_trigger` kennt ihn nicht. Die Routine steht sonst ohne Connectors da
   (`mcp_connections: []`) und kann weder Slack noch Drive noch das Doc erreichen.
3. Neue Routine aktivieren, alte Routine deaktivieren — erst wenn 1 und 2 stehen.

## Nicht übernommen

- Modell: die alte Routine läuft auf `claude-fable-5-1`. Bei der neuen ist das
  Feld leer, weil `create_trigger` kein Modell setzen kann.
- Uhrzeit: `0 8 * * 1-5` ist UTC, also 10 Uhr deutscher Sommerzeit. Unverändert
  aus der alten Routine übernommen.
