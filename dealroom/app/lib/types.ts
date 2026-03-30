export function generateId(): string {
  return Math.random().toString(36).substring(2, 11);
}

export type DocumentCategory =
  | 'financial'
  | 'contracts'
  | 'hr'
  | 'strategy'
  | 'customer_data'
  | 'unknown';

export type DocumentStatus = 'uploading' | 'processing' | 'done' | 'error';

export interface UploadedDocument {
  id: string;
  name: string;
  type: string;
  size: number;
  category: DocumentCategory;
  uploadedAt: string;
  status: DocumentStatus;
  content?: string;
  errorMessage?: string;
}

export interface FinancialYear {
  year: number;
  revenue?: number;
  ebitda?: number;
  ebitdaMargin?: number;
  ebit?: number;
  cashflow?: number;
  equity?: number;
  source: string;
}

export interface AdjustmentItem {
  description: string;
  amount: number;
  type: 'one_time_expense' | 'one_time_income' | 'normalization';
  year: number;
  source: string;
}

export interface WorkingCapitalYear {
  year: number;
  receivables?: number;
  inventories?: number;
  payables?: number;
  workingCapital?: number;
  source: string;
}

export interface Shareholder {
  name: string;
  stake: number;
}

export interface Subsidiary {
  name: string;
  location?: string;
  stake?: number;
}

export interface ManagementMember {
  name: string;
  role: string;
  yearsInRole?: number;
}

export interface CompanyStructure {
  name?: string;
  foundedYear?: number;
  legalForm?: string;
  shareholders?: Shareholder[];
  subsidiaries?: Subsidiary[];
  locations?: string[];
  headcount?: number;
  management?: ManagementMember[];
  source: string;
}

export interface ContractRisk {
  id: string;
  type: 'customer_concentration' | 'supplier_dependency' | 'change_of_control' | 'contract_expiry' | 'litigation' | 'other';
  description: string;
  severity: 'high' | 'medium' | 'low';
  details: string;
  source: string;
}

export interface Product {
  name: string;
  margin?: number;
  revenueShare?: number;
  description?: string;
}

export interface CustomerSegment {
  name: string;
  revenueShare?: number;
}

export interface MarketProduct {
  mainProducts?: Product[];
  customerSegments?: CustomerSegment[];
  marketShareDescription?: string;
  competitors?: string[];
  source: string;
}

export type GapSeverity = 'critical' | 'important' | 'nice_to_have';

export interface Gap {
  id: string;
  category: DocumentCategory | 'general';
  description: string;
  severity: GapSeverity;
  missingItem: string;
}

export interface Warning {
  id: string;
  type: 'contradiction' | 'inconsistency' | 'data_quality';
  description: string;
  sources: string[];
}

export interface ExtractedData {
  financials: FinancialYear[];
  adjustments: AdjustmentItem[];
  workingCapital: WorkingCapitalYear[];
  companyStructure?: CompanyStructure;
  risks: ContractRisk[];
  market?: MarketProduct;
  gaps: Gap[];
  warnings: Warning[];
  extractedAt: string;
}

export type SlideType =
  | 'executive_summary'
  | 'company_overview'
  | 'market_competition'
  | 'financial_overview'
  | 'ebitda_bridge'
  | 'valuation_multiples'
  | 'growth_strategy'
  | 'risks_opportunities'
  | 'appendix';

export type SlideStatus = 'filled' | 'in_progress' | 'empty';

export interface Slide {
  id: string;
  type: SlideType;
  title: string;
  content: string;
  bulletPoints: string[];
  data?: Record<string, unknown>;
  status: SlideStatus;
  lastEdited?: string;
}

export const SLIDE_DEFINITIONS: { type: SlideType; title: string; description: string }[] = [
  { type: 'executive_summary', title: 'Executive Summary', description: 'Key highlights and investment thesis' },
  { type: 'company_overview', title: 'Company Overview', description: 'Business model, history, structure' },
  { type: 'market_competition', title: 'Market & Competition', description: 'Market size, position, competitive landscape' },
  { type: 'financial_overview', title: 'Financial Overview', description: 'Revenue, EBITDA, key metrics (3 years)' },
  { type: 'ebitda_bridge', title: 'EBITDA Bridge', description: 'Reported vs. adjusted EBITDA, one-time effects' },
  { type: 'valuation_multiples', title: 'Valuation & Multiples', description: 'EV/EBITDA, peer comparison, valuation range' },
  { type: 'growth_strategy', title: 'Growth Strategy', description: 'Organic and inorganic growth levers' },
  { type: 'risks_opportunities', title: 'Risks & Opportunities', description: 'Key risks, mitigants, and upside potential' },
  { type: 'appendix', title: 'Appendix', description: 'Supporting data, working capital, contracts' },
];

export const CATEGORY_LABELS: Record<DocumentCategory, string> = {
  financial: 'Finanzen',
  contracts: 'Verträge',
  hr: 'HR / Personal',
  strategy: 'Strategie',
  customer_data: 'Kundendaten',
  unknown: 'Sonstige',
};

export const CATEGORY_COLORS: Record<DocumentCategory, string> = {
  financial: 'bg-emerald-100 text-emerald-800 border-emerald-200',
  contracts: 'bg-blue-100 text-blue-800 border-blue-200',
  hr: 'bg-purple-100 text-purple-800 border-purple-200',
  strategy: 'bg-amber-100 text-amber-800 border-amber-200',
  customer_data: 'bg-rose-100 text-rose-800 border-rose-200',
  unknown: 'bg-gray-100 text-gray-600 border-gray-200',
};
