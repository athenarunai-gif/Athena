import { NextRequest } from 'next/server';
import { DocumentCategory } from '@/app/lib/types';

// Categorize document by filename and content hints
function categorizeDocument(filename: string, mimeType: string): DocumentCategory {
  const lower = filename.toLowerCase();

  const financialKeywords = ['finan', 'bilanz', 'jahresabschluss', 'guv', 'gewinn', 'verlust', 'bwa', 'p&l', 'balance', 'income', 'cashflow', 'liquidity', 'revenue', 'ebitda', 'controlling', 'budget', 'forecast', 'plan', 'excel', 'financial'];
  const contractKeywords = ['vertrag', 'contract', 'agreement', 'kunden', 'lieferant', 'supplier', 'nda', 'lease', 'mietvertrag', 'rahmenvertrag', 'sla'];
  const hrKeywords = ['hr', 'personal', 'mitarbeiter', 'organigramm', 'org', 'gehalt', 'salary', 'organigram', 'management'];
  const strategyKeywords = ['strategie', 'strategy', 'market', 'markt', 'produkt', 'product', 'wettbewerb', 'competition', 'swot', 'businessplan', 'business plan', 'pitch'];
  const customerKeywords = ['kunde', 'customer', 'client', 'umsatz', 'segement', 'crm', 'sales'];

  for (const kw of financialKeywords) {
    if (lower.includes(kw)) return 'financial';
  }
  for (const kw of contractKeywords) {
    if (lower.includes(kw)) return 'contracts';
  }
  for (const kw of hrKeywords) {
    if (lower.includes(kw)) return 'hr';
  }
  for (const kw of strategyKeywords) {
    if (lower.includes(kw)) return 'strategy';
  }
  for (const kw of customerKeywords) {
    if (lower.includes(kw)) return 'customer_data';
  }

  // Spreadsheets are often financial
  if (mimeType.includes('spreadsheet') || mimeType.includes('excel') || lower.endsWith('.xlsx') || lower.endsWith('.xls') || lower.endsWith('.csv')) {
    return 'financial';
  }

  return 'unknown';
}

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const files = formData.getAll('files') as File[];

    if (!files || files.length === 0) {
      return Response.json({ error: 'No files provided' }, { status: 400 });
    }

    const results = [];

    for (const file of files) {
      const category = categorizeDocument(file.name, file.type);

      // Read file content for text extraction
      const buffer = await file.arrayBuffer();
      const bytes = new Uint8Array(buffer);

      let content = '';
      let base64Data = '';

      // Convert to base64 for Claude API
      const binaryString = Array.from(bytes)
        .map(byte => String.fromCharCode(byte))
        .join('');
      base64Data = btoa(binaryString);

      // For text-based files, extract text directly
      const ext = file.name.split('.').pop()?.toLowerCase();
      if (ext === 'txt' || ext === 'md' || ext === 'csv') {
        content = new TextDecoder().decode(bytes);
      }

      results.push({
        id: Math.random().toString(36).substring(2, 11),
        name: file.name,
        type: file.type || `application/${ext}`,
        size: file.size,
        category,
        base64Data,
        content: content.substring(0, 5000), // limit for storage
        mimeType: file.type,
      });
    }

    return Response.json({ files: results });
  } catch (error) {
    console.error('Upload error:', error);
    return Response.json({ error: 'Upload failed' }, { status: 500 });
  }
}
