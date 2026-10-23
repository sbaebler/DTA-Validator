# Beispiel: § 302 SGB V — Inkontinenzhilfsmittel, 45.000 Positionen

Synthetischer Last- und Volumentest: **eine Monatsabrechnung eines Homecare-Versorgers mit
45.000 Hilfsmittelpositionen** (9.000 Versorgte × 5 Positionen, Leistungsmonat 09/2026),
verteilt auf drei Kostenträger. Gedacht für Performance-, Speicher- und Regeltests.

> ## Wie belastbar ist dieses Beispiel?
>
> **Nur der Transportrahmen ist belegt**, die Fachsegmente sind es nicht.
>
> | Teil | Stand |
> |---|---|
> | Auftragssatz `TSOL0001.AUF` (348 Byte, 37 Felder) | belegt — Anlage 2 GGT; Verfahrenskennung `TSOL0` = Test + `SOL` (Sonstige Leistungserbringer) + Version 0, Anlage 4 GGT |
> | UNB/UNH/UNT/UNZ-Rahmen, Zeichensatz, Trennzeichen | **übernommen vom § 105-Beispiel**, für § 302 nicht gegen die TA geprüft |
> | Nachrichtentypen `SLGA` / `SLLA` | belegt als Namen (siehe `nachrichtentypen.yaml`); **Versionsnummer `:1` ist geraten** |
> | Segmente `FKT REC UST GES NAM` der SLGA | als Namen sekundär belegt, **Feldbelegung geraten** |
> | Segmente `INV NAD ESK EHE IAF` der SLLA | **Skizze.** Die Technische Anlage 1 zu § 302 liegt nicht vor; `EHE` und `IAF` sind hier als Hilfsmittelposition bzw. Fallende *angenommen* |
> | Hilfsmittelpositionsnummern | **erfunden.** Produktgruppe `15` (Inkontinenz) stimmt, alles danach nicht; ~2 % tragen die Ersatzform `<Produktart>900` |
> | KVNR-Prüfziffer | Algorithmus ist eine **Annahme** (KB: ❓ Lücke), reproduziert aber die KVNR des Pflege-Beispiels |
> | Zuzahlung | 10 % je Fall, max. 10 €; 18 % der Fälle befreit — fachlich plausibel, nicht aus einer Regelung abgeleitet |
>
> Als Positivfall für **§ 302-Regeln ist die Datei deshalb noch nicht geeignet**. Sie taugt für
> Transport-, Auftragssatz-, Zähler-, Summen- und Skalierungstests. Sobald die TA vorliegt, ist
> nur `erzeuge()` in `generate.py` anzupassen.

## Dateien

| Datei | Inhalt |
|---|---|
| `TSOL0001` | Nutzdaten, EDIFACT, ISO 8859-1, **ohne Zeilenumbrüche** (wie im Echtbetrieb), 2,36 MB, 81.035 Segmente |
| `TSOL0001.AUF` | Auftragssatz, 348 Byte; `DATEIGROESSE_NUTZDATEN` = `DATEIGROESSE_UEBERTRAGUNG` = 2357531 |
| `TSOL0001.zeilen.txt` | Lesefassung: **genau 45.000 Zeilen**, je Zeile eine Position (`KVNR\|Beleg\|IK KT\|Pos.-Nr.\|Kz\|Menge\|Einzelpreis\|Gesamt\|Bezeichnung`) |
| `beispiel-kennzahlen.yaml` | Erwartungswerte: Zahlen, Summen je Rechnung, SHA-256 |
| `generate.py` | Deterministischer Generator (`--positionen`, `--seed`); gleiche Parameter ergeben identische Bytes |

## Aufbau

6 Nachrichten: je Kostenträger ein Paar `SLGA` + `SLLA`.

| Rechnung | IK Kostenträger | Fälle | Positionen | Brutto EUR |
|---|---|---:|---:|---:|
| `2026100001:0` | `109524616` | 4.000 | 20.000 | 691.423,80 |
| `2026100002:0` | `105312075` | 3.000 | 15.000 | 518.823,10 |
| `2026100003:0` | `108433180` | 2.000 | 10.000 | 344.098,40 |
| **Summe** | | **9.000** | **45.000** | **1.554.345,30** |

Leistungserbringer-IK `591120416` (Klassifikation 59), Datenannahmestelle `661100423`.
Alle IK tragen eine gerechnete Prüfziffer. Je Fall: `INV NAD ESK EHE×5 IAF`.

## Datenschutz

Alle Daten sind frei erfunden (REQ-DSGVO-03). Namen stammen aus einer kleinen Liste,
Geburtsdaten und KVNR sind zufällig; eine Übereinstimmung mit realen Personen ist nicht
ausschließbar und ohne Bedeutung.

## Neu erzeugen

```bash
python3 beispiele/ultra-big-bills/hilfsmittel-302-inkontinenz-45000/generate.py            # 45.000 Positionen
python3 beispiele/ultra-big-bills/hilfsmittel-302-inkontinenz-45000/generate.py --positionen 10000 --seed 7
```

Die Positionszahl muss ein Vielfaches von 5 sein.
