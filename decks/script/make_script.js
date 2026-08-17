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
          text: "Fassung zum überarbeiteten Deck (11 Folien) · ca. 6:10",
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
      say("Das System kann es nicht. Der Hersteller sagt: nächstes Major-Release, frühestens 2027. Der Kollege, der die Logik gebaut hat, ist 2023 gegangen."),

      // ------------------------------------------------------------------
      beat("0:45 · Der Prüfer (50 Sek.)"),
      say("Also läuft es daneben. In Excel. Mit einem Sammelpostfach für die Freigaben."),
      pause("//"),
      say("Und dann fragt der Prüfer: Wer hat was wann freigegeben?"),
      pause("///"),
      say("Das System ist nicht schlecht. Es ist von 2015. Der Prozess ist gewachsen — das Werkzeug nicht."),
      pause("//"),
      say("Und mit dem Kollegen ist nicht nur ein Mitarbeiter gegangen. Mit ihm ist die einzige vollständige Fassung der Anforderung gegangen. Sie stand nirgends. Sie stand in seinem Kopf und im Code."),
      pause("//"),
      say("Deshalb erklären Ihre Leute dieselbe Sache zum vierten Mal. Das liegt nicht an Ihren Leuten."),
      pause("//"),
      say("Ihre Systeme haben Daten. Ihr Prozess hat kein Gedächtnis."),

      // ------------------------------------------------------------------
      beat("1:35 · Warum KI das nicht löst (55 Sek.)"),
      say("Und jetzt kommt KI. Und löst das erst mal nicht."),
      pause("//"),
      say("Rund die Hälfte aller KI-Prototypen wird auf dem Weg in den Betrieb wieder eingestampft. Nicht weil das Modell zu schwach war."),
      pause("//"),
      say("Ein Werkzeug baut heute jeder in einer Stunde. Ein System braucht vier Dinge, die kein Prompt mitbringt."),
      say("Es muss Ihre Regeln kennen. Es muss in Ihren Systemen leben, nicht daneben. Es muss beweisen können, was es getan hat. Und ein Mensch muss dafür geradestehen."),
      pause("//"),
      say("PwC hat viertausendvierhundert CEOs gefragt. Knapp sechzig Prozent sagen: kein nennenswerter finanzieller Nutzen aus KI."),
      say("Kein Wunder. Piloten sind Werkzeuge. Werkzeuge bewegen keine Zahl."),
      pause("//"),
      say("Und Sie denken jetzt vielleicht: noch eine Prompt-to-App-Bude. — Ja. Nennen Sie uns so. Mit einem Unterschied: Die liefert Ihnen einen Prototyp. Wir liefern Ihnen etwas, das der Prüfer akzeptiert."),

      // ------------------------------------------------------------------
      beat("2:30 · Was bei Ihnen liegt (70 Sek.)"),
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
      beat("3:40 · Das Gedächtnis (35 Sek.)"),
      say("Und keiner unserer Builds fängt bei null an."),
      say("Dreihunderteinundfünfzig bewährte Muster, die wir in jedem Projekt wiederverwenden. Zweitausendvierundsechzig Fehler, die wir schon kennen und deshalb nicht mehr machen."),
      pause("//"),
      say("Ihre Systeme haben Daten, Ihr Prozess hat kein Gedächtnis. Das hier ist das Gedächtnis."),
      say("Es wächst mit jedem Projekt. Auch mit Ihrem."),

      // ------------------------------------------------------------------
      beat("4:15 · Das läuft schon (35 Sek.)"),
      say("Was davon heute existiert."),
      say("Die Lead-Generierung läuft seit August beim zahlenden Kunden. Echter Produktivbetrieb."),
      say("Die CFO-Analyse ist gebaut und gegen eine echte Bank-Scorecard kalibriert. Kreditanalyse, Finanzierbarkeit."),
      say("Der Board-Agent läuft vollständig in Frankfurt. Lokale Modelle. Kein Training auf Ihren Daten."),
      pause("//"),
      say("Drei Bereiche, die nichts miteinander zu tun haben. Dieselbe Kette hat alle drei gebaut."),

      // ------------------------------------------------------------------
      beat("4:50 · Die Frage zurück (80 Sek.)"),
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
      note("Der Prüfer-Bogen, die Bookend-Frage und der Konzern mit den zwölf Gesellschaften bleiben unangetastet. Das ist der stärkste Teil und er trägt den ganzen Pitch."),
      note("1:35 — aus „Warum KI daran scheitert“ wird die Tool-gegen-System-Argumentation des neuen Decks: erst die eingestampften Prototypen, dann die vier Bedingungen (Regeln kennen, in Ihren Systemen leben, beweisen können, dafür geradestehen), dann die CEO-Zahl als Folgerung statt als Einstieg."),
      note("1:35 — die Prompt-to-App-Antwort behält den Ton, aber der Unterschied ist jetzt materiell: nicht „eine Prüfkette“, sondern etwas, das der Prüfer akzeptiert. Das Deck sagt auf dem Cover, dass KI keine fertigen Anwendungen liefert; die Kategorie einfach zu bejahen würde dem widersprechen."),
      note("2:30 — aus „Zwei Hälften“ wird „Was bei Ihnen liegt“. Die drei Dokumente standen vorher mitten im Absatz und sind jetzt der Einstieg. Neu ist der Satz zum Ausstieg an jedem Übergang, der die Gate-Aussage der Chain-Folie spiegelt."),
      note("3:40 — die 351 Muster und 2.064 Fehler bleiben, bekommen aber den Rückbezug auf „Ihr Prozess hat kein Gedächtnis“. Damit zahlt die beste Zeile des Pitches zweimal ein."),
      note("4:15 — „Drei Dinge laufen heute“ ist raus. Es laufen nicht drei, und der Satz zwingt den Zuhörer zum Nachzählen. Stattdessen „Was davon heute existiert“, und der Abschluss macht daraus eine Fähigkeitsaussage: drei fremde Bereiche, eine Kette."),
      note("4:50 — die Zwölf-Wochen-Aussage aus dem Deck landet hier als Angebot, nicht als Frage: die Eröffnungsfrage bleibt die Frage, und zwölf Wochen ist die Antwort darauf. „In Excel“ ist im Schluss gestrichen und bleibt nur in der Story, wo es verdient ist."),

      rule(),
      new Paragraph({
        spacing: { after: 160 },
        children: [new TextRun({ text: "Bitte prüfen, bevor das so gesprochen wird", bold: true, size: 26 })],
      }),
      note("Zahl im Deck gegen Zahl im Skript: Das Skript nennt PwC, viertausendvierhundert CEOs, knapp sechzig Prozent. Das Deck nennt 61 Prozent nach McKinsey. Zwei Quellen für dieselbe Aussage in einem Termin. Eine davon muss weg."),
      note("Baru: Das Skript sagt „seit August“, das Deck sagt „since June 2026“. Ein Datum ist falsch."),
      note("Board-Agent: Das Skript sagt „läuft vollständig in Frankfurt“. Das Deck sagt „built and verified, offered, not yet deployed“. Läuft er bei einem Kunden oder auf eigener Infrastruktur? Davon hängt ab, ob im Deck „audit-grade output in production“ stehen darf."),
      note("Die halbierten Prototypen und die vier Bedingungen brauchen im Deck dieselbe Quellenzeile, die die CEO-Zahl schon hat."),
    ],
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync("/home/user/Athena/speech/Pitch4_AthenaRun.docx", buf);
  console.log("written");
});
