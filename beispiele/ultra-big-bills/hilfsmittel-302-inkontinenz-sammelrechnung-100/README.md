# Konstellation: Sammelrechnung über 100 Abrechnungsfälle mit Leistungsnachweisen

Teilmenge des [45.000er-Beispiels](../hilfsmittel-302-inkontinenz-45000/): die **ersten 50 / 30 / 20
Abrechnungsfälle** der drei Kostenträger (zusammen **100 Fälle, 500 Positionen**), eingereicht über
eine **Abrechnungsstelle mit Inkassovollmacht** (Rechnungsart `3`). KVNR, Belegnummern, Positionen
und Beträge sind identisch zum Original (`INV`-Belegnummern `0000001`–`0000050`, `0004001`–`0004030`,
`0007001`–`0007020`) und eignen sich damit für Abgleichtests zwischen den beiden Dateien.

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
> - **Leistungsnachweise und Begleitzettel sind Skizzen.** Anlage 5 (Inhalt der Urbelege) und
>   Anlage 4 (Begleitzettel) zu § 302 liegen nicht vor; Inhalt und Layout sind erfunden.

## Dateien

| Datei | Inhalt |
|---|---|
| `TSOL0002` / `TSOL0002.AUF` | Nutzdaten (9 Nachrichten, 953 Segmente, 27.773 Byte) und Auftragssatz (348 Byte, Absender = Abrechnungsstelle `661233445`, Transfernummer `002`) |
| `leistungsnachweise.html` / `.pdf` | **100 Leistungsnachweise** (Lieferschein mit Empfangsbestätigung), eine A4-Seite je Fall, Reihenfolge wie in der Datei; Unterschriftsfelder bewusst leer |
| `begleitzettel.html` / `.pdf` | 3 Begleitzettel, einer je Kostenträger-Sammelrechnung |
| `beispiel-kennzahlen.yaml` | Erwartungswerte und SHA-256 |
| `generate.py` | Erzeugt alles aus dem Original-Generator; `--pdf` benötigt Chromium |

## Aufbau

Je Kostenträger drei Nachrichten: Sammel-`SLGA` (`FKT`: `J`), `SLGA` (mit `UST`), `SLLA`.

| Sammelrechnung | IK Kostenträger | Fälle | Positionen | Brutto EUR | Zuzahlung EUR |
|---|---|---:|---:|---:|---:|
| `2026100190:0` | `109524616` | 50 | 250 | 8.629,20 | 434,12 |
| `2026100290:0` | `105312075` | 30 | 150 | 5.317,40 | 225,63 |
| `2026100390:0` | `108433180` | 20 | 100 | 3.403,60 | 176,81 |
| **Summe** | | **100** | **500** | **17.350,20** | **836,56** |

Leistungserbringer-IK `591120416`, Abrechnungsstelle `661233445`, Datenannahme `661100423`.
Alle Daten sind synthetisch (REQ-DSGVO-03).

## Neu erzeugen

```bash
python3 beispiele/ultra-big-bills/hilfsmittel-302-inkontinenz-sammelrechnung-100/generate.py --pdf
```
