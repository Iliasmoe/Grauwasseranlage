# Grauwasser-Bewertungstool

Makrofreier, wissenschaftlich dokumentierter Excel-Prototyp für eine Offene Ganztagsschule mit Sporthalle. **Auslieferung mit fiktiven Beispieldaten und vorläufigen Ampelschwellen. Keine normative oder behördliche Freigabe.**

## Benutzung unter Microsoft Excel für Windows

1. `Grauwasser_Bewertungstool.xlsx` öffnen und Berechnung auf **Automatisch** stellen.
2. Blaue Felder in `Eingaben` durch Projektwerte ersetzen; alle Kosten in konsistenter Preis-/Steuerbasis.
3. `Nutzungsprofile` und `Kalender` auf tatsächliche Nutzergruppen, Ferien und Sporthallennutzung abstimmen. Profil-Nutzungstage dürfen aktive Gruppentage bei positiver Menge nicht übersteigen.
4. Nachweise und Gebührenentlastungen nur mit Projektbelegen eintragen. Abwasser-Einsparanteil startet bei 0 %.
5. `Prüfungen` auf Pflichtfehler kontrollieren. Dashboard, Rechenblätter und Begründungen prüfen.
6. Szenarien und Schwellen transparent verändern; Ergebnisse sind Annahmen, keine Prognosen.
7. Für die Studie pro Person eine frische Kopie benutzen; anonymisierte Ergebnisse in `Nutzertest` erfassen.

Blattschutz ohne Passwort verhindert versehentliches Überschreiben von Formeln. Für eine fachliche Prüfung oder zusätzliche Eingaben kann er unter **Überprüfen → Blattschutz aufheben** entfernt werden. Rechenblätter sind sichtbar. Die XY-Zahlungsdiagramme folgen dem gewählten Betrachtungszeitraum (maximal 50 Jahre). Technisch werden nicht benötigte Datenpunkte auf denselben Endpunkt gelegt; es entstehen keine Werte nach dem Horizont.

## Dateien

- `Grauwasser_Bewertungstool.xlsx`: Hauptanwendung, 16 Blätter, Wasserbilanz, Wirtschaftlichkeit, 15 Varianten, Nutzertest und Diagramme.
- `Methodik_Dokumentation.md`: Gleichungen, KPI-Katalog, Bewertungslogik, Annahmen und wissenschaftliche Grenzen.
- `Probandentest.md`: standardisierte Aufgaben, Fragebogen und Auswertungsregeln.
- `Validierungsbericht.md` und `Validierung_Ergebnisse.json`: tatsächliche Testergebnisse und verbleibende Grenzen.
- `src/generate.py`: reproduzierbare Erzeugung; `src/model.py`: unabhängige numerische Referenzrechnung.
- `tests/`: Referenz-, Struktur- und echte Tabellenkalkulations-Mutationstests.

## Reproduzieren

Python 3.10 oder neuer, `openpyxl==3.1.5`. Für Ausführung der Excel-Formeln zusätzlich LibreOffice/`soffice`. openpyxl speichert Formeln, **berechnet sie aber nicht**.

```bash
cd /workspace/Grauwasseranlage
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python src/generate.py --output build/raw/Grauwasser_Bewertungstool.xlsx
.venv/bin/python -m unittest discover -s tests -p 'test_*.py' -v
.venv/bin/python tests/engine_check.py
.venv/bin/python tests/final_check.py
mkdir -p build/recalculated
soffice -env:UserInstallation=file:///tmp/grauwasser-rebuild --headless --convert-to xlsx --outdir build/recalculated build/raw/Grauwasser_Bewertungstool.xlsx
cp build/recalculated/Grauwasser_Bewertungstool.xlsx Grauwasser_Bewertungstool.xlsx
```

In einer vorbereiteten Cloud-Maschine genügt das vorhandene Python mit openpyxl; das Anlegen eines venv ist optional. `tests/engine_check.py` braucht die oben erzeugte Datei in `build/raw`. Engine-Tests können einige Minuten dauern und ändern die Auslieferungsdatei nicht. Das Report-JSON wird neu geschrieben. Die endgültige XLSX enthält gecachte Resultate aus der Tabellenkalkulations-Engine; Excel berechnet Eingabeänderungen automatisch erneut.

Microsoft Excel für Windows wurde in der Cloud nicht ausgeführt. Die tatsächlich geprüfte LibreOffice-Version und Testergebnisse stehen im Validierungsbericht. Normvolltexte, echte Projektdaten und wissenschaftlich belegte Ampelschwellen müssen für den Einsatz in der Bachelorarbeit ergänzt werden.

## HTML-Anwendung mit Browser-Speicherung

**[`Grauwasser_App.html`](Grauwasser_App.html) herunterladen und im Browser öffnen.** Die einzelne Datei enthält alle Berechnungen und Exporte und funktioniert ohne Backend. Aktuelle Entwürfe werden automatisch im Browser gespeichert; unter „Zwischenstände“ lassen sich die letzten 20 Zustände pro Projekt sichern und wiederherstellen. Die [`HTML-Anleitung`](HTML_Anleitung.md) erklärt Nutzung, JSON-Sicherungen und Speichergrenzen.

Die responsive Oberfläche umfasst Tageskalender, Szenarien, Probandenauswertung sowie JSON-, CSV- und Excel-Export. Die Browserberechnung ist gegen das wissenschaftliche Python-Modell geprüft. Der [`HTML-Validierungsbericht`](web/HTML_VALIDIERUNG.md) dokumentiert die ausgeführten Prüfungen.

## Entwicklung und optionale Python-API

Quellcode und Entwicklungsanleitung liegen in [`web/`](web/README.md). Für das Frontend genügt Node.js; die bestehende API bleibt als Referenz verfügbar. Die vorbereitete Cloud-Umgebung startet beides weiterhin mit:

```bash
bash web/setup.sh
bash web/start.sh
```
