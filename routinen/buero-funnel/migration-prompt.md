# Einmaliger Migrations-Prompt

In Claude Desktop **auf dem Mac** ausführen, solange der Ordner „Büro"
verbunden ist. Läuft genau einmal.

---

Du überträgst den lokalen Ordner „Büro" einmalig in die neue Cloud-Ablage. Der
Ordner liegt unter `$HOME/mnt/Büro…` — nutze das Glob-Muster `"$HOME"/mnt/B*`,
der Name enthält ein Leerzeichen am Ende und ein dekomponiertes ü. Du liest den
lokalen Ordner nur. Du änderst, verschiebst und löschst dort nichts.

**1. Nach Google Drive (nur die Dateien, die die Routine später nur liest)**

- `CLAUDE.md` und `PROMPTS.md` in den Drive-Ordner „Büro",
  ID `1oK30eLw8IDxN_S-JxQm9n7UEnOtfnN19`.
- Inhalt von `Vorlagen/` in den Drive-Ordner „Büro/Vorlagen",
  ID `1MveaJ4XTVJyh1D-EgLy7debJ-mOGCCnJ`.
- Lade sie als Textdateien hoch, ohne Umwandlung in Google Docs
  (`disableConversionToGoogleType` auf true). Sonst sind es Docs statt Markdown.

**2. In das Dokument „Büro – Funnel"**

Doc-ID `d6e60a64-a58c-4a3e-9201-cc8b07c409ca`. Nutze die Claude-Docs-Werkzeuge.
Rufe die Dokument-URL nicht per Web-Abruf ab.

- Für jeden Ordner unter `Kunden/`: eine Zeile in der Tabelle unter „Kunden"
  (Firma, Phase, nächster Schritt, Datum) und darunter ein Abschnitt
  `### <Firma>` mit den MEDDPICC-Punkten und dem Log aus `verlauf.md`.
  Überfällige Schritte zuerst.
- Für jeden Ordner unter `Investoren/`: dasselbe unter „Investoren".
- `gelernt.md` in den Abschnitt „Gelernt".
- Den Zeitstempel aus `Kunden/_stand.md` in den Abschnitt „Stand", zusammen mit
  dem heutigen Datum als „letzter Lauf".
- Phasenbezeichnungen unverändert aus den Verläufen übernehmen, nicht neu
  erfinden. Was in den Dateien nicht steht, bleibt leer. Kein Feld mit „n/a"
  füllen.

**3. Am Ende melden**

Wie viele Kunden und Investoren übertragen wurden, und was du nicht zuordnen
konntest.

**Grenzen:** nichts im lokalen Ordner ändern oder löschen, nichts erfinden,
keine Slack-Nachricht, keine E-Mail, keine weiteren Dokumente oder Ordner
anlegen.
