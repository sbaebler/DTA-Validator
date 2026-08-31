# Roadmap und offene Punkte

## 1. Beschaffungsliste — Blocker vor dem Implementierungsstart

Diese Dokumente konnten in der Rechercheumgebung **nicht abgerufen** werden (Egress-Policy).
Ohne sie sind die genannten Prüfstufen nicht implementierbar.

| Prio | Dokument | Blockiert | Quelle |
|---|---|---|---|
| **1** | **Anlage 2 GGT — Auftragsdatei (Auftragssatz)** | Prüfstufe 1 vollständig; Feldpositionen, Längen, Pflichtfelder | [Q7] |
| **1** | **Anlage 4 GGT — Verfahrenskennungen** (47 S.) | Prüfstufe 0 und 1; Werteliste der Verfahrenskennungen | [Q20] |
| **1** | **§ 302 Anlage 1 — Technische Anlage** | Prüfstufen 3–6 für § 302; Segmentgrammatik SLGA/SLLA, Feldkatalog | [Q1] |
| **1** | **§ 302 Anlage 3 — Schlüsselverzeichnisse** (V22, ab 01.02.2027) | Prüfstufe 4; Verarbeitungskennzeichen, Leistungsarten | [Q1] |
| **2** | **Anlage 16 GGT — Security-Schnittstelle** (94 S., ab 01.01.2026) | Prüfstufe 2; verbindliche Algorithmen, LDAP-Schema Kap. 4.6.2 | [Q8] |
| **2** | **Kostenträgerdatei § 302** inkl. Satzartenbeschreibung | Prüfstufe 1 und 4; Routing-Prüfungen | [Q15] |
| **2** | **Gemeinsames Rundschreiben Institutionskennzeichen (ARGE·IK)** | IK-Prüfziffer verifizieren, Klassifikationstabelle Stellen 1–2 | [Q9] |
| **2** | **Richtlinie Gesamtsystem KVNR V3.4.0** | KVNR-Prüfziffer, insbesondere Behandlung des Buchstabens | [Q10] |
| **3** | **Anlage 6 GGT — Besonderheiten LE-Datenaustausch** | Verfahrensspezifische Abweichungen | [Q32] |
| **3** | **Anlage 1 GGT — KKS** | Formale Bestätigung des Dateipärchen-Prinzips | [Q14] |
| **3** | **Anlage 7/8/9/14/20 GGT** | Transportwegspezifische Prüfungen | [Q16][Q21][Q18] |
| **3** | **Positionsnummernverzeichnisse § 302** | Prüfstufe 4 Heilmittel | [Q24] |
| **3** | **GKV-Hilfsmittelverzeichnis** (Bezugsweg/Format) | Prüfstufe 4 Hilfsmittel | [Q24b] |
| **4** | § 105 SGB XI TA 1 V6.4.0 | Ausbaustufe Pflege | [Q22] |
| **4** | § 301 Gesamtdokument + Anlagen 1–5 | Ausbaustufe Krankenhaus | [Q5d] |
| **4** | § 300 TA 1/3/7 | Ausbaustufe Apotheken | [Q35] |

**Hinweis zur Beschaffung:** Die Dokumente sind auf <https://www.gkv-datenaustausch.de>
frei verfügbar. Beim Import in das Repository sind Urheber- und Nutzungsrechte zu
beachten — empfohlen wird, **nicht die PDFs selbst** zu committen, sondern die daraus
abgeleiteten strukturierten Regeldateien mit Fundstellenangabe.

## 2. Zu klärende Widersprüche (❓)

| Nr. | Frage | Fundstelle |
|---|---|---|
| ❓-01 | § 301: Ist Anlage 1 das Datensatzverzeichnis und Anlage 2 das Schlüsselverzeichnis, oder umgekehrt? Widersprüchliche Suchtreffer. | [20-verfahren/02-para301-krankenhaus.md](../20-verfahren/02-para301-krankenhaus.md) |
| ❓-02 | § 302: Welche Anlagen tragen die Nummern 2 und 6? Wie verhält sich die aktuelle Nummerierung zur historischen "TP5"-Systematik? | [20-verfahren/01-para302-sonstige-leistungserbringer.md](../20-verfahren/01-para302-sonstige-leistungserbringer.md) |
| ❓-03 | § 302: Vollständige SLLA-Segmentliste und die Sub-Nachrichtentypen je Leistungsbereich | ebenda |
| ❓-04 | § 302: Feldlänge und vollständige Werteliste der Verarbeitungskennzeichen (`02` vs. `2`?) | ebenda |
| ❓-05 | GGT: Titel und Inhalt der Anlagen 3, 10, 11, 12, 15, 18, 19 | [30-technik/01-ggt-und-anlagen.md](../30-technik/01-ggt-und-anlagen.md) |
| ❓-06 | Auftragssatz: vollständige Feldliste mit Positionen | [30-technik/02-kks-auftragsdatei-dateinamen.md](../30-technik/02-kks-auftragsdatei-dateinamen.md) |
| ❓-07 | Verwenden die GKV-Verfahren die EDIFACT-Default-Trennzeichen oder abweichende? | [30-technik/03-edifact-syntax-und-zeichensatz.md](../30-technik/03-edifact-syntax-und-zeichensatz.md) |
| ❓-08 | Zeichensatz für §§ 300/302 SGB V und § 105 SGB XI (nur für § 301 belegt) | ebenda |
| ❓-09 | SECON: Sind RSASSA-PSS und RSAES-OAEP inzwischen verpflichtend oder optional? | [30-technik/05-security-secon.md](../30-technik/05-security-secon.md) |
| ❓-10 | IK: Gewichtungsrichtung der Prüfziffernberechnung; Klassifikationstabelle Stellen 1–2 | [40-stammdaten/01-institutionskennzeichen.md](../40-stammdaten/01-institutionskennzeichen.md) |
| ❓-11 | KVNR: Wie geht der führende Großbuchstabe in die Prüfziffer ein? | [40-stammdaten/02-krankenversichertennummer.md](../40-stammdaten/02-krankenversichertennummer.md) |
| ❓-12 | KVNR: Stimmt die 20-stellige Zusammensetzung (10 + 9 + 1)? | ebenda |
| ❓-13 | § 105 SGB XI: `PLAA` oder `PLLA`? | [20-verfahren/05-para105-sgbxi-pflege.md](../20-verfahren/05-para105-sgbxi-pflege.md) |
| ❓-14 | Kostenträgerdatei: Satzartenstruktur und Verkettungslogik | [40-stammdaten/03-kostentraegerdateien-und-annahmestellen.md](../40-stammdaten/03-kostentraegerdateien-und-annahmestellen.md) |
| ❓-15 | TI-Pflicht ab 01.10.2027: gesetzliche Grundlage und exakter Wortlaut | [10-rechtsgrundlagen/01-gesetzliche-grundlagen.md](../10-rechtsgrundlagen/01-gesetzliche-grundlagen.md) |
| ❓-16 | Besteht eine Zertifizierungspflicht für § 302-Abrechnungssoftware analog zur ITSG-Systemuntersuchung? | [30-technik/05-security-secon.md](../30-technik/05-security-secon.md) |
| ❓-17 | Ausschluss-/Verjährungsfristen für die Abrechnung (Prüfstufe 6) | [50-anforderungen/02-validierungsregeln.md](../50-anforderungen/02-validierungsregeln.md) |

## 3. Roadmap-Vorschlag

### Phase 0 — Fundament (Voraussetzung)
- [ ] Primärdokumente Prio 1 und 2 aus der Beschaffungsliste beziehen
- [ ] Widersprüche ❓-01 bis ❓-14 klären, Marker in der Wissensbibliothek auf ✅ heben
- [ ] Technologieentscheidung treffen (siehe Architekturskizze, Abschnitt 6)
- [ ] Repository-Grundgerüst, CI, Lizenz- und Datenschutzkonzept

### Phase 1 — Transport- und Envelope-Validator
- [ ] Dateinamens- und Dateipärchen-Prüfung (Stufe 0)
- [ ] Auftragssatz-Parser und -Validierung (Stufe 1)
- [ ] Verfahrenskennungs-Registry aus Anlage 4 GGT
- [ ] IK-Prüfziffer mit Testvektoren
- [ ] CLI-Grundgerüst mit JSON-Ausgabe

### Phase 2 — Kryptografie
- [ ] PKCS#7/CMS-Verarbeitung (Stufe 2)
- [ ] X.509-Kettenprüfung inkl. CRL
- [ ] Gegenprüfung gegen `DieTechniker/secon-tool` ✅ [Q40]
- [ ] Algorithmus-agnostische Provider-Schnittstelle (PQC-Vorbereitung)

### Phase 3 — § 302 Nutzdaten
- [ ] EDIFACT-Parser mit UNA-basierten Trennzeichen und Zeichensatz-Handling (Stufe 3)
- [ ] Segmentgrammatik SLGA/SLLA als deklaratives Schema
- [ ] Feldformat- und Schlüsselprüfung (Stufe 4)
- [ ] Summen- und Integritätsprüfung (Stufe 5)
- [ ] Korrekturverfahren (Stufe 6)

### Phase 4 — Stammdaten
- [ ] Kostenträgerdatei-Import mit Versionierung
- [ ] Positionsnummernverzeichnisse und Hilfsmittelverzeichnis
- [ ] Gültigkeitszeitraumbasierte Schlüsselauflösung

### Phase 5 — Ausbau
- [ ] § 105 SGB XI (PLGA/PLAA)
- [ ] KIM-/TI-Transportprüfungen (Blick auf 01.10.2027)
- [ ] § 301 SGB V
- [ ] Optional: § 300 SGB V, HTTP-API

## 4. Risiken

| Risiko | Wirkung | Gegenmaßnahme |
|---|---|---|
| Regelwerke ändern sich stichtagsbezogen und häufig | Validator veraltet unbemerkt | Regelwerks-Registry mit Gültigkeitszeiträumen; Warnung bei abgelaufener Version; Monitoring der Portalseiten |
| Regelwerke sind PDF-Prosa, nicht maschinenlesbar | Manuelle Übertragung ist fehleranfällig | Jede Regel mit Fundstelle versehen; Review-Pflicht; `status: experimental` bis verifiziert |
| Kryptografie-Migration (PQC) bis 2031 | Krypto-Layer muss umgebaut werden | Algorithmus-agnostische Architektur von Anfang an (REQ-SEC-05) |
| Umstellung auf TI/KIM ab 01.10.2027 | Transportannahmen veralten | Transport-Layer entkoppelt halten; KIM früh berücksichtigen |
| Umstellung EDIFACT → XML (§ 95 SGB IV) | Parser wird obsolet | Parser und Regelwerk strikt trennen |
| Sozialdaten in Testfixtures oder Logs | Datenschutzverstoß | Nur synthetische Testdaten; Maskierung in Befunden (REQ-DSGVO-02/03) |
| Lizenzrechte an Katalogen (ICD-10-GM, OPS, PZN) | Rechtliches Risiko bei Auslieferung | Vor Einbindung klären; Kataloge ggf. nur importieren, nicht ausliefern |
| Etablierter Wettbewerb | Geringe Marktdurchdringung | Wettbewerbsanalyse vor Produktentscheidung nachholen |

## 5. Monitoring der Regelwerke

Zu beobachtende Seiten (Änderungen wirken sich direkt auf Prüfregeln aus):

- <https://www.gkv-datenaustausch.de/technische_standards_1/technische_standards.jsp> (GGT + Anlagen)
- <https://www.gkv-datenaustausch.de/leistungserbringer/sonstige_leistungserbringer/sonstige_leistungserbringer.jsp> (§ 302)
- <https://www.gkv-datenaustausch.de/leistungserbringer/sonstige_leistungserbringer/kostentraegerdateien_sle/kostentraegerdateien.jsp> (Kostenträgerdateien)
- <https://www.gkv-datenaustausch.de/leistungserbringer/sonstige_leistungserbringer/positionsnummernverzeichnisse/positionsnummernverzeichnisse.jsp>
- <https://www.gkv-datenaustausch.de/leistungserbringer/pflege/pflege.jsp> (§ 105 SGB XI)
- <https://www.gkv-datenaustausch.de/leistungserbringer/krankenhaeuser/krankenhaeuser.jsp> (§ 301)
