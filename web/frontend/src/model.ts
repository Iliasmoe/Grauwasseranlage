/** Browserfassung des Tages- und Kapitalwertmodells, geprüft gegen src/model.py. */
import seed from './model-data.json' with { type: 'json' };
import type { ApiResponse, Profile, Project, ProjectData, Result, Scenario, Study, StudyStats } from './types';
const groups = ['Schulbetrieb', 'Halle', 'Individuell'];
const finite = (v: unknown): v is number => typeof v === 'number' && Number.isFinite(v);
const sum = (v: number[]) => v.reduce((a, b) => a + b, 0);
const range = (v: unknown, lo: number, hi: number) => finite(v) && v >= lo && v <= hi;
const labels: Record<string, string> = seed.labels;
const error = (path: string, message?: string) => ({ path, message: message ?? `${labels[path] ?? path}: Wertebereich oder Pflichtfeld prüfen.` });
export const inputRows: Record<string, number> = seed.inputRows;
export function defaultCalendar(year: number): number[][] {
  if (!Number.isInteger(year) || year < 2020 || year > 2100) throw new Error('Bilanzjahr 2020–2100 erforderlich.');
  let school = 0, hall = 0;
  return Array.from({ length: (Date.UTC(year + 1, 0, 1) - Date.UTC(year, 0, 1)) / 86400000 }, (_, i) => {
    const d = new Date(Date.UTC(year, 0, i + 1)), excluded = [6, 7].includes(d.getUTCMonth()) || (d.getUTCMonth() === 11 && d.getUTCDate() >= 21);
    return [![0, 6].includes(d.getUTCDay()) && !excluded && school < 190 ? (++school, 1) : 0, !(d.getUTCMonth() === 11 && d.getUTCDate() >= 21) && hall < 280 ? (++hall, 1) : 0, 0];
  });
}
export function defaults(): ProjectData {
  const project = structuredClone(seed.project) as Project;
  return { project, calendar: defaultCalendar(project.year!), calendar_year: project.year!, scenarios: structuredClone(seed.scenarios), studies: [] };
}
export function validate(p: Project, calendar: number[][]): ApiResponse['errors'] {
  const errors: ApiResponse['errors'] = [], integer = new Set(['users', 'year', 'horizon', 'replacement_year']);
  const bounds: Record<string, number[]> = { users: [0, 1e6], year: [2020, 2100], horizon: [1, 50], other_water: [0, 1e7], yield_rate: [0, 1], availability: [0, 1], capacity: [0, 1e5], storage: [0, 1e5], overlap: [0, 1], storage_loss: [0, 1], sewage_credit: [0, 1], discount: [0, 1], water_growth: [-.5, 1], cost_growth: [-.5, 1], energy_growth: [-.5, 1], sewage_growth: [-.5, 1], replacement_year: [0, 50] };
  for (const key of Object.keys(p)) if (!(key in seed.project)) errors.push(error(key, 'Unbekannter Projektparameter.'));
  for (const key of Object.keys(seed.project)) {
    if (!(key in p)) { errors.push(error(key, `${labels[key] ?? key} fehlt.`)); continue; }
    const v = p[key]; if (key === 'sources' || key === 'demands') continue;
    if (typeof seed.project[key as keyof typeof seed.project] === 'string') {
      if (typeof v !== 'string' || !v.trim() || v.length > 4000) errors.push(error(key));
      else if (['hygiene', 'technical', 'legal'].includes(key) && !['Ungeklärt', 'Nachgewiesen', 'Nicht erfüllt'].includes(v)) errors.push(error(key));
      else if (key === 'data_status' && !['Beispieldaten', 'Projektdaten'].includes(v)) errors.push(error(key));
    } else {
      const [lo, hi] = bounds[key] ?? (key.startsWith('resource_') ? [0, 1] : key.startsWith('economic_') ? [-1, 1] : [0, 1e9]);
      if (!range(v, lo, hi) || (integer.has(key) && !Number.isInteger(v))) errors.push(error(key, !finite(v) ? `${labels[key]}: eine Zahl ist erforderlich.` : undefined));
    }
  }
  if (errors.length) return errors;
  const n = (k: string) => p[k] as number;
  if (n('grant') > n('planning') + n('equipment') + n('installation') + n('extra_investment')) errors.push(error('grant', 'Fördermittel dürfen die Gesamtinvestition nicht übersteigen.'));
  if (n('replacement_year') > n('horizon') || (n('replacement_cost') > 0 && n('replacement_year') === 0)) errors.push(error('replacement_year', 'Ersatzjahr muss im Betrachtungszeitraum liegen; positive Ersatzkosten benötigen ein Jahr ab 1.'));
  if (n('sewage_credit') > 0 && (p.billing_evidence as string).startsWith('Keine bestätigte')) errors.push(error('billing_evidence', 'Positive Abwasserentlastung benötigt einen projektspezifischen Gebührenbeleg.'));
  if (n('resource_yellow') > n('resource_green')) errors.push(error('resource thresholds', 'Ressourcenschwellen: 0 % ≤ Gelb ≤ Grün ≤ 100 %.'));
  if (n('economic_yellow') > n('economic_green')) errors.push(error('economic thresholds', 'Ökonomieschwellen: −100 % ≤ Gelb ≤ Grün ≤ 100 %.'));
  if (!Array.isArray(calendar) || calendar.length !== defaultCalendar(n('year')).length || calendar.some(row => !Array.isArray(row) || row.length !== 3 || row.some(v => v !== 0 && v !== 1))) { errors.push(error('calendar', 'Kalender muss alle Tage des Bilanzjahrs und ausschließlich 0/1-Werte enthalten.')); return errors; }
  const counts = groups.map((_, i) => sum(calendar.map(row => row[i])));
  for (const key of ['sources', 'demands'] as const) {
    const profiles = p[key];
    if (!Array.isArray(profiles) || profiles.length > 6) { errors.push(error(key, 'Bitte höchstens sechs Nutzungsprofile angeben.')); continue; }
    for (const q of profiles) {
      if (!q || Object.keys(q).sort().join(',') !== 'days,frequency,group,liters,name,users') { errors.push(error('profile', 'Ein Profil benötigt Name, Gruppe, Nutzer, Häufigkeit, Liter und Tage.')); continue; }
      if (typeof q.name !== 'string' || !q.name.trim() || q.name.length > 200 || !groups.includes(q.group) || !range(q.users, 0, 1e6) || !range(q.frequency, 0, 100) || !range(q.liters, 0, 1000) || !range(q.days, 0, 366) || !Number.isInteger(q.days)) errors.push(error('profile', 'Profile prüfen: Nutzer ≥ 0, Häufigkeit 0–100, Liter 0–1000 und ganzzahlige Tage 0–366.'));
      else if (q.users! * q.frequency! * q.liters! * q.days! > 0 && q.days! > counts[groups.indexOf(q.group)]) errors.push(error('profile days', 'Profiltage dürfen bei positiver Menge die aktiven Kalendertage der Gruppe nicht übersteigen.'));
    }
  }
  return errors.filter((v, i) => errors.findIndex(e => e.path === v.path) === i);
}
type Calculation = Result & { valid: true; flows: number[]; discounted: number[] };
export function evaluate(p: Project, calendar: number[][], factors: (number | null)[] = [1, 1, 1, 1, 1, 0]): Calculation | { valid: false; overall: string; errors: string[] } {
  const errors = validate(p, calendar);
  if (errors.length) return { valid: false, overall: 'Nicht bewertbar', errors: errors.map(e => e.path) };
  const n = (k: string) => p[k] as number, [invest, water, demand, supply, opFactor, delta] = factors as number[], rate = n('discount') + delta;
  if (factors.length !== 6 || factors.some(v => !finite(v)) || factors.slice(0, 5).some(v => !range(v, 0, 10)) || !range(rate, 0, 1)) return { valid: false, overall: 'Nicht bewertbar', errors: ['scenario'] };
  const counts = groups.map((_, i) => sum(calendar.map(row => row[i])));
  const amount = (profiles: Profile[], flags: number[], scale: number) => sum(profiles.map(q => { const i = groups.indexOf(q.group); return counts[i] ? q.users! * q.frequency! * q.liters! * q.days! / 1000 * flags[i] / counts[i] : 0; })) * scale;
  const totals = { raw: 0, demand: 0, processed: 0, available: 0, used: 0, makeup: 0, overflow: 0, storage_losses: 0 }; let tank = 0;
  const daily = calendar.map((flags, i) => {
    const raw = amount(p.sources, flags, supply), need = amount(p.demands, flags, demand), processed = Math.min(raw, n('capacity')) * n('availability');
    const available = processed * n('yield_rate'), start = tank * (1 - n('storage_loss')), fromTank = Math.min(start, need), direct = Math.min(available * n('overlap'), Math.max(0, need - fromTank)), end = Math.min(n('storage'), Math.max(0, available - direct));
    const row = { date: new Date(Date.UTC(n('year'), 0, i + 1)).toISOString().slice(0, 10), raw, demand: need, processed, available, used: fromTank + direct, makeup: need - fromTank - direct, overflow: Math.max(0, available - direct - end), storage_losses: tank * n('storage_loss') + start - fromTank, end };
    for (const key of Object.keys(totals) as (keyof typeof totals)[]) totals[key] += row[key]; tank = end; return row;
  });
  const gross = (n('planning') + n('equipment') + n('installation') + n('extra_investment')) * invest, net = gross - Math.min(n('grant'), gross), energy = totals.processed * n('energy_intensity');
  const costs = (n('maintenance') + n('other_cost') + energy * n('energy_price')) * opFactor, avoided = totals.used * (n('water_price') * water + n('sewage_price') * n('sewage_credit')), cf = avoided - costs;
  const flows = [-net], discounted = [-net]; let pvCost = net, pvVolume = 0;
  for (let t = 1; t <= n('horizon'); t++) {
    const benefit = totals.used * (n('water_price') * water * (1 + n('water_growth')) ** (t - 1) + n('sewage_price') * n('sewage_credit') * (1 + n('sewage_growth')) ** (t - 1));
    const op = ((n('maintenance') + n('other_cost')) * (1 + n('cost_growth')) ** (t - 1) + energy * n('energy_price') * (1 + n('energy_growth')) ** (t - 1)) * opFactor;
    const replacement = t === n('replacement_year') ? n('replacement_cost') * invest * (1 + n('cost_growth')) ** (t - 1) : 0, residual = t === n('horizon') ? n('residual') * invest : 0;
    flows.push(benefit - op - replacement + residual); discounted.push(flows[t] / (1 + rate) ** t); pvCost += (op + replacement - residual) / (1 + rate) ** t; pvVolume += totals.used / (1 + rate) ** t;
  }
  const npv = sum(discounted); let dynamic: number | null = null, cumulative = -net;
  discounted.slice(1).forEach((x, i) => { if (cumulative < 0 && cumulative + x >= 0 && dynamic === null) dynamic = i - cumulative / x; cumulative += x; });
  const recovery = dynamic as number | null;
  const stable = net > 0 && recovery !== null && Math.min(...discounted.map((_, t) => sum(discounted.slice(0, t + 1))).slice(Math.floor(recovery) + 1)) >= -1e-8;
  const baseline = totals.demand + n('other_water'), quota = baseline ? totals.used / baseline : 0;
  const econ = net === 0 ? (npv >= 0 ? 1 : 3) : npv / net >= n('economic_green') ? 1 : npv / net >= n('economic_yellow') ? 2 : 3, resource = totals.used <= 0 ? 3 : quota >= n('resource_green') ? 1 : quota >= n('resource_yellow') ? 2 : 3;
  const proofs = [p.hygiene, p.technical, p.legal], gate = proofs.includes('Nicht erfüllt') ? 3 : proofs.includes('Ungeklärt') ? 2 : 1, lights = ['', 'Grün', 'Gelb', 'Rot'];
  return { valid: true, ...totals, end_storage: tank, gross, net_investment: net, costs, avoided, cashflow: cf, npv, quota, cover: totals.demand ? totals.used / totals.demand : 0, utilization: totals.raw ? totals.used / totals.raw : 0, specific_cost: pvVolume ? pvCost / pvVolume : null, static: cf > 0 && net > 0 ? net / cf : null, dynamic: recovery, stable_recovery: stable, economic: lights[econ], resource: lights[resource], overall: lights[Math.max(econ, resource, gate)], gate: lights[gate], flows, discounted, daily };
}
export function studyStatistics(records: Study[]): StudyStats {
  const identified = records.filter(r => typeof r.id === 'string' && r.id.trim()), ids = identified.map(r => r.id.trim()), mean = (v: number[]) => v.length ? sum(v) / v.length : null;
  const ratings = Array.from({ length: 7 }, (_, i) => {
    const values: number[] = []; let missing = 0, invalid = 0;
    identified.forEach(r => { const v = r.ratings?.[i]; if (v == null || (v as unknown) === '') missing++; else if (finite(v) && [1, 2, 3, 4, 5].includes(v)) values.push(v); else invalid++; });
    const avg = mean(values); return { n: values.length, mean: avg, std: values.length > 1 ? Math.sqrt(sum(values.map(v => (v - avg!) ** 2)) / (values.length - 1)) : null, distribution: [1, 2, 3, 4, 5].map(v => values.filter(x => x === v).length), missing, invalid };
  });
  const times = identified.map(r => r.minutes).filter((v): v is number => range(v, 0, 1440)), mistakes = identified.map(r => r.mistakes).filter((v): v is number => range(v, 0, 10000) && Number.isInteger(v));
  const hasData = (v: unknown): boolean => Array.isArray(v) ? v.some(hasData) : v != null && v !== '';
  return { count: identified.length, duplicates: [...new Set(ids.filter((id, i) => ids.indexOf(id) !== i))].sort(), orphaned: records.filter(r => !identified.includes(r) && Object.entries(r).some(([k, v]) => k !== 'id' && hasData(v))).length, ratings, time_n: times.length, mean_minutes: mean(times), mistakes_n: mistakes.length, mean_mistakes: mean(mistakes), tasks: Array.from({ length: 4 }, (_, i) => Object.fromEntries(['Erfüllt', 'Teilweise', 'Nicht erfüllt'].map(s => [s, identified.filter(r => r.tasks?.[i] === s).length]))) };
}
export function compute(body: ProjectData): ApiResponse {
  const study = studyStatistics(body.studies);
  if (body.calendar_year !== body.project.year) return { valid: false, errors: [error('calendar', 'Der Kalender gehört zu einem anderen Jahr. Kalender für das Bilanzjahr neu erstellen oder importieren.')], study };
  const errors = validate(body.project, body.calendar); if (errors.length) return { valid: false, errors, study };
  const r = evaluate(body.project, body.calendar); if (!r.valid) return { valid: false, errors: r.errors.map(k => error(k)), study };
  const warnings: NonNullable<ApiResponse['warnings']> = [];
  if (body.project.data_status === 'Beispieldaten') warnings.push({ kind: 'info', text: 'Beispieldaten: Mengen, Preise und Anlagenparameter durch Projektbelege ersetzen.', page: 'inputs' });
  if (r.gate !== 'Grün') warnings.push({ kind: 'warning', text: 'Hygienische, technische oder rechtliche Nachweise sind ungeklärt bzw. nicht erfüllt. Keine Freigabe.', page: 'inputs' });
  if (r.static != null && r.static > body.project.horizon!) warnings.push({ kind: 'warning', text: 'Statische Amortisation liegt außerhalb des Betrachtungszeitraums.', page: 'inputs' });
  if (r.cashflow <= 0) warnings.push({ kind: 'warning', text: 'Im ersten Jahr entsteht keine positive Nettoeinsparung.', page: 'inputs' });
  if (r.dynamic != null && !r.stable_recovery) warnings.push({ kind: 'warning', text: 'Nach erster dynamischer Amortisation tritt später erneut Unterdeckung auf.', page: 'inputs' });
  const monthly = Array.from({ length: 12 }, (_, i) => ({ month: i + 1, raw: 0, used: 0, demand: 0, makeup: 0 }));
  r.daily.forEach(row => { const m = monthly[Number(row.date.slice(5, 7)) - 1]; for (const k of ['raw', 'used', 'demand', 'makeup'] as const) m[k] += row[k]; });
  let cumulative = 0; const payments = r.discounted.map((v, i) => ({ year: i, cashflow: r.flows[i], discounted: v, cumulative: cumulative += v }));
  const sensitivity: Scenario[] = [];
  ['Investition', 'Trinkwasserpreis', 'Betriebswasserbedarf', 'Grauwasseranfall', 'Betriebskosten', 'Kalkulationszins'].forEach((label, i) => { [-1, 1].forEach(d => { const factors = [1, 1, 1, 1, 1, 0]; factors[i] = i === 5 ? d * .01 : 1 + d * .2; sensitivity.push({ name: label + ' ' + (i === 5 ? d < 0 ? '−1 %-Punkt' : '+1 %-Punkt' : d < 0 ? '−20 %' : '+20 %'), factors }); }); });
  const runCase = (s: Scenario) => { const result = evaluate(body.project, body.calendar, s.factors); if (result.valid) { const { daily: _daily, flows: _flows, discounted: _discounted, ...summary } = result; return { ...s, result: summary as Result }; } return { ...s, result: result as unknown as Result }; };
  return { valid: true, errors: [], result: r, monthly, payments, scenarios: body.scenarios.map(runCase), sensitivity: sensitivity.map(runCase), warnings, calendar_counts: groups.map((_, i) => sum(body.calendar.map(row => row[i]))), study };
}
