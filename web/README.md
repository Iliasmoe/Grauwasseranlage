# Grauwasser-Webanwendung

Responsive Webanwendung zum vorhandenen wissenschaftlichen Excel-Prototyp. **Die Oberfläche arbeitet vollständig im Browser und wird zusätzlich als einzelne `Grauwasser_App.html` ausgeliefert.** React und TypeScript übernehmen Berechnung und Speicherung; die Python-API bleibt als Referenz und optionaler Dienst verfügbar. Das Browsermodell ist gegen `src/model.py` geprüft. Nutzung ohne Installation: [`HTML-Anleitung`](../HTML_Anleitung.md).

## Funktionen

- Dashboard mit Wasserbilanz, Monatsverlauf, Zahlungsreihe, Kapitalwert und transparenten Ampeln.
- Vollständige Projekt-, Anlagen- und Wirtschaftseingaben, jeweils mit Einheiten und Plausibilitätsprüfung.
- Sechs Grauwasserquellen und sechs Betriebswassernutzungen mit eigenen Nutzern und Nutzungstagen.
- Bearbeitbarer Tageskalender mit getrenntem Schulbetrieb, Hallennutzung und individueller Gruppe; Zeiträume gesammelt setzen.
- Drei frei konfigurierbare Szenarien und zwölf Einzelfaktor-Sensitivitäten.
- Veränderbare Ampelschwellen, KPI-Katalog und Methodik-Dokumente.
- Standardisierter Probandentest mit 50 anonymisierten Ergebnissen, Mittelwerten, Verteilungen, Zeiten, Fehlern und CSV-Export.
- Mehrere Projekte im Browser, automatisches Speichern auch unvollständiger Entwürfe, 20 wiederherstellbare Zwischenstände je Projekt, JSON-Sicherung und Import.
- Excel-Export der tatsächlich eingegebenen Projektwerte, Kalender, Szenarien, Schwellen und Testergebnisse.

Die Auslieferung startet mit **gekennzeichneten fiktiven Beispieldaten**. Ampelschwellen bleiben vorläufige Modellannahmen. Das Ergebnis ersetzt keine projektbezogenen hygienischen, technischen oder rechtlichen Nachweise.

## Installation und Start

Voraussetzungen: Python 3.10+, Node.js 22.12+ und npm. Getestet mit Python 3.12.14 und Node.js 24.19.0. Befehle im Repositoryverzeichnis:

```bash
bash web/setup.sh
bash web/start.sh
```

`setup.sh` legt eine lokale Python-Umgebung an, installiert gepinnte Abhängigkeiten, führt `npm ci` mit Lockdatei aus und baut das Frontend. `start.sh` startet Backend und fertiges Frontend gemeinsam auf Port **8000**. Im eigenen Rechner kann die Anwendung unter `http://localhost:8000` im Browser aufgerufen werden. Es wird kein zusätzlicher Frontend-Prozess für den Produktionsbuild benötigt.

Optionale Prozessvariablen, ohne Änderung der Projektdaten:

```bash
GRAUWASSER_PORT=8080 GRAUWASSER_HOST=127.0.0.1 bash web/start.sh
```

`GRAUWASSER_PYTHON` kann einen anderen Python-Interpreter bestimmen. Standard ist `web/.venv/bin/python`. Für eine lokale Windows-Entwicklung können dieselben Befehle einzeln ausgeführt werden: `py -m venv web/.venv`, Python-Interpreter aus `web/.venv/Scripts`, `npm ci` und `npm run build` in `web/frontend`, anschließend `python -m uvicorn web.backend.app:app --port 8000` im Repositoryverzeichnis.

### Frontend-Entwicklung

Nur das Frontend starten, ohne Backend:

```bash
cd web/frontend
npm run dev
```

Vite verwendet Port 5173. Die Oberfläche benötigt keine API-Anfragen. Vor der Auslieferung `npm run build` ausführen; dabei entsteht auch `Grauwasser_App.html` im Repositoryverzeichnis. Für Cloud-Aufgaben den vorhandenen Checkout verwenden; kein zusätzlicher Git-Worktree ist erforderlich.

## Datenhaltung und Export

Projekte werden im `localStorage` des jeweiligen Browsers und Ursprungs gespeichert. Die Oberfläche berechnet selbst und übermittelt keine Projektwerte an den Server. Die weiterhin vorhandene API besitzt keine Projektdatenbank. Ein anderer Browser, ein anderes Gerät oder ein anderer Port hat deshalb nicht automatisch dieselben Projekte. Browserdaten löschen entfernt die lokalen Projekte. Regelmäßig JSON-Sicherungen exportieren; ein Import legt ein weiteres Projekt an und überschreibt bestehende Projekte nicht.

JSON-Dateien enthalten ein Versionsfeld (`format: grauwasser-web`, `version: 1`). Ungültige Strukturen werden vor Übernahme abgewiesen. Fachlich unvollständige, aber strukturell gültige Projekte können als Entwurf gespeichert werden; die Bewertung ist dann gesperrt.

Der Excel-Export ist makrofrei und enthält Formeln für alle Rechenwege. Die Formeln werden **beim Öffnen in Excel automatisch neu berechnet**; der Browser entfernt veraltete Ergebnis-Caches aus der Vorlage. Benutzereingaben werden als Text und nicht als Excel-Formeln exportiert. Der CSV-Export der Studienantworten enthält keine persönlichen Identifikatoren, sofern ausschließlich anonyme IDs eingegeben wurden.

Die Webanwendung enthält keine Benutzerverwaltung, zentrale Zusammenarbeit oder öffentliche Bereitstellung. Diese Funktionen sind eigenständige Erweiterungen. Die laufende Cloud-Instanz ist keine Veröffentlichung auf einer öffentlichen Domain.

## Validierung

```bash
web/.venv/bin/python -m unittest discover -s web/tests -p 'test_*.py' -v
web/.venv/bin/python -m unittest discover -s tests -p 'test_model.py' -v
web/.venv/bin/python web/tests/browser_check.py
# Optionaler Excel-Engine-Vergleich nach dem Browserlauf (benötigt LibreOffice):
web/.venv/bin/python web/tests/export_engine_check.py
```

Browserprüfung setzt einen laufenden Server auf Port 8000 sowie Chromium voraus. In der vorbereiteten Cloud-Maschine steht `/usr/bin/chromium` bereit. Für andere Installationen `--browser /pfad/zum/browser` und gegebenenfalls `--url` angeben. Das Playwright-Paket allein installiert keine Browserbinärdatei.

API-Tests prüfen Referenzwerte, Nullmengen, ungültige Daten, Kalender, Szenarien, Nachweise und Excel-Export. Browsertests bedienen die tatsächliche Anwendung auf Desktop und Mobilgeräten, einschließlich Persistenz und Import/Export. Ergebnisse, Grenzen und ausgeführte Prüfungen werden in `web/VALIDIERUNG.md` dokumentiert.

## Rechenmodell

Die wissenschaftliche Basis bleibt in `Methodik_Dokumentation.md`, `Probandentest.md` und `Validierungsbericht.md` dokumentiert. Wasserbilanz, Speicherstrategie, nominale Kapitalwertrechnung, konservative Aggregation und Nachweisveto entsprechen dem Excel-Modell. Die API ergänzt Strukturprüfung, Tages-/Monats-/Zahlungsdarstellung und eine strikt typisierte Studienerfassung. Das TypeScript-Modell in `web/frontend/src/model.ts` überträgt diese Rechenwege in den Browser; dokumentierte Differentialtests vergleichen beide Implementierungen. Es macht aus vorläufigen Annahmen keine empirisch validierten Grenzen.

## Architektur

- `web/backend/app.py`: API, Eingabeprüfung, Ergebnisaufbereitung, Studienstatistik und Excel-Export.
- `web/frontend/src/`: Oberfläche, Formulare, SVG-Diagramme, Browser-Rechnung, XLSX-Export und Projektverwaltung.
- `web/frontend/scripts/`: Dokumente und Excel-Vorlage einbetten und fertigen Build in eine HTML-Datei zusammenführen.
- `Grauwasser_App.html`: vollständige Anwendung ohne Laufzeitabhängigkeiten.
- `web/frontend/package-lock.json`: reproduzierbare JavaScript-Abhängigkeiten.
- `web/requirements*.txt`: gepinnte Python-Abhängigkeiten für Anwendung und Entwicklung.
- `web/setup.sh`, `web/start.sh`: Installation und Start.
- `web/tests/`: automatisierte API- und Browserprüfungen.

Die API ist ohne externe Dienste oder Zugangsdaten lauffähig. Während der Anwendung werden keine externen Schriften, Bilder, Analyse- oder KI-Dienste angefragt. Die OpenAPI-Spezifikation ist unter `/api/openapi.json` verfügbar.

Weitere Offline- und Speicherprüfungen sind in [`HTML_VALIDIERUNG.md`](HTML_VALIDIERUNG.md) dokumentiert.

## Cloud-Umgebung

Installationsskript (`install_script`) und Startanleitung (`start_skill`) sind als Cloud-Konfigurationsentwurf gespeichert. Für weitere Aufgaben die Änderungen in den Umgebungseinstellungen prüfen, speichern und anschließend die Umgebung veröffentlichen. Das übernimmt den vorbereiteten Dateisnapshot und die Startanweisungen. Die aktuelle Webinstanz läuft bereits auf Port 8000; eine öffentliche Webbereitstellung wird separat eingerichtet.
