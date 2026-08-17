const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, BorderStyle,
} = require("docx");
const fs = require("fs");

const BODY = 23;      // half-points -> 11.5pt, matches the original's default body
const MONO_GREY = "6B6B72";

const beat = (t) =>
  new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 380, after: 140 },
    children: [new TextRun({ text: t, bold: true, size: 34 })],
  });

const say = (t) =>
  new Paragraph({
    spacing: { after: 130 },
    children: [new TextRun({ text: t, size: BODY })],
  });

// pause marks are stage directions, not lines to read out
const pause = (t, note) =>
  new Paragraph({
    spacing: { after: 130 },
    children: [
      new TextRun({ text: t, size: BODY, color: MONO_GREY }),
      ...(note ? [new TextRun({ text: "  " + note, size: 19, color: MONO_GREY, italics: true })] : []),
    ],
  });

const note = (t) =>
  new Paragraph({
    spacing: { after: 110 },
    children: [new TextRun({ text: t, size: 20, color: "44444A" })],
  });

const rule = () =>
  new Paragraph({
    spacing: { before: 300, after: 220 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "C8C8CE", space: 1 } },
    children: [new TextRun({ text: "", size: 2 })],
  });

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Calibri", size: BODY } } },
    paragraphStyles: [
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal",
        quickFormat: true, run: { font: "Calibri", size: 34, bold: true, color: "000000" } },
    ],
  },
  sections: [{
    properties: { page: { margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    children: [

      new Paragraph({
        spacing: { after: 60 },
        children: [new TextRun({ text: "AthenaRun · Pitch", bold: true, size: 44 })],
      }),
      new Paragraph({
        spacing: { after: 40 },
        children: [new TextRun({
          text: "Fassung zum überarbeiteten Deck (11 Folien) · ca. 6:15",
          size: 21, color: "44444A" })],
      }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun({
          text: "// kurze Pause   /// lange Pause, in den Raum schauen",
          size: 19, color: MONO_GREY, italics: true })],
      }),

      // ------------------------------------------------------------------
      beat("0:00 · Die Frage (45 Sek.)"),
      say("Eine Frage."),
      say("Welches System bei Ihnen auf der Arbeit kann heute etwas nicht, das es können müsste?"),
      pause("///", "(drei Sekunden. In den Raum schauen. Nicht weiterreden.)"),
      say("Sie haben gerade an etwas Bestimmtes gedacht."),
      pause("//"),
      say("Ich sage Ihnen, woran ich denke."),
      say("Ein Konzern. Zwölf Gesellschaften. Das Reporting läuft seit 2015 — und es läuft gut. Gebaut für zwölf Gesellschaften, deutsches Recht, einen Standard."),
      pause("//"),
      say("Dann kommen neue gesetzliche Anforderungen. Neue Kennzahlen. Neue Prüftiefe."),
      say("Das System kann es nicht. Der Hersteller sagt: nächstes Major-Release, frühestens 2027."),

      // ------------------------------------------------------------------
      beat("0:45 · Compliance (50 Sek.)"),
      say("Also läuft es daneben. Ein Sammelpostfach für die Freigaben, eine Excel-Datei für die Zahlen."),
      pause("//"),
      say("Und dann fragt der Prüfer: Wer hat was wann freigegeben?"),
      pause("///"),
      say("Niemand kann die Frage beantworten. Nicht weil geschludert wurde, sondern weil die Freigabe nie festgehalten wurde, als sie passiert ist."),
      say("Der Kollege, der die Freigabelogik gebaut hat, ist 2023 gegangen. Mit ihm die einzige vollständige Fassung der Anforderung. Sie stand nirgends. Sie stand in seinem Kopf und im Code."),
      pause("//"),
      say("Das System ist nicht schlecht. Es ist von 2015. Der Prozess ist gewachsen — das Werkzeug nicht."),
      pause("//"),
      say("Und Compliance war nie Teil dieses Prozesses. Compliance war eine Prüfung am Ende."),

      // ------------------------------------------------------------------
      beat("1:35 · Warum KI das nicht löst (60 Sek.)"),
      say("Und jetzt kommt KI. Und löst das erst mal nicht."),
      pause("//"),
      say("Rund die Hälfte aller KI-Prototypen wird auf dem Weg in den Betrieb wieder eingestampft. Nicht weil das Modell zu schwach war."),
      pause("//"),
      say("Das erste Gespräch kennt die Anforderung. Die Entwicklung kennt sie vom Hörensagen. Deshalb erklären Ihre Leute dieselbe Sache zum vierten Mal, und das liegt nicht an Ihren Leuten."),
      pause("//"),
      say("Ein Werkzeug baut heute jeder in einer Stunde. Ein System braucht vier Dinge, die kein Prompt mitbringt."),
      say("Es muss Ihre Regeln kennen. Es muss in Ihren Systemen leben, nicht daneben. Es muss beweisen können, was es getan hat. Und ein Mensch muss dafür geradestehen."),
      pause("//"),
      say("PwC hat viertausendvierhundert CEOs gefragt. Knapp sechzig Prozent sagen: kein nennenswerter finanzieller Nutzen aus KI."),
      say("Kein Wunder. Piloten sind Werkzeuge. Werkzeuge bewegen keine Zahl."),
      pause("//"),
      say("Und Sie denken jetzt vielleicht: noch eine Prompt-to-App-Bude. — Ja. Nennen Sie uns so. Mit einem Unterschied: Die liefert Ihnen einen Prototyp. Wir liefern Ihnen etwas, das der Prüfer akzeptiert."),

      // ------------------------------------------------------------------
      beat("2:35 · Was bei Ihnen liegt (70 Sek.)"),
      say("Was Sie dafür bekommen. Nicht wie wir arbeiten — was am Ende bei Ihnen liegt."),
      pause("//"),
      say("Zuerst drei Dokumente. Bevor ein Euro in Entwicklung geht."),
      say("Was die Plattform von Ihrer Anforderung schon abdeckt. Die Recherche, jede Aussage mit Quelle nachprüfbar. Und den Compliance-Bericht, geprüft gegen Recht und Datenschutz, bevor gebaut wird."),
      pause("//"),
      say("Das entsteht aus dem ersten Gespräch. Einer Besprechungsnotiz. Einem gesprochenen Satz. Daraus ziehen wir Anforderungen, Rollen und Regeln heraus."),
      pause("//"),
      say("Dann laufende Software. Automatisches Code-Review, Sicherheitsprüfung bei jedem Release, Ihre Freigabe davor. Und nach dem Start läuft es weiter: eingehende Meldungen werden zu Tickets, die Dokumentation bleibt aktuell."),
      pause("//"),
      say("An jedem Übergang können Sie aussteigen. Bevor Budget fließt."),
      pause("//"),
      say("Wenn der Prüfer dann fragt: Wer hat was wann freigegeben? — dann ist das keine Suche mehr. Das ist eine Abfrage."),

      // ------------------------------------------------------------------
      beat("3:45 · Das Gedächtnis (35 Sek.)"),
      say("Und keiner unserer Builds fängt bei null an."),
      say("Dreihunderteinundfünfzig bewährte Muster, die wir in jedem Projekt wiederverwenden. Zweitausendvierundsechzig Fehler, die wir schon kennen und deshalb nicht mehr machen."),
      pause("//"),
      say("Ihre Systeme haben Daten. Ihr Prozess hat kein Gedächtnis. Das hier ist das Gedächtnis."),
      say("Es wächst mit jedem Projekt. Auch mit Ihrem."),

      // ------------------------------------------------------------------
      beat("4:20 · Das läuft schon (35 Sek.)"),
      say("Was davon heute existiert."),
      say("Die Lead-Generierung läuft seit August beim zahlenden Kunden. Echter Produktivbetrieb."),
      say("Die CFO-Analyse ist gebaut und gegen eine echte Bank-Scorecard kalibriert. Kreditanalyse, Finanzierbarkeit."),
      say("Der Board-Agent läuft vollständig in Frankfurt. Lokale Modelle. Kein Training auf Ihren Daten."),
      pause("//"),
      say("Drei Bereiche, die nichts miteinander zu tun haben. Dieselbe Kette hat alle drei gebaut."),

      // ------------------------------------------------------------------
      beat("4:55 · Die Frage zurück (80 Sek.)"),
      say("Eine Sache noch."),
      say("Ich habe Sie am Anfang etwas gefragt. Welches System bei Ihnen heute etwas nicht kann, das es können müsste."),
      say("Sie haben an eines gedacht. Es ist Ihnen sofort eingefallen — das ist der Punkt."),
      pause("///"),
      say("Die Frage ist nicht, ob es gebaut werden kann. Die Frage ist, ob Sie darauf zwei Jahre warten oder zwölf Wochen."),
      pause("//"),
      say("Ich lasse Ihnen heute keinen Prospekt da. Ich lasse Ihnen diese Frage da."),
      say("Und wenn Ihnen dazu etwas eingefallen ist, das heute daneben läuft: darüber würde ich nachher gern reden. Nicht über AthenaRun. Über den Prozess."),
      pause("//"),
      say("Manchen von Ihnen ist genau einer eingefallen. Dann bauen wir den."),
      say("Anderen sind gerade zwanzig eingefallen. Dann bauen wir nicht zwanzig Anwendungen — dann steht die Plattform bei Ihnen im Haus, und Ihre Fachbereiche bauen selbst. Innerhalb dessen, was Ihre IT freigegeben hat."),
      pause("//"),
      say("Der Einstieg ist in beiden Fällen derselbe: ein Prozess. Nehmen Sie den, der am längsten nervt."),

      // ------------------------------------------------------------------
      rule(),
      new Paragraph({
        spacing: { after: 160 },
        children: [new TextRun({ text: "Was sich gegenüber Pitch3 geändert hat", bold: true, size: 26 })],
      }),
      note("Der Konzern mit den zwölf Gesellschaften, die Bookend-Frage und die Prüferfrage bleiben. Das ist der stärkste Teil und er trägt den ganzen Pitch."),
      note("0:45 — die Passage heißt jetzt Compliance und hat nur noch einen Höhepunkt. Die Prüferfrage ist der Höhepunkt, der gegangene Kollege ist ihre Ursache, nicht die zweite Pointe. Er ist deshalb aus 0:00 hierher gewandert; vorher stand er zweimal im Text."),
      note("0:45 — das Sammelpostfach steht jetzt vor Excel. Ein Sammelpostfach für Freigaben ist das belastendere Detail und nicht abgenutzt."),
      note("0:45 — die Entlastung („nicht schlecht, von 2015“) kommt nach dem Schmerz statt davor, wo sie ihn abgefedert hat. Die Passage landet auf Compliance als Prüfung am Ende, und damit direkt auf der Compliance-Spalte der Chain-Folie: dort ist die Freigabe unterschrieben, bevor Code entsteht."),
      note("1:35 — aus „Warum KI daran scheitert“ wird die Tool-gegen-System-Argumentation des Decks: erst die eingestampften Prototypen, dann der verlorene Kontext, dann die vier Bedingungen, dann die CEO-Zahl als Folgerung statt als Einstieg."),
      note("1:35 — die Prompt-to-App-Antwort behält den Ton, aber der Unterschied ist materiell: nicht „eine Prüfkette“, sondern etwas, das der Prüfer akzeptiert."),
      note("2:35 — aus „Zwei Hälften“ wird „Was bei Ihnen liegt“. Die drei Dokumente standen vorher mitten im Absatz und sind jetzt der Einstieg. Neu ist der Satz zum Ausstieg an jedem Übergang, der die Gate-Aussage der Chain-Folie spiegelt."),
      note("3:45 — „Ihre Systeme haben Daten, Ihr Prozess hat kein Gedächtnis“ steht jetzt nur noch hier, dafür ungeteilt. Vorher war es zweimal im Text und hat sich selbst die Wirkung genommen. Die 351 Muster und 2.064 Fehler bleiben."),
      note("4:20 — „Drei Dinge laufen heute“ ist raus. Es laufen nicht drei, und der Satz zwingt den Zuhörer zum Nachzählen. Der Abschluss macht daraus eine Fähigkeitsaussage: drei fremde Bereiche, eine Kette."),
      note("4:55 — die Zwölf-Wochen-Aussage aus dem Deck landet hier als Angebot, nicht als Frage: die Eröffnungsfrage bleibt die Frage, zwölf Wochen ist die Antwort darauf. „In Excel“ ist im Schluss gestrichen und bleibt nur in der Story, wo es verdient ist."),

      rule(),
      new Paragraph({
        spacing: { after: 160 },
        children: [new TextRun({ text: "Bitte prüfen, bevor das so gesprochen wird", bold: true, size: 26 })],
      }),
      note("Fehlt noch: die echte Konsequenz. Nach „Niemand kann die Frage beantworten“ gehört ein Halbsatz, was daraus wirklich folgt — eine Feststellung, ein eingeschränktes Testat, ein verschobener Abschluss. Momentan ist das schlimmste implizierte Ergebnis Peinlichkeit. Mit einer echten Folge ist es die Brücke zur EBIT-Zahl bei 1:35."),
      note("Offen: War der Auslöser Regulierung oder Wachstum? „Zwölf Gesellschaften“ fällt zweimal, aber die Zahl ändert sich nie. Wenn der Konzern inzwischen achtzehn hat, ist das die stärkere Fassung, weil Wachstum ein Offensiv-Etat ist und Regulierung ein Defensiv-Etat."),
      note("Zahl im Deck gegen Zahl im Skript: Das Skript nennt PwC, viertausendvierhundert CEOs, knapp sechzig Prozent. Das Deck nennt 61 Prozent nach McKinsey. Zwei Quellen für dieselbe Aussage in einem Termin. Eine davon muss weg."),
      note("Baru: Das Skript sagt „seit August“, das Deck sagt „since June 2026“. Ein Datum ist falsch."),
      note("Board-Agent: Das Skript sagt „läuft vollständig in Frankfurt“. Das Deck sagt „built and verified, offered, not yet deployed“. Läuft er bei einem Kunden oder auf eigener Infrastruktur? Davon hängt ab, ob im Deck „audit-grade output in production“ stehen darf."),
      note("Die halbierten Prototypen brauchen im Deck dieselbe Quellenzeile, die die CEO-Zahl schon hat."),
    ],
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync("/home/user/Athena/decks/script/Pitch4_AthenaRun.docx", buf);
  console.log("written");
});
