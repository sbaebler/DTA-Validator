# N2 — falscher UNT-Zähler

Identisch mit dem Positivfall bis auf eine Ziffer im `UNT`-Segment der PLAA-Nachricht.

## Diff

| Vorher | Nachher |
|---|---|
| `UNT+153+2'` | `UNT+152+2'` |

`0074` (Anzahl Einheiten) muss laut [`nachrichtentypen.yaml`](../../../knowledge-base/data/nachrichtentypen.yaml)
die Zahl der Segmente der Nachricht **einschließlich `UNH` und `UNT`** sein. Die
PLAA-Nachricht besteht tatsächlich aus 153 Segmenten (siehe Positivfall-README,
Abschnitt 5.4); der Zähler behauptet 152. Das `UNT` der PLGA (`UNT+8+1'`) bleibt
unverändert — nur der eine Zähler ist falsch.

## Erwarteter Befund

`S3-ALL-004` — Segmentzähler in `UNT` (`152`) ≠ tatsächliche Segmentanzahl der
Nachricht `2` (`153`). Alle anderen Regeln, insbesondere die Kreuzprüfungen aus
Prüfstufe 5, bleiben unberührt — der Fehler ist eine reine Zählfrage.
