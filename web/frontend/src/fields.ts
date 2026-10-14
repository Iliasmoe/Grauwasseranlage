export type Field = { key: string; label: string; unit?: string; hint?: string; type?: 'text' | 'select' | 'percent' | 'textarea'; options?: string[]; min?: number; max?: number; step?: string };
const status = ['Ungeklärt', 'Nachgewiesen', 'Nicht erfüllt'];
export const sections: { title: string; subtitle: string; fields: Field[] }[] = [
  { title: 'Projektdaten', subtitle: 'Gebäude und gemeinsame Rahmenbedingungen.', fields: [
    { key: 'name', label: 'Projektname', type: 'text' }, { key: 'building', label: 'Gebäudetyp', type: 'text' },
    { key: 'location', label: 'Standort', type: 'text' }, { key: 'plant', label: 'Geplante Anlage', type: 'text' },
    { key: 'users', label: 'Nutzer im Referenzprojekt', unit: 'Personen', min: 0, hint: 'Informativ. Jede Nutzergruppe erhält eigene Mengenprofile.' },
    { key: 'year', label: 'Bilanzjahr', min: 2020, max: 2100, hint: 'Bei Änderung den Tageskalender für das neue Jahr erstellen.' },
    { key: 'horizon', label: 'Betrachtungszeitraum', unit: 'Jahre', min: 1, max: 50 },
    { key: 'other_water', label: 'Sonstiger Trinkwasserbedarf', unit: 'm³/a', min: 0, hint: 'Außerhalb der erfassten Betriebswassernutzungen; keine Doppelzählung.' },
    { key: 'data_status', label: 'Datenbasis', type: 'select', options: ['Beispieldaten', 'Projektdaten'] },
  ]},
  { title: 'Aufbereitung & Speicher', subtitle: 'Kapazität und zeitliche Verfügbarkeit begrenzen die tatsächlich nutzbare Menge.', fields: [
    { key: 'yield_rate', label: 'Aufbereitungsausbeute', type: 'percent', min: 0, max: 100 },
    { key: 'availability', label: 'Betriebsverfügbarkeit', type: 'percent', min: 0, max: 100 },
    { key: 'capacity', label: 'Rohwasser-Aufbereitungskapazität', unit: 'm³/d', min: 0 },
    { key: 'storage', label: 'Nutzbares Speichervolumen', unit: 'm³', min: 0 },
    { key: 'overlap', label: 'Direkt nutzbarer Tagesanteil', type: 'percent', min: 0, max: 100, hint: 'Vereinfachte Überlappung von Anfall und Bedarf innerhalb des Tages.' },
    { key: 'storage_loss', label: 'Verlust beim Tagesübertrag', type: 'percent', min: 0, max: 100, hint: 'Frischer Rest wird für genau einen Folgetag gespeichert; keine Hygieneaussage.' },
  ]},
  { title: 'Nachweise & Zulässigkeit', subtitle: 'Gute Kennzahlen können fehlende hygienische, technische oder rechtliche Nachweise nicht ausgleichen.', fields: [
    { key: 'hygiene', label: 'Hygienische Nachweise', type: 'select', options: status },
    { key: 'technical', label: 'Technische Nachweise', type: 'select', options: status },
    { key: 'legal', label: 'Rechtliche Zulässigkeit', type: 'select', options: status },
    { key: 'evidence', label: 'Belege / Aktenverweise', type: 'textarea', hint: 'Status ist eine Selbstauskunft. Belege werden außerhalb des Tools geprüft.' },
  ]},
  { title: 'Investition', subtitle: 'Einheitlicher Preisstand und Brutto-/Nettobezug für alle Beträge.', fields: [
    { key: 'planning', label: 'Planungskosten', unit: '€', min: 0 }, { key: 'equipment', label: 'Anlagenkosten', unit: '€', min: 0 },
    { key: 'installation', label: 'Montagekosten', unit: '€', min: 0 }, { key: 'extra_investment', label: 'Sonstige Investitionskosten', unit: '€', min: 0 },
    { key: 'grant', label: 'Fördermittel im Jahr 0', unit: '€', min: 0 }, { key: 'residual', label: 'Nominaler Restwert am Ende', unit: '€', min: 0 },
    { key: 'replacement_year', label: 'Jahr der Ersatzinvestition', unit: 'Jahr', min: 0, max: 50, hint: '0 nur ohne Ersatzkosten. Sonst innerhalb des Betrachtungszeitraums.' },
    { key: 'replacement_cost', label: 'Ersatzinvestition (Preisstand Jahr 1)', unit: '€', min: 0 },
  ]},
  { title: 'Betriebskosten & Tarife', subtitle: 'Nur tatsächlich vermeidbare variable Gebühren als Einsparung ansetzen.', fields: [
    { key: 'maintenance', label: 'Wartungskosten', unit: '€/a', min: 0 }, { key: 'other_cost', label: 'Sonstige Betriebskosten', unit: '€/a', min: 0 },
    { key: 'energy_intensity', label: 'Spezifische Aufbereitungsenergie', unit: 'kWh/m³', min: 0, hint: 'Bezug: verarbeitetes Rohwasser, auch bei später ungenutztem Wasser.' },
    { key: 'energy_price', label: 'Strompreis', unit: '€/kWh', min: 0 }, { key: 'water_price', label: 'Vermiedener Trinkwasserpreis', unit: '€/m³', min: 0 },
    { key: 'sewage_price', label: 'Abwassergebühr', unit: '€/m³', min: 0 },
    { key: 'sewage_credit', label: 'Anerkannter Abwasser-Einsparanteil', type: 'percent', min: 0, max: 100, hint: 'Standard 0 %. Positive Werte benötigen einen nachprüfbaren Gebührenbeleg.' },
    { key: 'billing_evidence', label: 'Beleg der Gebührenentlastung', type: 'textarea' },
  ]},
  { title: 'Zins & Preisentwicklung', subtitle: 'Nominale Preissteigerungen mit einem konsistenten nominalen Kalkulationszins kombinieren.', fields: [
    { key: 'discount', label: 'Kalkulationszins', type: 'percent', min: 0, max: 100 },
    { key: 'water_growth', label: 'Trinkwasserpreissteigerung', type: 'percent', min: -50, max: 100 },
    { key: 'cost_growth', label: 'Wartung / sonstige Preissteigerung', type: 'percent', min: -50, max: 100 },
    { key: 'energy_growth', label: 'Strompreissteigerung', type: 'percent', min: -50, max: 100 },
    { key: 'sewage_growth', label: 'Abwassergebührensteigerung', type: 'percent', min: -50, max: 100 },
  ]},
];
export const thresholds: Field[] = [
  { key: 'economic_green', label: 'Ökonomie: Grün ab', type: 'percent', unit: 'NPV / Nettoinvestition', min: -100, max: 100 },
  { key: 'economic_yellow', label: 'Ökonomie: Gelb ab', type: 'percent', unit: 'NPV / Nettoinvestition', min: -100, max: 100 },
  { key: 'resource_green', label: 'Ressourcen: Grün ab', type: 'percent', unit: 'Einsparquote', min: 0, max: 100 },
  { key: 'resource_yellow', label: 'Ressourcen: Gelb ab', type: 'percent', unit: 'Einsparquote', min: 0, max: 100 },
];
