import { Slide, ExtractedData } from './types';
import { formatCurrency, formatPercent } from './utils';

// Dynamic import to avoid SSR issues
async function getPptxGen() {
  const pptxgenjs = await import('pptxgenjs');
  return pptxgenjs.default;
}

const BRAND_NAVY = '1a2744';
const BRAND_GOLD = 'c9a84c';
const BRAND_LIGHT = 'f0f4f8';
const TEXT_WHITE = 'ffffff';
const TEXT_DARK = '1e293b';
const TEXT_GRAY = '64748b';

export async function exportToPptx(slides: Slide[], extracted: ExtractedData | null, projectName = 'DealRoom Präsentation'): Promise<void> {
  const PptxGenJS = await getPptxGen();
  const pptx = new PptxGenJS();

  pptx.layout = 'LAYOUT_WIDE';
  pptx.author = 'DealRoom';
  pptx.company = 'DealRoom M&A';
  pptx.title = projectName;

  // Define slide master / theme
  const MASTER = {
    title: 'MASTER',
    bkgd: TEXT_WHITE,
  };

  for (let i = 0; i < slides.length; i++) {
    const slide = slides[i];
    const pptSlide = pptx.addSlide();

    // Background
    pptSlide.background = { color: TEXT_WHITE };

    // Left accent bar
    pptSlide.addShape(pptx.ShapeType.rect, {
      x: 0, y: 0, w: 0.12, h: 5.63,
      fill: { color: BRAND_NAVY },
    });

    // Header background
    pptSlide.addShape(pptx.ShapeType.rect, {
      x: 0.12, y: 0, w: 9.88, h: 1.1,
      fill: { color: BRAND_NAVY },
    });

    // Slide number circle
    pptSlide.addShape(pptx.ShapeType.ellipse, {
      x: 9.0, y: 0.22, w: 0.65, h: 0.65,
      fill: { color: BRAND_GOLD },
    });
    pptSlide.addText(`${i + 1}`, {
      x: 9.0, y: 0.22, w: 0.65, h: 0.65,
      align: 'center', valign: 'middle',
      fontSize: 11, bold: true, color: TEXT_WHITE,
    });

    // Title
    pptSlide.addText(slide.title, {
      x: 0.35, y: 0.12, w: 8.4, h: 0.85,
      fontSize: 22, bold: true, color: TEXT_WHITE,
      fontFace: 'Calibri', valign: 'middle',
    });

    // Gold accent line
    pptSlide.addShape(pptx.ShapeType.rect, {
      x: 0.35, y: 1.1, w: 1.2, h: 0.04,
      fill: { color: BRAND_GOLD },
    });

    // Content area y start
    let yPos = 1.25;

    // Main content text
    if (slide.content) {
      pptSlide.addText(slide.content, {
        x: 0.35, y: yPos, w: 9.3, h: 0.7,
        fontSize: 12, color: TEXT_DARK,
        fontFace: 'Calibri',
        wrap: true,
      });
      yPos += 0.8;
    }

    // Bullet points
    if (slide.bulletPoints && slide.bulletPoints.length > 0) {
      const bulletText = slide.bulletPoints.map(b => ({
        text: b,
        options: { bullet: { type: 'bullet' as const, code: '25CF', indent: 15 }, fontSize: 13, color: TEXT_DARK, breakLine: true },
      }));

      pptSlide.addText(bulletText, {
        x: 0.5, y: yPos, w: 9.1, h: Math.min(slide.bulletPoints.length * 0.45 + 0.2, 3.8),
        fontFace: 'Calibri',
        paraSpaceAfter: 4,
      });
      yPos += Math.min(slide.bulletPoints.length * 0.45 + 0.2, 3.8);
    }

    // For financial slides, add table if data available
    if (slide.type === 'financial_overview' && extracted && extracted.financials.length > 0) {
      const financials = [...extracted.financials].sort((a, b) => a.year - b.year);

      const tableData = [
        [
          { text: 'Kennzahl', options: { bold: true, color: TEXT_WHITE, fill: { color: BRAND_NAVY } } },
          ...financials.map(f => ({ text: String(f.year), options: { bold: true, color: TEXT_WHITE, fill: { color: BRAND_NAVY }, align: 'center' as const } })),
        ],
        [
          { text: 'Umsatz', options: { color: TEXT_DARK } },
          ...financials.map(f => ({ text: formatCurrency(f.revenue), options: { color: TEXT_DARK, align: 'right' as const, fontFace: 'Courier New' } })),
        ],
        [
          { text: 'EBITDA', options: { color: TEXT_DARK } },
          ...financials.map(f => ({ text: formatCurrency(f.ebitda), options: { color: TEXT_DARK, align: 'right' as const, fontFace: 'Courier New' } })),
        ],
        [
          { text: 'EBITDA-Marge', options: { color: TEXT_DARK } },
          ...financials.map(f => ({ text: formatPercent(f.ebitdaMargin), options: { color: BRAND_NAVY, bold: true, align: 'right' as const } })),
        ],
        [
          { text: 'EBIT', options: { color: TEXT_DARK } },
          ...financials.map(f => ({ text: formatCurrency(f.ebit), options: { color: TEXT_DARK, align: 'right' as const, fontFace: 'Courier New' } })),
        ],
      ];

      const tableY = Math.min(yPos + 0.1, 4.2);
      if (tableY < 5.2) {
        pptSlide.addTable(tableData as Parameters<typeof pptSlide.addTable>[0], {
          x: 0.35, y: tableY, w: 9.3,
          rowH: 0.35,
          fontSize: 11,
          fontFace: 'Calibri',
          border: { pt: 0.5, color: 'e2e8f0' },
          colW: [2.8, ...financials.map(() => (9.3 - 2.8) / financials.length)],
        });
      }
    }

    // Footer
    pptSlide.addShape(pptx.ShapeType.rect, {
      x: 0.12, y: 5.43, w: 9.88, h: 0.2,
      fill: { color: BRAND_LIGHT },
    });
    pptSlide.addText('VERTRAULICH — DealRoom M&A', {
      x: 0.35, y: 5.43, w: 6, h: 0.2,
      fontSize: 7, color: TEXT_GRAY, valign: 'middle',
    });
    pptSlide.addText(new Date().toLocaleDateString('de-DE'), {
      x: 8, y: 5.43, w: 2, h: 0.2,
      fontSize: 7, color: TEXT_GRAY, align: 'right', valign: 'middle',
    });
  }

  // Add cover slide at the beginning
  const coverSlide = pptx.addSlide();
  coverSlide.background = { color: BRAND_NAVY };

  coverSlide.addShape(pptx.ShapeType.rect, {
    x: 0, y: 2.5, w: 10, h: 0.06,
    fill: { color: BRAND_GOLD },
  });

  coverSlide.addText('INFORMATION MEMORANDUM', {
    x: 0.5, y: 1.0, w: 9, h: 0.8,
    fontSize: 14, color: BRAND_GOLD, bold: true,
    fontFace: 'Calibri', align: 'center', charSpacing: 4,
  });

  coverSlide.addText(projectName, {
    x: 0.5, y: 1.8, w: 9, h: 1.2,
    fontSize: 32, color: TEXT_WHITE, bold: true,
    fontFace: 'Calibri', align: 'center',
  });

  coverSlide.addText('Vertraulich — Nur für autorisierte Empfänger', {
    x: 0.5, y: 3.0, w: 9, h: 0.5,
    fontSize: 11, color: TEXT_GRAY,
    fontFace: 'Calibri', align: 'center', italic: true,
  });

  coverSlide.addText(new Date().toLocaleDateString('de-DE', { month: 'long', year: 'numeric' }), {
    x: 0.5, y: 4.5, w: 9, h: 0.5,
    fontSize: 12, color: TEXT_GRAY,
    fontFace: 'Calibri', align: 'center',
  });

  await pptx.writeFile({ fileName: `${projectName.replace(/[^a-z0-9]/gi, '_')}_IM.pptx` });
}
