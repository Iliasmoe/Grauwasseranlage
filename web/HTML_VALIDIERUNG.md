# Validierung der eigenständigen HTML-Anwendung

Prüfstand: 14.10.2026. Die Anwendung ist eine einzelne Datei mit eingebettetem JavaScript, CSS, Methodik-Dokumenten und XLSX-Vorlage. Eingaben und Zwischenstände werden ausschließlich im Browser gespeichert. Die Python-Referenz und Excel-Vorlage wurden nicht geändert.

| Prüfung | Ergebnis |
|---|---|
| TypeScript und Produktionsbuild | Bestanden |
| Vergleich Browsermodell / Python | 117 Fälle, 407.520 Einzelwerte bestanden |
| Vollständige Desktop-/Mobilabläufe mit der HTML-Datei | 16 von 16 bestanden |
| Zwischenstände und Speicherverhalten | 9 von 9 bestanden |
| Excel-Export aus der HTML-Anwendung | LibreOffice-Neuberechnung bestanden |
| Browserfehler | Keine |
| Zusätzliche Netzwerkanfragen | Keine |

## Rechenprüfung

`offline_model_check.py` verwendet die tatsächliche TypeScript-Quelle `web/frontend/src/model.ts`, keine Nachbildung für Tests. Die Prüfung vergleicht Basiswerte, Kalender einschließlich Schaltjahren, Handreferenzen, Nullmengen, Tagesübertrag, Altwasserverwerfung, Restbestand, Ersatzinvestition, volle Förderung, ungültige Eingaben, Nachweisveto, Schwellen, Studienstatistik, drei Szenarien und zwölf Sensitivitäten. Hinzu kommen 60 reproduzierbar zufällige Projekte sowie zwölf Fälle mit dezimalen Kapazitäten, Speichergrößen und Investitionsbeträgen.

Numerische Toleranz: relativ `1e-9`, absolut `1e-7`. Dezimale Werte werden direkt gegen `src/model.py` verglichen, weil die bisherige Python-API manche ursprünglich ganzzahligen Standardwerte zusätzlich auf Ganzzahligkeit prüft. Das fachliche Modell lässt bei Beträgen, Mengen und Kapazitäten Dezimalwerte zu; die Browserfassung entspricht diesen Modellgrenzen.

Belege: [`validation-results/offline-model-results.json`](validation-results/offline-model-results.json).

## Echte Browserabläufe

Die 16 allgemeinen Abläufe prüfen Dashboard, Monats- und Zahlungsdarstellungen, Eingabe- und Profiländerungen, gesperrte Bewertung bei fehlenden Werten, Schwellen, Szenarien, Einzeltage und Kalenderzeiträume, anonymisierte Studienantworten mit Auswertung, CSV-/JSON-/Excel-Export, Projektimport und -verwaltung, Persistenz, Nachweisveto und Mobilansicht mit 390 Pixeln.

Die neun zusätzlichen Abläufe prüfen automatische und benannte Zwischenstände, Wiederherstellung einschließlich Sicherung des vorherigen Stands, **Neuladen und vollständigen Browserneustart mit einem persistenten Browserprofil**, unvollständige Entwürfe, Begrenzung auf 20 Zustände, getrennte Projekthistorien, eingebettete Methodik-Dokumente, mobilen Zwischenstand-Dialog und gesperrten `localStorage` sowie Literaltexte und entfernte Ergebnis-Caches im Browser-XLSX. Bei Speicherfehlern zeigt die Anwendung „Nicht gespeichert“; Weiterarbeiten und JSON-Export funktionieren trotzdem.

Belege: [`validation-results/offline-browser-results.json`](validation-results/offline-browser-results.json), [`validation-results/offline-storage-results.json`](validation-results/offline-storage-results.json).

**Grenze der Prüfung:** Der verwaltete Cloud-Chromium blockiert `file://` durch seine administrative URL-Richtlinie. Diese Richtlinie wurde nicht geändert. Für die Tests wurde der unveränderte Inhalt von `Grauwasser_App.html` über Playwright an einer lokalen HTTP-Testadresse ausgeliefert. Es wurden keine Berechnungen oder API-Antworten simuliert. Der Browser war auf offline gesetzt; jede zusätzliche Anfrage wurde gesperrt und als Fehler erfasst. So wurden die Einzeldatei, ihre eingebetteten Berechnungen und Browser-Speicherung geprüft. Der direkte Aufruf per Doppelklick sowie das browserabhängige `localStorage`-Verhalten für `file://` wurden in dieser Cloud-Maschine nicht ausgeführt. Andere Browser und Betriebssysteme wurden nicht getestet.

## Excel-Export

Die Browserprüfung exportierte ein geändertes Projekt mit 100 Duschtagen, 4,25 €/m³ Trinkwasserpreis, konservativem Investitionsfaktor 1,50 und synthetischen Studienantworten. Der Export wurde mit openpyxl auf tatsächliche Eingaben geprüft und anschließend durch LibreOfficeDev 26.8.0.0.alpha0 neu berechnet. Die unabhängige Wasser-/Kapitalwertreferenz, alle 15 Varianten und Studienmittelwerte stimmen überein; keine Excel-Fehlerzellen.

Ergebnisse dieses Exports: 353,550380048 m³/a genutzt, Kapitalwert −14.138,112829087 €, Gesamtampel Rot. Der Export enthält Formeln; Benutzertexte werden als Literaltexte gesetzt. Vorlagen-Caches werden entfernt und vollständige Neuberechnung beim Öffnen angefordert. Microsoft Excel für Windows wurde nicht ausgeführt.

Beleg: [`validation-results/offline-export-engine-results.json`](validation-results/offline-export-engine-results.json).

## Prüfungen erneut ausführen

Im Repositoryverzeichnis, nach Installation der Entwicklungsabhängigkeiten:

```bash
npm run build --prefix web/frontend
web/.venv/bin/python web/tests/offline_model_check.py
web/.venv/bin/python web/tests/browser_check.py \
  --url http://localhost:8766/Grauwasser_App.html \
  --html Grauwasser_App.html --output web/test-results/offline
web/.venv/bin/python web/tests/offline_storage_check.py
# Optional, mit LibreOffice und laufender Referenz-API:
web/.venv/bin/python web/tests/export_engine_check.py \
  --project web/test-results/offline/Grauwasser_Projekt.json \
  --workbook web/test-results/offline/Grauwasser_Bewertungstool.xlsx
```

Die Browserabläufe verwenden System-Chromium unter `/usr/bin/chromium`. Python 3.12.14, Node.js 24.19.0, Playwright 1.62.0 und Chromium 154.0.8037.57 wurden verwendet. Die Excel-Prüfung benötigt die optionale API auf Port 8000 ausschließlich für den Vergleich; die HTML-Anwendung selbst benötigt sie nicht. Ein erneuter Build aus denselben Quellen erzeugt denselben HTML-Inhalt.

Die technischen Prüfungen belegen keine fachliche Freigabe, empirische Ampelschwellen oder reale Projektannahmen. Die Anwendung startet weiterhin mit eindeutig gekennzeichneten Beispieldaten.
