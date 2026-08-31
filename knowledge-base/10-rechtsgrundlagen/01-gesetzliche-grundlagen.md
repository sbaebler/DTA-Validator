# Rechtsgrundlagen

## 1. SGB V — Übermittlung von Leistungsdaten (§§ 294 ff.)

Der Vierte Abschnitt des Zehnten Kapitels SGB V ("Übermittlung von Leistungsdaten")
begründet die Pflicht der Leistungserbringer zur elektronischen Datenübermittlung
und delegiert die Ausgestaltung an Richtlinien und Vereinbarungen.

| Norm | Regelungsgegenstand | Umsetzungsdokument |
|---|---|---|
| **§ 294** | Grundpflicht der Leistungserbringer zur Datenaufzeichnung und -übermittlung | — |
| **§ 295** | Abrechnung ärztlicher Leistungen; **Abs. 1b**: Datenaustausch bei Verträgen nach §§ 64d, 73b, 132e, 132f, 140a SGB V ("Direktabrechner") ✅ [Q23] | Technische Anlage § 295 Abs. 1b SGB V |
| **§ 300** | Abrechnung der Apotheken und weiterer Stellen; Abs. 3 = Ermächtigung zur Abrechnungsvereinbarung ✅ [Q3a] | Arzneimittelabrechnungsvereinbarung + TA 1–7 |
| **§ 301** | Krankenhäuser und Rehabilitationseinrichtungen; **Abs. 3** = Vereinbarung über das Verfahren; **Abs. 4/4a** = Reha-Einrichtungen ✅ [Q3b] | § 301-Vereinbarung (GKV-SV ↔ DKG) mit Anlagen 1–5 |
| **§ 301a** | Abrechnung der Hebammen und Entbindungspfleger ⚠️ [Q1] | Richtlinien nach § 302 Abs. 2 SGB V (gemeinsam mit § 302) |
| **§ 302** | Abrechnung der sonstigen Leistungserbringer: Heilmittel, Hilfsmittel, digitale Gesundheitsanwendungen und weitere; **Abs. 2** = Ermächtigung des GKV-SV zu Richtlinien über Form und Inhalt ✅ [Q3] | Richtlinien nach § 302 Abs. 2 + Technische Anlagen |
| **§ 303** | Ergänzende Regelungen: **Nacherfassung** nicht maschinell verwertbarer Daten und **pauschale Rechnungskürzung bis zu 5 v. H. des Rechnungsbetrages**, wenn der Leistungserbringer die nicht maschinelle Übermittlung zu vertreten hat ✅ [Q4] | — |
| **§ 290** | Krankenversichertennummer | Richtlinie Gesamtsystem KVNR V3.4.0 (22.08.2024) ✅ [Q10] |

### § 303 SGB V — die wirtschaftliche Sanktion

> Werden die … zu übermittelnden Daten nicht im Wege elektronischer Datenübertragung
> oder maschinell verwertbar auf Datenträgern übermittelt, haben die Krankenkassen die
> Daten nachzuerfassen. Erfolgt die nicht maschinell verwertbare Datenübermittlung aus
> Gründen, die der Leistungserbringer zu vertreten hat, haben die Krankenkassen die mit
> der Nacherfassung verbundenen Kosten … durch eine pauschale Rechnungskürzung in Höhe
> von bis zu 5 vom Hundert des Rechnungsbetrages in Rechnung zu stellen.

Sinngemäße Wiedergabe ✅ [Q4] — **exakter Wortlaut vor Zitierung aus der Norm prüfen.**

**Konsequenz für das Projekt:** Eine syntaktisch oder fachlich fehlerhafte Datei ist nicht
nur ein IT-Problem, sondern unmittelbar zahlungswirksam. Der Validator ist damit ein
Werkzeug zur Vermeidung von Rechnungskürzungen und Absetzungen.

## 2. SGB XI — Pflege

| Norm | Regelungsgegenstand |
|---|---|
| **§ 105 SGB XI** | Abrechnung pflegerischer Leistungen; **Abs. 2** = einvernehmliche Festlegung von Form und Inhalt ✅ [Q22b] |

Umsetzung: Technische Anlage 1 zum DTA nach § 105 SGB XI, aktuell **Version 6.4.0 vom
07.07.2025** ✅ [Q22], sowie Vereinbarung nach § 105 Abs. 2 Satz 2 SGB XI vom 05.10.2023 ✅ [Q22b].

## 3. SGB IV — technischer Unterbau und Arbeitgeberverfahren

| Norm | Regelungsgegenstand |
|---|---|
| **§ 95 SGB IV** | **Gemeinsame Grundsätze Technik (GGT)** — schafft erstmals die Rechtsgrundlage, den Datenaustausch zur und innerhalb der Sozialversicherung technisch verbindlich zu spezifizieren ✅ [Q11] |
| **§§ 28a ff. SGB IV / DEÜV** | Arbeitgeber-Meldeverfahren (DEÜV) ⚠️ [Q19] |
| **§ 28f Abs. 3 i. V. m. § 95b Abs. 1 SGB IV, § 26 DEÜV** | Beitragsnachweise nur per **systemgeprüftem** Entgeltabrechnungsprogramm oder maschineller Ausfüllhilfe ⚠️ [Q26] |
| **§ 95a SGB IV** | Elektronisch gestützte Ausfüllhilfe (SV-Meldeportal) ⚠️ [Q19] |

### Verfahren der GGT-Verabschiedung ⚠️ [Q11]

Die GGT werden vereinbart von: GKV-Spitzenverband, Deutsche Rentenversicherung Bund,
Deutsche Rentenversicherung Knappschaft-Bahn-See, Bundesagentur für Arbeit und
Deutsche Gesetzliche Unfallversicherung. Sie bedürfen der **Genehmigung des BMAS** im
Benehmen mit dem BMG und — soweit Arbeitgebermeldeverfahren betroffen sind — nach
Anhörung der BDA.

Geregelt werden u. a.: Verschlüsselung der Daten, Übertragungstechniken, Kennzeichnung
für die Weiterleitung von Nachrichten über ein Stichtagsdatum, die jeweiligen
Schnittstellen und die Zeitpunkte der Umstellung einzelner technischer Verfahren auf
XML-basierte Verfahren. ⚠️ [Q11]

## 4. Datenschutz

Relevante Rahmenbedingungen (⚠️ nicht abschließend recherchiert, vor Konzeption vertiefen):

- **DSGVO** — insbesondere Art. 9 (Gesundheitsdaten als besondere Kategorie)
- **§ 35 SGB I** — Sozialgeheimnis
- **§§ 67 ff. SGB X** — Sozialdatenschutz, Zweckbindung, Übermittlungsbefugnisse
- **Trennungsgebot**: Die Auftragsdatei wird unverschlüsselt übertragen und darf deshalb
  **keine Sozialdaten** enthalten; die Nutzdaten sind stets verschlüsselt. ⚠️ [Q14][Q7]
  Für einen Validator bedeutet das: Testdaten dürfen niemals echte Versichertendaten
  enthalten, und Logs dürfen keine entschlüsselten Nutzdateninhalte persistieren.

## 5. Roadmap-relevante Fristen

| Datum | Ereignis | Marker |
|---|---|---|
| 01.07.2020 | Korrekturverfahren nach § 302 verpflichtend (eingeführt zum 01.01.2020) | ⚠️ [Q25b] |
| ab Mitte 2025 | Alle Bestandteile der DTA-Abrechnung inkl. Urbelege über KIM übermittelbar | ⚠️ [Q18b] |
| 01.01.2026 | Anlage 16 GGT (Security-Schnittstelle) in der Fassung vom 02.09.2025 gültig | ✅ [Q8] |
| 01.01.2026 | Anlage 4 GGT (Verfahrenskennungen) in der Fassung vom 06.11.2025 gültig | ✅ [Q20] |
| 01.02.2027 | § 302 Anlage 3 Version 22 (vom 21.05.2026) anzuwenden | ⚠️ [Q1] |
| 30.04.2027 | Ende der Übergangsfrist für § 302 Anlage 3 Version 21 | ⚠️ [Q1] |
| 30.09.2027 | Ende der Übergangsfrist für Urbelege in Papierform | ⚠️ [Q18b] |
| **01.10.2027** | **Abrechnung ausschließlich innerhalb der TI (KIM)**; ursprünglich 01.12.2026 | ⚠️ [Q18b] ❓ Rechtsgrundlage verifizieren |
| bis Ende 2031 | BSI: klassische asymmetrische Schlüsseleinigungsverfahren nur noch bis Ende 2031 → Migrationsdruck auf Anlage 16 GGT | ⚠️ [Q38] |
