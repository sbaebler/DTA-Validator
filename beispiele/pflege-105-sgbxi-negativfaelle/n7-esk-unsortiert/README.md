# N7 — ESK unsortiert

Identisch mit dem Positivfall, aber die beiden ersten `ESK`/`ELS`-Blöcke des ersten
Abrechnungsfalls (Tag `01` und Tag `02`) sind vertauscht.

## Diff

| Vorher | Nachher |
|---|---|
| `MAN+202607+++3'ESK+01+0715'ELS+…'ESK+02+0715'ELS+…'ESK+03+…` | `MAN+202607+++3'ESK+02+0715'ELS+…'ESK+01+0715'ELS+…'ESK+03+…` |

Die Reihenfolge ist jetzt `02, 01, 03, 06, 07, …` — an genau einer Stelle nicht mehr
aufsteigend. Weil beide vertauschten `ELS`-Segmente inhaltlich identisch sind (gleiche
Leistungsziffer, gleicher Preis), bleiben `GES`, alle `IAF`-Summen und die Anzahl der
`ELS`-Segmente je Leistungsziffer unverändert — der Fehler ist auf die Reihenfolge
beschränkt und zieht keine Summenabweichung nach sich.

## Erwarteter Befund

`S3-XI-006` — `ESK`-Segmente sind je Abrechnungsfall nicht aufsteigend nach
Kennzeichen der Leistungserbringung sortiert (TA 1 Abschnitt 4.4.2). Ein Validator,
der `ESK`-Kennzeichen nur als Menge statt als geordnete Folge behandelt, übersieht
diesen Fehler — er ist ein guter Test dafür, ob die Sortierprüfung tatsächlich
paarweise Nachbarn vergleicht und nicht nur auf Vollständigkeit der Tagesmenge
prüft.
