# N3 — Summenabweichung GES / IAF

Identisch mit dem Positivfall bis auf eine Ziffer im `GES`-Segment der PLGA-Nachricht.

## Diff

| Vorher | Nachher |
|---|---|
| `GES+1671,00+++1671,00'` | `GES+1671,00+++1691,00'` |

`GES` trägt vier Beträge: Summe Gesamtbrutto, Summe Zuzahlungen (leer), Summe
Beihilfe (leer), Gesamtrechnungsbetrag. Nur der **letzte** Wert — der
Gesamtrechnungsbetrag — wird verändert; die Summe Gesamtbrutto (erster Wert) bleibt
korrekt bei `1671,00`. Der tatsächliche Rechnungsbetrag ergibt sich unverändert aus
den beiden `IAF`-Segmenten der PLAA: `635,60 + 1035,40 = 1671,00`.

## Erwarteter Befund

`S5-XI-003` — `PLGA.GES.Gesamtrechnungsbetrag` (`1691,00`) ≠ Summe der
`PLAA.IAF.Rechnungsbeträge` (`1671,00`). Die Datei bleibt syntaktisch vollständig
korrekt (Prüfstufe 3) und alle IK-Prüfziffern gültig (Prüfstufe 4) — der Fehler ist
ausschließlich in Prüfstufe 5 sichtbar, als Beleg dafür, dass eine Implementierung
tatsächlich nachrechnet und nicht nur auf Formgültigkeit prüft.
