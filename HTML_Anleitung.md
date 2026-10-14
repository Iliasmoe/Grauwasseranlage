# Grauwasser als eigenständige HTML-Anwendung

**`Grauwasser_App.html` herunterladen und im Browser öffnen.** Die einzelne Datei enthält Oberfläche, Berechnungen, Dokumente und die Excel-Vorlage. Sie benötigt keine Installation, keinen Python-Server und keine Internetverbindung. Moderne Browser mit JavaScript, localStorage und den üblichen Datei-Downloadfunktionen verwenden, beispielsweise Chrome oder Edge.

## Arbeitsstände speichern

- Jede Eingabe speichert den aktuellen Projektstand automatisch in diesem Browser. Auch leere Felder und unvollständige Entwürfe bleiben erhalten; ungültige Daten werden nicht als gültige Ergebnisse angezeigt.
- Unter **„Zwischenstände“** einen Namen eingeben und **„Zwischenstand sichern“** anklicken, um eine bestimmte Variante festzuhalten.
- Bei Änderungen sichert die Anwendung frühere Zustände zusätzlich automatisch, maximal alle 30 Sekunden. Je Projekt bleiben die letzten **20 Zwischenstände** erhalten. Der aktuelle Arbeitsstand wird unabhängig von diesem Zeitabstand bei jeder Änderung gespeichert.
- **„Wiederherstellen“** übernimmt den ausgewählten Zwischenstand. Der vorherige Arbeitsstand wird zuerst als weiterer Zwischenstand gesichert.
- Projekte, Kalender, Szenarien, Nachweise, Schwellenwerte und Testantworten werden gemeinsam gespeichert. Verschiedene Projekte haben getrennte Historien.
- **„Projektdatei“** exportiert den aktuellen Stand als JSON. Der Importknopf legt daraus ein weiteres Projekt an. Die JSON-Datei enthält den aktuellen Projektstand, nicht die gesamte lokale Historie.

Die Anzeige **„Lokal gespeichert“** bestätigt erfolgreiche Browser-Speicherung. Bei gesperrtem oder vollem Browser-Speicher erscheint **„Nicht gespeichert“**. Sie können weiterarbeiten und den Stand als JSON herunterladen.

## Wo liegen die Daten?

Die Daten liegen im `localStorage` Ihres Browsers. Beim erneuten Öffnen werden sie automatisch geladen. Verwenden Sie denselben Browser und denselben Speicherort der HTML-Datei. Das Verhalten von `localStorage` für `file://` hängt vom Browser ab; Umbenennen oder Verschieben der Datei kann deshalb einen anderen Speicherbereich öffnen. Bei einer Auslieferung über HTTP ist der Ursprung aus Protokoll, Host und Port entscheidend. Bestehende Projekte der bisherigen Web-Version bleiben am gleichen HTTP-Ursprung lesbar.

Ein anderer Browser, ein anderes Gerät oder privates Browsen übernimmt die Daten nicht. **Browserdaten löschen entfernt auch die Zwischenstände.** Vor einem Gerätewechsel oder dem Verschieben der HTML-Datei den aktuellen Stand als JSON sichern. Die HTML-Datei selbst wird durch Eingaben nicht verändert und enthält weiterhin ausschließlich Beispieldaten.

## Berechnung und Export

Alle Berechnungen erfolgen auf Ihrem Gerät: Tagesbilanz, Speicherverluste, Kapitalwert, Zahlungsreihe, drei Szenarien, zwölf Sensitivitäten und Studienstatistik. Es erfolgen keine Anfragen an einen Berechnungsserver oder externe Dienste.

**„Excel exportieren“** erzeugt die wissenschaftliche XLSX-Vorlage mit Ihren tatsächlichen Eingaben, Kalender, Szenarien, Schwellen und Studienantworten. Excel oder LibreOffice berechnet die enthaltenen Formeln beim Öffnen neu. Veraltete Ergebnis-Caches aus der Beispielvorlage werden entfernt. Texteingaben werden als Textzellen exportiert und nicht als Formeln ausgeführt. Methodik, Validierungsbericht und Probandenprotokoll sind ebenfalls eingebettet und können offline heruntergeladen werden.

## Quellcode und erneuter Build

Voraussetzung für einen eigenen Build: Node.js 22.12+ und npm. Python wird nur für Referenztests benötigt.

```bash
cd web/frontend
npm ci
npm run build
```

Der Build erstellt `Grauwasser_App.html` im Repositoryverzeichnis und weiterhin das normale Frontend in `web/frontend/dist`. Die Einzeldatei kann auch auf einem gewöhnlichen statischen Webserver bereitgestellt werden; FastAPI wird für die Oberfläche nicht benötigt. Die bestehende Python-API bleibt als Referenz und optionaler Dienst verfügbar.

Die tatsächlich ausgeführten Tests und die Einschränkung des lokalen Cloud-Browsers stehen in [`web/HTML_VALIDIERUNG.md`](web/HTML_VALIDIERUNG.md). Beispieldaten und Ampelschwellen bleiben Modellannahmen; Projektbelege und fachliche Nachweise sind weiterhin erforderlich.
