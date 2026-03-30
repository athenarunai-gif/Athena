import { NextRequest } from 'next/server';
import Anthropic from '@anthropic-ai/sdk';
import { ExtractedData, Slide, SlideStatus, SLIDE_DEFINITIONS } from '@/app/lib/types';

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

function generateId(): string {
  return Math.random().toString(36).substring(2, 11);
}

export async function POST(request: NextRequest) {
  try {
    const { extracted }: { extracted: ExtractedData } = await request.json();

    if (!process.env.ANTHROPIC_API_KEY) {
      return Response.json({ error: 'ANTHROPIC_API_KEY not configured' }, { status: 500 });
    }

    const dataJson = JSON.stringify(extracted, null, 2);

    const prompt = `Du bist ein erfahrener M&A-Berater. Erstelle auf Basis der extrahierten Unternehmensdaten den Inhalt für ein Information Memorandum (Investment Memorandum).

Extrahierte Daten:
${dataJson}

Erstelle professionelle Präsentationsfolien für ein M&A Information Memorandum. Antworte NUR mit validem JSON (kein Markdown). Das JSON muss exakt dieser Struktur entsprechen:

{
  "slides": [
    {
      "type": "executive_summary",
      "title": "Executive Summary",
      "content": "Kernbotschaft der Präsentation in 2-3 Sätzen",
      "bulletPoints": [
        "Unternehmen XYZ: führender Anbieter mit €5M Umsatz",
        "Starke EBITDA-Marge von 15%",
        "Attraktive Wachstumsperspektive durch..."
      ],
      "status": "filled"
    },
    {
      "type": "company_overview",
      "title": "Unternehmensüberblick",
      "content": "Beschreibung des Unternehmens",
      "bulletPoints": [
        "Gegründet 2005 als GmbH",
        "150 Mitarbeiter an 2 Standorten"
      ],
      "status": "filled"
    },
    {
      "type": "market_competition",
      "title": "Markt & Wettbewerb",
      "content": "Marktbeschreibung und Wettbewerbsposition",
      "bulletPoints": ["..."],
      "status": "filled"
    },
    {
      "type": "financial_overview",
      "title": "Finanzübersicht",
      "content": "Übersicht der Finanzkennzahlen 2021-2023",
      "bulletPoints": [
        "Umsatz: €4,5M (2021) → €4,8M (2022) → €5,0M (2023)",
        "EBITDA-Marge: stabil bei 14-16%"
      ],
      "status": "filled"
    },
    {
      "type": "ebitda_bridge",
      "title": "EBITDA-Brücke",
      "content": "Überleitung vom berichteten zum bereinigten EBITDA",
      "bulletPoints": [
        "Berichtetes EBITDA 2023: €750K",
        "Bereinigung: Einmaliger Rechtsstreit +€150K",
        "Bereinigtes EBITDA 2023: €900K (18% Marge)"
      ],
      "status": "filled"
    },
    {
      "type": "valuation_multiples",
      "title": "Bewertung & Multiples",
      "content": "Indikative Bewertung auf Basis von Peer-Multiples",
      "bulletPoints": [
        "EV/EBITDA-Multiple Peer Group: 7-9x",
        "Implizite Bewertung: €6,3M - €8,1M (auf Basis bereinigtes EBITDA)"
      ],
      "status": "in_progress"
    },
    {
      "type": "growth_strategy",
      "title": "Wachstumsstrategie",
      "content": "Organische und anorganische Wachstumshebel",
      "bulletPoints": ["..."],
      "status": "filled"
    },
    {
      "type": "risks_opportunities",
      "title": "Risiken & Chancen",
      "content": "Wesentliche Risiken und Wachstumschancen",
      "bulletPoints": ["..."],
      "status": "filled"
    },
    {
      "type": "appendix",
      "title": "Anhang",
      "content": "Detaillierte Finanzübersichten und ergänzende Informationen",
      "bulletPoints": ["Working Capital Analyse", "Detaillierte Gewinn- und Verlustrechnung"],
      "status": "in_progress"
    }
  ]
}

Wichtig:
- Nutze alle verfügbaren Daten um realistische, professionelle Inhalte zu erstellen
- Wenn Daten fehlen, markiere den Status als "in_progress" oder "empty"
- Alle Zahlen in den bulletPoints sollen die echten Daten aus den extrahierten Daten verwenden
- Professioneller M&A-Ton, sachlich und überzeugend
- Schreibe KEIN Text außerhalb des JSON-Objekts`;

    let fullResponse = '';

    const stream = client.messages.stream({
      model: 'claude-opus-4-6',
      max_tokens: 8000,
      messages: [{ role: 'user', content: prompt }],
    });

    for await (const event of stream) {
      if (event.type === 'content_block_delta' && event.delta.type === 'text_delta') {
        fullResponse += event.delta.text;
      }
    }

    let slides: Slide[] = [];

    try {
      const cleaned = fullResponse
        .replace(/```json\s*/g, '')
        .replace(/```\s*/g, '')
        .trim();

      const parsed = JSON.parse(cleaned);
      slides = (parsed.slides || []).map((s: Partial<Slide>) => ({
        ...s,
        id: generateId(),
        bulletPoints: s.bulletPoints || [],
        status: s.status || 'in_progress',
        lastEdited: new Date().toISOString(),
      }));
    } catch {
      // Fallback: create empty slide structure
      slides = SLIDE_DEFINITIONS.map(def => ({
        id: generateId(),
        type: def.type,
        title: def.title,
        content: '',
        bulletPoints: [],
        status: 'empty' as const,
        lastEdited: new Date().toISOString(),
      }));
    }

    return Response.json({ slides });
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Unknown error';
    return Response.json({ error: `Slide generation failed: ${message}` }, { status: 500 });
  }
}
