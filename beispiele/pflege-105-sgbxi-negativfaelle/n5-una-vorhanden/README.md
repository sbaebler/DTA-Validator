# N5 — UNA-Segment vorhanden

Identisch mit dem Positivfall, aber der Nutzdatendatei ist ein `UNA`-Segment
vorangestellt.

## Diff

| Datei | Änderung |
|---|---|
| `TPFL0001` | `UNA:+,? '` (9 Byte) vor `UNB` eingefügt — Dateigröße 4924 → **4933** Byte |
| `TPFL0001.AUF` | `DATEIGRÖSSE_NUTZDATEN` und `DATEIGRÖSSE_ÜBERTRAGUNG` von `000000004924` auf `000000004933` angepasst |

Die `.AUF`-Anpassung ist bewusst Teil dieses Negativfalls: Ohne sie würde die
Auftragsdatei zusätzlich eine falsche Dateigröße behaupten (`S1-ALL-012`) — ein
zweiter, nicht beabsichtigter Fehler. Mit der Anpassung ist die **einzige**
Abweichung vom Positivfall das Vorhandensein des `UNA`-Segments selbst.

Die im `UNA` benannten Trennzeichen (`:` Komponente, `+` Element, `,` Dezimal, `?`
Freigabe, `'` Segmentende) entsprechen exakt den ohnehin fest vorgegebenen
Trennzeichen der TA 1 — das Segment ist also inhaltlich redundant und ändert am
Parsing der übrigen Datei nichts. Es ist ein reiner Regelverstoß, kein struktureller
Bruch.

## Erwarteter Befund

`S3-XI-002` — für § 105 SGB XI ist kein `UNA`-Segment vorgesehen (TA 1 Abschnitt 4.1
Absatz 10); seine bloße Anwesenheit ist der Fehler. `S3-ALL-001` greift hier nicht:
diese Regel prüft, *falls* ein `UNA` vorhanden ist, ob es genau sechs Trennzeichen
enthält — sie ist laut `pruefregeln.yaml` für `sgbxi-105` ausdrücklich ausgenommen
(`gilt_nicht_fuer: [sgbxi-105]`), weil das Verfahren gar kein `UNA` kennt.
