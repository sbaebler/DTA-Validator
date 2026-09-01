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

Vollständig aus der Portalseite „Technische Standards" übernommen (Abruf 01.09.2026). ✅ [Q12]
Damit ist ❓-05 (Titel der Anlagen 3, 10, 11, 12, 15, 18, 19) geschlossen.

| Anlage | Titel | Bekannte Fassung | Marker |
|---|---|---|---|
| **1** | Krankenkassenkommunikationssystem (KKS) | gültig ab 01.01.2020, Stand 23.10.2019, 4 Seiten | ✅ [Q14] |
| **2** | **Auftragsdatei (Auftragssatz)** | Auftragssatz-Version 1.0, gültig ab **01.01.2025**, Stand 10.10.2024, 15 Seiten — **ausgewertet** | ✅ [Q7] |
| **3** | Einheitliches XML-basiertes Transportverfahren (**eXTra**) | — | ✅ [Q12] |
| **4** | **Verfahrenskennungen** | Feldbeschreibung 1.1, gültig ab **01.01.2026**, Stand 06.11.2025, 47 Seiten — **ausgewertet** | ✅ [Q20] |
| **5** | Datenaustausch mit der Rentenversicherung | gültig ab 01.01.2025, Stand 06.08.2024, 13 Seiten | ✅ [Q31] |
| **6** | Besonderheiten des GKV-internen Datenaustauschs und des Datenaustauschs der GKV mit Leistungserbringern | — | ✅ [Q32] |
| **7** | Electronic Mail (E-Mail) | gültig ab 01.07.2016, Stand 23.06.2016 | ✅ [Q16] |
| **8** | Hypertext Transfer Protocol (http / https) | — | ✅ [Q12] |
| **9** | File-Transfer-Protocol (ftp / sftp / ftps) | — | ✅ [Q12] |
| **10** | File Transfer, Access and Management (**FTAM**) over IP | — | ✅ [Q12] |
| **11** | *auf der Portalseite nicht geführt* | — | ❓ |
| **12** | XML-Richtlinie (+ Anhang XSV-Basis-Schemata, ZIP) | — | ✅ [Q12] |
| **13** | GKV-Kommunikationsserver (KomServer) (+ Anhang Schemadaten, ZIP) | — | ✅ [Q17] |
| **14** | Datenträger | — | ✅ [Q21] |
| **15** | **Zeichensätze** | — | ✅ [Q12] |
| **16** | **Security-Schnittstelle (SECON)** (+ Anlage 1 Eigenerklärung) | gültig ab **01.01.2026**, Stand 02.09.2025, 94 Seiten | ✅ [Q8] |
| **17** | KomServer RV (Deutsche Rentenversicherung) | — | ✅ [Q17b] |
| **18** | Begriffs- und Abkürzungsverzeichnis | — | ✅ [Q12] |
| **19** | DiGA-Schnittstelle | — | ✅ [Q12] |
| **20** | Kommunikation im Medizinwesen (**KIM / KOM-LE**) | gültig ab 01.01.2023, Stand 17.11.2022, 4 Seiten | ✅ [Q18] |
| **21** | **Synchroner Dialog** | — | ✅ [Q12] |
| Zusatz | Best Practice zur Security-Schnittstelle | — | ✅ [Q27] |
| Zusatz | Änderungshistorie zu den GGT | — | ✅ [Q12] |

> **Anlage 11** wird auf der Portalseite nicht (mehr) geführt. Ob die Nummer entfallen ist
> oder das Dokument nur nicht öffentlich steht, ist offen. ❓
>
> **Anlage 21** war in der bisherigen Erfassung gar nicht enthalten — die Anlagenreihe endet
> nicht bei 20. Eine Regelwerks-Registry darf die Obergrenze also nicht hart kodieren.

**Für den Validator neu relevant:** **Anlage 15 (Zeichensätze)** ist das bislang fehlende
Bindeglied zu ❓-08 — die Zeichensatzkennungen `I1`/`I5`/`I7`/`I8`/`P8`/`U8` aus dem
Auftragssatz werden dort normativ beschrieben. **Anlage 12 (XML-Richtlinie)** und
**Anlage 3 (eXTra)** werden mit der von § 95 SGB IV angekündigten XML-Umstellung wichtiger.

## 3. Die für den Validator relevanten Anlagen

| Anlage | Warum relevant |
|---|---|
| **1 (KKS)** | Definiert das Dateipärchen-Prinzip — Grundlage jeder Übertragung |
| **2 (Auftragsdatei)** | Feldstruktur des Auftragssatzes → erste Prüfstufe des Validators |
| **4 (Verfahrenskennungen)** | Werteliste für Dateiname und Auftragssatz-Feld `VERFAHREN_KENNUNG` |
| **15 (Zeichensätze)** | Normative Beschreibung der Kennungen `I1`/`I5`/`I7`/`I8`/`P8`/`U8` aus dem Auftragssatz |
| **16 (SECON)** | Signatur-/Verschlüsselungsprüfung, Zertifikatsvalidierung |
| **6** | Besonderheiten speziell für den LE-Datenaustausch |
| **7/8/9/13/14/20** | Transportwegspezifische Zusatzregeln (z. B. "eine Nutzdatendatei pro E-Mail") |

## 4. Verhältnis GGT ↔ sektorspezifische Technische Anlagen

```
           ┌──────────────────────────────────────────────┐
           │  Gemeinsame Grundsätze Technik (§ 95 SGB IV) │
           │  Anlagen 1–21: Transport, Auftragsdatei,     │
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
