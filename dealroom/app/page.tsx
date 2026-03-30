'use client';

import { useState, useCallback } from 'react';
import {
  Upload, BarChart3, Presentation, ChevronRight,
  Sparkles, AlertCircle, RefreshCw, FileCheck
} from 'lucide-react';
import UploadZone from './components/UploadZone';
import CategoryProgress from './components/CategoryProgress';
import ExtractionDashboard from './components/ExtractionDashboard';
import PresentationBuilder from './components/PresentationBuilder';
import {
  UploadedDocument, DocumentCategory, ExtractedData,
  Slide, SLIDE_DEFINITIONS
} from './lib/types';

type AppTab = 'upload' | 'extraction' | 'presentation';

function generateId(): string {
  return Math.random().toString(36).substring(2, 11);
}

interface StoredDocMeta {
  base64Data: string;
  mimeType: string;
  category: DocumentCategory;
}

export default function DealRoom() {
  const [activeTab, setActiveTab] = useState<AppTab>('upload');
  const [documents, setDocuments] = useState<UploadedDocument[]>([]);
  const [extractedData, setExtractedData] = useState<ExtractedData | null>(null);
  const [slides, setSlides] = useState<Slide[]>([]);
  const [isExtracting, setIsExtracting] = useState(false);
  const [isGeneratingSlides, setIsGeneratingSlides] = useState(false);
  const [isExporting, setIsExporting] = useState(false);
  const [extractionError, setExtractionError] = useState<string | null>(null);
  const [projectName, setProjectName] = useState('Projekt Alpha');

  const handleDocumentsAdded = useCallback((newDocs: (UploadedDocument & { _replace?: string })[]) => {
    setDocuments(prev => {
      const updated = [...prev];
      for (const doc of newDocs) {
        if (doc._replace) {
          const idx = updated.findIndex(d => d.id === doc._replace);
          if (idx !== -1) {
            const { _replace: _r, ...cleanDoc } = doc;
            updated[idx] = cleanDoc as UploadedDocument;
          } else {
            const { _replace: _r, ...cleanDoc } = doc;
            updated.push(cleanDoc as UploadedDocument);
          }
        } else {
          const exists = updated.find(d => d.id === doc.id);
          if (!exists) updated.push(doc);
        }
      }
      return updated;
    });
  }, []);

  const handleCategoryChange = useCallback((id: string, category: DocumentCategory) => {
    setDocuments(prev => prev.map(d => d.id === id ? { ...d, category } : d));
    const stored = sessionStorage.getItem(`doc_${id}`);
    if (stored) {
      const parsed = JSON.parse(stored) as StoredDocMeta;
      sessionStorage.setItem(`doc_${id}`, JSON.stringify({ ...parsed, category }));
    }
  }, []);

  const handleDocumentRemove = useCallback((id: string) => {
    setDocuments(prev => prev.filter(d => d.id !== id));
    sessionStorage.removeItem(`doc_${id}`);
  }, []);

  const handleExtract = async () => {
    const readyDocs = documents.filter(d => d.status === 'done');
    if (readyDocs.length === 0) return;

    setIsExtracting(true);
    setExtractionError(null);

    try {
      const docsWithData = readyDocs.map(doc => {
        const stored = sessionStorage.getItem(`doc_${doc.id}`);
        const meta = stored ? JSON.parse(stored) as StoredDocMeta : null;
        return {
          id: doc.id,
          name: doc.name,
          category: meta?.category ?? doc.category,
          base64Data: meta?.base64Data,
          content: doc.content,
          mimeType: meta?.mimeType ?? doc.type,
        };
      });

      const response = await fetch('/api/extract', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ documents: docsWithData }),
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.error || 'Extraction failed');

      setExtractedData(data.extracted);
      setActiveTab('extraction');
    } catch (error) {
      setExtractionError(error instanceof Error ? error.message : 'Unbekannter Fehler');
    } finally {
      setIsExtracting(false);
    }
  };

  const handleGenerateSlides = async () => {
    if (!extractedData) return;
    setIsGeneratingSlides(true);

    try {
      const response = await fetch('/api/generate-slides', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ extracted: extractedData }),
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.error || 'Slide generation failed');

      setSlides(data.slides);
      setActiveTab('presentation');
    } catch {
      const emptySlides: Slide[] = SLIDE_DEFINITIONS.map(def => ({
        id: generateId(),
        type: def.type,
        title: def.title,
        content: '',
        bulletPoints: [],
        status: 'empty' as const,
        lastEdited: new Date().toISOString(),
      }));
      setSlides(emptySlides);
      setActiveTab('presentation');
    } finally {
      setIsGeneratingSlides(false);
    }
  };

  const handleSlideUpdate = useCallback((id: string, updates: Partial<Slide>) => {
    setSlides(prev => prev.map(s => s.id === id ? { ...s, ...updates } : s));
  }, []);

  const handleExport = async (format: 'pptx' | 'pdf') => {
    if (isExporting) return;
    setIsExporting(true);
    try {
      if (format === 'pdf') {
        window.print();
      } else {
        const { exportToPptx } = await import('./lib/exportPptx');
        await exportToPptx(slides, extractedData, projectName);
      }
    } catch (error) {
      console.error('Export error:', error);
    } finally {
      setIsExporting(false);
    }
  };

  const readyDocCount = documents.filter(d => d.status === 'done').length;

  const TABS: { id: AppTab; label: string; icon: React.ComponentType<{ className?: string }>; disabled?: boolean }[] = [
    { id: 'upload', label: 'Dokumente', icon: Upload },
    { id: 'extraction', label: 'Datenextraktion', icon: BarChart3, disabled: !extractedData },
    { id: 'presentation', label: 'Präsentation', icon: Presentation, disabled: slides.length === 0 },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Top Navigation */}
      <header className="bg-[#1a2744] shadow-lg sticky top-0 z-50">
        <div className="max-w-screen-xl mx-auto px-4 sm:px-6">
          <div className="flex items-center justify-between h-16 gap-4">
            {/* Logo */}
            <div className="flex items-center gap-3 flex-shrink-0">
              <div className="w-9 h-9 bg-[#c9a84c] rounded-lg flex items-center justify-center">
                <span className="text-white font-black text-lg">D</span>
              </div>
              <div className="hidden sm:block">
                <span className="text-white font-bold text-lg tracking-tight">DealRoom</span>
                <span className="text-[#c9a84c] text-xs ml-2 font-medium">M&A Intelligence</span>
              </div>
            </div>

            {/* Project name */}
            <div className="flex-1 max-w-xs">
              <input
                type="text"
                value={projectName}
                onChange={(e) => setProjectName(e.target.value)}
                className="w-full bg-white/10 border border-white/20 text-white placeholder-white/40 text-sm px-3 py-1.5 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#c9a84c]/50"
                placeholder="Projektname..."
              />
            </div>

            {/* Tab Navigation */}
            <nav className="flex items-center gap-1">
              {TABS.map((tab) => {
                const Icon = tab.icon;
                const isActive = activeTab === tab.id;
                return (
                  <button
                    key={tab.id}
                    onClick={() => !tab.disabled && setActiveTab(tab.id)}
                    disabled={tab.disabled}
                    className={`flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                      isActive
                        ? 'bg-white/20 text-white'
                        : tab.disabled
                          ? 'text-white/30 cursor-not-allowed'
                          : 'text-white/70 hover:text-white hover:bg-white/10'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span className="hidden md:block">{tab.label}</span>
                  </button>
                );
              })}
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-screen-xl mx-auto px-4 sm:px-6 py-6">

        {/* UPLOAD TAB */}
        {activeTab === 'upload' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 space-y-4">
              <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6">
                <div className="mb-5">
                  <h2 className="text-xl font-bold text-gray-900">Dokumente hochladen</h2>
                  <p className="text-sm text-gray-500 mt-1">
                    Laden Sie alle verfügbaren Unternehmensdokumente hoch. DealRoom kategorisiert und analysiert diese automatisch.
                  </p>
                </div>
                <UploadZone
                  documents={documents}
                  onDocumentsAdded={handleDocumentsAdded}
                  onDocumentCategoryChange={handleCategoryChange}
                  onDocumentRemove={handleDocumentRemove}
                />
              </div>

              {readyDocCount > 0 && (
                <div className="bg-gradient-to-r from-[#1a2744] to-[#243560] rounded-2xl p-5 text-white">
                  <div className="flex items-center justify-between gap-4">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <Sparkles className="w-5 h-5 text-[#c9a84c]" />
                        <h3 className="font-bold text-lg">KI-Analyse starten</h3>
                      </div>
                      <p className="text-sm text-white/70">
                        {readyDocCount} Dokument{readyDocCount !== 1 ? 'e' : ''} bereit zur Analyse mit Claude AI
                      </p>
                    </div>
                    <button
                      onClick={handleExtract}
                      disabled={isExtracting}
                      className="flex items-center gap-2 px-5 py-3 bg-[#c9a84c] hover:bg-[#b8973b] text-white font-bold rounded-xl transition-colors shadow-lg disabled:opacity-60 disabled:cursor-not-allowed flex-shrink-0"
                    >
                      {isExtracting ? (
                        <><div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />Analysiere...</>
                      ) : (
                        <><Sparkles className="w-4 h-4" />Jetzt analysieren</>
                      )}
                    </button>
                  </div>

                  {isExtracting && (
                    <div className="mt-4 pt-4 border-t border-white/20">
                      <div className="flex items-center gap-2 text-sm text-white/80">
                        <RefreshCw className="w-4 h-4 animate-spin" />
                        Claude AI extrahiert Finanzdaten, Unternehmensstruktur und Risiken...
                      </div>
                      <div className="mt-2 w-full bg-white/20 rounded-full h-1.5">
                        <div className="h-1.5 rounded-full bg-[#c9a84c] animate-pulse" style={{ width: '65%' }} />
                      </div>
                    </div>
                  )}

                  {extractionError && (
                    <div className="mt-4 pt-4 border-t border-white/20 flex items-start gap-2">
                      <AlertCircle className="w-4 h-4 text-red-400 flex-shrink-0 mt-0.5" />
                      <p className="text-sm text-red-300">{extractionError}</p>
                    </div>
                  )}
                </div>
              )}
            </div>

            <div className="space-y-4">
              <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-5">
                <CategoryProgress documents={documents} />
              </div>

              {documents.length === 0 && (
                <div className="bg-blue-50 border border-blue-100 rounded-2xl p-5">
                  <h3 className="font-semibold text-blue-800 text-sm mb-3">Welche Dokumente werden benötigt?</h3>
                  <div className="space-y-2.5">
                    {[
                      { cat: '📊 Finanzen', items: 'Jahresabschlüsse (3 Jahre), BWA, Planung' },
                      { cat: '📝 Verträge', items: 'Kunden- & Lieferantenverträge, Mietverträge' },
                      { cat: '👥 HR', items: 'Organigramm, Management-Profile, Mitarbeiterliste' },
                      { cat: '🎯 Strategie', items: 'Businessplan, Marktanalysen, Produktübersicht' },
                    ].map(({ cat, items }) => (
                      <div key={cat}>
                        <p className="text-xs font-semibold text-blue-700">{cat}</p>
                        <p className="text-xs text-blue-600 mt-0.5">{items}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {documents.length > 0 && (
                <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-5">
                  <h3 className="text-sm font-semibold text-gray-700 mb-3">Upload-Status</h3>
                  <div className="space-y-2">
                    <StatRow label="Hochgeladen" value={readyDocCount} color="text-green-600" />
                    <StatRow label="In Bearbeitung" value={documents.filter(d => d.status === 'uploading').length} color="text-blue-500" />
                    <StatRow label="Fehler" value={documents.filter(d => d.status === 'error').length} color="text-red-500" />
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* EXTRACTION TAB */}
        {activeTab === 'extraction' && extractedData && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6">
                <div className="flex items-center justify-between mb-5">
                  <div>
                    <h2 className="text-xl font-bold text-gray-900">Extrahierte Daten</h2>
                    <p className="text-xs text-gray-400 mt-0.5">
                      Analysiert: {new Date(extractedData.extractedAt).toLocaleString('de-DE')}
                    </p>
                  </div>
                  <button
                    onClick={handleExtract}
                    disabled={isExtracting}
                    className="flex items-center gap-1.5 px-3 py-2 text-sm text-gray-600 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50"
                  >
                    <RefreshCw className={`w-3.5 h-3.5 ${isExtracting ? 'animate-spin' : ''}`} />
                    Neu analysieren
                  </button>
                </div>
                <ExtractionDashboard data={extractedData} />
              </div>
            </div>

            <div className="space-y-4">
              <div className="bg-gradient-to-br from-[#1a2744] to-[#2d4a8a] rounded-2xl p-5 text-white">
                <div className="flex items-center gap-2 mb-2">
                  <Presentation className="w-5 h-5 text-[#c9a84c]" />
                  <h3 className="font-bold">Präsentation erstellen</h3>
                </div>
                <p className="text-sm text-white/70 mb-4">
                  Claude AI befüllt automatisch alle 9 Folien des Information Memorandums.
                </p>
                <button
                  onClick={handleGenerateSlides}
                  disabled={isGeneratingSlides}
                  className="w-full flex items-center justify-center gap-2 py-3 bg-[#c9a84c] hover:bg-[#b8973b] text-white font-bold rounded-xl transition-colors"
                >
                  {isGeneratingSlides ? (
                    <><div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />Erstelle Folien...</>
                  ) : (
                    <><Sparkles className="w-4 h-4" />Präsentation generieren</>
                  )}
                </button>
              </div>

              <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-5">
                <h3 className="text-sm font-semibold text-gray-700 mb-3 flex items-center gap-2">
                  <FileCheck className="w-4 h-4 text-green-500" />
                  Analyse-Zusammenfassung
                </h3>
                <div className="space-y-2">
                  <StatRow label="Finanzdaten" value={extractedData.financials.length} suffix="Jahre" color="text-gray-700" />
                  <StatRow label="Bereinigungen" value={extractedData.adjustments.length} color="text-gray-700" />
                  <StatRow label="Risiken" value={extractedData.risks.length} color={extractedData.risks.filter(r => r.severity === 'high').length > 0 ? 'text-red-600' : 'text-gray-700'} />
                  <StatRow label="Lücken erkannt" value={extractedData.gaps.length} color={extractedData.gaps.filter(g => g.severity === 'critical').length > 0 ? 'text-amber-600' : 'text-gray-700'} />
                  <StatRow label="Warnungen" value={extractedData.warnings.length} color={extractedData.warnings.length > 0 ? 'text-amber-600' : 'text-gray-700'} />
                </div>
              </div>

              <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-5">
                <h3 className="text-sm font-semibold text-gray-700 mb-2">Analysierte Dokumente</h3>
                <p className="text-2xl font-bold text-gray-900">{readyDocCount}</p>
                <p className="text-xs text-gray-400">Dokument{readyDocCount !== 1 ? 'e' : ''} analysiert</p>
                <button
                  onClick={() => setActiveTab('upload')}
                  className="mt-3 text-xs text-blue-600 hover:text-blue-700 font-medium"
                >
                  + Weitere hinzufügen
                </button>
              </div>
            </div>
          </div>
        )}

        {/* PRESENTATION TAB */}
        {activeTab === 'presentation' && slides.length > 0 && (
          <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6" style={{ minHeight: '80vh' }}>
            <PresentationBuilder
              slides={slides}
              onSlideUpdate={handleSlideUpdate}
              extractedData={extractedData}
              onExport={handleExport}
              isExporting={isExporting}
            />
          </div>
        )}
      </main>
    </div>
  );
}

function StatRow({ label, value, suffix, color }: { label: string; value: number; suffix?: string; color: string }) {
  return (
    <div className="flex items-center justify-between">
      <span className="text-xs text-gray-500">{label}</span>
      <span className={`text-sm font-bold ${color}`}>{value}{suffix ? ` ${suffix}` : ''}</span>
    </div>
  );
}
