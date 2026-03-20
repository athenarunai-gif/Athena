'use client';

import { useState } from 'react';
import { Plus, X, CheckCircle, Clock, Circle } from 'lucide-react';
import { Slide, SlideStatus, ExtractedData } from '@/app/lib/types';

interface SlideEditorProps {
  slide: Slide;
  extractedData: ExtractedData | null;
  onUpdate: (updates: Partial<Slide>) => void;
}

const STATUS_OPTIONS: { value: SlideStatus; label: string; icon: React.ComponentType<{ className?: string }>; color: string }[] = [
  { value: 'filled', label: 'Befüllt', icon: CheckCircle, color: 'text-green-600' },
  { value: 'in_progress', label: 'In Bearbeitung', icon: Clock, color: 'text-amber-500' },
  { value: 'empty', label: 'Leer', icon: Circle, color: 'text-gray-400' },
];

export default function SlideEditor({ slide, onUpdate }: SlideEditorProps) {
  const [newBullet, setNewBullet] = useState('');

  const updateContent = (content: string) => {
    onUpdate({
      content,
      status: content.trim() || slide.bulletPoints.length > 0 ? 'filled' : 'empty',
      lastEdited: new Date().toISOString(),
    });
  };

  const addBulletPoint = () => {
    if (!newBullet.trim()) return;
    const bulletPoints = [...slide.bulletPoints, newBullet.trim()];
    onUpdate({
      bulletPoints,
      status: 'filled',
      lastEdited: new Date().toISOString(),
    });
    setNewBullet('');
  };

  const removeBulletPoint = (index: number) => {
    const bulletPoints = slide.bulletPoints.filter((_, i) => i !== index);
    onUpdate({
      bulletPoints,
      status: bulletPoints.length > 0 || slide.content ? 'filled' : 'empty',
      lastEdited: new Date().toISOString(),
    });
  };

  const updateBulletPoint = (index: number, value: string) => {
    const bulletPoints = slide.bulletPoints.map((b, i) => i === index ? value : b);
    onUpdate({ bulletPoints, lastEdited: new Date().toISOString() });
  };

  const updateTitle = (title: string) => {
    onUpdate({ title, lastEdited: new Date().toISOString() });
  };

  return (
    <div className="p-4 space-y-4">
      {/* Title */}
      <div>
        <label className="text-xs font-semibold text-gray-500 uppercase tracking-wider block mb-1.5">Folientitel</label>
        <input
          type="text"
          value={slide.title}
          onChange={(e) => updateTitle(e.target.value)}
          className="w-full px-3 py-2 text-sm font-semibold border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-300 focus:border-transparent"
          placeholder="Folientitel..."
        />
      </div>

      {/* Main content / Narrative */}
      <div>
        <label className="text-xs font-semibold text-gray-500 uppercase tracking-wider block mb-1.5">Kernbotschaft / Einleitung</label>
        <textarea
          value={slide.content}
          onChange={(e) => updateContent(e.target.value)}
          rows={3}
          className="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-300 focus:border-transparent resize-none"
          placeholder="Kernbotschaft dieser Folie..."
        />
      </div>

      {/* Bullet Points */}
      <div>
        <label className="text-xs font-semibold text-gray-500 uppercase tracking-wider block mb-1.5">
          Bullet Points ({slide.bulletPoints.length})
        </label>

        <div className="space-y-2">
          {slide.bulletPoints.map((bullet, index) => (
            <div key={index} className="flex items-start gap-2">
              <div className="w-1.5 h-1.5 rounded-full bg-gray-400 mt-2.5 flex-shrink-0" />
              <input
                type="text"
                value={bullet}
                onChange={(e) => updateBulletPoint(index, e.target.value)}
                className="flex-1 px-2 py-1.5 text-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-300 focus:border-transparent"
              />
              <button
                onClick={() => removeBulletPoint(index)}
                className="p-1.5 text-gray-300 hover:text-red-400 transition-colors flex-shrink-0"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            </div>
          ))}

          {/* Add new bullet */}
          <div className="flex items-center gap-2">
            <div className="w-1.5 h-1.5 rounded-full bg-gray-300 flex-shrink-0" />
            <input
              type="text"
              value={newBullet}
              onChange={(e) => setNewBullet(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter') addBulletPoint(); }}
              placeholder="Neuen Punkt hinzufügen..."
              className="flex-1 px-2 py-1.5 text-sm border border-dashed border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-300 focus:border-transparent"
            />
            <button
              onClick={addBulletPoint}
              disabled={!newBullet.trim()}
              className="p-1.5 text-blue-500 hover:text-blue-600 disabled:text-gray-300 transition-colors flex-shrink-0"
            >
              <Plus className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Status selector */}
      <div>
        <label className="text-xs font-semibold text-gray-500 uppercase tracking-wider block mb-1.5">Status</label>
        <div className="flex gap-2">
          {STATUS_OPTIONS.map(opt => {
            const Icon = opt.icon;
            return (
              <button
                key={opt.value}
                onClick={() => onUpdate({ status: opt.value, lastEdited: new Date().toISOString() })}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium border transition-all ${
                  slide.status === opt.value
                    ? `${opt.color} bg-white border-current shadow-sm`
                    : 'text-gray-400 border-gray-200 hover:border-gray-300'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                {opt.label}
              </button>
            );
          })}
        </div>
      </div>

      {/* Last edited */}
      {slide.lastEdited && (
        <p className="text-xs text-gray-400">
          Zuletzt bearbeitet: {new Date(slide.lastEdited).toLocaleString('de-DE')}
        </p>
      )}
    </div>
  );
}
