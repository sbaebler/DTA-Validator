# Gemeinsame Grundsätze Technik (GGT) und ihre Anlagen

## 1. Was die GGT sind

Die **Gemeinsamen Grundsätze Technik nach § 95 SGB IV** sind das verfahrensübergreifende
technische Regelwerk für den Datenaustausch zur und innerhalb der Sozialversicherung. ✅ [Q11]

- Vereinbart von GKV-Spitzenverband, DRV Bund, DRV Knappschaft-Bahn-See,
  Bundesagentur für Arbeit und DGUV ⚠️ [Q11]
- Genehmigungspflichtig durch das **BMAS** im Benehmen mit dem **BMG**; bei
  Arbeitgebermeldeverfahren nach Anhörung der **BDA** ⚠️ [Q11]
- Veröffentlicht auf <https://www.gkv-datenaustausch.de> ✅ [Q12]
- Aktuelle Fassung: **gültig ab 01.09.2026** ⚠️ [Q12]

Regelungsgegenstände laut § 95 SGB IV: Verschlüsselung der Daten, Übertragungstechniken,
Kennzeichnung für die Weiterleitung von Nachrichten über ein Stichtagsdatum, die jeweiligen
Schnittstellen sowie die Zeitpunkte der Umstellung einzelner technischer Verfahren auf
XML-basierte Verfahren. ⚠️ [Q11]

## 2. Anlagenverzeichnis

Belegte Anlagen (Nummern und Titel aus Dokument-URLs/Metadaten ✅, Inhalte ⚠️):

| Anlage | Titel | Bekannte Fassung | Marker |
|---|---|---|---|
| **1** | Krankenkassenkommunikationssystem (KKS) | gültig ab 01.01.2020, Stand 23.10.2019, 4 Seiten | ✅ [Q14] |
| **2** | Auftragsdatei (Auftragssatz) | — | ✅ [Q7] |
| **3** | ❓ nicht belegt | — | ❓ |
| **4** | **Verfahrenskennungen** | gültig ab **01.01.2026**, Stand 06.11.2025, 47 Seiten | ✅ [Q20] |
| **5** | Datenaustausch mit der Rentenversicherung | gültig ab 01.01.2025, Stand 06.08.2024, 13 Seiten | ✅ [Q31] |
| **6** | Besonderheiten des GKV-internen Datenaustauschs und des Datenaustauschs der GKV mit Leistungserbringern | — | ✅ [Q32] |
| **7** | E-Mail | gültig ab 01.07.2016, Stand 23.06.2016, 17 Seiten | ✅ [Q16] |
| **8** | HTTP / HTTPS | — | ⚠️ [Q12] |
| **9** | File Transfer Protocol (FTP / SFTP / FTPS) | — | ⚠️ [Q12] |
| **10–12** | ❓ nicht belegt | — | ❓ |
| **13** | GKV-Kommunikationsserver | — | ✅ [Q17] |
| **14** | Datenträger | — | ✅ [Q21] |
| **15** | ❓ nicht belegt | — | ❓ |
| **16** | **Security-Schnittstelle (SECON)** | gültig ab **01.01.2026**, Stand 02.09.2025, 94 Seiten | ✅ [Q8] |
| **17** | Kommunikationsserver der Deutschen Rentenversicherung | — | ✅ [Q17b] |
| **18–19** | ❓ nicht belegt | — | ❓ |
| **20** | KIM (KOM-LE) innerhalb der Telematikinfrastruktur | gültig ab 01.01.2023, Stand 17.11.2022, 4 Seiten | ✅ [Q18] |
| Zusatz | Best Practice zur Security-Schnittstelle | — | ✅ [Q27] |

> ❓ **Lücken schließen:** Die Anlagen 3, 10, 11, 12, 15, 18 und 19 konnten nicht belegt
> werden. Vollständige Liste über die Portalseite "Technische Standards" [Q12] beziehen
> und [`../data/dokumentenregister.yaml`](../data/dokumentenregister.yaml) nachführen.

## 3. Die für den Validator relevanten Anlagen

| Anlage | Warum relevant |
|---|---|
| **1 (KKS)** | Definiert das Dateipärchen-Prinzip — Grundlage jeder Übertragung |
| **2 (Auftragsdatei)** | Feldstruktur des Auftragssatzes → erste Prüfstufe des Validators |
| **4 (Verfahrenskennungen)** | Werteliste für Dateiname und Auftragssatz-Feld `VERFAHREN_KENNUNG` |
| **16 (SECON)** | Signatur-/Verschlüsselungsprüfung, Zertifikatsvalidierung |
| **6** | Besonderheiten speziell für den LE-Datenaustausch |
| **7/8/9/13/14/20** | Transportwegspezifische Zusatzregeln (z. B. "eine Nutzdatendatei pro E-Mail") |

## 4. Verhältnis GGT ↔ sektorspezifische Technische Anlagen

```
           ┌──────────────────────────────────────────────┐
           │  Gemeinsame Grundsätze Technik (§ 95 SGB IV) │
           │  Anlagen 1–20: Transport, Auftragsdatei,     │
           │  Verfahrenskennungen, Security               │
           └──────────────────┬───────────────────────────┘
                              │ gelten für alle Verfahren
        ┌─────────────────────┼─────────────────────┬──────────────┐
        ▼                     ▼                     ▼              ▼
 § 301-Vereinbarung    Richtlinien § 302     § 300 TA 1–7    § 105 SGB XI TA 1
 Anlagen 1–5           Anlagen 1–6                            Anhänge 1–3
 (Krankenhaus)         (Sonstige LE)         (Apotheken)      (Pflege)
        │                     │                     │              │
        └─────────────────────┴─────────────────────┴──────────────┘
                    fachliche Nutzdaten-Struktur je Sektor
```

**Konsequenz für die Architektur:** Der Validator sollte zwei klar getrennte Schichten haben —
einen **verfahrensübergreifenden Envelope-/Transport-Validator** (GGT) und
**verfahrensspezifische Nutzdaten-Validatoren** (Sektor-TAs).
