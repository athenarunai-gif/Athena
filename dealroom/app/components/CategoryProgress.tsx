'use client';

import { CheckCircle, AlertCircle, Circle } from 'lucide-react';
import { UploadedDocument, DocumentCategory, CATEGORY_LABELS } from '@/app/lib/types';

interface CategoryProgressProps {
  documents: UploadedDocument[];
}

const REQUIRED_CATEGORIES: DocumentCategory[] = ['financial', 'contracts', 'hr', 'strategy'];

export default function CategoryProgress({ documents }: CategoryProgressProps) {
  const completedCategories = new Set(
    documents.filter(d => d.status === 'done').map(d => d.category)
  );

  const allRequired = REQUIRED_CATEGORIES.every(c => completedCategories.has(c));
  const completedCount = REQUIRED_CATEGORIES.filter(c => completedCategories.has(c)).length;

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <p className="text-sm font-semibold text-gray-700">Dokument-Vollständigkeit</p>
        <span className={`text-xs font-bold px-2 py-1 rounded-full ${allRequired ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'}`}>
          {completedCount}/{REQUIRED_CATEGORIES.length}
        </span>
      </div>

      <div className="w-full bg-gray-100 rounded-full h-1.5">
        <div
          className={`h-1.5 rounded-full transition-all duration-500 ${allRequired ? 'bg-green-500' : 'bg-amber-400'}`}
          style={{ width: `${(completedCount / REQUIRED_CATEGORIES.length) * 100}%` }}
        />
      </div>

      <div className="space-y-1.5">
        {REQUIRED_CATEGORIES.map(cat => {
          const has = completedCategories.has(cat);
          const count = documents.filter(d => d.category === cat && d.status === 'done').length;
          return (
            <div key={cat} className="flex items-center gap-2">
              {has
                ? <CheckCircle className="w-4 h-4 text-green-500 flex-shrink-0" />
                : <AlertCircle className="w-4 h-4 text-amber-400 flex-shrink-0" />
              }
              <span className={`text-xs flex-1 ${has ? 'text-gray-700' : 'text-amber-600 font-medium'}`}>
                {CATEGORY_LABELS[cat]}
              </span>
              {count > 0 && (
                <span className="text-xs text-gray-400">{count} Dok.</span>
              )}
              {!has && (
                <span className="text-xs text-amber-500 font-medium">Fehlt</span>
              )}
            </div>
          );
        })}

        {/* Optional categories */}
        {(['customer_data'] as DocumentCategory[]).map(cat => {
          const has = completedCategories.has(cat);
          const count = documents.filter(d => d.category === cat && d.status === 'done').length;
          return (
            <div key={cat} className="flex items-center gap-2 opacity-60">
              {has
                ? <CheckCircle className="w-4 h-4 text-green-400 flex-shrink-0" />
                : <Circle className="w-4 h-4 text-gray-300 flex-shrink-0" />
              }
              <span className="text-xs text-gray-500 flex-1">{CATEGORY_LABELS[cat]}</span>
              {count > 0 && <span className="text-xs text-gray-400">{count} Dok.</span>}
              {!has && <span className="text-xs text-gray-400">Optional</span>}
            </div>
          );
        })}
      </div>
    </div>
  );
}
