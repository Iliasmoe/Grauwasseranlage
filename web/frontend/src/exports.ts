import { unzipSync, zipSync, strFromU8, strToU8 } from 'fflate';
import { workbookBase64, documents } from './embedded-assets';
import { inputRows, compute } from './model';
import type { ProjectData } from './types';
const NS = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main';
export function documentFile(key: string) { const doc = documents[key]; return { filename: doc.filename, blob: new Blob([doc.text], { type: 'text/markdown;charset=utf-8' }) }; }
export function excelFile(data: ProjectData): Blob {
  if (!compute(data).valid) throw new Error('Eingaben prüfen.');
  const files = unzipSync(Uint8Array.from(atob(workbookBase64), c => c.charCodeAt(0))), parser = new DOMParser(), serializer = new XMLSerializer();
  const workbook = parser.parseFromString(strFromU8(files['xl/workbook.xml']), 'application/xml'), rels = parser.parseFromString(strFromU8(files['xl/_rels/workbook.xml.rels']), 'application/xml');
  const targets = new Map([...rels.getElementsByTagName('Relationship')].map(r => [r.getAttribute('Id'), r.getAttribute('Target')!]));
  const paths = new Map([...workbook.getElementsByTagName('sheet')].map(s => { const target = targets.get(s.getAttribute('r:id'))!; return [s.getAttribute('name')!, target.startsWith('/') ? target.slice(1) : 'xl/' + target]; }));
  function sheet(name: string, changes: [string, unknown][]) {
    const path = paths.get(name)!, xml = parser.parseFromString(strFromU8(files[path]), 'application/xml');
    const cells = new Map([...xml.getElementsByTagNameNS(NS, 'c')].map(c => [c.getAttribute('r'), c]));
    for (const [address, value] of changes) {
      let cell = cells.get(address);
      if (!cell) {
        const rowNumber = address.match(/\d+$/)![0]; let row = [...xml.getElementsByTagNameNS(NS, 'row')].find(r => r.getAttribute('r') === rowNumber);
        if (!row) { row = xml.createElementNS(NS, 'row'); row.setAttribute('r', rowNumber); xml.getElementsByTagNameNS(NS, 'sheetData')[0].appendChild(row); }
        cell = xml.createElementNS(NS, 'c'); cell.setAttribute('r', address);
        const colIndex = (a: string) => [...a.replace(/\d+/g, '')].reduce((n, c) => n * 26 + c.charCodeAt(0) - 64, 0);
        row.insertBefore(cell, [...row.children].find(c => colIndex(c.getAttribute('r')!) > colIndex(address)) ?? null); cells.set(address, cell);
      }
      cell.replaceChildren(); cell.removeAttribute('t'); if (value == null) continue;
      if (typeof value === 'string') { cell.setAttribute('t', 'inlineStr'); const inline = xml.createElementNS(NS, 'is'), t = xml.createElementNS(NS, 't'); t.setAttribute('xml:space', 'preserve'); t.textContent = value; inline.appendChild(t); cell.appendChild(inline); }
      else { const v = xml.createElementNS(NS, 'v'); v.textContent = String(value); cell.appendChild(v); }
    }
    files[path] = strToU8(serializer.serializeToString(xml));
  }
  sheet('Eingaben', Object.entries(inputRows).map(([k, r]) => ['B' + r, data.project[k]]));
  const profiles: [string, unknown][] = [];
  for (const [key, start] of [['sources', 6], ['demands', 17]] as const) for (let i = 0; i < 6; i++) { const p = data.project[key][i] ?? { name: 'Unbenutzt ' + (i + 1), group: 'Individuell', users: 0, frequency: 0, liters: 0, days: 0 }; [p.name, p.group, p.users, p.frequency, p.liters, p.days].forEach((v, j) => profiles.push([String.fromCharCode(65 + j) + (start + i), v])); }
  sheet('Nutzungsprofile', profiles);
  sheet('Kalender', Array.from({ length: 366 }, (_, i) => (data.calendar[i] ?? [0, 0, 0]).map((v, j) => [String.fromCharCode(67 + j) + (i + 5), v] as [string, unknown])).flat());
  sheet('Schwellenwerte', ([['economic_green', 5], ['economic_yellow', 6], ['resource_green', 9], ['resource_yellow', 10]] as const).map(([k, r]) => ['B' + r, data.project[k]]));
  sheet('Szenarien', data.scenarios.flatMap((s, i) => [s.name, ...s.factors].map((v, j) => [String.fromCharCode(65 + j) + (8 + i), v] as [string, unknown])));
  sheet('Nutzertest', Array.from({ length: 50 }, (_, i) => { const s = data.studies[i], values = s ? [s.id, s.role, s.experience, s.minutes, s.mistakes, ...Array.from({ length: 7 }, (_, j) => s.ratings[j] ?? null), ...Array.from({ length: 4 }, (_, j) => s.tasks[j] ?? null), s.errors, s.comment] : Array(18).fill(null); return values.map((v, j) => [String.fromCharCode(65 + j) + (i + 6), v] as [string, unknown]); }).flat());
  const calculation = workbook.getElementsByTagName('calcPr')[0]; calculation?.setAttribute('fullCalcOnLoad', '1'); calculation?.setAttribute('forceFullCalc', '1'); calculation?.setAttribute('calcMode', 'auto'); files['xl/workbook.xml'] = strToU8(serializer.serializeToString(workbook));
  // Keine alten Ergebnis-Caches aus der Beispielvorlage ausliefern.
  for (const path of Object.keys(files)) if (/^xl\/worksheets\/sheet\d+\.xml$/.test(path)) {
    files[path] = strToU8(strFromU8(files[path]).replace(/<c\b[^>]*>[\s\S]*?<\/c>/g, cell => /<f[\s>]/.test(cell) ? cell.replace(/<v(?:\s[^>]*)?>[\s\S]*?<\/v>|<v\s*\/>/g, '') : cell));
  }
  const bytes = zipSync(files, { level: 6 }); return new Blob([new Uint8Array(bytes).buffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
}
