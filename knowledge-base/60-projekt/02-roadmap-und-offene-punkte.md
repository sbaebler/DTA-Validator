# Roadmap und offene Punkte

## 1. Beschaffungsliste

Der PDF-Abruf ist seit dem 01.09.2026 möglich; die Egress-Policy blockiert nicht mehr.
Die Beschaffung ist damit kein Blocker mehr, sondern Arbeit.

### Erledigt (Stand 01.09.2026)

| Dokument | Wirkung | Abgeleitete Datei |
|---|---|---|
| ✅ **Anlage 2 GGT — Auftragsdatei** | Prüfstufe 1 vollständig spezifiziert | [`../data/auftragssatz.yaml`](../data/auftragssatz.yaml) |
| ✅ **Anlage 4 GGT — Verfahrenskennungen** | Prüfstufe 0 und 1 spezifiziert | [`../data/verfahrenskennungen.yaml`](../data/verfahrenskennungen.yaml) |
| ✅ **§ 105 SGB XI TA 1 V 6.4.0** (+ V 6.5.1, Anhang 1, Anhang 3) | Prüfstufen 3–6 für die Pflege spezifiziert | [`../data/nachrichtentypen.yaml`](../data/nachrichtentypen.yaml) |
| ✅ **§ 105 SGB XI TA 3 V 6.4.0** — Schlüsselverzeichnisse | Prüfstufe 4 für die Pflege | — |
| ✅ **Gemeinsames Rundschreiben Institutionskennzeichen 02/2026** | IK-Prüfziffer verifiziert (Testvektor `260326822`), Klassifikations- und Regionaltabellen | — |
| ✅ Portalseiten „Technische Standards" und „Pflege" | vollständiges GGT-Anlagenverzeichnis, Versionsstände § 105 | [`../data/dokumentenregister.yaml`](../data/dokumentenregister.yaml) |

### Offen

| Prio | Dokument | Blockiert | Quelle |
|---|---|---|---|
| **1** | **§ 302 Anlage 1 — Technische Anlage** | Prüfstufen 3–6 für § 302; Segmentgrammatik SLGA/SLLA, Feldkatalog | [Q1] |
| **1** | **§ 302 Anlage 3 — Schlüsselverzeichnisse** (V22, ab 01.02.2027) | Prüfstufe 4; Verarbeitungskennzeichen, Leistungsarten | [Q1] |
| **2** | **Anlage 16 GGT — Security-Schnittstelle** (94 S., ab 01.01.2026) | Prüfstufe 2; verbindliche Algorithmen, LDAP-Schema Kap. 4.6.2 | [Q8] |
| **2** | **Anlage 15 GGT — Zeichensätze** | Prüfregel S3-ALL-006; normative Bedeutung von `I1`/`I5`/`I7`/`I8`/`P8`/`U8` | [Q46] |
| **2** | **Kostenträgerdatei § 302** inkl. Satzartenbeschreibung | Prüfstufe 1 und 4; Routing-Prüfungen | [Q15] |
| **2** | **§ 105 SGB XI TA 1 Anhang 5 — Kostenträgerdatei V 5.2** | Prüfregel S1-ALL-006 für die Pflege; KIM-Adressermittlung über `DFU`/`IDK` | [Q22h] |
| **2** | **Richtlinie Gesamtsystem KVNR V3.4.0** | KVNR-Prüfziffer, insbesondere Behandlung des Buchstabens | [Q10] |
| **3** | **Anlage 6 GGT — Besonderheiten LE-Datenaustausch** | Verfahrensspezifische Abweichungen | [Q32] |
| **3** | **Anlage 1 GGT — KKS** | Formale Bestätigung des Dateipärchen-Prinzips | [Q14] |
| **3** | **Anlage 7/8/9/10/14/20 GGT** | Transportwegspezifische Prüfungen | [Q16][Q42][Q43][Q44][Q21][Q18] |
| **3** | **§ 105 SGB XI TA 5 — Datenübermittlung in der TI V 1.2.0** | TI-Strecke ab 01.02.2027 | [Q22j] |
| **3** | **§ 105 SGB XI TA 1 Anhang 4 — Softwareprüfung** | Prüfkatalog, Selbsterklärung | [Q22i] |
| **3** | **Positionsnummernverzeichnisse § 302** | Prüfstufe 4 Heilmittel | [Q24] |
| **3** | **GKV-Hilfsmittelverzeichnis** (Bezugsweg/Format) | Prüfstufe 4 Hilfsmittel | [Q24b] |
| **4** | § 301 Gesamtdokument + Anlagen 1–5 | Ausbaustufe Krankenhaus | [Q5d] |
| **4** | § 300 TA 1/3/7 | Ausbaustufe Apotheken | [Q35] |

**Hinweis zur Beschaffung:** Die Dokumente sind auf <https://www.gkv-datenaustausch.de>
frei verfügbar. Beim Import in das Repository sind Urheber- und Nutzungsrechte zu
beachten — **nicht die PDFs selbst** committen, sondern die daraus abgeleiteten
strukturierten Regeldateien mit Fundstellenangabe. So wurde mit Anlage 2 und Anlage 4
GGT sowie der TA 1/TA 3 Pflege verfahren.

## 2. Zu klärende Widersprüche (❓)

### Am 01.09.2026 geklärt

| Nr. | Frage | Antwort |
|---|---|---|
| ✅ ❓-05 | GGT: Titel und Inhalt der Anlagen 3, 10, 11, 12, 15, 18, 19 | Anlage 3 = eXTra, 10 = FTAM over IP, 12 = XML-Richtlinie, 15 = Zeichensätze, 18 = Begriffs-/Abkürzungsverzeichnis, 19 = DiGA-Schnittstelle. Zusätzlich existiert **Anlage 21 (Synchroner Dialog)**. **Anlage 11 bleibt offen** (siehe ❓-19). ✅ [Q12] |
| ✅ ❓-06 | Auftragssatz: vollständige Feldliste mit Positionen | 37 Felder, Stellen 1–348, vier Objekte. [`../data/auftragssatz.yaml`](../data/auftragssatz.yaml) ✅ [Q7] |
| ✅ ❓-07 | EDIFACT-Default-Trennzeichen oder abweichende? | Für § 105 SGB XI **abweichend**: Dezimalzeichen ist das **Komma**, und es gibt **kein `UNA`-Segment**. Für §§ 300/301/302 weiter offen. ✅ [Q22] |
| ✅ ❓-08 | Zeichensatz für §§ 300/302 SGB V und § 105 SGB XI | § 105: ISO 8859-1 / ISO 7-Bit / ISO 8-Bit für die Nutzdaten, UTF-8 nach DIN SPEC 91379 nur für die XML-Hülle in der TI. §§ 300/302 weiter offen. ✅ [Q22][Q22e] |
| ✅ ❓-10 | IK: Gewichtungsrichtung der Prüfziffer; Klassifikationstabelle | Modulo 10 über die Stellen 3–8, von rechts `1-2-1-2-1-2`, Quersumme der Produkte. Testvektor aus der Quelle: `260326822`. Klassifikationen in Anlage 1, Regionalschlüssel in Anlage 2.1/2.2 des Rundschreibens. ✅ [Q9b] |
| ✅ ❓-13 | § 105 SGB XI: `PLAA` oder `PLLA`? | **`PLAA`**. ✅ [Q22] |
| ✅ ❓-16 | Zertifizierungspflicht für Abrechnungssoftware | Für § 105 SGB XI **ja**: Softwareprüfung nach Anhang 4 der TA 1 (Prüfkatalog + Selbsterklärung), plus Anmeldung bei den Datenannahmestellen. Für § 302 SGB V weiter offen. ✅ [Q22] |

### Weiterhin offen

| Nr. | Frage | Fundstelle |
|---|---|---|
| ❓-01 | § 301: Ist Anlage 1 das Datensatzverzeichnis und Anlage 2 das Schlüsselverzeichnis, oder umgekehrt? Widersprüchliche Suchtreffer. | [20-verfahren/02-para301-krankenhaus.md](../20-verfahren/02-para301-krankenhaus.md) |
| ❓-02 | § 302: Welche Anlagen tragen die Nummern 2 und 6? Wie verhält sich die aktuelle Nummerierung zur historischen "TP5"-Systematik? | [20-verfahren/01-para302-sonstige-leistungserbringer.md](../20-verfahren/01-para302-sonstige-leistungserbringer.md) |
| ❓-03 | § 302: Vollständige SLLA-Segmentliste und die Sub-Nachrichtentypen je Leistungsbereich | ebenda |
| ❓-04 | § 302: Feldlänge und vollständige Werteliste der Verarbeitungskennzeichen (`02` vs. `2`?) | ebenda |
| ❓-07a | Verwenden §§ 300/301/302 SGB V die EDIFACT-Default-Trennzeichen? Für § 105 SGB XI ist die Frage geklärt. | [30-technik/03-edifact-syntax-und-zeichensatz.md](../30-technik/03-edifact-syntax-und-zeichensatz.md) |
| ❓-08a | Zeichensatz für §§ 300/302 SGB V; zusätzlich die normative Beschreibung der Kennungen in Anlage 15 GGT | ebenda |
| ❓-09 | SECON: Sind RSASSA-PSS und RSAES-OAEP inzwischen verpflichtend oder optional? | [30-technik/05-security-secon.md](../30-technik/05-security-secon.md) |
| ❓-11 | KVNR: Wie geht der führende Großbuchstabe in die Prüfziffer ein? | [40-stammdaten/02-krankenversichertennummer.md](../40-stammdaten/02-krankenversichertennummer.md) |
| ❓-12 | KVNR: Stimmt die 20-stellige Zusammensetzung (10 + 9 + 1)? | ebenda |
| ❓-14 | Kostenträgerdatei: Satzartenstruktur und Verkettungslogik | [40-stammdaten/03-kostentraegerdateien-und-annahmestellen.md](../40-stammdaten/03-kostentraegerdateien-und-annahmestellen.md) |
| ❓-15 | TI-Pflicht ab 01.10.2027: gesetzliche Grundlage und exakter Wortlaut | [10-rechtsgrundlagen/01-gesetzliche-grundlagen.md](../10-rechtsgrundlagen/01-gesetzliche-grundlagen.md) |
| ❓-16a | Besteht eine Zertifizierungspflicht für § 302-Abrechnungssoftware analog zur Softwareprüfung nach § 105 SGB XI? | [30-technik/05-security-secon.md](../30-technik/05-security-secon.md) |
| ❓-17 | Ausschluss-/Verjährungsfristen für die Abrechnung (Prüfstufe 6) | [50-anforderungen/02-validierungsregeln.md](../50-anforderungen/02-validierungsregeln.md) |
| ❓-18 | § 105 SGB XI: Wie löst man den Widerspruch zwischen Anhang 1 der TA 1 (Stand 2007: PEM, alte Komprimierungswerte) und der Anlage 2 GGT (Stand 2024: PKCS#7)? Die hier vertretene Auslegung „GGT schlägt Anhang, Zusatzbelegung bleibt" ist **nirgends ausgeschrieben**. | [20-verfahren/05-para105-sgbxi-pflege.md](../20-verfahren/05-para105-sgbxi-pflege.md) |
| ❓-19 | GGT: Existiert eine Anlage 11? Die Portalseite führt sie nicht. | [30-technik/01-ggt-und-anlagen.md](../30-technik/01-ggt-und-anlagen.md) |
| ❓-20 | Beschäftigtennummer nach § 293 Abs. 8 Satz 2 SGB V: Aufbau, Vergabe und Prüfziffer sind nicht erfasst — nur die Ersatzwerte sind belegt. | [20-verfahren/05-para105-sgbxi-pflege.md](../20-verfahren/05-para105-sgbxi-pflege.md) |

## 3. Roadmap-Vorschlag

### Phase 0 — Fundament (Voraussetzung)
- [x] Primärdokumente Anlage 2 GGT, Anlage 4 GGT, § 105 SGB XI TA 1/TA 3, IK-Rundschreiben beziehen
- [ ] Restliche Prio-1- und Prio-2-Dokumente beziehen (§ 302 Anlagen 1 und 3, Anlage 15 und 16 GGT, Kostenträgerdateien, KVNR-Richtlinie)
- [x] ❓-05, ❓-06, ❓-07, ❓-08, ❓-10, ❓-13, ❓-16 klären
- [ ] ❓-01 bis ❓-04, ❓-09, ❓-11, ❓-12, ❓-14, ❓-15, ❓-17 bis ❓-20 klären
- [ ] Technologieentscheidung treffen (siehe Architekturskizze, Abschnitt 6)
- [ ] Repository-Grundgerüst, CI, Lizenz- und Datenschutzkonzept

### Phase 1 — Transport- und Envelope-Validator

**Nicht mehr blockiert** — Anlage 2 und Anlage 4 GGT liegen strukturiert vor.

- [ ] Dateinamens- und Dateipärchen-Prüfung (Stufe 0) — Regeln `S0-ALL-001` bis `S0-ALL-009`
- [ ] Auftragssatz-Parser und -Validierung (Stufe 1) — Feldkatalog aus [`../data/auftragssatz.yaml`](../data/auftragssatz.yaml)
- [ ] Verfahrenskennungs-Registry aus [`../data/verfahrenskennungen.yaml`](../data/verfahrenskennungen.yaml)
- [ ] IK-Prüfziffer mit Testvektor `260326822` aus dem Gemeinsamen Rundschreiben ✅ [Q9b]
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
- [ ] § 105 SGB XI (PLGA/PLAA) — **vorziehbar**: Segmentgrammatik und Schlüsselverzeichnis liegen vor, § 302 ist der blockierte Teil
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
