# § 105 SGB XI — Pflege

> **Quellenstand:** Die Technische Anlage 1 liegt seit dem 01.09.2026 als Primärdokument vor
> und ist ausgewertet, ebenso Anhang 1 (Struktur Auftragsdatei), Anhang 3
> (Datenübermittlungsarten) und die Technische Anlage 3 (Schlüsselverzeichnisse). ✅ [Q22]

## 1. Grundlage

**§ 105 SGB XI** regelt die Abrechnung pflegerischer Leistungen. **Abs. 2** ermächtigt zur
einvernehmlichen Festlegung von Form und Inhalt des Abrechnungsverfahrens. ✅ [Q22b]

Vertragswerk:
- **Einvernehmliche Festlegung** nach § 105 Abs. 2 SGB XI (Stand 05.10.2022) ✅ [Q22f]
- **Vereinbarung nach § 105 Abs. 2 Satz 2 SGB XI** vom 05.10.2023 — regelt die Übermittlung
  elektronischer Dokumente (elektronische Leistungsnachweise) ✅ [Q22b]

## 2. Welche Version gilt? ✅ [Q22][Q22a]

Auf der Portalseite stehen **zwei** Fassungen der TA 1 nebeneinander im Bereich „aktuell" —
das ist kein Fehler, sondern die reguläre Vorlauffrist:

| Version | gültig ab | Status am 01.09.2026 | Dokument |
|---|---|---|---|
| **6.4.0** | **01.05.2026** | **in Kraft — maßgeblich** | `TA1_6.4.0_20250707_oA.pdf` |
| 6.5.0 | 01.02.2027 | von 6.5.1 abgelöst, im Archiv | `TA1_6.5.0_20260129.pdf` |
| **6.5.1** | **01.02.2027** | angekündigt, noch nicht in Kraft | `TA1_6.5.1_20260625.pdf` |

Die Frage, ob „6.4.0 noch aktuell ist oder schon eine 6.5.0 im Umlauf ist", hat also beide
Antworten: **6.4.0 ist die geltende Fassung**, und **6.5.1 ist bereits veröffentlicht** und
tritt zum 01.02.2027 an ihre Stelle. Ein Validator muss beide Fassungen parallel vorhalten
und stichtagsbezogen auflösen.

### Was 6.5.x ändert ✅ [Q22a]

Version 6.5.0 (Stand 29.01.2026) verlagert die **gesamte TI-Strecke** aus der TA 1 heraus:

| Änderung | Wirkung |
|---|---|
| Neue **Technische Anlage 5 — Datenübermittlung in der TI** (V 1.2.0, ab 01.02.2027) | Die XML-Datenstrukturen für die vollelektronische Abrechnung stehen künftig dort, nicht mehr in TA 1 Abschnitt 4.6 |
| **`IMG`-Segment aus PLAA entfernt** | PLAA erhält eine neue Gültigkeit; die Verknüpfung Abrechnungsfall ↔ elektronischer Leistungsnachweis wird anders gelöst |
| Abschnitt Testverfahren aus Anhang 2 in die TA 1 übernommen; **Anhang 2 entfällt** | |
| Abschnitt Softwareprüfung aus der TA 1 entfernt | verbleibt in Anhang 4 |

Version 6.5.1 (Stand 25.06.2026) ist eine rein redaktionelle Anpassung der Versionsangabe
der TA 5.

> ⚠️ **Für die Architektur relevant:** Das Verschieben des `IMG`-Segments zeigt, dass die
> Nachrichtenstruktur PLAA versionsabhängig ist. Segmentgrammatiken müssen deshalb je
> Nachrichtentyp**version** hinterlegt werden, nicht je Verfahren.

## 3. Dokumentenfamilie ✅ [Q22]

Bestandteile der Technischen Anlage laut TA 1 Version 6.4.0, Abschnitt 1 Abs. 1:

| Dokument | Version | gültig ab |
|---|---|---|
| **Anlage 1 — Technische Anlage 1** | 6.4.0 | 01.05.2026 |
| Anhang 1 — Struktur Auftragsdatei | 2.0 | 01.07.2007 |
| Anhang 2 — Erprobungs- und Testverfahren | 2.2 | 01.05.2026 |
| Anhang 3 — Datenübermittlungsarten | 2.1.2 | 01.05.2026 |
| Anhang 4 — Softwareprüfung (+ Anlage 1 Prüfkatalog, Anlage 2 Selbsterklärung) | 1.0 | 01.05.2026 |
| Anhang 5 — Kostenträgerdatei | 5.2 | 01.05.2026 |
| Anhang 6 — Fehlermeldeverfahren | 1.0 | 31.01.2003 |
| Anlage 2 — Abrechnung auf maschinellem Vordruck | 1.0 | 29.07.2003 |
| **Anlage 3 — Schlüsselverzeichnisse** | 6.4.0 | 01.05.2026 |
| Anlage 4 — Begleitzettel für Urbelege | 1.0 | 31.01.2003 |

Anhang 7 ist entfallen. Ab 01.02.2027 gelten TA 3 in 6.5.0, Anhang 3 in 2.2.0, Anhang 5 in
5.3 und die neue **Anlage 5 (TI)** in 1.2.0.

Die Versionierung folgt einem **SemVer-ähnlichen Schema** — anders als bei § 301
(fortlaufende Ganzzahlen) und § 302 (Anlagenversion + Stichtag). Bemerkenswert: die
Versionen **6.0.0 und 6.1.0 sind nie in Kraft getreten** („Tritt nicht in Kraft"). Eine
Regelwerks-Registry muss „veröffentlicht" und „in Kraft getreten" also getrennt führen.

## 4. Datenübermittlungsarten ✅ [Q22][Q22e]

Zwei Wege, deren Wahl **fachlich determiniert** ist:

| | außerhalb der TI | innerhalb der TI (KIM) |
|---|---|---|
| **Wann** | wenn **papiergebundene** Leistungsnachweise verwendet wurden | wenn **elektronische** Leistungsnachweise verwendet werden (vollelektronische Abrechnung) |
| **Medien** | E-Mail (Anlage 7 GGT), FTAM over IP (Anlage 10 GGT) — E-Mail bevorzugt | KIM |
| **Auftragsdatei** | **ja**, zu jeder Nutzdatendatei | **nein** |
| **Nutzdatenformat** | EDIFACT | XML-Umschlag mit base64-codierten, einzeln signierten Teilen |
| **Bündelung** | je Datenannahmestelle mit Entschlüsselungsbefugnis **eine Datei je Kassenart** | je Datei **nur eine Pflegekasse und nur eine Leistungsart** |
| **Verschlüsselung** | SECON (Anlage 16 GGT) | Ende-zu-Ende durch das KIM-Clientmodul |
| **Signatur** | PKCS#7 | CMS (CAdES) enveloping, fortgeschritten mittels **SMC-B**, jeder Bestandteil **einzeln** |
| **Komprimierung** | zulässig | **nein** — Übertragungsdateien werden nicht komprimiert |

> ⚠️ Die Bündelungsregeln sind **gegenläufig**: außerhalb der TI wird nach Kassenart
> gebündelt (mehrere Pflegekassen in einer Datei erlaubt), in der TI ist genau das
> **verboten**. Ein Validator muss die Regel also am Transportweg festmachen, nicht am
> Verfahren.

Vollelektronisch abrechenbar sind derzeit nur die Leistungsarten **01** (ambulante Pflege),
**07** (Verhinderungspflege) und **10** (Entlastungsleistungen, letztere nur wenn von
Leistungserbringern der ambulanten Pflege erbracht). ✅ [Q22]

## 5. Aufbau der Nutzdaten (EDIFACT) ✅ [Q22]

### Trennzeichen — fest vereinbart, **kein `UNA`**

| Funktion | Zeichen |
|---|---|
| Trennzeichen innerhalb zusammengesetzter Datenelemente | `:` |
| Trennzeichen Datenelemente | `+` |
| **Dezimalzeichen** | **`,`** (Komma) |
| Aufhebungszeichen (Escape) | `?` |
| Segmentendezeichen | `'` |

Die TA 1 legt diese Zeichen **direkt fest** und sieht **kein `UNA`-Segment** vor. Ein Parser
darf die Trennzeichen für § 105 SGB XI also nicht aus einem `UNA` lesen — und schon gar
nicht die EDIFACT-Defaults annehmen: das Dezimalzeichen ist das **Komma**, nicht der Punkt.

Beispiel für das Aufhebungszeichen: Luigi D'Angelo wird als `D?'Angelo+Luigi+` übermittelt.

### Dateirahmen

```
UNB  Kopfsegment der Nutzdatendatei      1× je Datei
  UNH  Nachrichtenkopf                   1× je Nachricht
    … PLGA- oder PLAA-Nutzsegmente …
  UNT  Nachrichtenende                   1× je UNH
UNZ  Endesegment der Datei               1× je Datei
```

`UNB`-Felder: Syntax `UNOC:3` · Absender-IK (9 n) · Empfänger-IK (9 n) ·
Datum/Uhrzeit `JJJJMMTT:hhmm` · Datenaustauschreferenz (..5 n, beginnend mit `1`) ·
**Anwendungsreferenz** = logischer Dateiname (11 an) · **Dateiindikator** (1 n).

`UNZ`: Anzahl der `UNH` (..6 n) + Datenaustauschreferenz wie im `UNB`.
`UNT`: Anzahl Segmente **einschließlich** `UNH` und `UNT` (..6 n) + Nachrichtenreferenznummer.

> **Dateiindikator (`UNB`, DE 0035) — dreiwertig:** `0` Testdatei, `1` **Erprobungsdatei**,
> `2` Echtdatei. Der physikalische Dateiname kennt dagegen nur `T` und `E`, wobei `T` sowohl
> Test als auch Erprobung abdeckt. Eine Kreuzprüfung „Dateiname vs. Dateiindikator" ist
> deshalb **keine Gleichheitsprüfung**: `T` ↔ {`0`,`1`} und `E` ↔ {`2`}.

### Rechnungsarten und Dateiaufbau ✅ [Q22]

Je Datei ist nur **eine** Rechnungsart zulässig (Schlüssel 2.1 der TA 3):

| Wert | Bedeutung |
|---|---|
| `1` | Abrechnung von Leistungserbringer, Zahlung an IK Leistungserbringer |
| `2` | Abrechnung über Abrechnungsstelle **ohne** Inkassovollmacht, Zahlung an IK Leistungserbringer |
| `3` | Abrechnung über Abrechnungsstelle **mit** Inkassovollmacht, Zahlung an IK Abrechnungsstelle |

Die Kernregel des Dateiaufbaus:

> **Auf eine PLGA-Nachricht hat immer eine PLAA-Nachricht zu folgen — es sei denn, die
> PLGA-Nachricht ist als Sammelrechnung gekennzeichnet. Bei einer Sammelrechnung darf nur
> einmal eine PLGA-Nachricht folgen.**

```
UNB
  ┌ je IK des Kostenträgers ──────────────────────────────────────┐
  │  [optional]  UNH · PLGA als Sammelrechnung · UNT              │
  │  ┌ je IK der Pflegekasse ─────────────────────────────────┐   │
  │  │  UNH · PLGA als Gesamtrechnung · UNT                   │   │
  │  │  UNH · PLAA                     · UNT                  │   │
  │  └────────────────────────────────────────────────────────┘   │
  └───────────────────────────────────────────────────────────────┘
UNZ
```

Bei Rechnungsart 2 ist dieser Block zusätzlich je IK des Leistungserbringers zu wiederholen;
eine Sammelrechnung unter dem IK der **Abrechnungsstelle** ist dabei **unzulässig**. Bei
Rechnungsart 3 **muss** die Abrechnungsstelle je Kostenträger eine Sammelrechnung erstellen.

## 6. Nachrichtentypen ✅ [Q22]

| Typ | Bedeutung | Nutzsegmente |
|---|---|---|
| **PLGA** | Gesamtaufstellung der Abrechnung (Rechnung) | `FKT` `REC` `SRD` `UST` `GES` `NAM` |
| **PLAA** | Abrechnungsdaten je Abrechnungsfall | `FKT` `REC` `INV` `NAD` `IMG` `MAN` `ESK` `ELS` `ZUS` `HIL` `IAF` |

Damit ist ❓-13 entschieden: Es heißt **`PLAA`**, nicht „PLLA". Strukturell das Gegenstück zu
`SLGA`/`SLLA` aus § 302 SGB V.

**Aktuelle Nachrichtentypversion: `6`** (PLGA und PLAA, jeweils gültig ab 01.09.2024, „auf
weiteres"). Im `UNH` steht sie als `PLGA:6` bzw. `PLAA:6`. Die Versionsnummern **können sich
zwischen PLGA und PLAA unterscheiden** — der Validator darf sie nicht gleichsetzen.

### PLGA — Segmentkardinalität

Alle sechs Segmente kommen **genau einmal** vor. `UST` entfällt in der Sammelrechnungs-PLGA.

| Segment | Art | Inhalt |
|---|---|---|
| `FKT` | M | Verarbeitungskennzeichen, Kennzeichen Sammelrechnung, IK Rechnungssteller/LE, IK Kostenträger, IK Pflegekasse, IK Absender der Datei |
| `REC` | M | Rechnungsnummer (`Sammel:Einzel`), Rechnungsdatum, Rechnungsart, Währungskennzeichen |
| `SRD` | M | Leistungserbringergruppe (Abrechnungscode + Tarifkennzeichen), Leistungsart |
| `UST` | K | Ordnungsnummer, Kennung USt-Befreiung, Grund der Befreiung |
| `GES` | M | Summe Gesamtbrutto, Summe Zuzahlungen/Eigenanteile, Summe Beihilfe, Gesamtrechnungsbetrag, MwSt-Betrag |
| `NAM` | M | Name 1–4 (Name/Firma des Rechnungsstellers, ggf. Ansprechpartner und Telefon) |

### PLAA — Segmentkardinalität

```
FKT   1× je Nachricht
REC   1× je Nachricht
 ├ INV   1–n je Nachricht   ← Beginn Abrechnungsfall
 │  NAD   1× je INV
 │  IMG   0–n je INV        ← nur vollelektronisch (in 6.5.x entfallen)
 │  MAN   1× je INV         ← Kalendermonat + Pflegegrad/Pflegestufe
 │   └ ESK   1–n je MAN     ← je Einsatz
 │      └ ELS   1–n je ESK  ← je Einzelleistung
 │         ├ ZUS   0–n je ELS
 │         └ HIL   0–1 je ELS
 │  IAF   1× je INV         ← Ende Abrechnungsfall
 └ (Folge INV … IAF wiederholt sich je Abrechnungsfall)
```

Ein **Abrechnungsfall** umfasst die Daten für **einen Versicherten in einem Kalendermonat
mit derselben Pflegestufe/Pflegeklasse oder demselben Pflegegrad**. Wechselt der Pflegegrad
innerhalb eines Kalendermonats, ist ein **neuer Abrechnungsfall mit neuer Rechnungsnummer
(neue Nachricht)** zu bilden.

`ESK` muss je Abrechnungsfall **aufsteigend** nach Kennzeichen der Leistungserbringung und
Uhrzeit sortiert sein — eine prüfbare Reihenfolgebedingung, nicht nur eine Kardinalität.

### Feldebene — die für einen Validator harten Punkte ✅ [Q22]

| Feld | Regel |
|---|---|
| `PLGA.FKT.IK der Pflegekasse` | **beginnt immer mit `18`** |
| `REC.Rechnungsnummer` | eindeutig je Rechnungs-Erstellungsjahr und je IK des Rechnungsstellers; Sonderzeichen inkl. Leerzeichen unzulässig, **außer** `-` und `/` als Gliederungszeichen; keine aufeinanderfolgenden Gliederungszeichen; darf nicht mit einem Gliederungszeichen beginnen oder enden |
| `REC` bei Einzel-LE | Sammel-Rechnungsnummer gefüllt, Einzel-Rechnungsnummer `0` (z. B. `4711:0`) |
| `INV.Eindeutige Belegnummer` | Buchstaben, Ziffern, `/` und `-`; alle anderen Sonderzeichen unzulässig; muss der Belegnummer auf dem Urbeleg entsprechen |
| `INV.Versicherten-Nummer` | ..12 an, **Füllzeichen unzulässig**; entfällt nur im Ersatzverfahren — dann **muss** die Anschrift im `NAD` übermittelt werden |
| `MAN` | entweder Pflegestufe **oder** Pflegegrad; Zeitraum vor 01.01.2017 → Pflegestufe, nach 31.12.2016 → Pflegegrad; Pflegeklasse nur teil-/vollstationär und nur bis 31.12.2016 |
| `ESK.Kennzeichen der Leistungserbringung` | Kalendertag `01`–`31`, **`99` nur bei fixen Monatspauschalen** |
| `ELS.Dauer/Kilometer/Zeitraum` | Bedeutung hängt von der Vergütungsart ab: `02` → Dauer in Minuten `mmmm`, `03` → Bis-Zeit `hhmm`, `04` → Von/Bis-Tag `TTTT`, `06` → ganze Kilometer, sonst `00` |
| `ELS.Beschäftigtennummer` | 9 n nach § 293 Abs. 8 Satz 2 SGB V; **Muss** bei ambulanten Pflege-/Betreuungsdiensten und Einzelpflegekräften nach § 77 SGB XI; Ersatzwerte `999999998` (neu), `999999997` (sonstiger Grund), `999999996` (Auszubildende) |
| `ZUS.Wert` | **immer alle 5 Nachkommastellen** melden (`9999,99999`) |
| `IAF.Rechnungsbetrag` | = Gesamtbruttobetrag ./. Zuzahlung/Eigenanteil ./. Beihilfebetrag, max. bis zum Höchstleistungsanspruch |
| `GES.Gesamtrechnungsbetrag` | = Summe der Rechnungsbeträge aus den PLAA |

**Feldübergreifende Gleichheitsbedingungen** (PLGA ↔ PLAA, Nachricht ↔ Datei) — jede davon
ist eine Prüfregel der Stufe 5:

- `UNB.Absender` = `PLGA.FKT.IK Absender der Datei`
- `PLGA.FKT.Verarbeitungskennzeichen` = `PLAA.FKT.Verarbeitungskennzeichen`
- `PLGA.FKT.IK des Rechnungsstellers/LE` = `PLAA.FKT.IK des Leistungserbringers`
- `PLGA.FKT.IK des Kostenträgers` = `PLAA.FKT.IK des Kostenträgers`
- `PLGA.FKT.IK der Pflegekasse` = `PLAA.FKT.IK der Pflegekasse`
- `PLGA.REC` = `PLAA.REC` (Rechnungsnummer außer bei Sammelrechnung, Datum, Rechnungsart, Währung)
- Das Währungskennzeichen muss in **allen** PLGA/PLAA einer Nutzdatendatei übereinstimmen
- Innerhalb einer PLGA dürfen nur PLAA **derselben Leistungsart** (`SRD`) abgerechnet werden

## 7. Schlüsselverzeichnisse (Technische Anlage 3, V 6.4.0) ✅ [Q22g]

| Abschnitt | Schlüssel | Größe |
|---|---|---|
| 2.1 | Rechnungsart | 1 n |
| 2.2.1 | Abrechnungscode | 2 an — `00` Abrechnungsstelle; `11`–`19` Pflegehilfsmittel; `35`–`39` ambulante Pflege; `81`–`84` Tagespflege; `86`–`89` Nachtpflege; `91`–`94` Kurzzeitpflege; `96`–`99` vollstationär |
| 2.2.2 | Tarifkennzeichen | 5 an — Stellen 1–2 Tarifbereich (`00` bundeseinheitlich, `01`–`16`, `23` Berlin), Stellen 3–5 Sondertarif (`000` ohne Besonderheiten) |
| 2.3 | Verarbeitungskennzeichen | 2 n — derzeit **nur `01`** (Abrechnung ohne Besonderheiten) |
| 2.4 | Art der abgegebenen Leistung | 2 an — `01`–`15` |
| 2.5 | Vergütungsart | 2 an — `01` Leistungskomplex, `02` Zeit, `03` teilstationär, `04` vollstationär/Kurzzeit, `05` Pflegehilfsmittel, `06` Wegegebühren, `07` Entlastung, `08` Pauschale, `99` keine Vertragspreisregelung |
| 2.6 | Qualifikationsabhängige Vergütung | 1 an — `0`–`4`, `8`; `5`–`7` nicht besetzt |
| 2.7.1–2.7.8 | Leistung, **abhängig von der Vergütungsart** | 1–10 an |
| 2.8–2.16 | Pflegehilfsmittel, MwSt, Pflegestufe, Pflegeklasse, Produktbesonderheiten, USt-Befreiung, Zu-/Abschläge, Pflegegrad, Zuschlagsberechnung | |
| 2.17 | Ersatz-Beschäftigtennummer | 9 n |
| 3.1–3.6 | vollelektronische Abrechnung: Fehlercodes, Art der Unterschrift, Grund fehlender Unterschrift, logische Version, Inhaltstyp, Dateityp | |

> **Kaskadierender Schlüssel.** Das Datenelement `Leistung` im `ELS` wird über die
> `Vergütungsart` aufgelöst: `01` → 2.7.1, `02` → 2.7.2, `03`/`04` → 2.7.3, `05` → 2.7.4,
> `06` → 2.7.5, `07` → 2.7.6, `08` → 2.7.7, `99` → 2.7.8. Eine flache Schlüsseltabelle
> genügt hier nicht; die Auflösung ist kontextabhängig.

> **Regionale und vertragliche Schlüsselwerte.** Die Leistungskomplexnummern (2.7.1) sind
> die „in den Vergütungsvereinbarungen verwandte lfd. Nummer" — sie sind **nicht bundesweit
> normiert**. Ein Validator kann sie formal (3 Stellen alphanumerisch) prüfen, inhaltlich
> aber nur gegen die jeweilige Vergütungsvereinbarung. Dasselbe gilt für den Sondertarif in
> den Stellen 3–5 des Tarifkennzeichens.

## 8. Auftragsdatei (Anhang 1 zur TA 1) ✅ [Q22d]

Anhang 1 beschreibt den Auftragssatz **verfahrensspezifisch** — und ist mit Version 2.0 vom
25.01.2007 deutlich älter als die Anlage 2 GGT (Stand 10.10.2024). Die Abweichungen sind
real und für einen Validator relevant:

| Punkt | Anhang 1 Pflege (2007) | Anlage 2 GGT (2024) |
|---|---|---|
| Zeichensatz der Auftragsdatei | ISO 7-Bit DIN 66003 DRV 7 bzw. ISO 8-Bit DIN 66303 DRV 8 | ISO 8859-1 (`I1`) |
| `VERSCHLÜSSELUNGSART` | `00` keine, `02` PEM — „ab 01.07.2007 findet PKCS#7 Anwendung" | `00` keine, `03` PKCS#7 |
| `KOMPRIMIERUNG` | `01` COMPRESS (CoCoNet), `03` ZIP, `04` COMPRESS (UNIX), `05` Jet x-press | `02` gzip, `03` ZIP, `07` bzip2, `13`/`23` ZIP-Archiv |
| `SEQUENZ_NR` | Feldart `M` | Feldart `m` |
| `DATEI_BEZEICHNUNG` (319–348) | Stellen **319–320 = Art der abgegebenen Leistung** (Schlüssel 2.4) | variabler Bereich, Stellen 347–348 Anzahl Gesamtpakete |
| Stellen 275–318 | `DATEINAME_PHYSIKALISCH` | `E-MAIL-ADRESSE ABSENDER` |

> ⚠️ **Auflösungsregel:** Die GGT sind das übergeordnete Regelwerk nach § 95 SGB IV; die
> sektorspezifische Anlage konkretisiert, ersetzt aber nicht. Wo Anhang 1 veraltete Werte
> nennt (PEM statt PKCS#7), gilt die Anlage 2 GGT. Wo Anhang 1 **zusätzlich** belegt
> (Stellen 319–320), gilt die Zusatzbelegung. Das ist eine Auslegung — sie ist **nicht**
> irgendwo ausgeschrieben und sollte vor Implementierung mit einer Datenannahmestelle
> abgestimmt werden. ❓

Verfahrenskennung: `EPFL0` / `TPFL0`. Physikalischer Dateiname und logischer Dateiname siehe
[`../30-technik/02-kks-auftragsdatei-dateinamen.md`](../30-technik/02-kks-auftragsdatei-dateinamen.md).

## 9. Vollelektronische Abrechnung über KIM ✅ [Q22][Q22e]

Gilt für TA 1 **6.4.0**; ab 01.02.2027 wandert dieser Teil in die neue Technische Anlage 5.

### Nutzdatendatei (XML statt EDIFACT-Datei pur)

```
Header                 (PFL_basis_2.2.0.xsd)
  Absender: KIM-Mailadresse + IK  (IK = UNB.Absender)
  Empfänger: IK
  Erstellungsdatum JJJJMMTT, Erstellungszeit hhmmss
  Datei-ID           ← UUID, je Nutzdatendatei neu, nie wiederverwendet
  Verfahrenskennung  ← "EPFL0" | "TPFL0"
  Nachrichtentyp     ← "ABR" | "FEH"
  logische Version   ← nnn.nnn.nnn, Schlüssel 3.4 der TA 3

Abrechnungsnachricht   (PFL_ABR_2.2.0.xsd)
  Abrechnungsdaten            ← die EDIFACT-Datei, signiert, base64
  Abrechnungsbegründende Unterlagen  1–999
    Leistungsnachweis-ID      ← UUID, muss zur IMG-Angabe im PLAA passen
    Erstelldatum, PRODMOD-ID
    Datei                     ← XML oder PDF, signiert, base64
    Inhaltstyp, Dateityp

Fehlernachricht        (PFL_FEH_2.2.0.xsd)
  Datei-ID, MessageID, 1–99 × {Fehlercode, Fehlertext, XPath}
```

Der **elektronische Leistungsnachweis** (`PFL_LNW_2.2.0.xsd`) trägt je Tag 1–99 Einsätze mit
je 1–99 Einzelleistungen, die Beschäftigtennummern (1–3 je Leistung) sowie die Unterschrift
des Versicherten oder deren dokumentierten Grund des Fehlens.

### Dateinamen in der TI

```
<Verfahrenskennung>_<Nachrichtentyp>_<IK>_<Leistungsart>_<MMJJJJ>_<lfd.Nr>.xml
EPFL0_ABR_501234567_01_082024_01.xml
EPFL0_FEH_501234567_01_082024_01.xml

Bei Entschlüsselungs- oder Signaturfehlern abweichend:
EPFL0_FEH_<JJJJMMDDhhmmss>.xml
```

### KIM-Rahmenbedingungen ✅ [Q22e]

- Genau **eine** Nutzdatendatei je KIM-Nachricht, als base64-MIME-Anhang
  (`Content-Description: PFL`), **maximal 15 MB**
- Betreff = Dateiname ohne Endung
- E-Mail-Body leer bei Abrechnungs-, Fehlertext bei Fehlernachrichten
- Zeichensatz der **XML-Hülle**: UTF-8 nach DIN SPEC 91379, nur normative darstellbare
  Zeichen, **kein BOM**. Die eingebetteten EDIFACT-Abrechnungsdaten behalten dagegen den
  Zeichensatz nach Anhang 1 (ISO 8859-1 / ISO 7-Bit / ISO 8-Bit).
- Signaturprüfung **auf den unveränderten Binärdaten** aus der KIM-Nachricht — vor der
  Prüfung darf **keine XML-Verarbeitung** stattfinden
- KIM-Adresse des Empfängers aus der Kostenträgerdatei (Anhang 5); steht dort im
  `DFU`-Segment das Kürzel `VZD`, ist sie im Verzeichnisdienst der TI über
  `domainID` = IK aus dem `IDK`-Segment und `entryType` = 5 zu ermitteln
- Antwortadresse: `Reply-To` vor `From`; erst danach VZD-Lookup
- Dienstkennung `PFL;ABR-nn;<version>` bzw. `PFL;FEH;<version>`, `nn` = Leistungsart

> ⚠️ Die Reihenfolgevorschrift „Signatur vor XML-Verarbeitung" ist eine
> **Sicherheitsanforderung an die Implementierung**, keine Formatregel. Ein Validator, der
> zuerst parst und dann prüft, verletzt sie — auch wenn das Ergebnis meist gleich aussieht.

## 10. Fehlerverfahren ✅ [Q22]

Vierstufiges Prüfkonzept beim Empfänger:

| Stufe | Prüfung | Wirkung |
|---|---|---|
| **1** | Datei und Dateistruktur: physikalische Lesbarkeit, Reihenfolge und Syntax der Kopf-/Endesegmente, Gültigkeit der Kommunikationspartner, **Signaturen** | fehlerhafte Signatur → **Abweisung der Nutzdatendatei** |
| **2** | Syntax je Nachricht: Segmentreihenfolge, je Segment Typ, Länge, Vorkommen (Kann/Muss) | Verletzung → **gesamte Datei** zurückweisen |
| **3** | Formale Prüfung der Datenelementinhalte, Schlüsselausprägungen gegen Anlage 3, Kombinationsprüfungen über mehrere Felder | Abweisung mit unverzüglicher Benachrichtigung |
| **4** | Fachverfahren der einzelnen Pflegekassen (vertrags-, versicherungs-, leistungsrechtlich) | **keine** Abweisung der Ursprungsdatei; Rechnungssteller wird informiert |

Das deckt sich strukturell mit dem Stufenmodell in
[`../50-anforderungen/02-validierungsregeln.md`](../50-anforderungen/02-validierungsregeln.md),
ist aber gröber: die Pflege-TA fasst unsere Stufen 0–2 in ihrer Stufe 1 zusammen und kennt
zwischen Stufe 3 und 4 keine eigene Summen-/Integritätsstufe.

**Bemerkenswert:** Ab Stufe 2 wird die **gesamte Datei** zurückgewiesen, nicht die einzelne
Nachricht. Ein Validator, der Befunde je Abrechnungsfall meldet, bildet damit die
tatsächliche Verarbeitungsfolge nicht ab — er sollte zusätzlich ausweisen, **ob die Datei als
Ganzes annahmefähig** ist.

## 11. Kostenträgerdateien und Annahmestellen ✅ [Q22]

- Datenannahmestellen sind der **Kostenträgerdatei der jeweiligen Kassenart** zu entnehmen
  (Struktur: Anhang 5 zur TA 1, V 5.2, ab 01.02.2027 V 5.3)
- Für jede **Datenannahmestelle mit Entschlüsselungsbefugnis** ist je Kassenart eine
  Nutzdatendatei (`UNB`…`UNZ`) zu erstellen
- Für die Übermittlung der **Urbelege** benennen die Pflegekassen ebenfalls Annahmestellen
  in der Kostenträgerdatei — diese sind **nicht** identisch mit den Datenannahmestellen
- Der GKV-Spitzenverband stellt die kassenartenbezogenen Dateien bereit, **ohne Gewähr für
  die Inhalte**

## 12. Softwareprüfung ✅ [Q22]

Nach Abschnitt 4.2.1 der Vereinbarung nach § 105 Abs. 2 SGB XI darf zur Abrechnung nur
Software verwendet werden, die die vereinbarten technischen Anforderungen sicherstellt; der
Nachweis erfolgt über eine **Softwareprüfung** nach Anhang 4 (Prüfkatalog + Selbsterklärung,
je V 1.0 ab 01.05.2026). Vor der erstmaligen Durchführung ist zudem eine **Anmeldung bei den
Datenannahmestellen** erforderlich.

Das beantwortet ❓-16 für den Pflegebereich: eine Prüfpflicht existiert, allerdings als
Prüfkatalog mit Selbsterklärung, nicht als Systemuntersuchung durch die ITSG. Für § 302 SGB V
ist die Frage weiter offen.
