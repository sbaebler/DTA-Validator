# § 302 SGB V — Sonstige Leistungserbringer

Das für den DTA-Validator wichtigste Verfahren.

## 1. Anwendungsbereich

§ 302 SGB V verpflichtet Leistungserbringer im Bereich **Heilmittel, Hilfsmittel,
digitale Gesundheitsanwendungen** sowie weitere sonstige Leistungserbringer, den
Krankenkassen die von ihnen erbrachten Leistungen **nach Art, Menge und Preis**
elektronisch zu übermitteln. ✅ [Q3]

Erfasste Leistungsbereiche (⚠️ [Q2][Q1]):
- Heilmittel (Physiotherapie, Ergotherapie, Logopädie, Podologie, Ernährungstherapie)
- Hilfsmittel (inkl. Homecare, Pflegehilfsmittel)
- Häusliche Krankenpflege (§ 37 SGB V)
- Haushaltshilfe (§ 38 SGB V)
- Krankentransport- und Fahrkosten (§ 60 SGB V)
- Digitale Gesundheitsanwendungen (DiGA)
- Hebammen und Entbindungspfleger (über § 301a SGB V, gleiche Richtlinien) ⚠️ [Q1]

## 2. Regelwerk

**Richtlinien des GKV-Spitzenverbandes nach § 302 Abs. 2 SGB V** über Form und Inhalt
des Abrechnungsverfahrens, nebst **Technischen Anlagen**. ✅ [Q3][Q1]

Bekannte Anlagenstruktur (⚠️ teilweise unvollständig — Titel gegen die Portalseite prüfen):

| Anlage | Inhalt | Marker |
|---|---|---|
| **Anlage 1** | Technische Anlage für die maschinelle Abrechnung (elektronische Datenübermittlung) — Datensatz-/Segmentbeschreibung | ⚠️ [Q1] |
| **Anlage 2** | ❓ nicht belegt | ❓ |
| **Anlage 3** | Schlüsselverzeichnisse zu den Datensätzen — **Version 22 vom 21.05.2026, anzuwenden ab 01.02.2027**; Version 21 verliert nach 3-monatiger Übergangsfrist am **30.04.2027** ihre Gültigkeit | ⚠️ [Q1] |
| **Anlage 4** | Begleitzettel für Urbelege | ✅ [Q36] |
| **Anlage 5** | Inhalt der Urbelege (Stand 27.09.2018) | ⚠️ [Q1] |
| **Anlage 6** | ❓ nicht belegt | ❓ |
| Zusatz | Gemeinsame Umsetzungsempfehlungen zum Korrekturverfahren Heilmittel (13.02.2025) | ✅ [Q25] |

> ❓ **Offener Punkt:** Historisch existieren Anlagen aus dem "Teilprojekt 5 (TP5)"
> (`Anlage_1_TP5_Vxx`, `Anlage_3_TP5_Vxx`). Ob die aktuelle Nummerierung deckungsgleich ist,
> muss gegen die Portalseite [Q1] geprüft werden.

## 3. Nachrichtentypen

| Typ | Bedeutung | Marker |
|---|---|---|
| **SLGA** | Gesamtaufstellung der Abrechnung (Sammelrechnung / Rechnungskopfdaten) | ⚠️ [Q1][Q30] |
| **SLLA** | Abrechnungsdaten / Leistungsabrechnung (die eigentlichen Leistungspositionen) | ⚠️ [Q1][Q30] |

Eine Nutzdatendatei besteht aus der Folge **UNB … UNZ** und enthält die Nachrichten
**SLGA und SLLA**, jeweils mehrfach wiederholbar. ⚠️ [Q1]

SLGA/SLLA erlauben es, **mehrere Abrechnungsfälle mit identischem Institutionskennzeichen
(aus der Krankenversichertenkarte) gemeinsam zu übermitteln**. ⚠️ [Q30]

### Segmente

**SLGA** — belegt genannte Segmente: `FKT`, `REC`, `UST`, `SKO`, `GES`, `NAM` ⚠️ [Q1]

| Segment | Bedeutung (⚠️ abgeleitet) |
|---|---|
| `FKT` | Funktionssegment: Verarbeitungskennzeichen, Absender-/Empfänger-IK |
| `REC` | Rechnungsdaten (Rechnungsnummer, Rechnungsdatum) |
| `UST` | Umsatzsteuerangaben |
| `SKO` | Skonto-/Zahlungskonditionen |
| `GES` | Gesamtsummen der Rechnung |
| `NAM` | Name/Anschrift des Leistungserbringers |

**SLLA** — belegt bzw. genannt: `ESK` (Einsatzkopfsegment), `EHE`/`EHK`, `ERI`, `ERL`,
`ERZ`, `ZUS` ⚠️❓ [Q1]

> ❓ Die SLLA-Segmentliste ist aus Suchtreffern zusammengetragen und **nicht vollständig
> verifiziert**. Belegt ist nur, dass eine SLLA-Nachricht aus Segmenten besteht, die
> ein- oder mehrfach bzw. nur in bestimmten Abrechnungsfällen vorkommen, und dass `ESK`
> das Einsatzkopfsegment für einen Einsatz/Hausbesuch ist.

**Verfahrensübergreifende Standardsegmente** (auch in § 302): `FKT`, `INV`, `NAD`, `CUX`, `DPV` ⚠️ [Q30]

| Segment | Bedeutung |
|---|---|
| `FKT` | Funktion |
| `INV` | Information des Versicherten (KVNR, Versichertenstatus) |
| `NAD` | Name und Adresse |
| `CUX` | Währung |
| `DPV` | ⚠️ nicht belegt |

> **Offener Punkt für die Implementierung:** SLLA differenziert nach Leistungsbereich
> (Hilfsmittel, Heilmittel, häusliche Krankenpflege, Haushaltshilfe, Krankentransport) ⚠️ [Q1].
> Die genauen Sub-Nachrichtentyp-Kennungen (in der Praxis oft als "SLLA A/B/C/D/E" o. ä.
> bezeichnet) konnten **nicht belegt werden** und sind aus Anlage 1 zu entnehmen. ❓

## 4. Korrekturverfahren (seit 01.07.2020 verpflichtend)

Eingeführt zum 01.01.2020, verpflichtend anzuwenden seit **01.07.2020**. ⚠️ [Q25b]

Nachträge und Korrekturen zu bereits erstellten Abrechnungen sind mit einem
**Verarbeitungskennzeichen (VKZ)** und einem **Bezug zur Ursprungsrechnung** einzureichen. ⚠️ [Q25b]

| VKZ | Bedeutung | Marker |
|---|---|---|
| `02` | Nachforderung (z. B. ein Hausbesuch wurde in der Ursprungsrechnung versehentlich nicht abgerechnet) | ⚠️ [Q25b] |
| `4` | Erneute Einreichung nach Absetzung wegen fehlender/fehlerhafter Daten | ⚠️ [Q25b] |
| `01`, `03`, … | ❓ nicht belegt — vollständige Werteliste aus Anlage 3 (Schlüsselverzeichnisse) ziehen | ❓ |

> ❓ Die Notation ist in den Quellen uneinheitlich (`02` vs. `2`, `4` vs. `04`). Die
> **Feldlänge und Wertemenge sind zwingend aus Anlage 1/3 zu übernehmen**, bevor eine
> Prüfregel implementiert wird.

Ergänzend: *Gemeinsame Umsetzungsempfehlungen zum Korrekturverfahren Heilmittel*
vom 13.02.2025 ✅ [Q25].

## 5. Urbelege

Zur elektronischen Abrechnung gehören die **Urbelege** (Verordnungen, Leistungsnachweise):

- **Anlage 4** definiert den *Begleitzettel für Urbelege* ✅ [Q36]
- **Anlage 5** definiert den *Inhalt der Urbelege* (Stand 27.09.2018) ⚠️ [Q1]
- Urbelege gehen an die **Belegannahmestelle** laut Kostenträgerdatei ⚠️ [Q15]
- Seit Mitte 2025 auch über KIM übermittelbar; Papierform noch bis **30.09.2027** zulässig ⚠️ [Q18b]

## 6. Erprobungs-/Testverfahren

⚠️ [Q37][Q2]

- Die Teilnahme am elektronischen Abrechnungsverfahren erfordert eine **Anmeldung** beim
  Kostenträger bzw. dessen Datenannahmestelle.
- Die Kassen führen eine **Erprobungsphase** durch: Abrechnungsdaten werden elektronisch
  übermittelt, parallel gehen die Abrechnungsunterlagen weiterhin in Papierform ein.
- Während der Erprobungsphase erfolgt **keine Rechnungskürzung**.
- Das Ende der Erprobungsphase teilt die Krankenkasse im Einzelfall mit.
- Kassen bieten Leistungserbringern, Softwareherstellern und Abrechnungszentren an,
  Dateien **vor Verfahrensstart und bei Versionswechseln zu testen**.

**Implikation für den Validator:** Der Test-/Echt-Modus ist im Dateinamen (Stelle 1 `T`/`E`)
kodiert — siehe [30-technik/02-kks-auftragsdatei-dateinamen.md](../30-technik/02-kks-auftragsdatei-dateinamen.md).

## 7. Abzurechnende Schlüssel

- **Hilfsmittel:** 10-stellige Positionsnummer aus dem GKV-Hilfsmittelverzeichnis
- **Heilmittel:** Positionsnummern aus den Positionsnummernverzeichnissen des GKV-SV
- **Diagnosen/Indikationen:** ICD-10-GM, Indikationsschlüssel des Heilmittelkatalogs

→ [40-stammdaten/04-schluessel-und-positionsnummern.md](../40-stammdaten/04-schluessel-und-positionsnummern.md)
