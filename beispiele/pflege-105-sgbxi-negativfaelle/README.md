# Negativfälle zu § 105 SGB XI — sieben Dateien, sieben Einzelfehler

Ergänzung zum Positivfall [`pflege-105-sgbxi/`](../pflege-105-sgbxi/): dieselbe
Abrechnung (`TPFL0001` / `TPFL0001.AUF`), aber je Unterverzeichnis mit **genau einem
eingebauten Fehler**. Gedacht, um zu belegen, dass eine Regel nicht nur beim
Positivfall schweigt, sondern beim passenden Negativfall auch wirklich anschlägt.

> **Belastbarkeit:** Jeder Fehler ist eine mechanische, minimale Abweichung vom
> Positivfall — erzeugt durch eine gezielte Textersetzung, nicht von Hand
> nachgetippt. Die Diffs unten sind das Ergebnis eines Abgleichs beider Dateien
> und zeigen genau die geänderte Stelle. Die fachliche Einordnung (welche Regel
> greifen sollte) stützt sich auf dieselben Primärdokumente wie der Positivfall
> (siehe dessen README, Abschnitt „Wie belastbar ist dieses Beispiel?").

## Übersicht

| Verzeichnis | Fehler | Betroffene Regel | Diff |
|---|---|---|---|
| [`n1-ik-pruefziffer/`](n1-ik-pruefziffer/) | IK der Datenannahmestelle mit falscher Prüfziffer | `S4-ALL-001` | `661100423` → `661100424` |
| [`n2-unt-zaehler/`](n2-unt-zaehler/) | `UNT`-Segmentzähler der PLAA stimmt nicht mit der tatsächlichen Segmentanzahl überein | `S3-ALL-004` | `UNT+153+2'` → `UNT+152+2'` |
| [`n3-summe-abweichung/`](n3-summe-abweichung/) | `PLGA.GES`-Gesamtrechnungsbetrag weicht von der Summe der `PLAA.IAF`-Rechnungsbeträge ab | `S5-XI-003` | `GES+1671,00+++1671,00'` → `GES+1671,00+++1691,00'` |
| [`n4-dateipaerchen-unvollstaendig/`](n4-dateipaerchen-unvollstaendig/) | Auftragsdatei fehlt, nur die Nutzdatendatei liegt vor | `S0-ALL-003` (Vollständigkeit des Dateipärchens) | `TPFL0001.AUF` entfernt |
| [`n5-una-vorhanden/`](n5-una-vorhanden/) | `UNA`-Segment vorhanden, obwohl die TA 1 für § 105 SGB XI keines vorsieht | `S3-XI-002` | `UNA:+,? '` vorangestellt |
| [`n6-dezimalpunkt/`](n6-dezimalpunkt/) | Dezimalpunkt statt Komma in allen Beträgen | `S3-XI-002` | jedes `,` in einem Betrag → `.` |
| [`n7-esk-unsortiert/`](n7-esk-unsortiert/) | Zwei `ESK`-Blöcke im ersten Abrechnungsfall vertauscht, Reihenfolge nicht mehr aufsteigend | `S3-XI-006` | `ESK+01…ESK+02` → `ESK+02…ESK+01` |

## Warum diese sieben

Die Liste ist keine willkürliche Auswahl, sondern stammt aus dem Abschnitt „Was noch
fehlt" der [Übersicht aller Beispiele](../README.md): falsche Prüfziffer, falscher
Zähler, abweichende Summe, unvollständiges Dateipärchen, vorhandenes `UNA`,
Dezimalpunkt statt Komma, unsortiertes `ESK`. Jeder Fall deckt eine andere Prüfstufe
ab (0, 3, 4, 5) und damit eine andere Klasse von Fehlern: Vollständigkeit,
Syntaxkonformität, Prüfziffernarithmetik, Kreuzsumme.

## Was diese Negativfälle nicht sind

- **Keine eigenständigen Beispiele.** Sie sind bewusst redundant zum Positivfall — nur
  die eine Abweichung zählt. Wer den Positivfall versteht, muss hier nur den Diff
  lesen.
- **Keine erschöpfende Fehlerliste.** Für jede der übrigen ~55 im Positivfall
  erfüllten Regeln ließe sich ein weiterer Negativfall bauen; das ist hier nicht
  geleistet.
- **Kein Ersatz für Grenzwerttests.** Die Fehler sind grobe, eindeutige Verstöße
  (falsche Prüfziffer, nicht "Prüfziffer um genau eine Stelle daneben, aber
  zufällig trotzdem gültig"). Randfälle einer Regel (z. B. Prüfziffer 0 vs. 10 als
  Sonderfall) sind nicht abgedeckt.

## Aufbau eines Unterverzeichnisses

Jedes Unterverzeichnis enthält `TPFL0001` (und, außer bei `n4`, `TPFL0001.AUF`) sowie
eine kurze `README.md`, die den Fehler benennt, den Diff zeigt und die erwartete
Regelverletzung nennt. Auf eigene Urbelege, PDF-Fassungen und eine vollständige
`beispiel-metadaten.yaml` wird verzichtet — sie wären reine Kopien des Positivfalls
und tragen zur Aussage "ein Fehler, eine Regel" nichts bei.
