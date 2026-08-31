# § 295 SGB V — Ärzte, Zahnärzte und Direktabrechner

## 1. Vertragsärztliche Regelversorgung

Die Abrechnung der Vertragsärzte läuft **nicht** über den GKV-DTA im engeren Sinn, sondern
über die Kassenärztlichen Vereinigungen (KVen) mit den KBV-Datensatzstandards
(**KVDT/ADT**, xDT-Familie). Die KV rechnet gesammelt mit den Kassen ab. ⚠️

Für den DTA-Validator zunächst **out of scope**, aber als Abgrenzung wichtig.

## 2. § 295 Abs. 1b SGB V — Direktabrechner / Selektivverträge

Für Verträge nach **§§ 64d, 73b, 132e, 132f und 140a SGB V** (Hausarztzentrierte
Versorgung, besondere Versorgung, Impfleistungen u. a.) rechnen Leistungserbringer
bzw. Vertragspartner **direkt** mit den Krankenkassen ab. ✅ [Q23]

**Regelwerk:** Technische Anlage zum Datenaustausch nach § 295 Abs. 1b SGB V

| Version | Stand | Anzuwenden ab |
|---|---|---|
| **10.0** | **02.04.2025** | **Datenlieferung Quartal 4/2025** ✅ [Q23] |
| 9.0 | 04.10.2023 | ⚠️ |
| 7.0 | 10.03.2020 | ⚠️ |
| 5.0 | 12.12.2017 | ⚠️ |
| 3.0 | 25.01.2012 | ⚠️ |

Die Versionshistorie zeigt: **quartalsweise Stichtage** sind hier das Steuerungsmerkmal —
der Validator muss die Regelwerksversion nach Abrechnungsquartal auswählen.

## 3. Zahnärzte

Eigenes Vertragswerk mit **Technischer Anlage** (Vertrag über den Datenaustausch). ⚠️ [Q28]

Bekannte Stände:
- TA Version 4.4, Stand 26.09.2022 (Archiv) ⚠️
- TA Version 4.0, Stand 05.09.2018 (Archiv) ⚠️
- **Anhang 1 zur TA TP2, Version 3.7, Stand 19.09.2025** ✅ [Q28]

Zusätzlich: **EBZ** — Vereinbarung über die Einführung eines elektronischen
Beantragungs- und Genehmigungsverfahrens; TA v1.4 (15.10.2021) im Archiv belegt. ⚠️

## 4. Offene Recherchepunkte ❓

- Nachrichtentypen und Satzaufbau der TA § 295 Abs. 1b
- Zuordnung "TP2" in der Zahnärzte-Systematik (Teilprojekt-Nummerierung des GKV-SV)
- Abgrenzung KVDT/ADT ↔ § 295 Abs. 1b-Datenaustausch bei Mischkonstellationen
