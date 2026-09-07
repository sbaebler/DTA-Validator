# N4 — unvollständiges Dateipärchen

Dieses Verzeichnis enthält **nur** die Nutzdatendatei `TPFL0001`, byte-identisch mit
dem Positivfall. Die zugehörige Auftragsdatei `TPFL0001.AUF` fehlt bewusst.

## Warum das ein Fehler ist

Nach Anlage 2 GGT gehört zu jeder Nutzdatendatei außerhalb der TI eine Auftragsdatei
mit demselben Transferdateinamen (`S0-ALL-003`). Eine Implementierung, die nur
Dateien parst, die tatsächlich vorliegen, und das Fehlen der Gegenstelle nicht
bemerkt, meldet für dieses Verzeichnis fälschlich einen Positivbefund.

## Erwarteter Befund

Ein Vollständigkeits-Befund auf Dateipärchen-Ebene — die Nutzdatendatei allein ist
nicht prüfbar, weil unter anderem `ZEICHENSATZ`, `VERSCHLÜSSELUNGSART` und
`DATEIGRÖSSE_NUTZDATEN` nur im Auftragssatz stehen. Das ist zugleich eine Lücke in der
aktuellen Regelliste: [`pruefregeln.yaml`](../../../knowledge-base/data/pruefregeln.yaml)
formuliert `S0-ALL-003` als Gleichheitsprüfung der Transferdateinamen **zwischen**
Nutzdaten- und Auftragsdatei, nicht explizit als Existenzprüfung "beide Dateien
liegen vor". Dieser Negativfall macht sichtbar, dass eine solche Existenzregel noch
fehlt oder `S0-ALL-003` entsprechend zu lesen ist — je nachdem, wie eine
Implementierung das Fehlen der zweiten Datei modelliert.
