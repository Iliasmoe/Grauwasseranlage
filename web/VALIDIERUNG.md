# Validierung der Webanwendung

Stand: 14.10.2026. Prüfung der implementierten Anwendung, getrennt von der wissenschaftlichen Validierung der Annahmen.

## Ausgeführte Prüfungen

| Prüfung | Ergebnis |
|---|---|
| Produktionsbuild mit TypeScript-Typprüfung | Bestanden |
| Installation über `web/setup.sh`, einschließlich wiederholter Ausführung | Bestanden |
| Start und Neustart über `web/start.sh` | Bestanden |
| API- und Exporttests | 25 von 25 bestanden |
| Bestehende numerische Referenztests (`tests/test_model.py`) | 26 von 26 bestanden |
| Echte Browserabläufe | 16 von 16 bestanden |
| Im Browser exportierte Excel-Datei mit LibreOffice berechnet | Bestanden, keine Fehlerzellen |
| Funktionale Readiness: HTML, Health, Default und Berechnungsrequest | Bestanden |

Prüfplattform: Python 3.12.14, Node.js 24.19.0, npm 11.9.0, React 19.3.0, Vite 8.3.4, FastAPI 0.141.1, Playwright 1.62.0 und System-Chromium 154.0.8037.57 unter Linux. LibreOfficeDev 26.8.0.0.alpha0 wurde für den Excel-Vergleich verwendet.

## Berechnung und API

Die Webanwendung verwendet unverändert `src/model.py`. Der Basisfall stimmt mit der vorhandenen, tatsächlichen Excel-Enginevalidierung überein:

- Grauwasseranfall: 742,20 m³/a.
- Betriebswasserbedarf: 1.018,70 m³/a.
- Trinkwassereinsparung: 555,3897572 m³/a.
- Kapitalwert: −17.797,8728210468 € bei 20 Jahren.
- Ökonomie Rot, Ressourcen Grün, Gesamt Rot; Nachweise ungeklärt.

API-Tests prüfen darüber hinaus: Mengen- und Monatsbilanz, alle drei Szenarien und zwölf Sensitivitäten, kein Grauwasser, kein Bedarf, fehlende/ungültige Angaben, unbekannte Felder, Nachweise, Schwellen, Nutzungstage, Kalenderwechsel und Schaltjahr, ungültige Kalenderflaggen, negative Nettoeinsparung, hohe Investition, lokal ungültige Szenarien, Studienstatistik, doppelte IDs, leere Studienzeilen, Exportwerte und erlaubte Dokumentpfade.

Streng typisierte Studienangaben verhindern unkontrollierte Strukturen. Für die Auswertung gelten nur numerische ganzzahlige Ratings 1–5. Text „3“ ist keine numerische Antwort. Fehlende Antworten werden nicht imputiert. Leere Platzhalterzeilen ohne ID werden nicht als verwaiste Daten gemeldet; tatsächlich vorhandene Daten ohne ID schon.

## Browserprüfung

`web/tests/browser_check.py` startet einen realen Chromium-Browser und bedient den Produktionsbuild. Es werden keine API-Ergebnisse für die Oberfläche gemockt.

1. Dashboard stimmt mit den Referenzwerten überein.
2. Monatsbilanz und jährliche Zahlungsreihe sind umschaltbar.
3. Nutzungstage verändern Mengen und Dashboard.
4. Wasserpreis verändert den Kapitalwert.
5. Fehlende Eingaben sperren Bewertung und Excel-Export; alte KPI-Werte werden entfernt.
6. Schwellenänderungen verändern die Ressourcenampel.
7. Szenarien werden eigenständig gerechnet; ungültige Varianten sperren nur ihre Zeile.
8. Einzeltage, Kalenderzeiträume und Wiederherstellung des Beispielkalenders funktionieren.
9. Testpersonen werden erfasst, bearbeitet und ausgewertet; CSV-Export funktioniert.
10. JSON- und Excel-Export enthalten die tatsächlichen Eingaben, Szenarien und Antworten.
11. Projekte überleben Neuladen und werden aus JSON importiert.
12. Anlegen, Wechseln und Löschen von Projekten sowie Dialogsteuerung funktionieren.
13. Fehlerhafte Importdateien verändern keine bestehenden Projekte.
14. Ein Nachweisveto bei günstiger Ökonomie wird als Nachweisproblem begründet; ohne Nettoinvestition wird keine irreführende Amortisation gemeldet.
15. Bei 390 px Breite funktionieren Navigation, Eingaben und Persistenz ohne horizontalen Seitenüberlauf.
16. Es entstehen keine Browserfehler oder externen Laufzeit-Anfragen.

Die Desktopprüfung verwendet 1440 × 1080 px, die mobile Prüfung 390 × 844 px. Screenshots sind echte Renderings der Anwendung. Reale Nutzer/Probanden wurden nicht getestet.

## Dynamischer Excel-Export

Der Browserlauf exportiert ein Projekt mit geänderten Werten: Trinkwasserpreis 4,25 €/m³, 100 Duschtagen, konservativer Investitionsfaktor 1,50 und einer synthetischen Probandenantwort. `web/tests/export_engine_check.py` berechnet diesen Export mit LibreOffice und vergleicht ihn mit der Web-API und der unabhängigen Referenz:

- Trinkwassereinsparung: 353,550380048 m³/a.
- Kapitalwert: −14.138,11282908662 €.
- Alle 15 Varianten stimmen hinsichtlich Menge, Quote, Cashflow, Kapitalwert und Ampel überein.
- Studienmittelwerte stimmen ebenfalls überein.
- Keine Excel-Fehlerzellen und keine externen Arbeitsmappenlinks.

Der Serverexport selbst enthält Formeln ohne Zell-Caches. Excel berechnet sie beim Öffnen neu. Eingaben, die mit einem Formelzeichen beginnen, werden explizit als Text exportiert. Der numerische Rechenkern wird nicht dupliziert oder abgeändert.

## Behobene Entwicklungsprobleme

- Bei den Kalender-Schaltern lag die dekorative Fläche über dem eigentlichen Eingabeelement. Die Klickfläche wurde so korrigiert, dass echte Checkbox-Bedienung und Tastaturfokus funktionieren. Es wurde kein erzwungener Testklick als Ersatz verwendet.
- Leere Szenariofaktoren werden als fehlend behandelt und sperren die entsprechende Variante. Sie werden nicht automatisch zu einer gültigen Null.
- Falsche Projekt-/Studienstrukturen werden vor Verarbeitung abgewiesen; Importdateien können bestehende Projekte nicht überschreiben.
- Die Gesamtüberschrift unterscheidet ökonomische, ressourcenbezogene und Nachweisprobleme.
- Eine fehlende Nettoinvestition wird auch bei der dynamischen Amortisation ausdrücklich als eigener Fall dargestellt.
- Leere Probanden-Platzhalter und Textantworten werden konsistent zur Excel-Auswertung behandelt.

## Reproduzieren

Im Repositoryverzeichnis, nach Installation und Start:

```bash
web/.venv/bin/python -m unittest discover -s web/tests -p 'test_*.py' -v
web/.venv/bin/python -m unittest discover -s tests -p 'test_model.py' -v
web/.venv/bin/python web/tests/browser_check.py
web/.venv/bin/python web/tests/export_engine_check.py
```

Die letzte Prüfung benötigt LibreOffice und die vom Browserlauf erzeugten Dateien. Die Prüfskripte behalten die tatsächlichen Prozess-Exitcodes bei. Tabellenkalkulationsprüfungen verwenden neue temporäre Verzeichnisse, keine alten Ergebnisdateien.

Maschinenlesbare Protokolle werden in `web/test-results/` erzeugt. Das Auslieferungspaket enthält die abschließenden Browser- und Excel-Engineberichte sowie API-/Referenztestprotokolle; synthetische Projekt-/Studienexporte aus den Browserprüfungen werden nicht als echte Projektdaten ausgeliefert.

## Grenzen

Die Ampelschwellen und Beispieldaten sind unverändert vorläufig. Stündliche Hydraulik, Wasserqualität, tatsächliche Nachweise, kommunale Gebührenregeln und empirische Schwellenvalidierung wurden nicht neu untersucht. Die Weboberfläche erweitert die Bedienung, nicht die fachliche Reichweite des Modells.

Geprüft wurde Chromium unter Linux. Ein vollständiger browserübergreifender oder Barrierefreiheits-Audit sowie eine Zielplattformprüfung unter Microsoft Excel für Windows stehen aus. Projekte sind browserlokal, ohne zentrale Datenbank oder Anmeldung. Eine öffentliche Bereitstellung wurde nicht durchgeführt.
