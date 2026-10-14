# Validierungsbericht

Version 1.0, 14.10.2026. Prüfung des tatsächlich erzeugten wissenschaftlichen Excel-Prototyps, kein fachlicher Freigabenachweis.

## Ergebnis

- **31 von 31 Python-Referenz- und Strukturtests bestanden**: 26 numerische/inhaltliche Tests und fünf Arbeitsmappenprüfungen.
- **26 von 26 Excel-Mutationsfällen bestanden**, tatsächlich mit Tabellenkalkulations-Engine gerechnet.
- **Zwei zusätzliche Engine-Nachprüfungen bestanden**: 5 und 35 Jahre Horizont, alle 15 Varianten, Diagrammkoordinaten und strenge Probandenauswertung.
- Finale Auslieferungsdatei separat gegen Basisreferenz und alle 15 Varianten geprüft: **bestanden**, keine Excel-Fehlerzellen.
- 16 Blätter, sieben Diagramme, benannte Excel-Tabelle `AnonymeTests`, Datenvalidierungen und entsperrte Eingabefelder vorhanden.
- 92.207 Formeln des abschließenden Generatorstands strukturell geprüft; vollständiger Zell-Abhängigkeitsgraph ohne Zirkelbezug; keine ungültigen Blattreferenzen oder externen Arbeitsmappenverknüpfungen.

## Prüfplattform und Reproduzierbarkeit

Python 3.12.14, openpyxl 3.1.5, LibreOfficeDev 26.8.0.0.alpha0 2c87e51eeaa2b413ff4ae097b2705eea1995d8e5 unter Linux. Die verfügbare Engine ist eine LibreOffice-Entwicklungsversion, nicht Microsoft Excel. Keine Ausführung unter Microsoft Excel für Windows; ein abschließender Zielplattformtest bleibt erforderlich.

Befehle in `/workspace/Grauwasseranlage`:

```bash
python3 src/generate.py --output build/raw/Grauwasser_Bewertungstool.xlsx
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 tests/engine_check.py
python3 tests/final_check.py
soffice -env:UserInstallation=file:///tmp/grauwasser-delivery-office --headless --convert-to xlsx --outdir . build/raw/Grauwasser_Bewertungstool.xlsx
```

Die große Engine-Serie dauerte 866.2 Sekunden einschließlich Erstellung und Prüfung. Frische temporäre Verzeichnisse und kontrollierte Prozess-Exitcodes verhindern Verwendung alter Ergebnisdateien. Jede Arbeitsmappe wurde geöffnet, berechnet und als XLSX gespeichert; geprüft wurden die gecachten tatsächlichen Zellergebnisse, nicht bloß das Vorhandensein von Formeln. Originalprojektdaten bleiben unberührt; Testmutationen erfolgen in temporären Kopien.

Maschinenlesbare Ergebnisse: `Validierung_Ergebnisse.json` und `Validierung_Nachpruefung.json`. Referenztests: `tests/test_model.py`, Strukturprüfung: `tests/test_workbook.py`, Engine-Fälle: `tests/engine_check.py`, Nachprüfung: `tests/final_check.py`.

## Methoden der Prüfung

1. Unabhängige Python-Rechnung der Tageszustände und diskontierten Zahlungsreihe gegen Excel-Zellen; sie benutzt keine Excel-Formeltexte.
2. Zusätzliche hand-/analytisch gerechnete Referenzfälle, damit eine gemeinsame Modellimplementierung nicht als einzige Wahrheit dient.
3. Tagesinvarianten: Nutzung nicht negativ oder größer als Bedarf; täglich und jährlich geschlossene Wasserbilanz; korrekte Profilintegration.
4. Szenarien: jede der 15 Varianten im Basisfall sowie in den zwei finalen Nachprüfungen gegen die unabhängige Python-Rechnung verglichen.
5. Propagation: Eingabeänderungen, Nutzer-/Nutzungstage, Nachweise und Schwellen bis zu Berechnung, Dashboard-Karten und Gesamtampel geprüft.
6. Formel-/Dateistruktur: alle Formeln, vollständiger Abhängigkeitsgraph, externe Links/Makros, bearbeitbare Eingaben, Schutz, Tabellen und Diagramme.
7. Auswertung: gültige/fehlende/ungültige Likertantworten, Zeiten/Fehler, fehlende IDs und Endpunkte der Diagramme geprüft.

Numerische Vergleichstoleranz: relative Abweichung 10⁻⁹ bzw. absolute Abweichung 10⁻⁷ (für nahezu null). Diese Rechentoleranz beschreibt Gleitkommaeffekte, nicht die Unsicherheit realer Mess-/Planungswerte.

## Ausgeführte Excel-Mutationsfälle

| Nr. | Fall | Ergebnis | Erwarteter Bewertungsstatus |
|---:|---|---|---|
| 1 | Basis | Bestanden | Rot |
| 2 | Kein Grauwasser | Bestanden | Rot |
| 3 | Kein Bedarf | Bestanden | Rot |
| 4 | Anfall kleiner Bedarf | Bestanden | Grün |
| 5 | Anfall groesser Bedarf | Bestanden | Grün |
| 6 | Hohe Investition | Bestanden | Rot |
| 7 | Negativer Cashflow | Bestanden | Rot |
| 8 | Amortisation innerhalb | Bestanden | Grün |
| 9 | Amortisation ausserhalb | Bestanden | Rot |
| 10 | Fehlende Eingabe | Bestanden | Nicht bewertbar |
| 11 | Ungueltige Eingabe | Bestanden | Nicht bewertbar |
| 12 | Hygiene ungeklaert | Bestanden | Gelb |
| 13 | Geaenderte Schwellen | Bestanden | Rot |
| 14 | Geaenderte Tage | Bestanden | Rot |
| 15 | Zins Referenz | Bestanden | Grün |
| 16 | Tagesversatz Speicher | Bestanden | Rot |
| 17 | Hygiene nicht erfuellt | Bestanden | Rot |
| 18 | Ungueltige Schwellen | Bestanden | Nicht bewertbar |
| 19 | Schaltjahr | Bestanden | Rot |
| 20 | Abwasser unbelegt | Bestanden | Nicht bewertbar |
| 21 | Abwasser belegt | Bestanden | Gelb |
| 22 | Vollfoerderung | Bestanden | Grün |
| 23 | Spaetere Unterdeckung | Bestanden | Rot |
| 24 | Endbestand | Bestanden | Rot |
| 25 | Text statt Zahl | Bestanden | Nicht bewertbar |
| 26 | Nicht ganzzahlig | Bestanden | Nicht bewertbar |

Ungeklärte hygienische Zulässigkeit begrenzt einen ansonsten günstigen Fall auf Gelb; Nicht-Erfüllung ergibt Rot unabhängig vom Nutzen. Ungültige/fehlende Pflichtfelder und unbelegte positive Abwasserentlastung erzeugen Nicht bewertbar. Eine normale Nullmenge ist dagegen gültig und führt zu fehlendem Ressourcen-Nutzen.

## Unabhängige Referenzrechnungen

### A. Jahresbilanz ohne Verluste, Speicherung oder Zins

365 identische Tage, 1 m³/d Rohgrauwasser, 2 m³/d Bedarf, Ausbeute/Verfügbarkeit/Direktanteil je 100 %, keine Betriebskosten, Investition 100 €, Wasserpreis 2 €/m³, 10 Jahre, keine Steigerungen:

- Rohmenge 365 m³/a, Bedarf 730 m³/a.
- Nutzung 365 m³/a, Nachspeisung 365 m³/a.
- Netto-Cashflow 730 €/a.
- Kapitalwert −100 + 10 × 730 = **7.200 €**.
- Statische Amortisation 100 / 730 = **0,1369863 Jahre**.

Excel und Python stimmen damit überein.

### B. Anfall über Bedarf

Gleiche Annahmen, Bedarf 0,5 m³/d: Nutzung 182,5 m³/a, Überschuss 182,5 m³/a, Deckungsgrad 100 %, Kapitalwert −100 + 10 × 365 = **3.550 €**. Nutzung bleibt auf tatsächlichen Bedarf begrenzt.

### C. Analytischer Kapitalwert mit Zins

Investition 1.000 €, Jahres-Cashflow 730 €, 10 Jahre, Zins 5 %, sonst Fall A:

`NPV = −1000 + 730 × (1 − 1,05⁻¹⁰) / 0,05`.

Die analytische Rentenbarwertformel wurde unabhängig von der jährlichen Schleife geprüft; Engine und Python stimmen innerhalb der Toleranz überein.

### D. Speicher mit Tagesversatz

Nur Tag 1: 1 m³ Anfall. Nur Tag 2: 1 m³ Bedarf. 1 m³ Tank, kein direkter Tagesverbrauch, Übertragsverlust 10 %: Nutzung **0,9 m³**, Nachspeisung **0,1 m³**, Speicherverlust **0,1 m³**. Ein Bedarf erst an Tag 3 erhält aus dieser Produktion nichts, da alte Reste am Ende des Folgetags verworfen werden.

### E. Ersatzinvestition nach erster Amortisation

Investition 730 €, CF 730 €/a, diskontfreier Horizont 10 Jahre, Ersatzinvestition 10.000 € in Jahr 3: erste Rückgewinnung nach einem Jahr, danach erneute Unterdeckung und negativer Kapitalwert. Die Anwendung zeigt die fehlende Stabilität; die erste Amortisation wird nicht als hinreichender Wirtschaftlichkeitsnachweis verwendet.

### F. Endbestand

1 m³ ausschließlich am letzten Jahrestag produziert, kein Bedarf, Tank 1 m³: Jahresnutzung 0, Endbestand 1 m³. Der Bestand wird nicht als Einsparung verbucht. Die Jahresbilanz ist geschlossen.

## Ergebnis des fiktiven Auslieferungsdatensatzes

| Kennzahl | Ergebnis |
|---|---:|
| Rohgrauwasser | 742,20 m³/a |
| Verarbeitetes Rohwasser | 705,09 m³/a |
| Aufbereitetes Wasser | 634,581 m³/a |
| Betriebsbedarf | 1.018,70 m³/a |
| Tatsächliche Trinkwassereinsparung | 555,3897572 m³/a |
| Nachspeisung | 463,3102428 m³/a |
| Speicherverluste / verworfene Altmenge | 79,1912428 m³/a |
| Einsparquote der Trinkwasser-Baseline | 22,0507 % |
| Deckungsgrad | 54,5195 % |
| Investition | 25.000,00 € |
| Betriebskosten Jahr 1 | 781,527 €/a |
| Vermiedene Kosten Jahr 1 | 1.388,474393 €/a |
| Nettoeinsparung Jahr 1 | 606,947393 €/a |
| Statische Amortisation | 41,1897 Jahre, **außerhalb** des 20-Jahre-Horizonts |
| Dynamische Amortisation | Im Zeitraum nicht erreicht |
| Kapitalwert | −17.797,872821 € |
| Spezifische Lebenszykluskosten | 5,132758 €/m³ |
| Ökonomie / Ressourcen / Gesamt | Rot / Grün / Rot |
| Nachweise | Ungeklärt – Prüfbedarf |

Dies ist ein Modellbeispiel und keine Bewertung der tatsächlichen OGS.

## Nachprüfung der Studienauswertung und Diagramme

- Erster Auswertungsfall: zwei gültige Ratings 2 und 4, ein ungültiges Rating 9, eine fehlende Antwort. Ergebnis n=2, Mittelwert 3, Stichprobenstreuung √2, jeweils ein fehlender und ungültiger Wert.
- Abschließender Fall: Ratings 1, 3 und Text „3“. Numerische gültige Antworten n=2, Mittelwert 2; Text ausgeschlossen und als ungültig gezählt. Daten ohne ID separat gemeldet.
- Zeiten 10 und 20 Minuten, dritte Eingabe Text: n=2, Mittelwert 15; Fehlerzahlen 0 und 2, dritte Eingabe 1,5: n=2, Mittelwert 1; zwei ungültige Zeit-/Fehlerfelder erkannt.
- Diagrammreihen bei 5 und 35 Jahren: tatsächliche X-Koordinaten innerhalb 0 bis gewählter Horizont; letzte kumulierte Y-Koordinate gleich Kapitalwert. Auslieferung separat mit 20 Jahren geprüft.

## Erkannte und behobene Entwicklungsfehler

- Tiefe Kopie einer openpyxl-Mappe beschädigte Tabellenmetadaten im Testläufer. Für jeden Fall wird die Vorlage neu eingelesen. Die finale Engine-Serie lief danach vollständig erfolgreich.
- Diagramme mit leeren Daten hinter dem Horizont wurden von LibreOffice als Null interpretiert und erzeugten eine falsche Cashflow-Bewegung. Ersatz durch XY-Reihen mit auf den Horizont geklemmten, deckungsgleichen Endpunkten; keine künstliche Null und keine absichtlichen #N/A-Zellen.
- Dynamische benannte Diagrammbereiche wurden im verfügbaren LibreOffice-Export nicht zuverlässig erhalten. Der finale Prototyp nutzt daher Standard-XY-Reihen mit Zellformeln, keine solchen Diagramm-Namen.
- Eingabegrenzen der Anlage wurden zwischen Datenvalidierung und Prüfblatt angeglichen.
- Studienauswertung wurde gegen Textantworten, nicht ganzzahlige Fehlerzahlen und Daten ohne ID abgesichert.
- Eine Strukturprüfung wurde einmal während des Schreibens der Vorlage gestartet und scheiterte am unvollständigen ZIP. Nach abgeschlossenem Schreiben erneut ausgeführt: alle 31 Tests bestanden. Der Fehler betraf den Entwicklungsablauf, nicht die fertige Datei.

Nach Abschluss sind keine unerklärten Fehltests oder offenen Rechenfehler bekannt. Es wurden keine Assertions deaktiviert und keine fehlerhaften Fachresultate durch triviale Prüfungen ersetzt.

## Verbleibende Grenzen

- Microsoft Excel für Windows wurde nicht ausgeführt; Bedienung, Diagramme und Nachberechnung dort abschließend prüfen.
- Keine realen Projektdaten, frühere Excel-Datei, Primärmessungen, Normvolltexte oder wissenschaftlich validierten Schwellen vorhanden.
- Tagesmodell mit pauschalem Direktanteil, Verfügbarkeit und eintägiger Altwasserstrategie; keine stündliche Hydraulik/Hygienesimulation.
- Keine vollständige Energie-/Ökobilanz oder Mehrfach-Ersatzzyklen; finanzielle Zukunftsannahmen nicht empirisch validiert.
- Der Probandentest ist vorbereitet, aber **nicht mit realen Probanden durchgeführt**. Die anonymisierten Auslieferungstabellen sind leer.
- Softwarevalidierung bestätigt Implementierung und interne Konsistenz, nicht normative Zulässigkeit oder die empirische Güte des Bewertungssystems.
