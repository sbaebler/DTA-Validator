# Konstellation: Sammelrechnung (Rechnungsart 3) — `TPFL0002` / `TPFL0002.AUF`

Dieselbe Pflege-Abrechnung wie im Positivfall [`pflege-105-sgbxi/`](../pflege-105-sgbxi/),
aber über eine **Abrechnungsstelle mit Inkassovollmacht** eingereicht statt vom
Pflegedienst direkt. Zeigt den strukturell anderen Dateiaufbau, den Rechnungsart `3`
verlangt: eine zusätzliche, verschachtelte `PLGA`-Ebene.

> ## Wie belastbar ist dieses Beispiel?
>
> **Weniger belastbar als der Positivfall.** Zwei Fakten sind direkt aus
> [`knowledge-base/20-verfahren/05-para105-sgbxi-pflege.md`](../../knowledge-base/20-verfahren/05-para105-sgbxi-pflege.md)
> und [`knowledge-base/data/nachrichtentypen.yaml`](../../knowledge-base/data/nachrichtentypen.yaml)
> belegt: die **Verschachtelung** (Sammelrechnungs-`PLGA` → je Pflegekasse eine
> Gesamtrechnungs-`PLGA` → `PLAA`) und die **Position** des Sammelrechnungs-Kennzeichens
> im `FKT`-Segment. Alles, was darüber hinausgeht — insbesondere, **welche** IK an
> welcher `FKT`-Stelle steht, wenn Rechnungssteller und Leistungserbringer
> auseinanderfallen — ist eine **eigene, im Abschnitt "Offene Fragen" unten markierte
> Schlussfolgerung**, keine Primärquellen-Aussage. Wer die TA 1 Abschnitt 4.5
> (Feldkatalog) im Detail für Rechnungsart 2/3 auswertet, wird diese Datei
> voraussichtlich korrigieren müssen.

## 1. Der Sachverhalt

Der Pflegedienst Sonnenhof GmbH (derselbe Fall wie im Positivfall) lässt seine
Abrechnung nun über eine **Abrechnungsstelle mit Inkassovollmacht** einreichen. Die
Pflegekasse zahlt an die Abrechnungsstelle, nicht an den Pflegedienst — das ist
per Definition der Unterschied zwischen Rechnungsart 1 und 3.

| | |
|---|---|
| **Leistungserbringer** | Pflegedienst Sonnenhof GmbH, IK `461100877` (wie Positivfall) |
| **Abrechnungsstelle** | Pflegeabrechnung Nord GmbH, IK `661233445` (neu, Klassifikation `66`) |
| **Kostenträger** | Muster BKK, IK `109524616` (wie Positivfall) |
| **Pflegekasse** | Pflegekasse bei der Muster BKK, IK `189524616` (wie Positivfall) |
| **Rechnungsart** | `3` — Abrechnung über Abrechnungsstelle **mit** Inkassovollmacht, Zahlung an IK Abrechnungsstelle |
| **Abgerechnete Fälle** | dieselben zwei Abrechnungsfälle wie im Positivfall, unverändert: `2607001` (635,60 EUR), `2607002` (1.035,40 EUR) |
| **Sammel-Rechnungsnummer** | `2026080001`, Datum 10.08.2026 |

Bewusst minimal gehalten: **eine** Abrechnungsstelle, **ein** Kostenträger, **eine**
Pflegekasse, **ein** Leistungserbringer. Der Dateiaufbau verlangt die
Sammelrechnungs-Ebene bereits bei dieser einfachsten Besetzung — eine Sammelrechnung
mit nur einer Pflegekasse darunter ist kein Sonderfall, sondern die Mindestform.

## 2. Dateiaufbau

```
UNB                                                            (Absender: Abrechnungsstelle)
  UNH+1+PLGA:6'    ← Sammelrechnungs-PLGA je IK Kostenträger, kein UST, FKT.Sammelrechnung = J
  UNH+2+PLGA:6'    ← Gesamtrechnungs-PLGA je IK Pflegekasse darunter
  UNH+3+PLAA:6'    ← Abrechnungsdaten, inhaltlich identisch mit dem Positivfall
UNZ+3+1'
```

Das folgt direkt der in der Wissensbibliothek dokumentierten Kernregel: „Auf eine
PLGA-Nachricht hat immer eine PLAA-Nachricht zu folgen — es sei denn, die
PLGA-Nachricht ist als Sammelrechnung gekennzeichnet. Bei einer Sammelrechnung darf
nur einmal eine PLGA-Nachricht folgen." Die erste `PLGA` hier ist als Sammelrechnung
gekennzeichnet und hat **keine** direkt folgende `PLAA` — stattdessen folgt genau
einmal die nächste `PLGA` (die Gesamtrechnung), und erst danach deren `PLAA`.

## 3. Die drei Nachrichten im Detail

### 3.1 Sammelrechnungs-PLGA

```
UNH+1+PLGA:6'
FKT+01+J+661233445+109524616++661233445'
REC+2026080001:0+20260810+3+EUR'
SRD+36:23000+01'
GES+1671,00+++1671,00'
NAM+Pflegeabrechnung Nord GmbH+Inkassovollmacht Muster BKK'
UNT+7+1'
```

- `FKT`: `01` Verarbeitungskennzeichen, `J` **Kennzeichen Sammelrechnung** (im
  Positivfall an dieser Stelle leer — belegt durch dessen README: „Das zweite
  Datenelement (Sammelrechnung) ist leer — es wird nur in der Sammelrechnungs-PLGA
  mit `J` belegt."), danach IK Rechnungssteller/LE, IK Kostenträger, IK Pflegekasse
  (**leer** — siehe Abschnitt 4), IK Absender der Datei.
- `UST` **entfällt** — laut Nachrichtenkatalog ausdrücklich für die
  Sammelrechnungs-`PLGA` vorgesehen ("entfällt in der Sammelrechnungs-PLGA").
  Deshalb hat diese `PLGA` nur 5 Inhaltssegmente statt 6, `UNT` zählt `7`
  (`UNH FKT REC SRD GES NAM UNT`) statt `8`.
- `GES` deckt in diesem Beispiel dieselbe Summe wie die einzelne Gesamtrechnung ab,
  weil nur eine Pflegekasse existiert — real wäre das die Summe **über alle**
  Pflegekassen dieses Kostenträgers.

### 3.2 Gesamtrechnungs-PLGA

```
UNH+2+PLGA:6'
FKT+01++661233445+109524616+189524616+661233445'
REC+2026080001:1+20260810+3+EUR'
SRD+36:23000+01'
UST+DE999999999+J+01'
GES+1671,00+++1671,00'
NAM+Pflegeabrechnung Nord GmbH+Inkassovollmacht Muster BKK'
UNT+8+2'
```

Strukturell identisch mit der `PLGA` des Positivfalls (alle sechs Segmente, `UNT`
zählt `8`). Das Sammelrechnungs-Kennzeichen ist hier leer — nur die oberste `PLGA`
trägt `J`. Die Rechnungsnummer trägt jetzt eine **Einzel**-Nummer (`:1`), die diese
Pflegekasse innerhalb der Sammelrechnung identifiziert.

### 3.3 PLAA

Inhaltlich **byte-identisch** mit dem Positivfall (dieselben zwei Abrechnungsfälle,
dieselben `ESK`/`ELS`-Blöcke, dieselben `IAF`-Summen) — nur `UNH`-Referenz (`3` statt
`2`), `FKT` und `REC` wurden angepasst:

```
FKT+01+461100877+109524616+189524616+661233445'
REC+2026080001:1+20260810+3+EUR'
```

`FKT` hier: Verarbeitungskennzeichen, **IK Leistungserbringer** (`461100877`,
unverändert der Pflegedienst — die Person, die die Leistung erbracht hat, ändert
sich durch die Abrechnungsstelle nicht), IK Kostenträger, IK Pflegekasse, **IK
Rechnungssteller** (`661233445`, die Abrechnungsstelle). Das ist der Grund, warum
`PLAA.FKT` in der Wissensbibliothek als fünf **getrennte** Felder katalogisiert ist
("Verarbeitungskennzeichen, IK LE, IK Kostenträger, IK Pflegekasse, IK
Rechnungssteller") — im Positivfall sind IK LE und IK Rechnungssteller zufällig
gleich, weil dort Rechnungsart 1 gilt.

## 4. Offene Fragen — was hier Interpretation ist

**Wo im `FKT` der `PLGA` steht die Abrechnungsstelle?** Das Feld heißt in der
Wissensbibliothek einheitlich „IK Rechnungssteller/LE" — ein **kombiniertes** Feld.
Für Rechnungsart 1 ist die Frage müßig, weil Rechnungssteller und LE dieselbe IK
tragen. Für Rechnungsart 3 fallen sie auseinander, und die Quelle sagt nicht, welche
der beiden IK an dieser einen Stelle steht. Diese Datei setzt dort konsequent die
**Abrechnungsstelle** ein (das Feld folgt also der Rolle "Rechnungssteller", nicht
"LE") — mit der Konsequenz, dass die für den Positivfall dokumentierte Kreuzprüfung

> `PLGA.FKT.IK des Rechnungsstellers/LE` = `PLAA.FKT.IK des Leistungserbringers`

auf diese Datei **nicht** anwendbar ist: `661233445` (PLGA) ≠ `461100877` (PLAA IK
LE). Stattdessen passt hier `PLGA.FKT.IK Rechnungssteller/LE` (`661233445`) zu
`PLAA.FKT.IK Rechnungssteller` (`661233445`). Die naheliegende Lesart ist, dass die
im Positivfall notierte Kreuzprüfung eine **Verkürzung** ist, die nur für
Rechnungsart 1 zufällig richtig aussieht, weil dort beide PLAA-Felder gleich sind —
und dass die eigentliche Regel `PLGA.field3 = PLAA.IK-Rechnungssteller` lautet. Das
ist eine Hypothese, keine belegte Aussage; eine Implementierung sollte beide Lesarten
kennen, bis die TA 1 dazu im Detail geprüft ist.

**Bleibt `IK Pflegekasse` in der Sammelrechnungs-`FKT` leer?** Angenommen, weil eine
Sammelrechnung mehrere Pflegekassen desselben Kostenträgers bündeln kann und die
Ebene damit keiner einzelnen Pflegekasse zuzuordnen ist. Nicht durch einen Wortlaut
belegt.

**Trägt `NAM` auf beiden `PLGA`-Ebenen den Namen der Abrechnungsstelle?** Angenommen,
weil "Rechnungssteller" bei Rechnungsart 3 die Abrechnungsstelle ist und `NAM` als
"Name des Rechnungsstellers" katalogisiert ist. Denkbar wäre auch, dass die
Gesamtrechnungs-Ebene den Namen des tatsächlichen Leistungserbringers trägt — nicht
geprüft.

**`SRD` unverändert auf beiden Ebenen übernommen.** Realistisch wäre `SRD` auf der
Sammelebene nur dann sinnvoll belegbar, wenn alle gebündelten Leistungserbringer
dieselbe Leistungserbringergruppe und Leistungsart haben — was die Wissensbibliothek
mit „Innerhalb einer PLGA dürfen nur PLAA derselben Leistungsart abgerechnet werden"
für die einzelne `PLGA` festhält, aber nicht für die Sammelebene über mehrere `PLGA`
hinweg diskutiert. Für dieses minimale Ein-LE-Beispiel ist die Frage nicht sichtbar.

## 5. Was in diesem Beispiel unverändert bleibt

Beteiligte-Stammdaten, Prüfziffern, Abrechnungsfälle, Leistungsziffern,
Einsatzkalender und Beträge sind identisch mit dem Positivfall — nur nachzulesen dort
([`pflege-105-sgbxi/README.md`](../pflege-105-sgbxi/README.md)). Die neue IK der
Abrechnungsstelle (`661233445`) ist nach demselben, dort verifizierten
Prüfziffernverfahren gebildet: Kern `123344`, Prüfziffer `5`.

## 6. Dateien

| Datei | Inhalt | Größe |
|---|---|---|
| [`TPFL0002`](TPFL0002) | Nutzdaten, 3 Nachrichten (2× PLGA, 1× PLAA), 170 Segmente | 5118 Byte |
| [`TPFL0002.AUF`](TPFL0002.AUF) | Auftragsdatei, Festsatzformat | 348 Byte |

Keine Urbelege — sie wären identisch mit denen des Positivfalls, weil sich am
Leistungsgeschehen nichts ändert, nur am Abrechnungsweg.
