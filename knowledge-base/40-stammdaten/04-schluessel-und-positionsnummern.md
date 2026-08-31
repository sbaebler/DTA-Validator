# Schlüsselverzeichnisse und Positionsnummern

## 1. Landkarte der Schlüsselwelten

| Schlüsselart | Verfahren | Quelle | Marker |
|---|---|---|---|
| **Hilfsmittelpositionsnummer** (10-stellig) | § 302 | GKV-Hilfsmittelverzeichnis | ⚠️ [Q24][Q24b] |
| **Heilmittelpositionsnummern** | § 302 | Positionsnummernverzeichnisse des GKV-SV | ⚠️ [Q24] |
| **Indikationsschlüssel** | § 302 Heilmittel | Heilmittelkatalog (G-BA, Heilmittel-Richtlinie) | ⚠️ |
| **PZN** (Pharmazentralnummer) | § 300 | IFA | ⚠️ |
| **Sonderkennzeichen** | § 300 | TA 1 Anhang 1 (national) / Anhang 2 (bilateral) | ⚠️ [Q35] |
| **Krankenhausschlüssel** (Aufnahmegrund, Entgeltarten, Entlassungsgrund …) | § 301 | § 301 Anlage 2 Schlüsselverzeichnis | ⚠️ [Q5] |
| **ICD-10-GM** | § 301, § 302 | BfArM, jahresbezogen | ⚠️ |
| **OPS** | § 301 | BfArM, jahresbezogen | ⚠️ |
| **§ 302-Schlüssel** (Verarbeitungskennzeichen, Leistungsarten …) | § 302 | § 302 Anlage 3 Schlüsselverzeichnisse | ⚠️ [Q1] |
| **Verfahrenskennungen** | alle | Anlage 4 GGT | ✅ [Q20] |

## 2. Hilfsmittelpositionsnummer

⚠️ [Q24][Q24b]

Das GKV-Hilfsmittelverzeichnis ist hierarchisch gegliedert nach
**Produktgruppe → Anwendungsort → Untergruppe → Produktart → Einzelprodukt**.

| Ebene | Stellenzahl |
|---|---|
| Produktart | **7-stellig** |
| Einzelprodukt | **10-stellig** |

- **Stellen 1–2**: Produktgruppe (welche Art von Hilfsmittel)

### Ersatzregel für nicht vergebene Einzelproduktnummern ⚠️ [Q24]

Wenn auf Bundesebene noch **keine 10-stellige Positionsnummer** vergeben wurde, die
Struktur der Produktgruppe aber bereits besteht, ist abzurechnen mit:

```
  Stellen 1–7 der Produktart  +  "9"  +  "00"
  └──────────┬──────────┘        │      └─┬─┘
             │                   │        └── Stellen 9–10: "00"
             │                   └─────────── Stelle 8: "9"
             └─────────────────────────────── Produktart
```

Ergebnis: die Nummer endet auf **`900`**.

**Prüfregel-Kandidat:** Eine 10-stellige Hilfsmittelnummer ist gültig, wenn sie
entweder im Hilfsmittelverzeichnis als Einzelprodukt existiert **oder** dem
`<7-stellige Produktart>900`-Muster folgt und die Produktart existiert.

## 3. Positionsnummernverzeichnisse (§ 302)

Der GKV-Spitzenverband veröffentlicht **aktuelle Positionsnummernverzeichnisse** für
sonstige Leistungserbringer. ⚠️ [Q24]

Portalseite:
`https://www.gkv-datenaustausch.de/leistungserbringer/sonstige_leistungserbringer/positionsnummernverzeichnisse/positionsnummernverzeichnisse.jsp`

> ❓ Format, Aktualisierungsrhythmus und Struktur der Positionsnummernverzeichnisse sind
> nicht recherchiert. Sie sind für die fachliche Prüfstufe des Validators zwingend nötig.

## 4. Versionierung und Stichtage

Alle Schlüsselverzeichnisse sind **stichtagsbezogen versioniert**. Beispiel § 302 Anlage 3:

| Version | Stand | Anzuwenden ab | Gültigkeit endet |
|---|---|---|---|
| 22 | 21.05.2026 | **01.02.2027** | — |
| 21 | ⚠️ | ⚠️ | **30.04.2027** (3 Monate Übergang) |

⚠️ [Q1]

**Architekturkonsequenz:** Der Validator darf Schlüsseltabellen nicht als statische
Konstanten führen. Er braucht ein **gültigkeitszeitraumbasiertes Modell**:

```
Schluesselwert(schluesselart, wert, gueltig_ab, gueltig_bis, verfahren, regelwerksversion)
```

Die Auswahl erfolgt nach dem **fachlich maßgeblichen Datum** — je nach Verfahren
Leistungsdatum, Abrechnungsmonat oder Datenlieferungsquartal, nicht nach dem Systemdatum.

## 5. Bezugsquellen im Überblick

| Verzeichnis | Bezug |
|---|---|
| GKV-Hilfsmittelverzeichnis | REHADAT-GKV <https://www.rehadat-gkv.de/> |
| Positionsnummernverzeichnisse § 302 | gkv-datenaustausch.de |
| § 301 Anlage 2 Schlüsselverzeichnis | gkv-datenaustausch.de |
| Heilmittelkatalog | G-BA, Heilmittel-Richtlinie |
| ICD-10-GM / OPS | BfArM |
| PZN | IFA GmbH |

> ⚠️ **Lizenzhinweis:** Vor Einbindung eines Katalogs in ein Softwareprodukt sind
> Nutzungsbedingungen und Lizenzrechte zu prüfen (insbesondere ICD-10-GM/OPS bei BfArM
> und PZN bei IFA). Das ist kein technischer, sondern ein rechtlicher Vorbehalt und
> gehört in die Projektplanung.
