import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
const root = fileURLToPath(new URL('../../../', import.meta.url));
const docs = Object.fromEntries(Object.entries({ methodik: 'Methodik_Dokumentation.md', probandentest: 'Probandentest.md', validierung: 'Validierungsbericht.md' }).map(([key, filename]) => [key, { filename, text: readFileSync(root + filename, 'utf8') }]));
writeFileSync(new URL('../src/embedded-assets.ts', import.meta.url), '/* Automatisch eingebettet; npm run build. */\nexport const workbookBase64 = ' + JSON.stringify(readFileSync(root + 'Grauwasser_Bewertungstool.xlsx').toString('base64')) + ';\nexport const documents: Record<string, {filename: string; text: string}> = ' + JSON.stringify(docs) + ';\n');
