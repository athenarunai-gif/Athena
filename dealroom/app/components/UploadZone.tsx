'use client';

import { useCallback, useState } from 'react';
import { Upload, FileText, Sheet, File } from 'lucide-react';
import { UploadedDocument, DocumentCategory, CATEGORY_LABELS, CATEGORY_COLORS } from '@/app/lib/types';
import { formatFileSize } from '@/app/lib/utils';
import { generateId } from '@/app/lib/types';

interface UploadZoneProps {
  documents: UploadedDocument[];
  onDocumentsAdded: (docs: UploadedDocument[]) => void;
  onDocumentCategoryChange: (id: string, category: DocumentCategory) => void;
  onDocumentRemove: (id: string) => void;
}

const FILE_ICONS: Record<string, React.ComponentType<{ className?: string }>> = {
  pdf: FileText,
  xlsx: Sheet,
  xls: Sheet,
  docx: File,
  doc: File,
  csv: Sheet,
  txt: FileText,
};

const ACCEPTED_TYPES = [
  'application/pdf',
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  'application/vnd.ms-excel',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  'application/msword',
  'text/csv',
  'text/plain',
];

export default function UploadZone({
  documents,
  onDocumentsAdded,
  onDocumentCategoryChange,
  onDocumentRemove,
}: UploadZoneProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);

  const processFiles = useCallback(async (files: FileList | File[]) => {
    const fileArray = Array.from(files);
    const validFiles = fileArray.filter(f => {
      const ext = f.name.split('.').pop()?.toLowerCase();
      return ACCEPTED_TYPES.includes(f.type) || ['pdf', 'xlsx', 'xls', 'docx', 'doc', 'csv', 'txt'].includes(ext ?? '');
    });

    if (validFiles.length === 0) return;

    setIsUploading(true);

    // Add placeholder documents with uploading status
    const placeholders: UploadedDocument[] = validFiles.map(f => ({
      id: generateId(),
      name: f.name,
      type: f.type,
      size: f.size,
      category: 'unknown' as DocumentCategory,
      uploadedAt: new Date().toISOString(),
      status: 'uploading' as const,
    }));

    onDocumentsAdded(placeholders);

    try {
      const formData = new FormData();
      validFiles.forEach(f => formData.append('files', f));

      const response = await fetch('/api/upload', { method: 'POST', body: formData });
      const data = await response.json();

      if (!response.ok) throw new Error(data.error || 'Upload failed');

      // Update placeholders with real data
      const updatedDocs: UploadedDocument[] = placeholders.map((placeholder, idx) => {
        const serverFile = data.files[idx];
        return {
          ...placeholder,
          id: serverFile.id,
          category: serverFile.category,
          status: 'done' as const,
          content: serverFile.content,
          // Store base64 in sessionStorage to avoid re-upload
        };
      });

      // Store base64 data in sessionStorage
      data.files.forEach((f: { id: string; base64Data: string; mimeType: string; category: DocumentCategory }) => {
        sessionStorage.setItem(`doc_${f.id}`, JSON.stringify({
          base64Data: f.base64Data,
          mimeType: f.mimeType,
          category: f.category,
        }));
      });

      // Replace placeholders with updated docs
      onDocumentsAdded(updatedDocs.map((d, idx) => ({ ...d, _replace: placeholders[idx].id } as UploadedDocument & { _replace: string })));
    } catch (error) {
      // Mark all as error
      const errorDocs = placeholders.map(p => ({
        ...p,
        status: 'error' as const,
        errorMessage: error instanceof Error ? error.message : 'Upload fehlgeschlagen',
      }));
      onDocumentsAdded(errorDocs.map(d => ({ ...d, _replace: d.id } as UploadedDocument & { _replace: string })));
    } finally {
      setIsUploading(false);
    }
  }, [onDocumentsAdded]);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files.length > 0) {
      processFiles(e.dataTransfer.files);
    }
  }, [processFiles]);

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.length) {
      processFiles(e.target.files);
    }
    e.target.value = '';
  };

  const getFileIcon = (name: string) => {
    const ext = name.split('.').pop()?.toLowerCase() ?? '';
    const Icon = FILE_ICONS[ext] || File;
    return <Icon className="w-5 h-5" />;
  };

  const CATEGORIES: DocumentCategory[] = ['financial', 'contracts', 'hr', 'strategy', 'customer_data', 'unknown'];

  return (
    <div className="space-y-4">
      {/* Drop Zone */}
      <div
        onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        className={`
          relative border-2 border-dashed rounded-xl p-8 text-center transition-all duration-200 cursor-pointer
          ${isDragging
            ? 'border-blue-400 bg-blue-50 scale-[1.01]'
            : 'border-gray-300 bg-gray-50 hover:border-blue-300 hover:bg-blue-50/50'
          }
        `}
        onClick={() => document.getElementById('file-input')?.click()}
      >
        <input
          id="file-input"
          type="file"
          multiple
          accept=".pdf,.xlsx,.xls,.docx,.doc,.csv,.txt"
          className="hidden"
          onChange={handleFileInput}
        />
        <div className="flex flex-col items-center gap-3">
          <div className={`w-14 h-14 rounded-full flex items-center justify-center transition-colors ${isDragging ? 'bg-blue-100' : 'bg-gray-100'}`}>
            <Upload className={`w-7 h-7 ${isDragging ? 'text-blue-500' : 'text-gray-400'}`} />
          </div>
          <div>
            <p className="text-sm font-semibold text-gray-700">
              {isUploading ? 'Dokumente werden hochgeladen...' : 'Dokumente hier ablegen oder klicken'}
            </p>
            <p className="text-xs text-gray-500 mt-1">PDF, Excel (.xlsx), Word (.docx), CSV — max. 50 MB pro Datei</p>
          </div>
          {!isUploading && (
            <div className="flex gap-2 mt-1">
              {['PDF', 'Excel', 'Word', 'CSV'].map(t => (
                <span key={t} className="px-2 py-0.5 bg-white border border-gray-200 rounded text-xs text-gray-500">{t}</span>
              ))}
            </div>
          )}
        </div>
        {isUploading && (
          <div className="absolute inset-0 flex items-center justify-center bg-white/70 rounded-xl">
            <div className="flex items-center gap-2 text-blue-600">
              <div className="w-5 h-5 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
              <span className="text-sm font-medium">Wird hochgeladen...</span>
            </div>
          </div>
        )}
      </div>

      {/* Document List */}
      {documents.length > 0 && (
        <div className="space-y-2">
          <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider">{documents.length} Dokument{documents.length !== 1 ? 'e' : ''}</p>
          <div className="space-y-2">
            {documents.map(doc => (
              <div
                key={doc.id}
                className="flex items-center gap-3 p-3 bg-white border border-gray-200 rounded-lg hover:border-gray-300 transition-colors group"
              >
                {/* Icon */}
                <div className="flex-shrink-0 w-9 h-9 rounded-lg bg-gray-100 flex items-center justify-center text-gray-500">
                  {getFileIcon(doc.name)}
                </div>

                {/* File info */}
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-800 truncate">{doc.name}</p>
                  <p className="text-xs text-gray-400">{formatFileSize(doc.size)}</p>
                </div>

                {/* Status / Category */}
                {doc.status === 'uploading' && (
                  <div className="w-5 h-5 border-2 border-blue-500 border-t-transparent rounded-full animate-spin flex-shrink-0" />
                )}

                {doc.status === 'error' && (
                  <span className="text-xs text-red-500 flex-shrink-0" title={doc.errorMessage}>Fehler</span>
                )}

                {doc.status === 'done' && (
                  <select
                    value={doc.category}
                    onChange={(e) => onDocumentCategoryChange(doc.id, e.target.value as DocumentCategory)}
                    className={`text-xs px-2 py-1 rounded-full border font-medium cursor-pointer focus:outline-none focus:ring-2 focus:ring-blue-300 ${CATEGORY_COLORS[doc.category]}`}
                    onClick={e => e.stopPropagation()}
                  >
                    {CATEGORIES.map(cat => (
                      <option key={cat} value={cat} className="bg-white text-gray-700 font-normal">
                        {CATEGORY_LABELS[cat]}
                      </option>
                    ))}
                  </select>
                )}

                {/* Remove button */}
                <button
                  onClick={() => onDocumentRemove(doc.id)}
                  className="flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center text-gray-300 hover:text-red-400 hover:bg-red-50 opacity-0 group-hover:opacity-100 transition-all"
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
