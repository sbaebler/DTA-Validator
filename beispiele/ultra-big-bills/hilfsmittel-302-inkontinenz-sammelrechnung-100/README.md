# Konstellation: Sammelrechnung über 100 Abrechnungsfälle mit Leistungsnachweisen

Teilmenge des [45.000er-Beispiels](../hilfsmittel-302-inkontinenz-45000/): die **ersten 50 / 30 / 20
Abrechnungsfälle** der drei Kostenträger (zusammen **100 Fälle, 500 Positionen**), eingereicht über
eine **Abrechnungsstelle mit Inkassovollmacht** (Rechnungsart `3`). KVNR, Belegnummern, Positionen
und Beträge sind identisch zum Original (`INV`-Belegnummern `0000000001`–`0000000050`, `0000004001`–`0000004030`,
`0000007001`–`0000007020`) und eignen sich damit für Abgleichtests zwischen den beiden Dateien.

> **Auslegung der Vorgabe:** „100 Positionen" und „100 Abrechnungsfälle" waren im Auftrag nicht
> deckungsgleich; umgesetzt sind **100 Abrechnungsfälle** (je 5 Positionen = 500).

> ## Wie belastbar ist dieses Beispiel?
>
> **Gering.** Es gilt alles aus dem [45.000er-Beispiel](../hilfsmittel-302-inkontinenz-45000/README.md):
> nur der Auftragssatz ist belegt. Zusätzlich:
>
> - Die **Sammelrechnungs-Verschachtelung** (Sammel-`SLGA` mit `FKT`-Kennzeichen `J` → `SLGA` → `SLLA`
>   je Kostenträger) ist aus dem § 105-Verfahren **analog übernommen** (siehe
>   [`pflege-105-sgbxi-sammelrechnung/`](../../pflege-105-sgbxi-sammelrechnung/)), für § 302 nicht belegt.
> - Die IK-Zuordnung im `FKT` bei Rechnungsart 3 ist dieselbe offene Interpretation wie dort.
> - **Begleitzettel:** Pflichtinhalt nach **Anlage 4 (V 2.0) ausgewertet und umgesetzt** (IK/Name Krankenkasse, Name/Anschrift
>   und IK von Abrechnungsstelle und Leistungserbringer, Rechnungsnummer/-datum, Anzahl Urbelege, erste/letzte Belegnummer).
>   Layout erfunden; Anlage 4 regelt kein Format.
> - **Leistungsnachweise sind eine Variante, kein Regelfall:** Laut **Anlage 5 (V 4.0)** steht die Empfangsbestätigung auf dem
>   Verordnungsblatt (Muster 16); ein eigener Lieferschein gilt nur kraft Vereinbarung. Layout erfunden.
> - Nummernformate (Sammelrechnungsnr 14, Einzelrechnungsnr 6, Belegnummer 10 Stellen) folgen der ImageLink-Spezifikation,
>   siehe [`imagelink.yaml`](../../../knowledge-base/data/imagelink.yaml). Welche Rechnungsebene die Einzelrechnungsnummer trägt,
>   ist eine Auslegung (hier: `000000` auf der Sammel-`SLGA`, `000001` auf der Gesamtrechnung).

## Dateien

| Datei | Inhalt |
|---|---|
| `TSOL0002` / `TSOL0002.AUF` | Nutzdaten (9 Nachrichten, 953 Segmente, 28.154 Byte) und Auftragssatz (348 Byte, Absender = Abrechnungsstelle `661233445`, Transfernummer `002`) |
| `leistungsnachweise.html` / `.pdf` | **100 Leistungsnachweise** (Lieferschein mit Empfangsbestätigung), eine A4-Seite je Fall, Reihenfolge wie in der Datei; Unterschriftsfelder bewusst leer |
| `begleitzettel.html` / `.pdf` | 3 Begleitzettel, je Gesamtrechnung einer (Anlage 4) |
| `beispiel-kennzahlen.yaml` | Erwartungswerte und SHA-256 |
| `generate.py` | Erzeugt alles aus dem Original-Generator; `--pdf` benötigt Chromium |

## Aufbau

Je Kostenträger drei Nachrichten: Sammel-`SLGA` (`FKT`: `J`), `SLGA` (mit `UST`), `SLLA`.

| Sammelrechnung | IK Kostenträger | Fälle | Positionen | Brutto EUR | Zuzahlung EUR |
|---|---|---:|---:|---:|---:|
| `SU202610120001:000001` | `109524616` | 50 | 250 | 8.629,20 | 434,12 |
| `SU202610120002:000001` | `105312075` | 30 | 150 | 5.317,40 | 225,63 |
| `SU202610120003:000001` | `108433180` | 20 | 100 | 3.403,60 | 176,81 |
| **Summe** | | **100** | **500** | **17.350,20** | **836,56** |

Leistungserbringer-IK `591120416`, Abrechnungsstelle `661233445`, Datenannahme `661100423`.
Alle Daten sind synthetisch (REQ-DSGVO-03).

## ImageLink-Lieferpaket (`imagelink-paket/`)

Aus den 100 Leistungsnachweisen entsteht ein Paket nach [Anhang 4a/4b](../../../knowledge-base/data/imagelink.yaml):
je Beleg ein **PDF + XML-Paar**, je Sammelrechnung **eine ZIP-Datei** (Name ohne Endung) mit **Auftragsdatei**.

| Datei | Inhalt |
|---|---|
| `D261012.T081200.T1IM0001` / `.AUF` | 50 Belege, Sammelrechnung `SU202610120001`, Transfernummer 001 |
| `D261012.T081200.T1IM0002` / `.AUF` | 30 Belege, Sammelrechnung `SU202610120002`, Transfernummer 002 |
| `D261012.T081200.T1IM0003` / `.AUF` | 20 Belege, Sammelrechnung `SU202610120003`, Transfernummer 003 |
| `zuordnung.csv` | je Beleg: ZIP, Ordner, Dokument-/Vorgangsidentifikator, Sammel-/Einzelrechnungsnr, Belegnummer, KVNR, Kostenträger-IK, Seite in `leistungsnachweise.pdf`, SHA-256 des PDF |

Aufbau im ZIP: Ordner `SUE_SU2026101200nn01/` (`<ABR 3>_<Sammelrechnungsnr 14><Zähler 2>`) mit je Beleg
`SUE_<Sammel 14><Einzel 6><Beleg 10><Zähler 01>.PDF` und `.XML` (36 Zeichen, Grenze 40). Dokumentklasse `ER_SOLE_HIMI_ON`,
Eingangskanal 2, Vorgangsumfang 001, Nutzdaten Sammel-/Einzelrechnungsnummer, Rechnungsdatum, Rechnungsart `3`, Belegnummer,
Leistungserbringer-IK, KVNR als Ordnungsbegriff `PKKVDE`. Die Zuordnung Seite → Beleg wird beim Bau über den Seitentext
(Belegnummer, KVNR) geprüft.

**Abweichungen vom Echtbetrieb (bewusst):**

- **Nicht signiert/verschlüsselt (out of scope, Entscheidung 23.10.2026):** Spezifikation verlangt PKCS#7 (`VERSCHLUESSELUNGSART` und
  `ELEKTRONISCHE_UNTERSCHRIFT` = `03`). Das Fixture führt `00` und ist **nicht einreichbar**; `KOMPRIMIERUNG` = `03` (ZIP) stimmt.
- **`Beschreibung`** fest `AOK Systems GmbH`, weil das XSD den Wert festschreibt; das Dokument nennt ihn „von annehmender Stelle zu definieren".
- **ABR-Kürzel** `SUE` (3 Stellen laut Text; das Beispiel der Spezifikation zeigt 7 Zeichen).
- **`DATEINAME`-Feld** im Auftragssatz und Empfänger-IK (`661100559`, Belegannahme) sind erfunden; die Spezifikation regelt sie nicht.
- **Dokumentklasse:** Der Nachweis ist ein Lieferschein; `ER_SOLE_HIMI_ON` erlaubt laut Anhang 4a neben der Verordnung auch weitere Belege
  (z. B. Empfangsbestätigung), das Erfordernis ist zu vereinbaren. Sammelrechnungs-Images (`SR_SOLE_HIMI_ON`) und Begleitzettel werden
  nicht ins Paket gelegt (Zusammenspiel ungeklärt).
- **`Erstellungszeitpunkt`** ist für alle Belege `2026-10-12T08:12:00Z` (synthetisch).
- ZIP und PDF sind reproduzierbar (feste Zeitstempel, normalisierte PDF-`/ID`).

**Prüfung:** `pruefe_paket.py` prüft XSD-Validität (`knowledge-base/data/schemas/`), Dateinamen, Identifikatoren, Ordner- und
Größengrenzen, Auftragssatz und den Abgleich jedes Dokuments mit dem DTA-Fall in `TSOL0002`; `test_pruefe_paket.py` baut
zehn Fehlerfälle und erwartet die richtigen Befunde.

## Neu erzeugen

```bash
python3 beispiele/ultra-big-bills/hilfsmittel-302-inkontinenz-sammelrechnung-100/generate.py --pdf     # DTA, Auftragssatz, Nachweise
python3 beispiele/ultra-big-bills/hilfsmittel-302-inkontinenz-sammelrechnung-100/build_imagelink.py     # ImageLink-Paket
python3 beispiele/ultra-big-bills/hilfsmittel-302-inkontinenz-sammelrechnung-100/pruefe_paket.py        # prüfen
```

Voraussetzungen: Python 3 mit `lxml`, poppler-utils (`pdfseparate`, `pdftotext`, `pdfinfo`), für `--pdf` Chromium.
