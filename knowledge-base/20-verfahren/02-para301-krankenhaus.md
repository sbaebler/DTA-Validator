# § 301 SGB V — Krankenhäuser

## 1. Grundlage

Die **Vereinbarung nach § 301 Abs. 3 SGB V** zwischen dem GKV-Spitzenverband und der
Deutschen Krankenhausgesellschaft (DKG) regelt das Verfahren der Datenübermittlung
zwischen nach § 108 SGB V zugelassenen Krankenhäusern und den Krankenkassen. ⚠️ [Q5][Q5e]

**§ 301 Gesamtdokument, gültig ab 01.11.2025** (PDF, ca. 4,5 MB) beschreibt die
Datenstrukturen mit ihren Segmenten, Inhalten, Typen und Datenformaten und erläutert
deren Verwendung. ✅ [Q5d]

## 2. Anlagenstruktur

| Anlage | Inhalt | Marker |
|---|---|---|
| **Anlage 1** | Datensätze für die Datenübermittlung (Inhalt und Aufbau) | ⚠️ [Q5] |
| **Anlage 2** | Schlüsselverzeichnis (in den Datensätzen zu verwendende Schlüssel) | ⚠️ [Q5] |
| **Anlage 3** | Formulare | ⚠️ [Q5] |
| **Anlage 4** | Technische Anlage (Syntax, Transport, Dateiaufbau) | ⚠️ [Q5][Q30] |
| **Anlage 5** | Durchführungshinweise | ⚠️ [Q5] |

Bekannte Versionsstände aus Dokumenttiteln (nur als Beleg für die fortlaufende
Versionierung, nicht als aktueller Stand zu verwenden):

- Anlage 2 Schlüsselverzeichnis — Version 110 (Archiv) ⚠️ [Q5]
- Anlage 4 Technische Anlage — Versionen 39, 46, 51, 59 (Archiv) ⚠️ [Q5][Q5f]
- Anlage 5 Durchführungshinweise — Versionen 57, 63, 69, 76A (Archiv) ⚠️ [Q5]

> ❓ **Widerspruch zu klären:** Eine Suchtreffer-Zusammenfassung nennt "Anlage 1 – Version 47,
> gültig ab 01.10.2025" als *Schlüsselübersicht*, während andere Quellen Anlage 1 als
> *Datensätze* und Anlage 2 als *Schlüsselverzeichnis* führen. Die tatsächliche Zuordnung
> und die aktuellen Versionsnummern sind der Portalseite [Q5] zu entnehmen.

## 3. Nachrichtentypen (EDIFACT)

⚠️ [Q30][Q5]

### Krankenhaus → Krankenkasse

| Typ | Bedeutung |
|---|---|
| `AUFN` | Aufnahmeanzeige stationäre Behandlung |
| `VERL` | Verlängerungsanzeige stationäre Behandlung |
| `MBEG` | Medizinische Begründung (zur Verlängerung) |
| `ENTL` | Entlassungsanzeige |
| `RECH` | Rechnungssatz bei stationären und teilstationären Behandlungen |
| `AMBO` | Rechnungssatz ambulantes Operieren |
| `ZGUT` | Zuzahlungsgutschrift |

### Krankenkasse → Krankenhaus

| Typ | Bedeutung |
|---|---|
| `KOUB` | Kostenübernahme |
| `ANFM` | Anforderung medizinische Begründung |
| `ZAHL` | Zahlungssatz — Bestätigung/Ablehnung zu `RECH` |
| `ZAAO` | Zahlungssatz ambulantes Operieren — Bestätigung/Ablehnung zu `AMBO` |
| `SAMU` | Sammelrechnung / Sammelüberweisung (Rückmeldung) |
| `FEHL` | Fehlernachricht |

Die Nachrichtentypen erscheinen als Kennung im **UNB-Segment** der Übertragungsdatei;
für den ambulanten Bereich werden `ZAAO`, `SAMU`, `FEHL` und für den stationären Bereich
`KOUB`, `ANFM`, `ZAHL`, `SAMU`, `FEHL` als Rückmeldungen genannt. ⚠️ [Q30]

## 4. Zeichensatz

Für die Datenübermittlung nach § 301 Abs. 3 SGB V sind genannt: ⚠️ [Q1]

- **DIN 66303:2000-06** — 8-Bit-Code, deutsche Referenzversion
- **DIN 66003 DRV** — 7-Bit-Code, deutsche Referenzversion

## 5. Fachliche Besonderheiten (Recherchehinweise)

Für ein späteres § 301-Modul sind zusätzlich zu erschließen (⚠️ nicht recherchiert):

- **DRG-/Entgeltsystematik**: aG-DRG, Fallpauschalenkatalog, Zusatzentgelte, NUB
- **Diagnose-/Prozedurenschlüssel**: ICD-10-GM, OPS (jahresbezogene Kataloge!)
- **Abrechnungsprüfung**: Prüfverfahrensvereinbarung (PrüfvV), MD-Prüfungen,
  Datensatzbeschreibungen zur Abrechnungsprüfung des GKV-SV
  (z. B. "Anlage 1 Datensatzbeschreibung", Stand 06.02.2026) ⚠️
- **Anschlussrehabilitation** (eigenes Verfahren, TA 1.1 vom 15.05.2024)
- **Hybrid-DRG** nach § 115f SGB V (TA V1.2 vom 12.08.2025) ✅ [Q33]
