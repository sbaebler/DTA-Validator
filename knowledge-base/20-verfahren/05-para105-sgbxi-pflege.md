# § 105 SGB XI — Pflege

## 1. Grundlage

**§ 105 SGB XI** regelt die Abrechnung pflegerischer Leistungen. **Abs. 2** ermächtigt zur
einvernehmlichen Festlegung von Form und Inhalt des Abrechnungsverfahrens. ✅ [Q22b]

Vertragswerk: **Vereinbarung nach § 105 Abs. 2 Satz 2 SGB XI vom 05.10.2023** ✅ [Q22b]

## 2. Technische Anlagen

| Dokument | Version | Stand | Marker |
|---|---|---|---|
| **Technische Anlage 1** zur Regelung der Datenübermittlung nach § 105 Abs. 2 SGB XI | **6.4.0** | **07.07.2025** | ✅ [Q22] |
| Technische Anlage 1 (Vorversion) | 6.0.0 | 14.09.2023 | ✅ |
| TA 1 Anhang 1 — Struktur Auftragsdatei | — | 25.01.2007 | ⚠️ |
| TA 1 Anhang 3 — Datenübermittlungsarten | — | 07.09.2017 | ⚠️ |
| Technische Beschreibung elektronischer Versorgungsplan | 1.3 | 26.06.2024 | ⚠️ |
| Broschüre "Information zu den elektronischen Abrechnungsverfahren" (TP 6) | — | 14.07.2025 | ✅ [Q22c] |

Die Versionierung folgt einem **SemVer-ähnlichen Schema (6.4.0)** — anders als bei § 301
(fortlaufende Ganzzahlen) und § 302 (Anlagenversion + Stichtag). Der Validator braucht
deshalb ein **verfahrensspezifisches Versionsmodell**, keinen globalen Zähler.

## 3. Nachrichtentypen

| Typ | Bedeutung | Marker |
|---|---|---|
| **PLGA** | Gesamtaufstellung der Abrechnung | ⚠️ [Q22] |
| **PLAA** | Abrechnungsdaten | ⚠️ [Q22] |

Strukturell das Gegenstück zu **SLGA/SLLA** aus § 302 SGB V — daher hohe
Wiederverwendbarkeit im Validator-Kern.

> ❓ In der Literatur taucht gelegentlich "PLLA" auf; belegt ist **PLAA**. Vor
> Implementierung gegen TA 1 Version 6.4.0 verifizieren.

## 4. Kostenträgerdateien

Eigene Kostenträgerdateien für den Pflegebereich, separat von denen der sonstigen
Leistungserbringer und der Apotheken. ⚠️ [Q15]

## 5. TI/KIM

Pflegeeinrichtungen sind in die TI-Anbindung einbezogen; die Abrechnung nach SGB XI und
nach SGB V soll **synchron** auf vollelektronische Verfahren in der TI umgestellt werden
(Zielzeitpunkt 01.10.2027). ⚠️ [Q18b]
