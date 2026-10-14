# Standardisierter Probandentest

Version 1.0, 14.10.2026. Ziel: Verständlichkeit und Gebrauchstauglichkeit des Excel-Prototyps. **Kein Ersatz für die fachliche Validierung von Mengen, Formeln, Normen oder Ampelschwellen.**

## Vorbereitung und Stichprobe

Zielgerichtet Personen aus TGA-Planung, Studium und Gebäudebetrieb rekrutieren; Rollen/Excel-Erfahrung dokumentieren. Umfang und Auswahl vor Durchführung begründen. Eine kleine Gelegenheitsstichprobe erlaubt keine Verallgemeinerung auf alle Fachplaner.

Für jede Person eine frische Kopie der unveränderten Beispieldatei verwenden. Microsoft Excel für Windows, automatische Berechnung, gleiche Bildschirmgröße und gleiche Einführung. Keine persönliche Identifikation in der Arbeitsmappe. Anonyme IDs `P001` usw.; eine gegebenenfalls notwendige Zuordnung ausschließlich separat und datenschutzgerecht verwahren. Teilnahme freiwillig, Einwilligung und institutionelle Vorgaben vor Durchführung klären.

Moderator liest: „Dies ist ein Rechenprototyp mit Beispieldaten und vorläufigen Bewertungsschwellen. Bitte bearbeiten Sie die Aufgaben ohne Anleitung. Sie können laut denken. Wir testen das Werkzeug, nicht Ihre Leistung.“ Moderator gibt Hilfen erst nach dokumentierter Blockade; jede Hilfe mit Aufgabe und Zeitpunkt protokollieren. Unterbrechungen und technische Probleme separat markieren.

Zeitmessung: Beginn nach Aufgabenübergabe, Ende nach Ergebnisinterpretation. Einheit Minuten, zwei Nachkommastellen. Fehlerzahl nach folgender Regel: eine falsche Handlung zählt einmal, ihre Folgefehler nicht erneut; nach erfolgreicher Korrektur kann eine erneute falsche Handlung wieder zählen. Verständnisschwierigkeiten, Hilfen und Eingabefehler im Freitext getrennt beschreiben.

## Aufgaben mit festem Testdatensatz

Aufgaben auf einer Kopie bearbeiten. Die Person darf vorhandene Modellwerte lesen und die Anleitung benutzen.

1. **Projekt erfassen.** Projektname auf „Testprojekt Pxxx“, Datenstatus auf „Projektdaten“ setzen. Standort/Anlage auf „Testdatensatz – nicht real“ setzen. Alle drei Nachweise bleiben ungeklärt. Erwartung: Projektname im Dashboard geändert, Nachweis-Prüfbedarf bleibt sichtbar. Als erfüllt nur werten, wenn die Person nicht aus dem Datenstatus eine Freigabe ableitet.
2. **Mengen verändern.** Im Profil „Duschen Sporthalle“ Nutzungstage von 280 auf 100 ändern. Erwartung: Rohgrauwasser 418,2 m³/a statt 742,2 m³/a; Einsparung sinkt. Person soll den Unterschied zwischen Jahresanfall, aufbereitetem Wasser und tatsächlicher Nutzung erklären. Wieder auf 280 zurücksetzen.
3. **Kennzahlen interpretieren.** Ausgangs-Dashboard: Einsparung ca. 555,39 m³/a, Kapitalwert ca. −17.797,87 €, statische Amortisation ca. 41,19 Jahre bei 20 Jahren Horizont. Erwartung: statische Zahl nicht als innerhalb des Horizonts erreichte Amortisation bezeichnen; dynamisch nicht erreicht.
4. **Szenario konfigurieren.** In der Zeile „Konservativ“ Investitionsfaktor 1,20 auf 1,50 ändern. Erwartung: Kapitalwert dieser Zeile sinkt; das Original-Dashboard bleibt unverändert. Die Person erklärt, dass es eine Modellvariante und keine Eintrittswahrscheinlichkeit ist.
5. **Ampel begründen.** Ausgangsdaten: Ökonomie Rot, Ressourcen Grün, Gesamt Rot, Nachweise ungeklärt. Erwartung: unterschiedliche Kriterien und konservative Aggregation nennen; keine Kompensation und keine behördliche Freigabe behaupten.
6. **Fehler erkennen.** Moderator hebt auf der Testkopie den Schutz im Blatt Eingaben auf, leert den Wasserpreis und übergibt die Mappe. Erwartung: „Nicht bewertbar“ erkennen, Prüfungen öffnen, Pflichtfeld B36 korrigieren (2,50 €/m³). Fehlenden Wert nicht als gültigen Nullpreis behandeln.

Die vier strukturierten Erfolgsfelder in `Nutzertest` bündeln: A1 = Aufgabe 1, A2 = Aufgaben 2 + 4, A3 = Aufgaben 3 + 5, A4 = Aufgabe 6. „Erfüllt“ = ohne Hilfe richtig; „Teilweise“ = richtig nach Hilfe oder unvollständig; „Nicht erfüllt“ = ungelöst/falsch. Freitext erklärt Abweichungen; Bearbeitungszeit und Fehlerzahl erfassen den gesamten Durchlauf.

## Fragebogen

Skala: **1 stimme gar nicht zu · 2 stimme eher nicht zu · 3 weder noch · 4 stimme eher zu · 5 stimme voll zu**. Nicht beurteilbare Antworten leer lassen, nicht mit 3 ersetzen. Alle Aussagen sind in positiver Richtung; hohe Werte sind günstige subjektive Beurteilungen.

| Dimension / Spalte | Aussage |
|---|---|
| Verständlichkeit / F | Ich verstehe, welche Eingabedaten für die Bewertung erforderlich sind. |
| Bedienbarkeit / G | Ich kann die benötigten Eingabefelder leicht bearbeiten. |
| Übersichtlichkeit / H | Das Dashboard stellt die wichtigsten Ergebnisse übersichtlich dar. |
| Rechenweg verständlich / I | Ich kann nachvollziehen, wie aus den Eingaben die Kennzahlen entstehen. |
| Ampel verständlich / J | Ich verstehe die Ampelfarben und die Grenzen ihrer Aussagekraft. |
| Fehlersicherheit / K | Hinweise und Prüfungen helfen mir, Eingabefehler zu erkennen und zu korrigieren. |
| Praxistauglichkeit / L | Ich halte das Werkzeug nach projektspezifischer Validierung für eine hilfreiche Planungsunterstützung. |

Zusätzliche offene Fragen: Welche Eingabe war unklar? Welche Erklärung fehlt? Welche Annahme müsste für ein reales Projekt geprüft werden? Welche einzelne Änderung würde die Nutzung am stärksten verbessern?

## Erfassung und Auswertung

`Nutzertest` hat 50 vorbereitete Zeilen. Rolle, Excel-Erfahrung (1 sehr gering bis 5 sehr hoch), Zeit, Fehlerzahl, sieben Antworten, vier Erfolgsfelder und Beobachtungen erfassen. Keine reale Studienantwort ist vorbefüllt.

`Testauswertung` berechnet pro Dimension gültiges n, Mittelwert, Stichprobenstreuung und absolute Verteilung 1–5. Fehlende und ungültige Ratings separat ausweisen. Nicht zugeordnete Zeilen und doppelte IDs prüfen; Duplikate werden gemeldet, **nicht automatisch gelöscht oder dedupliziert**. Deshalb erst nach Bereinigung interpretieren. Gültige Antworten sind numerische ganze Zahlen 1–5 mit ID. Angaben ohne ID zählen nicht in der Dimensionsauswertung.

Zeit-/Fehler-Mittelwerte sind deskriptiv; fehlende Werte werden ausgeschlossen. Plausibilitätsgrenzen: Zeit 0–1440 Minuten, Fehlerzahl ganzzahlig 0–10000. Bei auffälligen Zeiten Unterbrechungen prüfen. Mittelwerte ordinaler Antworten nur als ergänzende Übersicht behandeln und stets Antwortverteilungen und n berichten. Keine zusammengesetzte validierte Usabilityskala oder festgelegte Bestehensgrenze wird behauptet.

Für das Methodenkapitel dokumentieren: Rekrutierung, Anzahl begonnen/abgeschlossen, Rollen, Erfahrung, Testbedingungen, Hilferegel, Abweichungen, fehlende Daten, Auswertung und ethische/datenschutzrechtliche Rahmenbedingungen. Im Ergebniskapitel subjektive Aussagen, beobachtete Bedienfehler und separat geprüfte fachliche Korrektheit auseinanderhalten.
