const pptxgen = require("pptxgenjs");
const sharp = require("sharp");

/* ---------------- Design-Tokens (helles AthenaRun-Design) ---------------- */
const C = {
  bg:      "F8FAFC",
  card:    "FFFFFF",
  flat:    "F1F5F9",
  line:    "E2E8F0",
  ink:     "0F172A",
  ink2:    "475569",
  muted:   "94A3B8",
  accent:  "FF5533",
  tint:    "FFF6F5",   // accent @ 5 % auf weiß
  tint2:   "FFEEEB",   // accent @ 10 %
  tintLn:  "FFC7BB",   // accent @ 20 %
};
// Inter (Marken-Schrift) ist auf fremden Rechnern nicht garantiert; Arial ist der
// nächstliegende Grotesk-Ersatz, den jedes Office mitbringt — und hier exakt messbar.
const F = { head: "Arial", body: "Arial" };

const W = 13.333, H = 7.5, M = 0.7;         // Bühne + Seitenrand
const CW = W - 2 * M;                        // Inhaltsbreite = 11.933

const shadow = () => ({ type: "outer", color: "0F172A", blur: 14, offset: 2, angle: 90, opacity: 0.07 });

/* ---------------- SVG → PNG ---------------- */
const LOGO_SVG = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 70.1445 69.8402" width="512" height="512">
<path d="M9.0078,0h56.6585c2.3085,0,4.1832,1.8653,4.1947,4.1738l.2835,56.6915c.0124,2.4796-3.5307,2.9248-4.1321.5192l-8.4761-33.9046c-1.8201-7.2802-7.5045-12.9646-14.7847-14.7847L8.4991,4.1322c-2.3995-.5999-1.9647-4.1322.5087-4.1322Z" fill="#FF5533"/>
<path d="M45.2096,37.9781L3.3785,69.3983c-1.9407,1.4577-4.3943-.996-2.9367-2.9366L31.8618,24.6306c3.162-4.2099,9.138-5.0591,13.3477-1.8972,5.0582,3.6732,5.0288,11.5747,0,15.2448h0Z" fill="#FF5533"/></svg>`;

const ICONS = {
  x:        `<path d="M18 6L6 18M6 6l12 12"/>`,
  lock:     `<rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>`,
  shield:   `<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12l2 2l4-4"/>`,
  alert:    `<circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/>`,
  repeat:   `<path d="m17 2l4 4l-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="m7 22l-4-4l4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/>`,
  clock:    `<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>`,
  layers:   `<path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m6.08 9.5l-3.5 1.6a1 1 0 0 0 0 1.81l8.6 3.91a2 2 0 0 0 1.65 0l8.58-3.9a1 1 0 0 0 0-1.83l-3.5-1.59"/><path d="m6.08 14.5l-3.5 1.6a1 1 0 0 0 0 1.81l8.6 3.91a2 2 0 0 0 1.65 0l8.58-3.9a1 1 0 0 0 0-1.83l-3.5-1.59"/>`,
  trending: `<path d="M22 7l-8.5 8.5l-5-5L2 17"/><path d="M16 7h6v6"/>`,
  fileCheck:`<path d="M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z"/><path d="M14 2v5a1 1 0 0 0 1 1h5M9 15l2 2l4-4"/>`,
  message:  `<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>`,
};

async function png(svg) {
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}
const iconSvg = (name, color) =>
  `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="256" height="256" fill="none"
     stroke="${color}" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">${ICONS[name]}</svg>`;

/* ---------------- Bausteine ---------------- */
function card(slide, x, y, w, h, opt = {}) {
  slide.addShape("roundRect", {
    x, y, w, h, rectRadius: 0.1,
    fill: { color: opt.fill || C.card },
    line: { color: opt.line || C.line, width: 1 },
    ...(opt.flat ? {} : { shadow: shadow() }),
  });
}

function iconBox(slide, img, x, y, opt = {}) {
  const s = opt.size || 0.44;
  slide.addShape("roundRect", {
    x, y, w: s, h: s, rectRadius: 0.06,
    fill: { color: opt.bg || C.tint },
    line: { color: opt.line || C.tint2, width: 1 },
  });
  slide.addImage({ data: img, x: x + s * 0.24, y: y + s * 0.24, w: s * 0.52, h: s * 0.52 });
}

function header(slide, kicker, logo) {
  slide.addText(kicker.toUpperCase(), {
    x: M, y: 0.4, w: 8, h: 0.3, fontFace: F.body, fontSize: 10, bold: true,
    color: C.muted, charSpacing: 1.6, margin: 0, valign: "middle",
  });
  slide.addText("AthenaRun", {
    x: 10.6, y: 0.4, w: 1.55, h: 0.3, fontFace: F.head, fontSize: 12,
    color: C.ink, align: "right", margin: 0, valign: "middle",
  });
  slide.addImage({ data: logo, x: 12.28, y: 0.44, w: 0.23, h: 0.23 });
}

function footer(slide, num) {
  slide.addText("AthenaRun · Marktbeobachtung CDMO", {
    x: M, y: 6.92, w: 7, h: 0.28, fontFace: F.body, fontSize: 9, color: C.muted, margin: 0, valign: "middle",
  });
  slide.addText(num, {
    x: W - M - 1, y: 6.92, w: 1, h: 0.28, fontFace: F.body, fontSize: 9, color: C.muted,
    align: "right", margin: 0, valign: "middle",
  });
}

/* ---------------- Deck ---------------- */
async function main() {
  const logo = await png(LOGO_SVG);
  const ic = {};
  for (const k of Object.keys(ICONS)) {
    ic[k] = await png(iconSvg(k, "#FF5533"));
    ic[k + "_m"] = await png(iconSvg(k, "#94A3B8"));
  }

  const p = new pptxgen();
  p.layout = "LAYOUT_WIDE";
  p.author = "AthenaRun";
  p.title = "Marktbeobachtung CDMO";

  const newSlide = () => { const s = p.addSlide(); s.background = { color: C.bg }; return s; };

  /* ========== 1 · Titel ========== */
  {
    const s = newSlide();
    s.addImage({ data: logo, x: 8.9, y: 1.5, w: 4.6, h: 4.6, transparency: 94 });

    s.addImage({ data: logo, x: M, y: 0.55, w: 0.3, h: 0.3 });
    s.addText("AthenaRun", {
      x: M + 0.42, y: 0.55, w: 2.2, h: 0.3, fontFace: F.head, fontSize: 14, color: C.ink, margin: 0, valign: "middle",
    });

    s.addShape("roundRect", {
      x: M, y: 1.95, w: 2.72, h: 0.4, rectRadius: 0.2,
      fill: { color: C.tint }, line: { color: C.tintLn, width: 1 },
    });
    s.addShape("ellipse", { x: M + 0.2, y: 2.11, w: 0.09, h: 0.09, fill: { color: C.accent }, line: { color: C.accent, width: 0 } });
    s.addText("Marktbeobachtung CDMO", {
      x: M + 0.36, y: 1.95, w: 2.3, h: 0.4, fontFace: F.body, fontSize: 11, color: C.accent, margin: 0, valign: "middle",
    });

    s.addText([
      { text: "Nachweisbare Marktbeobachtung", options: { breakLine: true } },
      { text: "statt stiller Zusammenfassung." },
    ], {
      x: M, y: 2.62, w: 9.2, h: 1.7, fontFace: F.head, fontSize: 40, bold: true,
      color: C.ink, lineSpacingMultiple: 1.06, margin: 0, valign: "top",
    });

    s.addText(
      "Was ein wöchentlicher Branchen-Newsletter leisten muss, damit er vor VRP, Versicherer und Prüfer Bestand hat — und warum ein Chat-Abo das strukturell nicht kann.",
      { x: M, y: 4.6, w: 7.6, h: 1.1, fontFace: F.body, fontSize: 15, color: C.ink2, lineSpacingMultiple: 1.3, margin: 0 }
    );

    s.addText("Gesprächsgrundlage · Termin mit Alexandra", {
      x: M, y: 6.5, w: 6, h: 0.3, fontFace: F.body, fontSize: 10, color: C.muted, margin: 0, valign: "middle",
    });
    s.addText("AthenaRun GmbH, Frankfurt am Main", {
      x: 6.6, y: 6.5, w: W - M - 6.6, h: 0.3, fontFace: F.body, fontSize: 10, color: C.muted,
      align: "right", margin: 0, valign: "middle",
    });
    s.addNotes("Einstieg: Ziel des Termins ist nicht ein Newsletter-Angebot, sondern der Unterschied zwischen einer Zusammenfassung und einem nachweisbaren Prozess.");
  }

  /* ========== 2 · Ihr Ziel ========== */
  {
    const s = newSlide();
    header(s, "01 · Ihr Ziel", logo);

    card(s, M, 1.12, CW, 1.92);
    s.addText("ANFORDERUNG", {
      x: M + 0.42, y: 1.36, w: 3, h: 0.26, fontFace: F.body, fontSize: 9.5, bold: true,
      color: C.accent, charSpacing: 1.4, margin: 0, valign: "middle",
    });
    s.addText([
      { text: "„A comprehensive weekly newsletter to understand " },
      { text: "key trends", options: { color: C.accent } },
      { text: " in the CDMO sector.“" },
    ], {
      x: M + 0.42, y: 1.72, w: CW - 0.84, h: 1.1, fontFace: F.head, fontSize: 23,
      color: C.ink, lineSpacingMultiple: 1.25, margin: 0, valign: "top",
    });

    const cw = (CW - 0.4) / 3, cy = 3.34, ch = 2.85;
    const cols = [
      ["clock", "Wöchentlich", "Fester Takt, nicht anlassbezogen. Jede Woche ein Lauf, der stattfindet — auch wenn niemand nachfragt."],
      ["layers", "Umfassend", "Vollständige, definierte Quellenbasis. „Umfassend“ ist nur prüfbar, wenn die Basis benannt und ihr Zustand messbar ist."],
      ["trending", "Trends erkennbar", "Trends zeigen sich erst im Vergleich über Monate — und der setzt voraus, dass jede Woche dasselbe gemessen wird."],
    ];
    cols.forEach(([icon, t, b], i) => {
      const x = M + i * (cw + 0.2);
      card(s, x, cy, cw, ch);
      iconBox(s, ic[icon], x + 0.36, cy + 0.34);
      s.addText(t, { x: x + 0.36, y: cy + 0.96, w: cw - 0.72, h: 0.34, fontFace: F.head, fontSize: 16, bold: true, color: C.ink, margin: 0, valign: "middle" });
      s.addText(b, { x: x + 0.36, y: cy + 1.36, w: cw - 0.72, h: 1.28, fontFace: F.body, fontSize: 12.5, color: C.ink2, lineSpacingMultiple: 1.25, margin: 0, valign: "top" });
    });

    footer(s, "01");
    s.addNotes("Die drei Begriffe aus ihrem eigenen Satz sind bereits die Anforderungsliste — jeder einzelne ist ohne Messung nicht prüfbar.");
  }

  /* ========== 3 · Befund ========== */
  {
    const s = newSlide();
    header(s, "02 · Befund aus der ersten Stunde Messung", logo);

    const hw = (CW - 0.2) / 2;
    const stats = [
      ["x", "2 Quellen", "tot — HTTP 410, Betrieb eingestellt"],
      ["lock", "Mehrere", "verbieten AI-Nutzung explizit — FT, Endpoints …"],
    ];
    stats.forEach(([icon, v, l], i) => {
      const x = M + i * (hw + 0.2);
      card(s, x, 1.12, hw, 1.95);
      iconBox(s, ic[icon], x + 0.4, 1.42);
      s.addText(v, { x: x + 1.0, y: 1.38, w: hw - 1.4, h: 0.62, fontFace: F.head, fontSize: 30, bold: true, color: C.ink, margin: 0, valign: "middle" });
      s.addText(l, { x: x + 0.4, y: 2.22, w: hw - 0.8, h: 0.66, fontFace: F.body, fontSize: 12.5, color: C.ink2, lineSpacingMultiple: 1.2, margin: 0, valign: "top" });
    });

    card(s, M, 3.28, CW, 1.4, { fill: C.tint, line: C.tintLn, flat: true });
    iconBox(s, ic.alert, M + 0.42, 3.65, { bg: C.card, line: C.tintLn });
    s.addText([
      { text: "Ein Chat oder eine Routine überwacht tote und gesperrte Quellen stumm weiter.", options: { bold: true } },
      { text: " Sie liefert halt weniger — und niemand merkt es." },
    ], {
      x: M + 1.06, y: 3.5, w: CW - 1.5, h: 0.96, fontFace: F.body, fontSize: 15,
      color: C.ink, lineSpacingMultiple: 1.28, margin: 0, valign: "middle",
    });

    card(s, M, 4.9, CW, 1.42, { fill: C.flat, flat: true });
    iconBox(s, ic.shield, M + 0.42, 5.25, { bg: C.card, line: C.line });
    s.addText([
      { text: "Wir haben das in der " },
      { text: "ersten Stunde Messung", options: { bold: true, color: C.ink } },
      { text: " gefunden, weil Quellen-Validierung Teil des Produkts ist: Ausfälle werden " },
      { text: "erkannt, gemeldet, ersetzt.", options: { bold: true, color: C.ink } },
    ], {
      x: M + 1.06, y: 5.12, w: CW - 1.5, h: 0.98, fontFace: F.body, fontSize: 13.5,
      color: C.ink2, lineSpacingMultiple: 1.28, margin: 0, valign: "middle",
    });

    footer(s, "02");
    s.addNotes("Wichtig: Das ist kein hypothetisches Risiko, sondern der Befund aus ihrer eigenen Quellenliste — nach einer Stunde.");
  }

  /* ========== 4 · Argument 1 ========== */
  {
    const s = newSlide();
    header(s, "03 · Argument 1", logo);
    s.addText("Prozess-Beweis statt Selbstauskunft.", {
      x: M, y: 0.92, w: CW, h: 0.62, fontFace: F.head, fontSize: 30, bold: true, color: C.ink, margin: 0, valign: "middle",
    });

    const hw = (CW - 0.2) / 2, cy = 1.78, ch = 3.05;

    card(s, M, cy, hw, ch, { fill: C.flat, flat: true });
    s.addText("SELBSTAUSKUNFT", {
      x: M + 0.4, y: cy + 0.3, w: hw - 0.8, h: 0.26, fontFace: F.body, fontSize: 9.5, bold: true,
      color: C.muted, charSpacing: 1.4, margin: 0, valign: "middle",
    });
    s.addText("„Frag Claude nach der Quellenliste“", {
      x: M + 0.4, y: cy + 0.62, w: hw - 0.8, h: 0.36, fontFace: F.head, fontSize: 16, bold: true, color: C.ink, margin: 0, valign: "middle",
    });
    s.addText([
      { text: "Liefert eine Behauptung des Modells — dieselbe Klasse Output wie halluzinierte Zitate.", options: { bullet: { code: "2715" }, breakLine: true, paraSpaceAfter: 8 } },
      { text: "Unabhängig prüfbar ist daran nichts.", options: { bullet: { code: "2715" }, breakLine: true, paraSpaceAfter: 8 } },
      { text: "Scheitert ein Abruf, fasst der Chat stillschweigend zusammen, was er hat.", options: { bullet: { code: "2715" } } },
    ], {
      x: M + 0.4, y: cy + 1.12, w: hw - 0.8, h: 1.7, fontFace: F.body, fontSize: 12.5,
      color: C.ink2, lineSpacingMultiple: 1.2, margin: 0, valign: "top",
    });

    const x2 = M + hw + 0.2;
    card(s, x2, cy, hw, ch);
    s.addText("MASCHINEN-EVIDENZ", {
      x: x2 + 0.4, y: cy + 0.3, w: hw - 1.0, h: 0.26, fontFace: F.body, fontSize: 9.5, bold: true,
      color: C.accent, charSpacing: 1.4, margin: 0, valign: "middle",
    });
    s.addImage({ data: ic.fileCheck, x: x2 + hw - 0.72, y: cy + 0.28, w: 0.3, h: 0.3 });
    s.addText("Unser Lauf erzeugt Nachweise", {
      x: x2 + 0.4, y: cy + 0.62, w: hw - 0.8, h: 0.36, fontFace: F.head, fontSize: 16, bold: true, color: C.ink, margin: 0, valign: "middle",
    });
    s.addText([
      { text: "HTTP-Status je Quelle, je Lauf", options: { bullet: { code: "2713" }, breakLine: true, paraSpaceAfter: 8 } },
      { text: "Item-Hashes und Zeitstempel", options: { bullet: { code: "2713" }, breakLine: true, paraSpaceAfter: 8 } },
      { text: "Hash-verkettete Audit-Kette mit signiertem Export", options: { bullet: { code: "2713" }, breakLine: true, paraSpaceAfter: 8 } },
      { text: "Läuft bereits — Teil der 158 Tests", options: { bullet: { code: "2713" } } },
    ], {
      x: x2 + 0.4, y: cy + 1.12, w: hw - 0.8, h: 1.7, fontFace: F.body, fontSize: 12.5,
      color: C.ink2, lineSpacingMultiple: 1.2, margin: 0, valign: "top",
    });

    card(s, M, 5.05, CW, 1.5, { fill: C.tint, line: C.tintLn, flat: true });
    s.addText([
      { text: "Fragt VRP, Versicherer oder Prüfer „Zeigen Sie Ihren Marktbeobachtungsprozess“, übergibt sie einen " },
      { text: "signierten Export", options: { bold: true, color: C.ink } },
      { text: " — kein Chat-Transkript. Ihre eigene Bayer/Monsanto-Analogie: Haftung entfällt bei " },
      { text: "nachweislich", options: { bold: true, color: C.ink } },
      { text: " sorgfältiger Grundlage. " },
      { text: "„Nachweislich“ ist das Produkt.", options: { bold: true, color: C.accent } },
    ], {
      x: M + 0.42, y: 5.2, w: CW - 0.84, h: 1.2, fontFace: F.body, fontSize: 13.5,
      color: C.ink2, lineSpacingMultiple: 1.28, margin: 0, valign: "middle",
    });

    footer(s, "03");
    s.addNotes("Kernsatz: Eine Modellantwort über die Quellen ist derselbe Output-Typ wie ein halluziniertes Zitat. Evidenz entsteht nur außerhalb des Modells.");
  }

  /* ========== 5 · Argument 2 ========== */
  {
    const s = newSlide();
    header(s, "04 · Argument 2", logo);
    s.addText([
      { text: "Verantwortung ist delegierbar,", options: { breakLine: true } },
      { text: "an einen Chat nicht." },
    ], {
      x: M, y: 0.9, w: CW, h: 1.1, fontFace: F.head, fontSize: 30, bold: true,
      color: C.ink, lineSpacingMultiple: 1.08, margin: 0, valign: "middle",
    });

    const hw = (CW - 0.2) / 2, ch = 1.98;
    const items = [
      ["shield", "Eine Vertragspartei haftet", [["Bei uns ist eine Vertragspartei dafür verantwortlich, dass das Monitoring "], ["läuft", 1], [", "], ["vollständig", 1], [" ist und "], ["rechtlich sauber beschafft", 1], [" wird."]], false],
      ["alert_m", "Ein Abo schuldet ihr nichts", [["Verhungert die Routine still, "], ["haftet niemand", 1], [". Es gibt keine Zusage, die verletzt werden könnte — und keinen Adressaten für die Frage, warum Wochen fehlen."]], true],
      ["repeat", "Identischer Lauf, jede Woche", [["Ergebnisse bleiben über Monate vergleichbar — Voraussetzung für die gewünschte "], ["Trendanalyse", 1], [". Ein Chat improvisiert jede Woche neu."]], false],
      ["lock", "Beweisbar whitelist-only", [["Beschaffung ausschließlich aus freigegebenen Quellen. Eine "], ["offene Websuche", 1], [" spült FT-Content über Snippets herein — ob sie will oder nicht."]], false],
    ];
    items.forEach(([icon, title, parts, flat], i) => {
      const x = M + (i % 2) * (hw + 0.2);
      const y = 2.18 + Math.floor(i / 2) * (ch + 0.2);
      card(s, x, y, hw, ch, flat ? { fill: C.flat, flat: true } : {});
      iconBox(s, ic[icon], x + 0.36, y + 0.3, flat ? { bg: C.card, line: C.line } : {});
      s.addText(title, {
        x: x + 0.94, y: y + 0.3, w: hw - 1.3, h: 0.44, fontFace: F.head, fontSize: 15.5, bold: true,
        color: C.ink, margin: 0, valign: "middle",
      });
      s.addText(parts.map(([t, b]) => ({ text: t, options: b ? { bold: true, color: C.ink } : {} })), {
        x: x + 0.36, y: y + 0.86, w: hw - 0.72, h: 0.92, fontFace: F.body, fontSize: 12.5,
        color: C.ink2, lineSpacingMultiple: 1.24, margin: 0, valign: "top",
      });
    });

    footer(s, "04");
    s.addNotes("Der Unterschied ist vertraglich, nicht technisch: Bei einem Abo gibt es keinen Adressaten für eine ausgefallene Woche.");
  }

  /* ========== 6 · Gegenüberstellung ========== */
  {
    const s = newSlide();
    header(s, "05 · Gegenüberstellung", logo);
    s.addText("Chat-Routine oder Marktbeobachtung.", {
      x: M, y: 0.92, w: CW, h: 0.6, fontFace: F.head, fontSize: 28, bold: true, color: C.ink, margin: 0, valign: "middle",
    });

    const th = { fontFace: F.body, fontSize: 9.5, bold: true, color: C.muted, charSpacing: 1.3, fill: { color: C.flat } };
    const rows = [
      [{ text: "", options: th }, { text: "CHAT / ABO", options: th }, { text: "ATHENARUN", options: { ...th, color: C.accent } }],
      ["Quellenliste", "Behauptung des Modells", "HTTP-Status je Quelle, je Lauf"],
      ["Quellenausfall", "bleibt stumm, Output schrumpft", "erkannt, gemeldet, ersetzt"],
      ["Nachweis", "Chat-Transkript", "signierter Export, hash-verkettet"],
      ["Verantwortung", "niemand", "Vertragspartei"],
      ["Wiederholbarkeit", "wöchentlich neu improvisiert", "identischer Lauf, vergleichbar über Monate"],
      ["Beschaffung", "offene Websuche, FT-Content über Snippets", "beweisbar whitelist-only"],
    ].map((r, i) =>
      i === 0 ? r : [
        { text: r[0], options: { color: C.ink2, bold: true } },
        { text: r[1], options: { color: C.muted } },
        { text: r[2], options: { color: C.ink, bold: true } },
      ]
    );

    s.addTable(rows, {
      x: M, y: 1.72, w: CW, colW: [2.6, 4.4, 4.933],
      rowH: [0.36, 0.62, 0.62, 0.62, 0.62, 0.62, 0.62],
      fontFace: F.body, fontSize: 13, valign: "middle",
      fill: { color: C.card },
      border: [
        { type: "solid", color: C.line, pt: 1 },
        { type: "none" },
        { type: "solid", color: C.line, pt: 1 },
        { type: "none" },
      ],
      margin: [0, 14, 0, 14],
    });

    footer(s, "05");
    s.addNotes("Abschluss: Jede Zeile ist eine Frage, die im Ernstfall gestellt wird. Die linke Spalte hat auf keine davon eine belegbare Antwort.");
  }

  const out = "/home/user/Athena/AthenaRun-Marktbeobachtung-CDMO.pptx";
  await p.writeFile({ fileName: out });
  await fixBullets(out);
  console.log("geschrieben");
}

/* pptxgenjs schreibt <a:buChar> ohne <a:buFont>. U+2713/U+2715 fehlen in Arial —
   auf fremden Rechnern droht ein Ersatzkästchen. Auf Wingdings umstellen (dort
   0xFC = Haken, 0xFB = Kreuz) und die Marke einfärben. */
async function fixBullets(file) {
  const JSZip = require("jszip");
  const fs = require("fs");
  const zip = await JSZip.loadAsync(fs.readFileSync(file));
  const wing = '<a:buFont typeface="Wingdings" pitchFamily="2" charset="2"/>';
  const map = [
    ['<a:buChar char="&#x2713;"/>', `<a:buClr><a:srgbClr val="${C.accent}"/></a:buClr>${wing}<a:buChar char="&#xFC;"/>`],
    ['<a:buChar char="&#x2715;"/>', `<a:buClr><a:srgbClr val="${C.muted}"/></a:buClr>${wing}<a:buChar char="&#xFB;"/>`],
  ];
  for (const name of Object.keys(zip.files)) {
    if (!/^ppt\/slides\/slide\d+\.xml$/.test(name)) continue;
    let xml = await zip.file(name).async("string");
    let touched = false;
    for (const [from, to] of map) {
      if (xml.includes(from)) { xml = xml.split(from).join(to); touched = true; }
    }
    if (touched) zip.file(name, xml);
  }
  fs.writeFileSync(file, await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" }));
}

main().catch((e) => { console.error(e); process.exit(1); });
