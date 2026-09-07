# N6 — Dezimalpunkt statt Komma

Identisch mit dem Positivfall, aber jedes Komma, das als Dezimalzeichen in einem
Betrag steht, ist durch einen Punkt ersetzt — `24,50` → `24.50`, `1671,00` →
`1671.00` und so weiter, insgesamt 186 Stellen. Die Datei bleibt exakt 4924 Byte
groß, da jede Ersetzung ein Zeichen gegen ein Zeichen tauscht.

## Warum eine einzelne systematische Ersetzung als "ein Fehler" zählt

Die TA 1 legt das Dezimalzeichen **verfahrensweit** auf das Komma fest (Abschnitt 4.1
Absatz 10) — es ist keine Eigenschaft einzelner Felder, sondern eine
Dateieigenschaft. Ein Absender, der versehentlich die EDIFACT-Voreinstellung
(Punkt) statt der TA-1-Vorgabe (Komma) implementiert, macht diesen Fehler
systematisch, nicht an einzelnen Stellen. Der Negativfall bildet genau dieses
Fehlerbild ab: eine falsche globale Annahme, nicht 93 unabhängige Tippfehler.

Keine andere Stelle der Datei verwendet ein Komma außerhalb von Beträgen — die
Ersetzung ist deshalb strukturell folgenlos für alles andere (Leistungsziffern
nutzen `:`, das Rechnungsnummernpaar nutzt ebenfalls `:`, Daten sind `JJJJMMTT`).

## Erwarteter Befund

`S3-XI-002` — Dezimalzeichen ist nicht das vorgeschriebene Komma. Eine
Implementierung, die stattdessen den EDIFACT-Standardwert (Punkt) unterstellt oder
ein `UNA:+.? '` annimmt, liest diese Datei **fehlerfrei, aber falsch**: Beträge wie
`24.50` erscheinen ihr gültig, obwohl sie nach TA 1 nicht spezifikationskonform sind.
Das macht diesen Negativfall zur schärfsten Prüfung von `S3-XI-002` — ein Parser mit
falscher Default-Annahme fällt hier nicht durch einen Absturz auf, sondern durch
stilles Falsch-Akzeptieren.
