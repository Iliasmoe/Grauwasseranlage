# Materialien und Methoden: Bewertungssystem für Grauwasseranlagen

Version 1.0, 14. Oktober 2026. Wissenschaftlicher, weiter zu validierender Prototyp für eine OGS mit Sporthalle. Die Datei enthält **fiktive Rechenbeispiele**, keine erhobenen Gebäudedaten. Der bereitgestellte Entwicklungsauftrag war die einzige fachliche Unterlage; eine frühere Excel-Datei, reale Messdaten und Normvolltexte lagen nicht vor.

## 1. Ziel, Forschungsbezug und Evidenzstatus

Das Werkzeug untersucht die Hypothese, dass sich die Eignung einer Grauwasseranlage mit einem transparenten Ampelmodell unter ökonomischen und ressourcenschonenden Kriterien darstellen lässt. Es operationalisiert diese Hypothese; die erfolgreiche Softwareprüfung beweist weder die Hypothese noch die Gültigkeit der Schwellen.

Zielgruppe: TGA-Planung, Gebäudebetrieb und Entscheidungsträger. Ergebnis: zwei getrennte Kategorieampeln, ein konservatives Gesamtergebnis, ein Nachweisstatus und nachvollziehbare Kennzahlen. Das Ergebnis ist **keine normative, hygienische oder behördliche Freigabe**.

| Element | Evidenz / Herkunft | Noch erforderliche Validierung |
|---|---|---|
| Mengengleichung Nutzer × Häufigkeit × Volumen × Tage | Dimensionskonsistente Bilanzdefinition | Nutzerzählung, Messung, Lastprofile |
| Tagesaufbereitung / Speicherstrategie | explizite vereinfachte Modellannahme | Stundenbilanz, tatsächliche Speicher- und Anlagensteuerung |
| Kapitalwert | definierte diskontierte Zahlungsrechnung | projektspezifische Kosten, Zins und Preisentwicklung |
| Ampelschwellen 15 %, 5 %, 0 %, −20 % | **vorläufige, nicht literaturvalidierte Annahmen** | Literaturrecherche und dokumentiertes Expertenverfahren |
| schlechteste Kategorie / Nachweisveto | bewusste methodische Entscheidung | Expertenreview, Vergleich mit Alternativen |
| Beispieldaten | frei gewählter Rechenansatz | vollständiger Ersatz durch Projektdaten |
| Nachweisstatus | Nutzereingabe / Selbstauskunft | Prüfung tatsächlicher Dokumente außerhalb des Tools |

Es wurden keine Norminhalte oder Literaturgrenzwerte erfunden. Die Schwellen dürfen in der Bachelorarbeit erst nach wissenschaftlicher Begründung als validiert bezeichnet werden.

## 2. Aufbau und Datenstruktur

| Blatt | Funktion |
|---|---|
| Dashboard | Projekt, Kennzahlen, Ampeln, Begründungen, Hinweise, Wasser- und Zahlungsdiagramme |
| Eingaben | Projekt, Anlage, Kosten, Tarife, Preissteigerungen, Nachweise |
| Nutzungsprofile | sechs Grauwasserquellen und sechs Betriebswassernutzungen mit eigenen Nutzern und Tagen |
| Kalender | 366 Zeilen; 0/1-Aktivität von Schule, Halle und individueller Gruppe |
| Schwellenwerte | vier frei änderbare Ampelgrenzen und Aggregationsentscheidung |
| Wasserbilanz | täglicher Rechenweg und Volumen-Kontrollgleichung |
| Zahlungen | Jahr 0 bis 50, diskontierte Zahlungsreihe und Amortisation |
| Berechnung | Jahresaggregation, KPI-Formeln, Scores und Bilanzprüfungen |
| Szenarien | drei kombinierte und zwölf Einzelfaktorvarianten, jeweils veränderbar |
| Variantenbilanz / VariantenCF | vollständige Tages-/Zahlungsrechnung je Variante |
| KPI_Katalog | Definition, Formel, Einheit, Interpretation, Herkunft, Grenzen, Ampelverwendung |
| Prüfungen | Pflichtwerte, Wertebereiche und Zusammenhänge |
| Nutzertest / Testauswertung | anonymisierte Erfassung, Antwortverteilungen, Mittelwerte, Zeiten, Fehler |
| Anleitung | Bedienung, Modellgrenzen und Einordnung in der Arbeitsmappe |

Eingaben sind blau und entsperrt. Formeln sind geschützt; der Blattschutz hat kein Passwort und kann für eine fachliche Prüfung aufgehoben werden. Er ist kein Sicherheitsmechanismus. Alle Rechenblätter bleiben sichtbar. Keine Makros, externen Arbeitsmappen, Datenverbindungen oder versteckten Rechenkonstanten.

Die Formeln werden in OOXML mit englischen Funktionsnamen und Komma geschrieben; deutsches Excel zeigt sie lokalisiert an. Verwendet werden Standardfunktionen ohne dynamische Arrays, VBA oder Excel-Datentabellen. Microsoft Excel für Windows ist die Zielanwendung; ein tatsächlicher Windows-Excel-Test steht aus.

## 3. Eingaben und Qualitätssicherung

### 3.1 Profilmodell

Je Quelle/Nutzung: Bezeichnung, Kalendergruppe, Nutzerzahl \(n\), Ereignishäufigkeit je Nutzungstag \(f\), spezifisches Volumen \(v\) in L/Ereignis und jährliche Nutzungstage \(d\).

\[
Q_{j,a}=\frac{n_j f_j v_j d_j}{1000}\quad[\mathrm{m^3/a}]
\]

Die Nutzerzahlen der Profile sind eigenständig. Eine Schule und eine von externen Vereinen genutzte Sporthalle können deshalb verschiedene Mengen und Nutzungstage erhalten. Die Nutzerzahl im Projektkopf ist eine informative Größe und wird nicht nochmals multipliziert.

Zulässigkeit weiterer Quellen und Nutzungen wird **nicht** aus ihrer Bezeichnung hergeleitet. Küchen-/belastete Abwässer dürfen nicht ungeprüft als Grauwasser eingesetzt werden. Das Werkzeug führt keine Wasserqualitätsanalyse durch.

### 3.2 Kalender und Jahresverteilung

Der Kalender enthält Aktivitätsindikatoren \(a_{g,k}\in\{0,1\}\) je Gruppe \(g\) und Tag \(k\). Für ein Nicht-Schaltjahr ist die letzte Zeile leer und alle drei Aktivitätswerte müssen null sein.

\[
D_g=\sum_k a_{g,k},\qquad Q_{j,k}=Q_{j,a}\frac{a_{g,k}}{D_g}
\]

Bei \(D_g=0\) darf ein Profil kein positives Jahresvolumen haben. Bei positivem Profilvolumen gilt \(d_j\le D_g\). Weniger Profiltage werden gleichmäßig als geringere Intensität auf die aktiven Gruppentage verteilt; eine individuelle Anwesenheitsliste wird damit nicht simuliert. Für genau getrennte Abwesenheiten die Kalendergruppen entsprechend definieren. Das ist eine **zu validierende Vereinfachung**.

Der Beispielkalender hat 190 ausgewählte Wochentage für Schule und 280 Hallentage einschließlich Wochenenden. Juli/August und ein Teil des Dezembers werden bei der Schulauswahl ausgespart; Hallentage werden aus den ersten 280 zugelassenen Tagen gewählt. **Dies ist kein recherchierter Ferien- oder Feiertagskalender.** Tatsächliche Ferien, Wochenenden und außerschulische Belegung manuell ersetzen. Beim Wechsel des Bilanzjahrs bleiben die editierbaren Flaggen an ihren Tagespositionen: Kalender prüfen und bei einem nicht vorhandenen 366. Tag alle Flaggen auf 0 setzen.

Die zusätzliche Tagesbilanz ist notwendig, weil die kleinere Jahresmenge allein die mögliche Nutzung bei zeitlich getrenntem Anfall und Bedarf überschätzt. Innerhalb des Tages wird die Übereinstimmung weiterhin pauschalisiert; ein stündlicher Validierungsschritt bleibt erforderlich.

### 3.3 Prüfungen

Pflichtfelder dürfen nicht fehlen. Prozentwerte müssen numerisch innerhalb ihres Bereichs liegen, Nutzungstage und Zeiträume ganzzahlig sein, Mengen/Kosten nicht negativ. Förderung darf die Investition nicht übersteigen. Ersatzkosten brauchen ein Jahr im Betrachtungszeitraum. Schwellen müssen geordnet sein. Positive Abwasserentlastung benötigt einen geänderten projektspezifischen Belegtext; dieser Texttest ersetzt keine Belegprüfung.

Ungültige Projektwerte erzeugen **Nicht bewertbar** und sperren die KPI-Karten. Rechenhilfen werden teilweise auf null gesetzt, um Folgefehler zu vermeiden; diese Hilfswerte sind bei Pflichtfehlern keine Ergebnisse. Nullmengen sind gültige Grenzfälle und werden getrennt von fehlenden Daten behandelt. Ungültige Varianten sperren nur die jeweilige Variantenzeile.

## 4. Wasserbilanz

Notation je Tag: Rohmenge \(G_k\), Betriebsbedarf \(B_k\), Rohwasser-Aufbereitungskapazität \(C\), Verfügbarkeit \(u\), Ausbeute \(\eta\), direkt nutzbarer Anteil \(\alpha\), Tankkapazität \(V\), Übertragsverlust \(\lambda\). Der Tank beginnt am 1. Januar leer.

\[
P_k=\min(G_k,C)u,\quad A_k=P_k\eta
\]

\(P\) ist verarbeitetes Rohwasser, \(A\) aufbereitetes Wasser. Nicht verarbeitet: \(G-P\); Aufbereitungsverlust: \(P-A\). Die Verfügbarkeit reduziert jeden Tag pauschal und bildet keine zusammenhängenden Ausfälle ab.

Mit frischem Endbestand \(S_{k-1}\) aus dem Vortag:

\[
H_k=S_{k-1}(1-\lambda),\quad U_{alt,k}=\min(H_k,B_k)
\]
\[
U_{direkt,k}=\min(\alpha A_k,\max(0,B_k-U_{alt,k}))
\]
\[
U_k=U_{alt,k}+U_{direkt,k},\quad N_k=B_k-U_k
\]
\[
S_k=\min(V,\max(0,A_k-U_{direkt,k}))
\]
\[
O_k=\max(0,A_k-U_{direkt,k}-S_k),\quad L_k=S_{k-1}-U_{alt,k}
\]

\(N\): Trinkwassernachspeisung; \(O\): nicht speicherbarer frischer Überschuss; \(L\): Übertragsverlust plus verworfene ungenutzte Altmenge. Altbestand wird zuerst verwendet. **Nur frischer Tagesrest wird erneut übertragen**; nach dem Folgetag übrig gebliebenes altes Wasser wird verworfen. Die eintägige Speicherregel ist eine konservative Rechenannahme, **keine hygienisch zulässige Aufenthaltszeit**. Tankkapazität und Direktanteil sind editierbar. Der zeitliche Verlauf innerhalb eines Tages bleibt unbekannt.

Kontrollgleichungen:

\[
A_k+S_{k-1}=U_k+O_k+L_k+S_k
\]
\[
\sum A=\sum U+\sum O+\sum L+S_{Ende},\qquad \sum B=\sum U+\sum N
\]

Die tatsächliche Jahresnutzung ist \(\sum U\), nicht \(\min(\sum A,\sum B)\). Der Jahresendbestand wird separat ausgewiesen und gilt nicht als im Bilanzjahr eingespartes Wasser. Das Profil beginnt für jedes Wirtschaftsjahr wieder mit leerem Tank; ein dauerhaft periodischer Jahresübergang wird nicht iteriert.

## 5. Wirtschaftlichkeit

Alle Kosten und Tarife in einer konsistenten Brutto-/Nettobasis und demselben Jahr-1-Preisstand eingeben. Finanzierung, Steuern und fixe Grundgebühren werden nicht modelliert.

\[
I_0=I_{Planung}+I_{Anlage}+I_{Montage}+I_{Sonstige},\quad I_{net}=I_0-F
\]

Fördermittel \(F\) werden vollständig in Jahr 0 angenommen. Varianten halten den Förderbetrag absolut konstant, begrenzen ihn aber auf die jeweilige Investition.

\[
E_a=\sum P_k\,e\quad[\mathrm{kWh/a}]
\]

Der Energiekennwert \(e\) bezieht sich auf verarbeitetes Rohwasser, auch wenn das aufbereitete Wasser später ungenutzt bleibt.

Vermiedene Kosten in Jahr \(t\):

\[
R_t=U_a\left[p_W(1+g_W)^{t-1}+p_A\beta(1+g_A)^{t-1}\right]
\]

\(\beta\in[0,1]\) ist der nachweislich anerkannte variable Abwasser-Einsparanteil. Standardmäßig null. Eine interne Wiederverwendung bedeutet nicht automatisch eine Gebührenentlastung; kommunale Abrechnung und tatsächliche Ableitung sind zu prüfen. Der Trinkwasserpreis umfasst nur den tatsächlich vermeidbaren variablen Anteil.

\[
K_t=(Wartung+Sonstiges)(1+g_K)^{t-1}+E_a p_E(1+g_E)^{t-1}
\]

Eine optionale Ersatzinvestition in Jahr \(t_E\) wird vom Jahr-1-Preisstand mit \(g_K\) hochgerechnet. Ein optionaler **nominaler** Restwert wird ausschließlich am Betrachtungsende gutgeschrieben. Es wird genau ein Ersatzereignis berücksichtigt.

\[
CF_0=-I_{net},\quad CF_t=R_t-K_t-I_{E,t}+Restwert_t
\]
\[
NPV=\sum_{t=0}^{T}\frac{CF_t}{(1+i)^t}
\]

Nominale Steigerungen erfordern einen konsistenten nominalen Zins. Zahlungen am Jahresende, konstante jährliche Wasserprofile und sichere Förderung sind Modellannahmen. Steigerungen sind frei veränderbar, keine Prognosen.

Statische Amortisation: \(I_{net}/(R_1-K_1)\), nur bei positiver Nettoeinsparung und positiver Nettoinvestition. Bei nicht positivem CF: **Nicht erreichbar**; bei Nullinvestition: **Keine Nettoinvestition**. Zahlen außerhalb des Betrachtungszeitraums werden durch einen Dashboard-Hinweis als außerhalb gekennzeichnet.

Dynamische Amortisation: erste nichtnegative kumulierte diskontierte Zahlung, lineare Interpolation zwischen Jahresendpunkten. Ohne Rückgewinnung: **Im Zeitraum nicht erreicht**. Die Interpolation ist ein Reportingansatz und keine exakte unterjährige Zahlungsrechnung. Eine spätere Ersatzinvestition kann wieder Unterdeckung auslösen; das Blatt Berechnung prüft ausdrücklich die Stabilität bis zum Horizont. Erste Amortisation allein garantiert deshalb keine Wirtschaftlichkeit.

Spezifische Lebenszykluskosten:

\[
k_{spez}=\frac{I_{net}+\sum_t(K_t+I_{E,t}-Restwert_t)/(1+i)^t}{\sum_t U_a/(1+i)^t}\quad[\mathrm{€/m^3}]
\]

Der Zähler enthält **keine** vermiedenen Gebühren, da diese Kennzahl die Kosten der bereitgestellten Ersatzwassermenge beschreibt. Diskontierung des Volumens ist eine explizite Levelized-Cost-Konvention, keine behauptete Normvorschrift. Ohne Einsparmenge: Statusmeldung statt Division durch null.

## 6. KPI-Katalog und Auswahl

Der vollständige achtspaltige Katalog steht in `KPI_Katalog` der XLSX. Kurzfassung:

| KPI | Formel / Einheit | Interpretation / Limit | Ampelrolle |
|---|---|---|---|
| Einsparmenge | \(U_a\), m³/a | absolute Trinkwassersubstitution, keine Umwelt-Gesamtbilanz | Nullmenge = Ressourcen Rot |
| Einsparquote | \(U_a/(B_a+Q_{sonstig})\), % | Bezug auf Trinkwasser-Baseline ohne Anlage | einziges Ressourcen-Kriterium |
| Deckungsgrad | \(U_a/B_a\), % | Deckung des Betriebsbedarfs; bei Nullbedarf nicht definiert | Information |
| Nutzungsgrad | \(U_a/G_a\), % | Anteil genutzter Rohmenge; bei Nullanfall nicht definiert | Information |
| Investition | \(I_0\), € | Gesamtumfang der Investition | Information |
| Nettoinvestition | \(I_0-F\), € | Einsatz nach Förderung | Nenner des relativen NPV |
| Nettoeinsparung | \(R_1-K_1\), €/a | erstes Jahr, ohne Zins/Ersatz | Information |
| Statische Amortisation | \(I_{net}/CF_1\), Jahre | nur CF1 > 0; Horizont beachten | Information |
| Kapitalwert | \(NPV\), € | Zukunftswerte/Annahmen entscheidend | einziges Ökonomie-Kriterium |
| Dynamische Amortisation | erste diskontierte Rückgewinnung, Jahre | spätere Unterdeckung möglich | Information |
| Lebenszykluskosten | \(PV(Kosten)/PV(Volumen)\), €/m³ | Konvention transparent, keine LCA | Information |
| Strombedarf | \(P_a e\), kWh/a | nur Anlagenstrom | Information |

Quellen aller KPI-Eingaben: tatsächliche Nutzer-/Verbrauchsmessungen, Belegungspläne, Herstellerdaten, Kostenangebote, Tarife und Gebührenbescheide. **Für den ausgelieferten Beispieldatensatz liegen diese Quellen nicht vor.** Nullquotienten werden intern als 0 angezeigt, mit explizitem Nullmengenhinweis; ihre Aussagekraft ist dann eingeschränkt.

Einsparquote und Deckungsgrad werden nicht gleichzeitig gewichtet. Kapitalwert, Nettoeinsparung und Amortisation beruhen auf denselben Zahlungsströmen; nur der Kapitalwert bestimmt die ökonomische Ampel.

## 7. Ampelmodell

Ökonomie bei positiver Nettoinvestition: \(r=NPV/I_{net}\).

- Grün: \(r\ge0\) im voreingestellten Modell.
- Gelb: \(-0{,}20\le r<0\).
- Rot: \(r<-0{,}20\).
- Ohne Nettoinvestition wird der undefinierte Quotient vermieden: nichtnegativer NPV grün, negativer NPV rot.

Ressourcen: Einsparquote \(q=U_a/(B_a+Q_{sonstig})\).

- Grün: \(q\ge0{,}15\).
- Gelb: \(0{,}05\le q<0{,}15\).
- Rot: \(q<0{,}05\); bei keiner Einsparung immer rot.

**Alle vier Schwellen sind veränderbare, noch wissenschaftlich zu validierende Modellannahmen.** NPV = 0 ist der mathematische Indifferenzpunkt der gewählten Zahlungsrechnung; die Erweiterung zu Ampelklassen ist eine Bewertungsentscheidung. Die −20 % beschreiben einen vorläufigen Verlust-/Prüfbereich, keine akzeptierte allgemeine Investitionsgrenze. Die Wasserquoten sind ohne empirische/normative Herkunft gewählt.

Aggregation: Grün = Score 1, Gelb = 2, Rot = 3. Maximum aus Ökonomie, Ressourcen und Nachweisstatus. Hygienische, technische oder rechtliche Nicht-Erfüllung erhält Score 3; ungeklärte Nachweise Score 2 und expliziten Prüfbedarf; alle nachgewiesen Score 1. Grün setzt günstige Kategorien und vollständig eingetragene Nachweise voraus. Ein positives Wirtschaftsergebnis kann keinen fehlenden Nachweis kompensieren. Fehlende/ungültige Daten erzeugen keine Ampelfarbe, sondern **Nicht bewertbar**.

Eine gewichtete Summe wurde als Default verworfen: Sie erlaubt Kompensation, benötigt unbelegte Präferenzgewichte und verstärkt das Risiko korrelierter Doppelbewertungen. Die konservative Methode ist verständlich, aber strikt und weniger fein abgestuft. Für die Bachelorarbeit sollten beide Methoden mit Experten diskutiert werden; der ausgelieferte Prototyp implementiert ausschließlich das dokumentierte konservative Modell.

## 8. Szenarien und Sensitivität

Drei frei änderbare Szenarien:

| Variante | Investition | Wasserpreis | Betriebsbedarf | GW-Anfall | Betriebskosten | Zinsänderung |
|---|---:|---:|---:|---:|---:|---:|
| Konservativ | 1,20 | 0,90 | 0,90 | 0,80 | 1,20 | +1 Prozentpunkt |
| Basis | 1,00 | 1,00 | 1,00 | 1,00 | 1,00 | 0 |
| Optimistisch | 0,80 | 1,10 | 1,10 | 1,20 | 0,80 | −1 Prozentpunkt |

Dies sind **keine Wahrscheinlichkeiten** oder wissenschaftlich kalibrierten Bandbreiten. Zusätzlich gibt es je zwei Einzelfaktorvarianten: Investition, Wasserpreis, Bedarf, Grauwasser und Betriebskosten ±20 %; Zins ±1 Prozentpunkt. Die Zeilenbezeichnungen beschreiben Startwerte; nach eigener Änderung die Beschriftung entsprechend interpretieren.

Jede Variante berechnet die gesamte Tagesbilanz neu. Kapazität/Speicher bleiben konstant. Die übrige Trinkwasser-Baseline bleibt konstant. OPEX-Faktor wirkt auf Wartung, sonstige Kosten und Energie; der Bedarf-/Anfallfaktor verändert zugleich die behandelte Menge und damit den Energieaufwand. Investitionsfaktor skaliert auch Ersatzinvestition und Restwert; Förderung bleibt gedeckelter absoluter Betrag. Wasserpreisfaktor verändert nur Trinkwasser, nicht Abwasser. Zinssätze unter 0 oder über 100 % sperren die jeweilige Variante.

Das Basis-Szenario startet mit Projektwerten, ist aber eigenständig konfigurierbar. Änderungen in Szenarien verändern nicht die Originaleingaben oder das Projekt-Dashboard.

## 9. Probandentest und fachliche Validierung

Der Nutzertest untersucht Verständlichkeit, Bedienung, Übersicht, Rechenweg, Ampel, Fehlersicherheit und wahrgenommene Praxistauglichkeit. Er setzt eine 5-stufige Zustimmungsskala und standardisierte Aufgaben ein. Protokoll und Abgrenzungen: `Probandentest.md`.

Das Auswertungsblatt berechnet gültige Antwortzahlen, Mittelwerte, Stichprobenstreuung und absolute Antwortverteilungen. Fehlende Werte werden nicht imputiert; ungültige Ratings und doppelte IDs werden ausgewiesen. Mittelwerte ordinaler Likertantworten dienen ausschließlich der deskriptiven Übersicht; Antwortverteilungen mitberichten. Keine Normwerte, Signifikanztests oder psychometrische Gütekriterien werden behauptet.

Subjektive Zustimmung ist **kein fachlicher Nachweis der Formeln**. Softwaretests, handgerechnete Referenzfälle, tatsächliche Tabellenkalkulations-Engine und spätere Experten-/Messdatenvalidierung sind separate Ebenen. Die dokumentierten tatsächlich ausgeführten Tests stehen in `Validierungsbericht.md`.

## 10. Einschränkungen und nächste wissenschaftliche Schritte

1. Tagesprofilannahmen mit Stundenmessungen prüfen; insbesondere Schulbedarf versus Abendduschen und tatsächliche Ferienkalender.
2. Quellenqualität, Trennung, Nachspeisung, Betriebsüberwachung und anwendbare rechtliche Anforderungen fachlich nachweisen.
3. Hersteller-Kapazität, Energie, Ausbeute, Verfügbarkeit und Speicherstrategie belegen; keine Hygieneaussage aus Bilanz ableiten.
4. Kostenangebote, Gebührenregeln, Ersatzbedarf und Preis-/Zinsansätze ersetzen; mehrere Ersatzzyklen gegebenenfalls als spätere Modellerweiterung.
5. Schwellen mit wissenschaftlicher Literatur und strukturiertem Expertenreview validieren; übertragbare Gebäude-Baselines festlegen.
6. Prüfen, ob ressourcenschonende Aussagen eine zusätzliche Energie-/Lebenszyklusanalyse verlangen: das Modell bewertet lokal eingespartes Trinkwasser, nicht umfassende Umweltwirkung.
7. Realer Nutzertest und abschließende Bedien-/Rechenprüfung unter Microsoft Excel für Windows.

## 11. Regelwerke und Quellenhinweise

Es erfolgte keine Literaturvolltextrecherche und keine Prüfung konkreter Normforderungen. Die folgenden **Recherchehinweise sind keine Belege für Modellparameter**:

- DIN EN 16941-2: Regelwerk für Systeme zur Verwendung von aufbereitetem Grauwasser; aktuelle Ausgabe und Projektanwendbarkeit im offiziellen [DIN-Media-Katalog](https://www.dinmedia.de/) prüfen.
- DIN EN 1717: Schutz des Trinkwassers gegen Verunreinigungen; aktuelle Ausgabe, Schnittstellen und konkrete Anforderungen fachlich prüfen, ebenfalls DIN Media.
- [Trinkwasserverordnung – amtlicher Gesetzestext](https://www.gesetze-im-internet.de/trinkwv_2023/): mögliche Projektpflichten anhand des aktuellen Textes prüfen. Es werden keine Paragrafen oder konkreten Grenzwerte daraus behauptet.
- Tatsächliche kommunale Wasser-/Abwassergebührensatzung, Förderbescheide, Belegungspläne und Anlagen-/Betriebsdokumente: noch zu beschaffende Primärdaten des Referenzprojekts.

Für die Bachelorarbeit sind bibliografische Angaben, Ausgabejahr, relevante Abschnitte und Zugriffsdaten erst nach tatsächlicher Recherche zu ergänzen. Die vorliegende Methodik kann als Struktur für Kapitel 4 dienen; sie darf nicht ungeprüft als normativ abgesicherte Planungsgrundlage übernommen werden.
