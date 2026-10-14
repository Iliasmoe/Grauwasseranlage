import { useId, useState } from 'react';
import { Download, Maximize2 } from 'lucide-react';
export const number = (v: number | null | undefined, digits = 1) => v == null ? '—' : new Intl.NumberFormat('de-DE', { maximumFractionDigits: digits, minimumFractionDigits: digits }).format(v);
export const money = (v: number | null | undefined, digits = 0) => v == null ? '—' : new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR', maximumFractionDigits: digits }).format(v);
export const percent = (v: number | null | undefined) => v == null ? '—' : number(v * 100) + ' %';
export const short = (v: number) => Math.abs(v) >= 1000 ? number(v / 1000, 0) + ' Tsd.' : number(v, 0);

type Point = { label: string; value: number; secondary?: number };
export function LinePlot({ points, unit = '€', secondary = false, label = 'Kapitalwert', secondLabel = 'Cashflow' }: { points: Point[]; unit?: string; secondary?: boolean; label?: string; secondLabel?: string }) {
  const [hover, setHover] = useState<number | null>(null);
  const id = useId().replaceAll(':', '');
  const width = 720, height = 250, left = 67, right = 18, top = 22, bottom = 35;
  const values = points.flatMap(p => secondary && p.secondary != null ? [p.value, p.secondary] : [p.value]);
  const min = Math.min(0, ...values), max = Math.max(0, ...values);
  const range = max - min || 1;
  const y = (v: number) => top + (max - v) / range * (height - top - bottom);
  const x = (i: number) => left + i / Math.max(1, points.length - 1) * (width - left - right);
  const path = points.map((p, i) => `${i === 0 ? 'M' : 'L'} ${x(i)} ${y(p.value)}`).join(' ');
  const active = hover == null ? null : points[hover];
  return <div className="chart-frame">
    <svg viewBox={`0 0 ${width} ${height}`} role="img" aria-label={`${label} über ${points.length} Zeitpunkte`} onMouseLeave={() => setHover(null)}>
      <defs><linearGradient id={id} x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#0e9789" stopOpacity=".18"/><stop offset="100%" stopColor="#0e9789" stopOpacity=".02"/></linearGradient></defs>
      {Array.from({ length: 5 }, (_, i) => max - range * i / 4).map((v, i) => <g key={i}><line x1={left} x2={width - right} y1={y(v)} y2={y(v)} stroke="#e9eef0"/><text x={left - 12} y={y(v) + 4} textAnchor="end" className="axis-text">{short(v)}</text></g>)}
      <path d={`${path} L ${x(points.length - 1)} ${y(0)} L ${x(0)} ${y(0)} Z`} fill={`url(#${id})`}/>
      <line x1={left} x2={width - right} y1={y(0)} y2={y(0)} stroke="#9fb4ba" strokeDasharray="4 4"/>
      <path d={path} fill="none" stroke="#078a80" strokeWidth="2.8" strokeLinejoin="round"/>
      {secondary && <path d={points.map((p, i) => `${i === 0 ? 'M' : 'L'} ${x(i)} ${y(p.secondary ?? 0)}`).join(' ')} fill="none" stroke="#aab9cc" strokeWidth="1.8" strokeDasharray="5 4"/>}
      {points.map((p, i) => <g key={i}>
        {(i === 0 || i === points.length - 1 || i % Math.max(1, Math.ceil(points.length / 7)) === 0) && <text x={x(i)} y={height - 8} textAnchor="middle" className="axis-text">{p.label}</text>}
        <rect x={x(i) - (width - left - right) / Math.max(1, points.length - 1) / 2} y={top} width={(width - left - right) / Math.max(1, points.length - 1)} height={height - bottom - top} fill="transparent" onMouseEnter={() => setHover(i)}><title>{`${p.label}: ${number(p.value, 2)} ${unit}`}</title></rect>
      </g>)}
      {active && hover != null && <g><line x1={x(hover)} x2={x(hover)} y1={top} y2={height - bottom} stroke="#6f9296" strokeDasharray="3 3"/><circle cx={x(hover)} cy={y(active.value)} r="5" fill="#078a80" stroke="white" strokeWidth="2"/></g>}
    </svg>
    <div className="chart-legend"><span><i className="legend-dot teal"/>{label}</span>{secondary && <span><i className="legend-dot gray"/>{secondLabel}</span>}<span className="chart-unit">{active ? `${active.label}: ${number(active.value, 2)} ${unit}` : `Angaben in ${unit} · Maus über die Kurve bewegen`}</span></div>
  </div>;
}

export function WaterBars({ data }: { data: { label: string; value: number; color: string }[] }) {
  const max = Math.max(1, ...data.map(d => d.value));
  return <div className="water-bars">{data.map(d => <div className="water-bar-row" key={d.label}><div className="water-bar-label">{d.label}</div><div className="water-bar-track"><div style={{ width: `${d.value / max * 100}%`, background: d.color }}/></div><strong>{number(d.value, 0)} <span>m³</span></strong></div>)}</div>;
}
export function MonthlyPlot({ points }: { points: { month: number; used: number; demand: number }[] }) {
  const months = ['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez'];
  return <LinePlot points={points.map(p => ({ label: months[p.month - 1], value: p.used, secondary: p.demand }))} unit="m³" secondary label="Trinkwassereinsparung" secondLabel="Betriebswasserbedarf"/>;
}
export function ChartActions({ title }: { title: string }) {
  const [full, setFull] = useState(false);
  return <div className="chart-actions"><button className="icon-button" title={full ? 'Normalansicht' : 'Diagramm vergrößern'} aria-label={`${title} vergrößern`} onClick={e => {
    const element = e.currentTarget.closest('.panel') as HTMLElement;
    if (!full) element?.requestFullscreen?.().then(() => setFull(true)).catch(() => {});
    else document.exitFullscreen?.().then(() => setFull(false)).catch(() => {});
  }}><Maximize2 size={16}/></button></div>;
}
export function downloadBlob(blob: Blob, filename: string) {
  const url = URL.createObjectURL(blob); const a = document.createElement('a'); a.href = url; a.download = filename; a.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
}
export function DownloadIcon() { return <Download size={16}/>; }
