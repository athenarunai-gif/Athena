export function formatCurrency(value: number | undefined, decimals = 1): string {
  if (value === undefined || value === null) return '–';
  const abs = Math.abs(value);
  if (abs >= 1_000_000) {
    return `€${(value / 1_000_000).toFixed(decimals)}M`;
  }
  if (abs >= 1_000) {
    return `€${(value / 1_000).toFixed(decimals)}K`;
  }
  return `€${value.toFixed(0)}`;
}

export function formatPercent(value: number | undefined, decimals = 1): string {
  if (value === undefined || value === null) return '–';
  return `${value.toFixed(decimals)}%`;
}

export function formatNumber(value: number | undefined): string {
  if (value === undefined || value === null) return '–';
  return new Intl.NumberFormat('de-DE').format(value);
}

export function getFileExtension(filename: string): string {
  return filename.split('.').pop()?.toLowerCase() ?? '';
}

export function formatFileSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export function truncate(str: string, maxLength: number): string {
  if (str.length <= maxLength) return str;
  return str.substring(0, maxLength) + '…';
}
