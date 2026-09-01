# Verfahrensübersicht

Die GKV kennt keinen einheitlichen "DTA-Standard", sondern **eine Familie sektorspezifischer
Verfahren** mit gemeinsamem technischem Unterbau (GGT/KKS/SECON) und je eigenen
Nachrichtenformaten, Schlüsselverzeichnissen und Fristen.

## Matrix der Verfahren

| Verfahren | Rechtsgrundlage | Leistungserbringer | Nachrichtentypen | Regelwerk | Marker |
|---|---|---|---|---|---|
| **Krankenhaus** | § 301 Abs. 3 SGB V | Zugelassene Krankenhäuser (§ 108 SGB V) | AUFN, KOUB, VERL, ANFM, MBEG, ENTL, RECH, ZAHL, AMBO, ZAAO, SAMU, FEHL, ZGUT | § 301-Vereinbarung GKV-SV ↔ DKG, Anlagen 1–5 | ⚠️ [Q30][Q5] |
| **Reha** | § 301 Abs. 4, 4a SGB V | Rehabilitationseinrichtungen | ⚠️ analog § 301 | TA 1 Reha (14.03.2024) | ⚠️ [Q29] |
| **Sonstige Leistungserbringer** | § 302 SGB V | Heilmittel, Hilfsmittel, häusliche Krankenpflege, Haushaltshilfe, Krankentransport, DiGA | SLGA, SLLA | Richtlinien § 302 Abs. 2 + Technische Anlagen 1–6 | ⚠️ [Q1][Q2] |
| **Hebammen** | § 301a SGB V | Hebammen / Entbindungspfleger | ⚠️ analog § 302 | Richtlinien nach § 302 Abs. 2 SGB V | ⚠️ [Q1] |
| **Apotheken** | § 300 SGB V | Apotheken und weitere Stellen (i. d. R. über Apothekenrechenzentren) | ⚠️ satzartenbasiert | Arzneimittelabrechnungsvereinbarung § 300 Abs. 3 + TA 1–7 | ⚠️ [Q6][Q35] |
| **Direktabrechner (Selektivverträge)** | § 295 Abs. 1b SGB V | Vertragspartner nach §§ 64d, 73b, 132e, 132f, 140a SGB V | ⚠️ | Technische Anlage V10.0 (02.04.2025) | ✅ [Q23] |
| **Vertragsärzte** | § 295 SGB V | Ärzte über die KVen | KVDT/ADT (nicht GKV-DTA im engeren Sinn) | KBV-Regelwerk | ⚠️ |
| **Zahnärzte** | § 295 SGB V | Vertragszahnärzte | ⚠️ | TA Zahnärzte + Anhang 1 zur TA TP2 V3.7 (19.09.2025); EBZ | ⚠️ [Q28] |
| **Pflege** | § 105 SGB XI | Pflegeeinrichtungen, Pflegedienste | PLGA, PLAA (Version 6) | TA 1 Version 6.4.0, gültig ab 01.05.2026; Nachfolger 6.5.1 ab 01.02.2027 | ✅ [Q22][Q22a] |
| **Hybrid-DRG** | § 115f SGB V | Krankenhäuser / Vertragsärzte | ⚠️ | TA Hybrid-DRG V1.2 (12.08.2025) | ✅ [Q33] |
| **Klinische Krebsregister** | — | Klinische Krebsregister | ⚠️ | TA V1.6 (15.03.2024) | ✅ [Q34] |
| **Anschlussrehabilitation** | — | Krankenhäuser / Reha | ⚠️ | TA 1.1 (15.05.2024) | ⚠️ |
| **GKV-SV ↔ MD** | — | Medizinischer Dienst | ⚠️ | Anlage 2 Anhang 1, V2.10 (29.09.2025) | ⚠️ |
| **Arbeitgeber / Zahlstellen** | §§ 28a ff. SGB IV, DEÜV | Arbeitgeber, Zahlstellen | eXTra-XML-Meldungen | Gemeinsame Grundsätze DEÜV / Beitragsnachweis | ⚠️ [Q19][Q26] |

## Was allen Verfahren gemeinsam ist

Diese Gemeinsamkeiten sind der **Kern eines wiederverwendbaren Validator-Frameworks**:

1. **Identifikation über Institutionskennzeichen (IK)** — Absender, Empfänger, Kostenträger,
   Leistungserbringer. Einheitliche Struktur und Prüfziffer.
   → [40-stammdaten/01-institutionskennzeichen.md](../40-stammdaten/01-institutionskennzeichen.md)
2. **Dateipärchen aus Nutzdaten- und Auftragsdatei (KKS)** mit einheitlicher
   Namenskonvention und Verfahrenskennung.
   → [30-technik/02-kks-auftragsdatei-dateinamen.md](../30-technik/02-kks-auftragsdatei-dateinamen.md)
3. **Signatur und Verschlüsselung nach Anlage 16 GGT (SECON)** auf PKCS#7/CMS-Basis.
   → [30-technik/05-security-secon.md](../30-technik/05-security-secon.md)
4. **EDIFACT-nahe Satz-/Segmentsyntax** mit UNA/UNB/…/UNZ-Rahmen (in den §§ 300/301/302-Verfahren).
   → [30-technik/03-edifact-syntax-und-zeichensatz.md](../30-technik/03-edifact-syntax-und-zeichensatz.md)
5. **Routing über Kostenträgerdateien** (amtliches Verzeichnis der Daten- und Belegannahmestellen).
   → [40-stammdaten/03-kostentraegerdateien-und-annahmestellen.md](../40-stammdaten/03-kostentraegerdateien-und-annahmestellen.md)
6. **Versionierte Technische Anlagen mit Stichtag und Übergangsfrist** — der Validator muss
   **mehrere Regelwerksversionen parallel** halten und nach Leistungs-/Abrechnungsdatum auswählen.
7. **Rückmeldekanal mit Fehler-/Absetzungsnachrichten** und ein Korrekturverfahren mit
   Bezug auf die Ursprungsrechnung.

## Was sich unterscheidet

| Dimension | Spannweite |
|---|---|
| Nachrichtenformat | EDIFACT-nahe Segmente (§§ 301/302) ↔ satzartenbasierte Formate (§ 300) ↔ XML (Arbeitgeber, teils Reha) |
| Schlüsselverzeichnisse | § 301 Anlage 2 (Krankenhausschlüssel) ↔ § 302 Anlage 3 ↔ Hilfsmittelverzeichnis ↔ PZN |
| Versionierung | § 301: fortlaufende Anlagen-Versionsnummern ↔ § 302: Anlagenversion + Stichtag ↔ § 105 SGB XI: SemVer-ähnlich (6.4.0) |
| Zwischenschaltung | Apotheken praktisch immer über Rechenzentrum; § 302 optional |

## Priorisierungsempfehlung für den DTA-Validator

| Prio | Verfahren | Begründung |
|---|---|---|
| 1 | **§ 302 (Sonstige Leistungserbringer)** | Größte Zahl kleiner Marktteilnehmer, höchster Fehler- und Absetzungsdruck, Repo-Namensgebung legt diesen Fokus nahe |
| 2 | **§ 105 SGB XI (Pflege)** | Fachlich und technisch eng verwandt (PLGA/PLAA ↔ SLGA/SLLA), hohe Wiederverwendung — und als einziges Sektorverfahren mit **vollständig ausgewerteter** Technischer Anlage ✅ [Q22][Q22g] |
| 3 | **Transport-/Security-Layer (KKS + SECON)** | Verfahrensübergreifend, einmal gebaut für alle nutzbar |
| 4 | **§ 301 (Krankenhaus)** | Größte fachliche Tiefe, aber etablierte Marktlösungen |
| 5 | **§ 300 (Apotheken)** | Stark durch Rechenzentren abgedeckt, geringerer Bedarf an Einzelplatz-Validierung |
