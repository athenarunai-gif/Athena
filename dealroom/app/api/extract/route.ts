import { NextRequest } from 'next/server';
import Anthropic from '@anthropic-ai/sdk';
import { ExtractedData, FinancialYear, AdjustmentItem, Gap, Warning, ContractRisk } from '@/app/lib/types';

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

function generateId(): string {
  return Math.random().toString(36).substring(2, 11);
}

interface DocumentInput {
  id: string;
  name: string;
  category: string;
  base64Data?: string;
  content?: string;
  mimeType?: string;
}

export async function POST(request: NextRequest) {
  try {
    const { documents }: { documents: DocumentInput[] } = await request.json();

    if (!documents || documents.length === 0) {
      return Response.json({ error: 'No documents provided' }, { status: 400 });
    }

    if (!process.env.ANTHROPIC_API_KEY) {
      return Response.json({ error: 'ANTHROPIC_API_KEY not configured' }, { status: 500 });
    }

    // Build content blocks for Claude
    const contentBlocks: Anthropic.MessageParam['content'] = [];

    contentBlocks.push({
      type: 'text',
      text: `Du bist ein erfahrener M&A-Berater und Finanzanalyst. Analysiere die folgenden Unternehmensdokumente und extrahiere alle relevanten Informationen für ein Information Memorandum (IM).

Wichtige Hinweise:
- Extrahiere alle Finanzkennzahlen für die letzten 3 verfügbaren Jahre
- Identifiziere Einmaleffekte und Bereinigungen für das EBITDA
- Erkenne Risiken, Vertragsklauseln und Abhängigkeiten
- Melde fehlende Informationen als "Gaps"
- Melde Widersprüche zwischen Dokumenten als "Warnings"
- Alle Geldbeträge in Euro (oder die im Dokument angegebene Währung)

Antworte NUR mit validem JSON ohne Markdown-Code-Blöcke. Das JSON muss exakt der folgenden Struktur entsprechen:

{
  "financials": [
    {
      "year": 2023,
      "revenue": 5000000,
      "ebitda": 750000,
      "ebitdaMargin": 15.0,
      "ebit": 600000,
      "cashflow": 500000,
      "equity": 2000000,
      "source": "Jahresabschluss 2023"
    }
  ],
  "adjustments": [
    {
      "description": "Einmaliger Rechtsstreit",
      "amount": 150000,
      "type": "one_time_expense",
      "year": 2023,
      "source": "Dokumentname"
    }
  ],
  "workingCapital": [
    {
      "year": 2023,
      "receivables": 800000,
      "inventories": 300000,
      "payables": 400000,
      "workingCapital": 700000,
      "source": "Bilanz 2023"
    }
  ],
  "companyStructure": {
    "name": "Muster GmbH",
    "foundedYear": 2005,
    "legalForm": "GmbH",
    "shareholders": [{"name": "Max Mustermann", "stake": 100}],
    "subsidiaries": [],
    "locations": ["München", "Berlin"],
    "headcount": 150,
    "management": [{"name": "Max Mustermann", "role": "Geschäftsführer", "yearsInRole": 10}],
    "source": "Handelsregister"
  },
  "risks": [
    {
      "type": "customer_concentration",
      "description": "Top-3-Kunden machen 60% des Umsatzes aus",
      "severity": "high",
      "details": "Kunden A, B, C sind für je 20% verantwortlich",
      "source": "Kundenumsatzliste"
    }
  ],
  "market": {
    "mainProducts": [
      {"name": "Produkt A", "margin": 35.0, "revenueShare": 60.0, "description": "Kernprodukt"}
    ],
    "customerSegments": [
      {"name": "Industrie", "revenueShare": 70.0}
    ],
    "marketShareDescription": "ca. 15% Marktanteil in Deutschland",
    "competitors": ["Wettbewerber A", "Wettbewerber B"],
    "source": "Strategiepräsentation"
  },
  "gaps": [
    {
      "category": "financial",
      "description": "Jahresabschluss 2021 fehlt",
      "severity": "critical",
      "missingItem": "Jahresabschluss 2021"
    }
  ],
  "warnings": [
    {
      "type": "contradiction",
      "description": "Umsatz 2023 unterscheidet sich zwischen zwei Dokumenten",
      "sources": ["Dokument A", "Dokument B"]
    }
  ]
}

Wenn du bestimmte Informationen nicht findest, lass das Feld leer (null) oder verwende ein leeres Array. Schreibe KEIN Text außerhalb des JSON-Objekts.

Analysiere jetzt folgende Dokumente:`
    });

    // Add each document as content
    for (const doc of documents) {
      const ext = doc.name.split('.').pop()?.toLowerCase();
      const isPdf = ext === 'pdf' || doc.mimeType?.includes('pdf');
      const isExcel = ext === 'xlsx' || ext === 'xls' || doc.mimeType?.includes('spreadsheet') || doc.mimeType?.includes('excel');
      const isWord = ext === 'docx' || ext === 'doc' || doc.mimeType?.includes('word');

      contentBlocks.push({
        type: 'text',
        text: `\n\n--- DOKUMENT: "${doc.name}" (Kategorie: ${doc.category}) ---`
      });

      if (isPdf && doc.base64Data) {
        try {
          contentBlocks.push({
            type: 'document',
            source: {
              type: 'base64',
              media_type: 'application/pdf',
              data: doc.base64Data,
            },
          } as Anthropic.DocumentBlockParam);
        } catch {
          // Fallback to text if PDF parsing fails
          contentBlocks.push({
            type: 'text',
            text: doc.content || '[PDF-Inhalt konnte nicht gelesen werden]'
          });
        }
      } else if (doc.content) {
        // Text content (CSV, TXT, or pre-extracted)
        contentBlocks.push({
          type: 'text',
          text: doc.content.substring(0, 10000) // limit token usage
        });
      } else if (doc.base64Data) {
        // Try to decode as text for Excel/Word
        try {
          const decoded = atob(doc.base64Data);
          // Check if it's readable text
          const isText = /^[\x20-\x7E\n\r\t]*$/.test(decoded.substring(0, 100));
          if (isText) {
            contentBlocks.push({
              type: 'text',
              text: decoded.substring(0, 10000)
            });
          } else {
            contentBlocks.push({
              type: 'text',
              text: `[Binärdatei: ${doc.name} - Typ: ${doc.mimeType || ext}. Konnte nicht als Text gelesen werden. Bitte gib an welche Informationen fehlen.]`
            });
          }
        } catch {
          contentBlocks.push({
            type: 'text',
            text: `[Datei: ${doc.name} konnte nicht dekodiert werden]`
          });
        }
      } else {
        contentBlocks.push({
          type: 'text',
          text: `[Datei: ${doc.name} - Kein Inhalt verfügbar]`
        });
      }
    }

    // Call Claude API with streaming for long outputs
    let fullResponse = '';

    const stream = client.messages.stream({
      model: 'claude-opus-4-6',
      max_tokens: 16000,
      thinking: { type: 'adaptive' },
      messages: [
        {
          role: 'user',
          content: contentBlocks,
        }
      ],
    });

    for await (const event of stream) {
      if (event.type === 'content_block_delta' && event.delta.type === 'text_delta') {
        fullResponse += event.delta.text;
      }
    }

    // Parse the JSON response
    let extracted: Partial<ExtractedData> = {};
    try {
      // Clean up the response (remove potential markdown code blocks)
      const cleaned = fullResponse
        .replace(/```json\s*/g, '')
        .replace(/```\s*/g, '')
        .trim();

      const parsed = JSON.parse(cleaned);

      // Add IDs to risks, gaps, warnings
      extracted = {
        financials: (parsed.financials || []).map((f: FinancialYear) => ({
          ...f,
          ebitdaMargin: f.ebitdaMargin ?? (f.revenue && f.ebitda ? (f.ebitda / f.revenue) * 100 : undefined),
        })),
        adjustments: (parsed.adjustments || []).map((a: AdjustmentItem) => ({ ...a, id: generateId() })),
        workingCapital: parsed.workingCapital || [],
        companyStructure: parsed.companyStructure,
        risks: (parsed.risks || []).map((r: ContractRisk) => ({ ...r, id: generateId() })),
        market: parsed.market,
        gaps: (parsed.gaps || []).map((g: Gap) => ({ ...g, id: generateId() })),
        warnings: (parsed.warnings || []).map((w: Warning) => ({ ...w, id: generateId() })),
        extractedAt: new Date().toISOString(),
      };
    } catch (parseError) {
      console.error('JSON parse error:', parseError);
      console.error('Raw response:', fullResponse.substring(0, 500));

      // Return a minimal structure with a warning
      extracted = {
        financials: [],
        adjustments: [],
        workingCapital: [],
        risks: [],
        gaps: [{
          id: generateId(),
          category: 'general',
          description: 'Automatische Extraktion fehlgeschlagen. Bitte überprüfen Sie die hochgeladenen Dokumente.',
          severity: 'critical',
          missingItem: 'Alle Daten',
        }],
        warnings: [{
          id: generateId(),
          type: 'data_quality',
          description: 'Die KI-Antwort konnte nicht als strukturiertes JSON geparst werden.',
          sources: ['Claude API'],
        }],
        extractedAt: new Date().toISOString(),
      };
    }

    return Response.json({ extracted });
  } catch (error) {
    console.error('Extraction error:', error);
    const message = error instanceof Error ? error.message : 'Unknown error';
    return Response.json({ error: `Extraction failed: ${message}` }, { status: 500 });
  }
}
