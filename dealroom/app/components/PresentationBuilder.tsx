'use client';

import { useState } from 'react';
import { CheckCircle, Clock, Circle, Edit3, Download, FileText, ChevronDown, ChevronUp } from 'lucide-react';
import { Slide, SlideStatus, ExtractedData } from '@/app/lib/types';
import SlideEditor from './SlideEditor';

interface PresentationBuilderProps {
  slides: Slide[];
  onSlideUpdate: (id: string, updates: Partial<Slide>) => void;
  extractedData: ExtractedData | null;
  onExport: (format: 'pptx' | 'pdf') => void;
  isExporting: boolean;
}

const STATUS_CONFIG: Record<SlideStatus, { label: string; icon: React.ComponentType<{ className?: string }>; color: string; bg: string }> = {
  filled: {
    label: 'Befüllt',
    icon: CheckCircle,
    color: 'text-green-600',
    bg: 'bg-green-50 border-green-200',
  },
  in_progress: {
    label: 'In Bearbeitung',
    icon: Clock,
    color: 'text-amber-500',
    bg: 'bg-amber-50 border-amber-200',
  },
  empty: {
    label: 'Leer',
    icon: Circle,
    color: 'text-gray-400',
    bg: 'bg-gray-50 border-gray-200',
  },
};

export default function PresentationBuilder({
  slides,
  onSlideUpdate,
  extractedData,
  onExport,
  isExporting,
}: PresentationBuilderProps) {
  const [editingSlide, setEditingSlide] = useState<string | null>(null);
  const [showExportMenu, setShowExportMenu] = useState(false);

  const filledCount = slides.filter(s => s.status === 'filled').length;
  const inProgressCount = slides.filter(s => s.status === 'in_progress').length;
  const emptyCount = slides.filter(s => s.status === 'empty').length;
  const completionPercent = Math.round((filledCount / slides.length) * 100);

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="flex-shrink-0 pb-4 border-b border-gray-200">
        <div className="flex items-center justify-between mb-3">
          <div>
            <h2 className="text-lg font-bold text-gray-900">Präsentations-Builder</h2>
            <p className="text-xs text-gray-500 mt-0.5">
              {filledCount} befüllt · {inProgressCount} in Bearbeitung · {emptyCount} leer
            </p>
          </div>

          {/* Export Button */}
          <div className="relative">
            <button
              onClick={() => setShowExportMenu(!showExportMenu)}
              disabled={isExporting || slides.length === 0}
              className="flex items-center gap-2 px-4 py-2 bg-[#1a2744] text-white text-sm font-semibold rounded-xl hover:bg-[#243560] disabled:opacity-50 disabled:cursor-not-allowed transition-colors shadow-sm"
            >
              {isExporting ? (
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <Download className="w-4 h-4" />
              )}
              {isExporting ? 'Exportiere...' : 'Exportieren'}
              {!isExporting && (showExportMenu ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />)}
            </button>

            {showExportMenu && !isExporting && (
              <div className="absolute right-0 top-full mt-1 bg-white rounded-xl border border-gray-200 shadow-lg overflow-hidden z-10 min-w-[160px]">
                <button
                  onClick={() => { onExport('pptx'); setShowExportMenu(false); }}
                  className="w-full flex items-center gap-3 px-4 py-3 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
                >
                  <FileText className="w-4 h-4 text-orange-500" />
                  PowerPoint (.pptx)
                </button>
                <button
                  onClick={() => { onExport('pdf'); setShowExportMenu(false); }}
                  className="w-full flex items-center gap-3 px-4 py-3 text-sm text-gray-700 hover:bg-gray-50 transition-colors border-t border-gray-100"
                >
                  <FileText className="w-4 h-4 text-red-500" />
                  PDF drucken
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Progress bar */}
        <div className="w-full bg-gray-100 rounded-full h-2">
          <div
            className="h-2 rounded-full bg-gradient-to-r from-blue-500 to-emerald-500 transition-all duration-500"
            style={{ width: `${completionPercent}%` }}
          />
        </div>
        <div className="flex justify-between mt-1">
          <span className="text-xs text-gray-400">{completionPercent}% vollständig</span>
          <span className="text-xs text-gray-400">{slides.length} Folien</span>
        </div>
      </div>

      {/* Slide List */}
      <div className="flex-1 overflow-y-auto pt-4 space-y-2 pr-1">
        {slides.map((slide, index) => {
          const config = STATUS_CONFIG[slide.status];
          const StatusIcon = config.icon;
          const isEditing = editingSlide === slide.id;

          return (
            <div key={slide.id} className={`border rounded-xl overflow-hidden transition-all ${isEditing ? 'ring-2 ring-blue-400 ring-offset-1' : ''}`}>
              {/* Slide Header */}
              <div
                className={`flex items-center gap-3 p-3 cursor-pointer hover:bg-gray-50 transition-colors ${config.bg}`}
                onClick={() => setEditingSlide(isEditing ? null : slide.id)}
              >
                <div className="flex-shrink-0 w-7 h-7 rounded-lg bg-white border border-gray-200 flex items-center justify-center">
                  <span className="text-xs font-bold text-gray-500">{index + 1}</span>
                </div>

                <div className="flex-1 min-w-0">
                  <p className="text-sm font-semibold text-gray-800 truncate">{slide.title}</p>
                  {slide.content && !isEditing && (
                    <p className="text-xs text-gray-500 truncate mt-0.5">{slide.content}</p>
                  )}
                </div>

                <div className="flex items-center gap-2 flex-shrink-0">
                  <div className={`flex items-center gap-1 text-xs font-medium ${config.color}`}>
                    <StatusIcon className="w-3.5 h-3.5" />
                    <span className="hidden sm:block">{config.label}</span>
                  </div>
                  <button
                    onClick={(e) => { e.stopPropagation(); setEditingSlide(isEditing ? null : slide.id); }}
                    className="p-1 rounded-lg hover:bg-white/80 transition-colors"
                    title="Bearbeiten"
                  >
                    <Edit3 className="w-3.5 h-3.5 text-gray-400" />
                  </button>
                </div>
              </div>

              {/* Slide Editor (expanded) */}
              {isEditing && (
                <div className="border-t border-gray-200 bg-white">
                  <SlideEditor
                    slide={slide}
                    extractedData={extractedData}
                    onUpdate={(updates) => onSlideUpdate(slide.id, updates)}
                  />
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
