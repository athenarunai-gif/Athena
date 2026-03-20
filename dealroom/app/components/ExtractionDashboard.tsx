'use client';

import { AlertTriangle, AlertCircle, TrendingUp, TrendingDown, Building2, Users, Shield, BarChart3 } from 'lucide-react';
import { ExtractedData } from '@/app/lib/types';
import { formatCurrency, formatPercent, formatNumber } from '@/app/lib/utils';

interface ExtractionDashboardProps {
  data: ExtractedData;
}

export default function ExtractionDashboard({ data }: ExtractionDashboardProps) {
  const { financials, adjustments, workingCapital, companyStructure, risks, market, gaps, warnings } = data;

  // Sort financials by year
  const sortedFinancials = [...financials].sort((a, b) => a.year - b.year);
  const latestYear = sortedFinancials[sortedFinancials.length - 1];
  const prevYear = sortedFinancials[sortedFinancials.length - 2];

  const revenueGrowth = latestYear?.revenue && prevYear?.revenue
    ? ((latestYear.revenue - prevYear.revenue) / prevYear.revenue) * 100
    : undefined;

  const criticalGaps = gaps.filter(g => g.severity === 'critical');
  const highRisks = risks.filter(r => r.severity === 'high');

  const adjustedEbitda = latestYear
    ? (latestYear.ebitda ?? 0) + adjustments
        .filter(a => a.year === latestYear.year)
        .reduce((sum, a) => sum + (a.type === 'one_time_expense' ? a.amount : -a.amount), 0)
    : undefined;

  return (
    <div className="space-y-6">
      {/* Warnings & Gaps Banner */}
      {(criticalGaps.length > 0 || warnings.length > 0) && (
        <div className="space-y-2">
          {criticalGaps.length > 0 && (
            <div className="flex items-start gap-3 p-4 bg-red-50 border border-red-200 rounded-xl">
              <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
              <div>
                <p className="text-sm font-semibold text-red-800">
                  {criticalGaps.length} kritische Lücke{criticalGaps.length !== 1 ? 'n' : ''} erkannt
                </p>
                <ul className="mt-1 space-y-0.5">
                  {criticalGaps.map(g => (
                    <li key={g.id} className="text-xs text-red-700">• {g.description}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}
          {warnings.length > 0 && (
            <div className="flex items-start gap-3 p-4 bg-amber-50 border border-amber-200 rounded-xl">
              <AlertTriangle className="w-5 h-5 text-amber-500 flex-shrink-0 mt-0.5" />
              <div>
                <p className="text-sm font-semibold text-amber-800">
                  {warnings.length} Warnung{warnings.length !== 1 ? 'en' : ''}: Widersprüche erkannt
                </p>
                <ul className="mt-1 space-y-0.5">
                  {warnings.map(w => (
                    <li key={w.id} className="text-xs text-amber-700">• {w.description}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>
      )}

      {/* KPI Cards */}
      {latestYear && (
        <div>
          <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">
            Finanzkennzahlen {latestYear.year}
          </h3>
          <div className="grid grid-cols-2 gap-3">
            <KpiCard
              label="Umsatz"
              value={formatCurrency(latestYear.revenue)}
              source={latestYear.source}
              trend={revenueGrowth}
              trendLabel={prevYear ? `vs. ${prevYear.year}` : undefined}
            />
            <KpiCard
              label="EBITDA"
              value={formatCurrency(latestYear.ebitda)}
              sub={latestYear.ebitdaMargin !== undefined ? `${formatPercent(latestYear.ebitdaMargin)} Marge` : undefined}
              source={latestYear.source}
            />
            <KpiCard
              label="Bereinigtes EBITDA"
              value={formatCurrency(adjustedEbitda)}
              sub={latestYear.revenue && adjustedEbitda ? `${formatPercent((adjustedEbitda / latestYear.revenue) * 100)} Marge` : undefined}
              source="Berechnet"
              highlight={adjustments.filter(a => a.year === latestYear.year).length > 0}
            />
            <KpiCard
              label="EBIT"
              value={formatCurrency(latestYear.ebit)}
              source={latestYear.source}
            />
            {latestYear.cashflow !== undefined && (
              <KpiCard
                label="Cashflow"
                value={formatCurrency(latestYear.cashflow)}
                source={latestYear.source}
              />
            )}
            {latestYear.equity !== undefined && (
              <KpiCard
                label="Eigenkapital"
                value={formatCurrency(latestYear.equity)}
                source={latestYear.source}
              />
            )}
          </div>
        </div>
      )}

      {/* Multi-year Financial Table */}
      {sortedFinancials.length > 1 && (
        <div>
          <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">Mehrjahresübersicht</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-2 pr-4 text-xs text-gray-500 font-semibold">Kennzahl</th>
                  {sortedFinancials.map(f => (
                    <th key={f.year} className="text-right py-2 px-3 text-xs text-gray-500 font-semibold">{f.year}</th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {[
                  { label: 'Umsatz', key: 'revenue' as const },
                  { label: 'EBITDA', key: 'ebitda' as const },
                  { label: 'EBITDA-Marge', key: 'ebitdaMargin' as const, isPercent: true },
                  { label: 'EBIT', key: 'ebit' as const },
                ].map(({ label, key, isPercent }) => (
                  <tr key={key} className="hover:bg-gray-50">
                    <td className="py-2 pr-4 text-xs text-gray-600 font-medium">{label}</td>
                    {sortedFinancials.map(f => (
                      <td key={f.year} className="py-2 px-3 text-right text-xs text-gray-800 font-mono">
                        {f[key] !== undefined
                          ? isPercent ? formatPercent(f[key] as number) : formatCurrency(f[key] as number)
                          : <span className="text-gray-300">–</span>
                        }
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* EBITDA Adjustments */}
      {adjustments.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">EBITDA-Bereinigungen</h3>
          <div className="space-y-2">
            {adjustments.map((adj, idx) => (
              <div key={idx} className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg border border-gray-100">
                <div className={`w-2 h-2 rounded-full mt-1.5 flex-shrink-0 ${adj.type === 'one_time_expense' ? 'bg-green-400' : 'bg-red-400'}`} />
                <div className="flex-1 min-w-0">
                  <p className="text-xs font-medium text-gray-700">{adj.description}</p>
                  <p className="text-xs text-gray-400">{adj.year} · {adj.source}</p>
                </div>
                <span className={`text-xs font-bold font-mono flex-shrink-0 ${adj.type === 'one_time_expense' ? 'text-green-600' : 'text-red-600'}`}>
                  {adj.type === 'one_time_expense' ? '+' : '-'}{formatCurrency(adj.amount)}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Company Structure */}
      {companyStructure && (
        <div>
          <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3 flex items-center gap-2">
            <Building2 className="w-4 h-4" /> Unternehmensstruktur
          </h3>
          <div className="grid grid-cols-2 gap-3">
            {companyStructure.name && (
              <InfoCard label="Unternehmen" value={companyStructure.name} />
            )}
            {companyStructure.legalForm && (
              <InfoCard label="Rechtsform" value={companyStructure.legalForm} />
            )}
            {companyStructure.foundedYear && (
              <InfoCard label="Gründungsjahr" value={String(companyStructure.foundedYear)} />
            )}
            {companyStructure.headcount && (
              <InfoCard label="Mitarbeiter" value={formatNumber(companyStructure.headcount)} icon={<Users className="w-3 h-3" />} />
            )}
            {companyStructure.locations && companyStructure.locations.length > 0 && (
              <InfoCard label="Standorte" value={companyStructure.locations.join(', ')} fullWidth />
            )}
          </div>

          {companyStructure.shareholders && companyStructure.shareholders.length > 0 && (
            <div className="mt-3">
              <p className="text-xs font-semibold text-gray-500 mb-2">Gesellschafter</p>
              <div className="space-y-1">
                {companyStructure.shareholders.map((s, idx) => (
                  <div key={idx} className="flex items-center justify-between py-1.5 px-3 bg-gray-50 rounded-lg">
                    <span className="text-xs text-gray-700">{s.name}</span>
                    <span className="text-xs font-bold text-gray-800">{s.stake}%</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {companyStructure.management && companyStructure.management.length > 0 && (
            <div className="mt-3">
              <p className="text-xs font-semibold text-gray-500 mb-2">Management</p>
              <div className="space-y-1">
                {companyStructure.management.map((m, idx) => (
                  <div key={idx} className="flex items-center justify-between py-1.5 px-3 bg-gray-50 rounded-lg">
                    <span className="text-xs text-gray-700">{m.name}</span>
                    <span className="text-xs text-gray-500">{m.role}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Risks */}
      {risks.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3 flex items-center gap-2">
            <Shield className="w-4 h-4" /> Risiken & Vertragsklauseln
          </h3>
          <div className="space-y-2">
            {risks.map(risk => (
              <div key={risk.id} className={`p-3 rounded-lg border ${
                risk.severity === 'high' ? 'bg-red-50 border-red-200' :
                risk.severity === 'medium' ? 'bg-amber-50 border-amber-200' :
                'bg-gray-50 border-gray-200'
              }`}>
                <div className="flex items-start justify-between gap-2">
                  <p className="text-xs font-semibold text-gray-800">{risk.description}</p>
                  <span className={`text-xs px-2 py-0.5 rounded-full font-medium flex-shrink-0 ${
                    risk.severity === 'high' ? 'bg-red-100 text-red-700' :
                    risk.severity === 'medium' ? 'bg-amber-100 text-amber-700' :
                    'bg-gray-100 text-gray-600'
                  }`}>
                    {risk.severity === 'high' ? 'Hoch' : risk.severity === 'medium' ? 'Mittel' : 'Niedrig'}
                  </span>
                </div>
                {risk.details && <p className="text-xs text-gray-500 mt-1">{risk.details}</p>}
                <p className="text-xs text-gray-400 mt-1">Quelle: {risk.source}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Market */}
      {market && (
        <div>
          <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3 flex items-center gap-2">
            <BarChart3 className="w-4 h-4" /> Markt & Produkte
          </h3>
          {market.mainProducts && market.mainProducts.length > 0 && (
            <div className="space-y-2 mb-3">
              <p className="text-xs font-semibold text-gray-500 mb-1">Hauptprodukte</p>
              {market.mainProducts.map((p, idx) => (
                <div key={idx} className="flex items-center gap-3 p-2.5 bg-gray-50 rounded-lg">
                  <span className="text-xs text-gray-700 flex-1">{p.name}</span>
                  {p.margin !== undefined && (
                    <span className="text-xs font-medium text-emerald-600">{p.margin}% Marge</span>
                  )}
                  {p.revenueShare !== undefined && (
                    <span className="text-xs text-gray-500">{p.revenueShare}% Umsatz</span>
                  )}
                </div>
              ))}
            </div>
          )}
          {market.marketShareDescription && (
            <p className="text-xs text-gray-600 p-2.5 bg-blue-50 rounded-lg border border-blue-100">
              📊 {market.marketShareDescription}
            </p>
          )}
        </div>
      )}

      {/* All Gaps */}
      {gaps.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">
            Identifizierte Lücken ({gaps.length})
          </h3>
          <div className="space-y-1.5">
            {gaps.map(gap => (
              <div key={gap.id} className="flex items-start gap-2 py-2 px-3 rounded-lg bg-gray-50 border border-gray-100">
                <span className={`text-xs px-1.5 py-0.5 rounded font-medium flex-shrink-0 ${
                  gap.severity === 'critical' ? 'bg-red-100 text-red-700' :
                  gap.severity === 'important' ? 'bg-amber-100 text-amber-700' :
                  'bg-gray-100 text-gray-500'
                }`}>
                  {gap.severity === 'critical' ? '!' : gap.severity === 'important' ? '~' : 'i'}
                </span>
                <p className="text-xs text-gray-700">{gap.description}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function KpiCard({
  label,
  value,
  sub,
  source,
  trend,
  trendLabel,
  highlight,
}: {
  label: string;
  value: string;
  sub?: string;
  source: string;
  trend?: number;
  trendLabel?: string;
  highlight?: boolean;
}) {
  return (
    <div className={`p-3 rounded-xl border ${highlight ? 'bg-blue-50 border-blue-200' : 'bg-white border-gray-200'}`}>
      <p className="text-xs text-gray-500 mb-1">{label}</p>
      <p className={`text-lg font-bold font-mono ${highlight ? 'text-blue-700' : 'text-gray-900'}`}>{value}</p>
      {sub && <p className="text-xs text-gray-500 mt-0.5">{sub}</p>}
      {trend !== undefined && (
        <div className={`flex items-center gap-1 mt-1 ${trend >= 0 ? 'text-green-600' : 'text-red-600'}`}>
          {trend >= 0 ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
          <span className="text-xs font-medium">{trend >= 0 ? '+' : ''}{trend.toFixed(1)}%</span>
          {trendLabel && <span className="text-xs text-gray-400">{trendLabel}</span>}
        </div>
      )}
      <p className="text-xs text-gray-400 mt-1 truncate" title={source}>📄 {source}</p>
    </div>
  );
}

function InfoCard({ label, value, fullWidth, icon }: { label: string; value: string; fullWidth?: boolean; icon?: React.ReactNode }) {
  return (
    <div className={`p-3 bg-gray-50 rounded-lg border border-gray-100 ${fullWidth ? 'col-span-2' : ''}`}>
      <p className="text-xs text-gray-400">{label}</p>
      <p className="text-sm font-semibold text-gray-800 flex items-center gap-1 mt-0.5">
        {icon} {value}
      </p>
    </div>
  );
}
