# Konstellation: Umlaute und Freigabezeichen — `TPFL0004` / `TPFL0004.AUF`

Derselbe Fall wie im Positivfall [`pflege-105-sgbxi/`](../pflege-105-sgbxi/), aber mit
zwei Versichertennamen, die deutsche Sonderzeichen und einen Fall des
**Freigabezeichens** `?` auslösen — dem einzigen Zeichen in § 105 SGB XI, das ein
Trennzeichen im Datenstrom selbst maskieren muss.

> ## Wie belastbar ist dieses Beispiel?
>
> **Der Apostroph-Fall ist wörtlich aus der Primärquelle übernommen.** Die TA 1
> (Pflege) nennt in Abschnitt 4.1 als Beispiel ausdrücklich „Luigi D'Angelo wird als
> `D?'Angelo+Luigi+` übermittelt" — siehe
> [`knowledge-base/30-technik/03-edifact-syntax-und-zeichensatz.md`](../../knowledge-base/30-technik/03-edifact-syntax-und-zeichensatz.md).
> Dieses Beispiel baut genau diesen Fall in ein vollständiges, sonst unverändertes
> Dateipärchen ein. **Nicht primärquellen-belegt** ist dagegen, dass Umlaute (`ü`,
> `ö`, `ß`) in Namens- und Adressfeldern zulässig sind — das folgt hier nur aus der
> allgemeinen Zeichensatzfestlegung (ISO 8859-1 lässt sie zu) und aus **Anlage 15
   GGT (Zeichensätze)**, die laut Wissensbibliothek „noch nicht ausgewertet" ist ❓.
> Ob ein Kostenträgersystem Umlaute in der Praxis tatsächlich akzeptiert oder auf den
> 7-Bit-Zeichenvorrat transliteriert, ist damit offen.

## 1. Was geändert wurde

Beide Abrechnungsfälle sind inhaltlich identisch mit dem Positivfall — gleiche KVNR,
gleicher Pflegegrad, gleiche Leistungen, gleiche Beträge. Geändert sind ausschließlich
die `NAD`-Segmente:

| Abrechnungsfall | Positivfall | Diese Konstellation |
|---|---|---|
| `2607001` | `NAD+Kerzenmacher+Hanna+19480312+Rosenweg+3+12345+Musterstadt'` | `NAD+Grünberg+Björn+19480312+Kirchstraße+3+12345+Musterstadt'` |
| `2607002` | `NAD+Brinkmeier+Otto+19391127'` | `NAD+D?'Angelo+Luigi+19391127'` |

Fall `2607001` deckt `ü`, `ö` und `ß` in Nachname, Vorname und Straße ab — drei
Zeichen außerhalb des 7-Bit-ASCII-Bereichs in einem einzigen Segment. Fall `2607002`
ist das TA-1-eigene Beispiel für das **Freigabezeichen**: Der Apostroph in
"D'Angelo" ist selbst kein Trennzeichen, muss aber vom Segmentendezeichen `'`
unterschieden werden — dafür steht ihm das Zeichen `?` unmittelbar voran. Ohne diese
Maskierung würde ein Parser das Segment fälschlich nach `D` beenden.

Alles Übrige — `UNB` (bis auf Anwendungsreferenz und Erstellungszeit, siehe unten),
`FKT`, `REC`, `SRD`, `UST`, `GES`, `NAM`, `MAN`, `ESK`, `ELS`, `IAF`, `UNT`, `UNZ` —
ist byte-identisch mit dem Positivfall.

## 2. Warum ein neuer Dateiname

`UNB`-Anwendungsreferenz und Auftragssatz-`DATEINAME` wurden von `PL076001SBK` auf
`PL076002SBK` geändert (laufende Nummer je Kalenderjahr und Datenannahme `01` → `02`)
— zwei Dateien desselben Abrechnungszeitraums mit identischem logischem Dateinamen
wären selbst ein Fehler (`S5-ALL-002`). Erstellungsdatum/-zeit wurden auf den
06.08.2026, 12:00 Uhr gesetzt, einen Tag nach dem Positivfall, um die Dateien
unterscheidbar zu halten.

## 3. Warum das Dezimalzeichen davon unberührt bleibt

Dieses Beispiel testet eine andere Achse der Zeichensatzfrage als
[`pflege-105-sgbxi-negativfaelle/n6-dezimalpunkt/`](../pflege-105-sgbxi-negativfaelle/n6-dezimalpunkt/):
dort geht es um das **Dezimaltrennzeichen** in Zahlen, hier um **Buchstaben** in
Freitextfeldern. Beide Achsen sind in TA 1 Abschnitt 4.1 geregelt, aber unabhängig
voneinander — ein Parser kann das eine richtig und das andere falsch behandeln.

## 4. Erwartetes Verhalten einer Implementierung

- **Kein Befund.** Dieses Beispiel ist ein Positivfall: Umlaute in ISO 8859-1 und ein
  korrekt maskierter Apostroph sind spezifikationskonform. Eine Implementierung, die
  hier einen Fehler meldet, behandelt den Zeichensatz zu eng (z. B. reines ASCII
  erwartet) oder das Freigabezeichen falsch.
- **Die Falle:** Ein Parser, der Trennzeichen per Regex ohne Berücksichtigung des
  Freigabezeichens sucht (`split("'")` ohne Escape-Behandlung), zerlegt
  `NAD+D?'Angelo+Luigi+19391127'` an der falschen Stelle — mitten im Namen statt am
  echten Segmentende. Das Ergebnis sind zwei kaputte Segmente statt eines gültigen,
  ohne dass ein offensichtlicher Absturz die Implementierung warnt.
- **Byte- vs. zeichenweise Länge:** In ISO 8859-1 ist jedes der Zeichen `ü`, `ö`,
  `ß` genau **ein** Byte — anders als in UTF-8, wo sie zwei Byte belegen. Eine
  Implementierung, die die Datei versehentlich als UTF-8 einliest (statt den in
  `ZEICHENSATZ` deklarierten Wert `I1` zu nutzen), verschiebt ab der ersten
  Mehrbyte-Fehlinterpretation alle nachfolgenden Feldgrenzen.

## 5. Dateien

| Datei | Inhalt | Größe |
|---|---|---|
| [`TPFL0004`](TPFL0004) | Nutzdaten, ISO 8859-1, 163 Segmente | 4923 Byte |
| [`TPFL0004.AUF`](TPFL0004.AUF) | Auftragsdatei, Festsatzformat | 348 Byte |

Keine Urbelege — sie wären bis auf dieselben zwei Namen identisch mit denen des
Positivfalls und sind für die hier geprüfte Frage (Zeichensatz und Freigabezeichen im
EDIFACT-Strom) nicht zusätzlich aussagekräftig.
