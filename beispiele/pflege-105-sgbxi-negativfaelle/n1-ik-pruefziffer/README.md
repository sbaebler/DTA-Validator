# N1 — falsche IK-Prüfziffer

Identisch mit [`pflege-105-sgbxi/TPFL0001`](../../pflege-105-sgbxi/TPFL0001) und
`.AUF`, bis auf **eine** Ziffer: Das Institutionskennzeichen der Datenannahmestelle
`661100423` wird zu `661100424`.

## Warum genau diese Stelle

`661100423` = Klassifikation `66`, Kern (Stellen 3–8) `110042`, Prüfziffer (Stelle 9)
`3` — siehe [`pflege-105-sgbxi/README.md`](../../pflege-105-sgbxi/README.md#8-prüfziffern--nachrechnen).
Die Prüfziffer wird **nur** über die Stellen 3–8 berechnet; ändert man ausschließlich
Stelle 9, bleibt der Kern unangetastet und **nur** die Prüfziffer wird falsch. Damit
ist der Fehler auf `S4-ALL-001` isoliert, ohne beiläufig eine Kreuzprüfung (`S5-…`)
mitzureißen — die Datenannahmestelle taucht in den Nutzdaten nur einmal auf (`UNB`-
Empfänger) und im Auftragssatz zweimal (`EMPFAENGER_NUTZER`, `EMPFAENGER_PHYSIKALISCH`),
beide Vorkommen wurden konsistent geändert.

## Diff

| Datei | Vorher | Nachher |
|---|---|---|
| `TPFL0001` (`UNB`-Empfänger) | `661100423` | `661100424` |
| `TPFL0001.AUF` (`EMPFAENGER_NUTZER`) | `661100423` | `661100424` |
| `TPFL0001.AUF` (`EMPFAENGER_PHYSIKALISCH`) | `661100423` | `661100424` |

Beide Dateien bleiben byte-identisch in der Länge (4924 / 348 Byte).

## Erwarteter Befund

`S4-ALL-001` — IK-Prüfziffer ungültig für `661100424` (Kern `110042`, erwartete
Prüfziffer `3`, vorhanden `4`). Eine korrekte Implementierung muss diesen Fund und
**nur** diesen melden.
