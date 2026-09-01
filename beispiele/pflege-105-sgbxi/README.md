# Beispiel: § 105 SGB XI (Pflege) — Dateipärchen `TPFL0001` / `TPFL0001.AUF`

Synthetisches Abrechnungsbeispiel eines ambulanten Pflegedienstes gegenüber einer
Pflegekasse. Gedacht als **Fixture** für Parser- und Regelentwicklung.

> ## Wie belastbar ist dieses Beispiel?
>
> **Struktur und Feldbelegung sind gegen die Primärdokumente gebaut.** Am 01.09.2026
> wurden ausgewertet: Anlage 2 GGT (Auftragssatz V 1.0), Anlage 4 GGT
> (Verfahrenskennungen), § 105 SGB XI Technische Anlage 1 V 6.4.0, Technische Anlage 3
> V 6.4.0 (Schlüsselverzeichnisse), TA 1 Anhang 1 (Struktur Auftragsdatei) und Anhang 3
> (Datenübermittlungsarten) sowie das Gemeinsame Rundschreiben Institutionskennzeichen
> 02/2026.
>
> **Erfunden sind nur die Stammdaten** — Namen, Anschriften, IK, KVNR, Preise,
> Leistungskomplexnummern und der Sachverhalt selbst.
>
> Das Beispiel ist ein **Positivfall**: eine korrekte Implementierung meldet darauf
> keinen Befund. Was es *nicht* leistet, steht in Abschnitt 8.

### Was sich gegenüber der Vorfassung geändert hat

Die frühere Fassung (`TPLG0001`, erstellt ohne Primärdokumente) war strukturell falsch.
Die Unterschiede sind lehrreich genug, um sie festzuhalten:

| Vorher | Jetzt | Warum |
|---|---|---|
| Dateiname `TPLG0001`, Verfahrenskennung `PLG` | `TPFL0001`, Kennung `TPFL0` | Anlage 4 GGT Kapitel 1.5: `PFL` für den Datenaustausch nach § 105 SGB XI |
| Auftragssatz 128 Byte, Layout geraten | **348 Byte**, 37 Felder nach Katalog | Anlage 2 GGT: `LÄNGE_AUFTRAG` = Konstante `00000348` |
| `UNA:+.? '` mit Dezimalpunkt | **kein `UNA`**, Dezimalzeichen `,` | TA 1 Abschnitt 4.1 Abs. 10 legt die Trennzeichen fest und sieht kein `UNA` vor |
| 1 PLGA + 2 PLAA | 1 PLGA + **1** PLAA mit zwei `INV`-Blöcken | „Auf eine PLGA hat immer eine PLAA zu folgen" — beide Fälle betreffen dieselbe Pflegekasse |
| Segmente `SKO`, `EPL`, `GES` in PLAA | `SRD`, `MAN`, `ELS`, `IAF` | `SKO` und `EPL` existieren in § 105 SGB XI nicht; `GES` gehört in die PLGA, das Fall-Ende ist `IAF` |
| Monatsmengen (`20`, `31`) in einer Zeile | **ein `ESK` je Einsatz**, darunter die `ELS` | `ESK` ist je Leistungseinsatz vorzugeben, aufsteigend nach Tag und Uhrzeit |
| `UNH+…+PLGA:06:04:00` | `UNH+…+PLGA:6` | `S009` besteht aus Nachrichtentyp-Kennung und **Versionsnummer** (aktuell `6`) |
| IK des Pflegedienstes `261099874` (Klassifikation 26 = Krankenhaus) | `461100877` (Klassifikation 46) | Klassifikationstabelle des Gemeinsamen Rundschreibens IK |
| Kostenträger-IK als Pflegekasse geführt | getrennte IK für Kostenträger (`10…`) und Pflegekasse (`18…`) | TA 1: `IK der Pflegekasse` beginnt immer mit `18` |
| Firmenname 38 Zeichen | auf 27 gekürzt | `PLGA.NAM.Name 1` ist `..30` Stellen lang |

## 1. Datenschutz

Alle Daten sind frei erfunden (REQ-DSGVO-03). Personennamen, Anschriften, KVNR, IK,
Rechnungsnummern und Beträge sind synthetisch; Prüfziffern wurden nach den in der
Wissensbibliothek dokumentierten Algorithmen gerechnet, damit die Werte formal gültig
sind. IK sind neunstellige Zahlen aus einem endlichen Wertebereich — eine zufällige
Übereinstimmung mit einem real vergebenen IK ist nicht ausschließbar und ohne Bedeutung.

Als **Beschäftigtennummern** nach § 293 Abs. 8 Satz 2 SGB V verwendet das Beispiel
ausschließlich die in Schlüssel 2.17 der TA 3 definierten **Ersatzwerte**
(`999999998` neu, `999999996` Auszubildende). Vergabe und Prüfverfahren echter
Beschäftigtennummern sind in dieser Wissensbibliothek nicht erfasst — eine erfundene
neunstellige Nummer würde eine Formatzusage machen, die nicht belegt ist.

## 2. Der abgebildete Fall

| | |
|---|---|
| **Leistungserbringer** | Pflegedienst Sonnenhof GmbH, Lindenweg 14, 12345 Musterstadt |
| **IK Leistungserbringer** | `461100877` (Klassifikation 46, Regionalbereich 11 Berlin) |
| **Datenannahmestelle** | `661100423` (Klassifikation 66, Rechenzentrum) |
| **Belegannahmestelle** | `661100559` |
| **Kostenträger** | `109524616` — Muster BKK (Klassifikation 10) |
| **Pflegekasse** | `189524616` — Pflegekasse bei der Muster BKK (Klassifikation 18) |
| **Abrechnungscode / Tarifkennzeichen** | `36` (privat gewerblicher Anbieter) / `23000` (Berlin, ohne Sondertarif) |
| **Leistungsart** | `01` — ambulante Pflege |
| **Rechnungsart** | `1` — Abrechnung von Leistungserbringer, Zahlung an IK Leistungserbringer |
| **Abrechnungszeitraum** | 01.07.2026 – 31.07.2026 |
| **Rechnungsnummer / -datum** | `2026070001:0` / 05.08.2026 |
| **Dateierstellung** | 05.08.2026, 11:47 |
| **Abrechnungsfälle** | 2 Pflegebedürftige |
| **Rechnungsbetrag** | 1.671,00 EUR |
| **Umsatzsteuer** | befreit, Grund `01` (§ 4 Nr. 16 UStG) |

> Kostenträger und Pflegekasse teilen Regionalbereich und Seriennummer und unterscheiden
> sich nur in der Klassifikation. Weil die Prüfziffer **nur aus den Stellen 3–8** gebildet
> wird, ist sie bei beiden IK dieselbe (`6`). Das ist kein Zufall des Beispiels, sondern
> eine Eigenschaft des Verfahrens — und eine gute Testfalle für eine Implementierung, die
> die Klassifikation versehentlich in die Rechnung einbezieht.

### Abrechnungsfall `2607001`

| | |
|---|---|
| Versicherte | Hanna Kerzenmacher, geb. 12.03.1948 |
| KVNR | `K741852967` |
| Pflegegrad | 3 |
| Einsätze | 20 (je 07:15 Uhr) |

| Leistungsziffer | Bezeichnung | Einsätze | Einzelpreis | Betrag |
|---|---|---:|---:|---:|
| `01:01:1:003` | Große Morgentoilette (Pflegefachkraft) | 20 | 24,50 | 490,00 |
| `01:01:2:015` | Hauswirtschaftliche Versorgung (hausw. Fachkraft) | 8 | 18,20 | 145,60 |
| | **Summe** | | | **635,60** |

### Abrechnungsfall `2607002`

| | |
|---|---|
| Versicherter | Otto Brinkmeier, geb. 27.11.1939 |
| KVNR | `M305921844` |
| Pflegegrad | 4 |
| Einsätze | 31 (je 07:45 Uhr) |

| Leistungsziffer | Bezeichnung | Einsätze | Einzelpreis | Betrag |
|---|---|---:|---:|---:|
| `01:01:1:004` | Kleine Morgentoilette mit Lagern | 31 | 28,90 | 895,90 |
| `01:06:0:03` | Wegepauschale (Einsatz-/Fahrtkostenpauschale) | 31 | 4,50 | 139,50 |
| | **Summe** | | | **1.035,40** |

Beide Beträge liegen unter dem monatlichen Sachleistungsbetrag des jeweiligen
Pflegegrades; ein Eigenanteil entsteht daher nicht und wird nicht modelliert.

**Die Leistungsziffer ist zusammengesetzt** aus Art der abgegebenen Leistung (2.4),
Vergütungsart (2.5), qualifikationsabhängiger Vergütung (2.6) und Leistung (2.7.n) —
getrennt durch Doppelpunkte. Welcher Abschnitt für „Leistung" gilt, entscheidet die
Vergütungsart: `01` → 2.7.1 (Leistungskomplexe, 3 Stellen), `06` → 2.7.5
(Wegegebühren-Art, 2 Stellen). Die Leistungskomplexnummern `003`, `004` und `015` sind
**erfunden** — sie ergeben sich real aus der jeweiligen Vergütungsvereinbarung.

## 3. Das Dateipärchen

| Datei | Inhalt | Größe |
|---|---|---|
| [`TPFL0001`](TPFL0001) | Nutzdaten (PLGA/PLAA), EDIFACT, **Klartext** | 4924 Bytes, 163 Segmente |
| [`TPFL0001.AUF`](TPFL0001.AUF) | Auftragsdatei, Klartext, Festsatzformat | 348 Bytes |
| [`urbeleg-leistungsnachweis.html`](urbeleg-leistungsnachweis.html) | Urbeleg: Leistungsnachweise beider Abrechnungsfälle | 2 Seiten |
| [`urbeleg-begleitzettel.html`](urbeleg-begleitzettel.html) | Begleitzettel für die Urbelege an die Belegannahmestelle | 1 Seite |
| [`urbeleg-leistungsnachweis.pdf`](urbeleg-leistungsnachweis.pdf) | dasselbe als PDF, A4 quer | 2 Seiten |
| [`urbeleg-begleitzettel.pdf`](urbeleg-begleitzettel.pdf) | dasselbe als PDF, A4 hoch | 1 Seite |
| [`beispiel-metadaten.yaml`](beispiel-metadaten.yaml) | Erwartungswerte für Tests | — |

### Zwei Dateinamen, zwei Systematiken

Der **physikalische** (Transfer-)Dateiname nach Anhang 3 Abschnitt 2.2.2:

```
  T   P F L   0    0 0 1
  │   └─┬─┘   │    └─┬─┘
  │     │     │      └──── Stellen 6–8: Transfernummer        "001"
  │     │     └─────────── Stelle 5:    Verfahrensversion     "0"
  │     └───────────────── Stellen 2–4: Verfahren             "PFL"
  └─────────────────────── Stelle 1:    "T" = Test/Erprobung
```

Der **logische** Dateiname nach Anhang 3 Abschnitt 2.2.1 — er steht im Feld `DATEINAME`
des Auftragssatzes (Stellen 105–115) **und** in der `UNB`-Anwendungsreferenz:

```
  P L  0 7 6  0  0 1  S  B K
  └┬┘  └─┬─┘  │  └┬┘  │  └┬┘
   │     │    │   │   │   └── Stellen 10–11: Kassenart "BK" = Betriebskrankenkassen
   │     │    │   │   └────── Stelle 9:      "S" = Selbstabrechner
   │     │    │   └────────── Stellen 7–8:   lfd. Nummer je Kalenderjahr  "01"
   │     │    └────────────── Stelle 6:      "0" = Regeldaten
   │     └─────────────────── Stellen 3–5:   Abrechnungszeitraum "MMJ" = Juli 2026
   └───────────────────────── Stellen 1–2:   "PL" = Pflege-Leistungserbringer
```

Nur der physikalische Name trägt das Test-/Echt-Kennzeichen. Die beiden Namen dürfen
nicht verwechselt werden — und `DATEINAME` im Auftragssatz ist der **logische**.

### Zwei bewusste Abweichungen von der Realität

| Abweichung | Grund |
|---|---|
| Die Nutzdatendatei ist **unverschlüsselt** | Real wäre `TPFL0001` der SECON-Umschlag (`EnvelopedData` über `SignedData`, Anlage 16 GGT). Hier liegt der Klartext unter dem Dateinamen, damit die Fixture ohne Schlüsselmaterial nutzbar ist. Prüfstufe 2 ist damit **nicht** testbar. Der Auftragssatz weist das konsistent aus: `VERSCHLÜSSELUNGSART` und `ELEKTRONISCHE_UNTERSCHRIFT` stehen beide auf `00` — eine der zwei zulässigen Kombinationen. |
| Test-, nicht Echtdaten (`T` / Dateiindikator `0`) | Beispieldaten gehören nie in den Echtdatenpfad. |

## 4. Auftragsdatei `TPFL0001.AUF`

Positionsbasiertes Festsatzformat, **348 Byte**, ISO 8859-1, keine Trennzeichen, keine
Zeilenumbrüche. Feldkatalog:
[`../../knowledge-base/data/auftragssatz.yaml`](../../knowledge-base/data/auftragssatz.yaml).

`␣` steht für ein Leerzeichen.

| Feld | Stellen | Länge | Wert |
|---|---|---|---|
| `IDENTIFIKATOR` | 1–6 | 6 | `500000` |
| `VERSION` | 7–8 | 2 | `01` |
| `LAENGE_AUFTRAG` | 9–16 | 8 | `00000348` |
| `SEQUENZ_NR` | 17–19 | 3 | `000` |
| `VERFAHREN_KENNUNG` | 20–24 | 5 | `TPFL0` |
| `TRANSFER_NUMMER` | 25–27 | 3 | `001` |
| `VERFAHREN_KENNUNG_SPEZIFIKATION` | 28–32 | 5 | `␣␣␣␣␣` |
| `ABSENDER_EIGNER` | 33–47 | 15 | `461100877␣␣␣␣␣␣` |
| `ABSENDER_PHYSIKALISCH` | 48–62 | 15 | `461100877␣␣␣␣␣␣` |
| `EMPFAENGER_NUTZER` | 63–77 | 15 | `661100423␣␣␣␣␣␣` |
| `EMPFAENGER_PHYSIKALISCH` | 78–92 | 15 | `661100423␣␣␣␣␣␣` |
| `FEHLER_NUMMER` | 93–98 | 6 | `000000` |
| `FEHLER_MASSNAHME` | 99–104 | 6 | `000000` |
| `DATEINAME` | 105–115 | 11 | `PL076001SBK` |
| `DATUM_ERSTELLUNG` | 116–129 | 14 | `20260805114700` |
| `DATUM_UEBERTRAGUNG_GESENDET` | 130–143 | 14 | `20260805114730` |
| `DATUM_UEBERTRAGUNG_EMPFANGEN_START` | 144–157 | 14 | `00000000000000` |
| `DATUM_UEBERTRAGUNG_EMPFANGEN_ENDE` | 158–171 | 14 | `00000000000000` |
| `DATEIVERSION` | 172–177 | 6 | `000000` |
| `KORREKTUR` | 178–178 | 1 | `0` |
| `DATEIGROESSE_NUTZDATEN` | 179–190 | 12 | `000000004924` |
| `DATEIGROESSE_UEBERTRAGUNG` | 191–202 | 12 | `000000004924` |
| `ZEICHENSATZ` | 203–204 | 2 | `I1` |
| `KOMPRIMIERUNG` | 205–206 | 2 | `00` |
| `VERSCHLUESSELUNGSART` | 207–208 | 2 | `00` |
| `ELEKTRONISCHE_UNTERSCHRIFT` | 209–210 | 2 | `00` |
| `SATZFORMAT` | 211–213 | 3 | `␣␣␣` |
| `SATZLAENGE` | 214–218 | 5 | `00000` |
| `BLOCKLAENGE` | 219–226 | 8 | `00000000` |
| `STATUS` | 227–227 | 1 | `␣` |
| `WIEDERHOLUNG` | 228–229 | 2 | `00` |
| `UEBERTRAGUNGSWEG` | 230–230 | 1 | `5` |
| `VERZOEGERTER_VERSAND` | 231–240 | 10 | `0000000000` |
| `INFO_UND_FEHLERFELDER` | 241–246 | 6 | `000000` |
| `VARIABLES_INFO_FELD` | 247–274 | 28 | `␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣` |
| `E-MAIL-ADRESSE_ABSENDER` | 275–318 | 44 | `␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣…` |
| `DATEI_BEZEICHNUNG` | 319–348 | 30 | `01␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣01` |

Bemerkenswert an dieser Belegung:

- **`VERFAHREN_KENNUNG_SPEZIFIKATION` bleibt leer.** Anlage 4 GGT legt die Werte je
  Verfahren fest und schreibt die Beispiellisten nicht fort; für § 105 SGB XI ist keine
  Belegung vorgesehen.
- **`DATEI_BEZEICHNUNG` trägt zwei Dinge.** Stellen 319–320 die Art der abgegebenen
  Leistung (`01`) — das ist eine Zusatzbelegung aus Anhang 1 der TA 1, die die Anlage 2
  GGT nicht kennt. Stellen 347–348 die Anzahl der Gesamtpakete (`01`) nach Anlage 2 GGT.
  Dazwischen 26 Leerzeichen.
- **`E-MAIL-ADRESSE ABSENDER` bleibt leer.** Das Feld ist optional; für § 105 SGB XI
  belegt Anhang 1 die Stellen 275–318 zudem abweichend als `DATEINAME_PHYSIKALISCH`.
  Solange dieser Widerspruch offen ist (❓-18), macht das Beispiel keine Aussage.
- **Kann-Felder sind nicht leer.** `DATUM_ÜBERTRAGUNG_EMPFANGEN_START` und `…_ENDE` sind
  numerische Kann-Felder und deshalb mit Nullen gefüllt, nicht mit Leerzeichen.

## 5. Nutzdatendatei `TPFL0001`

### 5.1 Trennzeichen und Zeichensatz

Die TA 1 legt die Trennzeichen **fest** und sieht **kein `UNA`-Segment** vor:

| Funktion | Zeichen |
|---|---|
| innerhalb zusammengesetzter Datenelemente | `:` |
| Datenelementtrenner | `+` |
| **Dezimalzeichen** | **`,`** |
| Aufhebungszeichen | `?` |
| Segmentendezeichen | `'` |

Beträge stehen also als `1671,00`, nicht `1671.00`. Ein Parser, der die
EDIFACT-Defaults annimmt, liest sie falsch.

Zulässig sind ISO 8859-1, ISO 7-Bit (DIN 66003 DRV 7) und ISO 8-Bit (DIN 66303 DRV 8);
der Auftragssatz deklariert `I1` = ISO 8859-1. Die Datei enthält nur Zeichen, die in
allen drei Kodierungen byte-identisch sind — deshalb steht dort „Große Morgentoilette"
nicht als Klartext, sondern gar nicht: Leistungsbezeichnungen werden im EDIFACT nicht
übertragen, nur die Leistungsziffer.

Die Datei enthält **keine Zeilenumbrüche**. Die Beispiele unten sind zur Lesbarkeit
umbrochen.

### 5.2 Dateirahmen und PLGA

```
UNH+1+PLGA:6'
FKT+01++461100877+109524616+189524616+461100877'
REC+2026070001:0+20260805+1+EUR'
SRD+36:23000+01'
UST+DE999999999+J+01'
GES+1671,00+++1671,00'
NAM+Pflegedienst Sonnenhof GmbH+Abrechnung 030 5550123'
UNT+8+1'
```

- `UNB`: Syntax `UNOC:3`, Absender-IK, Empfänger-IK, `JJJJMMTT:hhmm`,
  Datenaustauschreferenz `1`, Anwendungsreferenz (logischer Dateiname), Dateiindikator
  `0` = Testdatei.
- `FKT`: Das zweite Datenelement (Sammelrechnung) ist leer — es wird nur in der
  Sammelrechnungs-PLGA mit `J` belegt. Anstelle eines leeren Kann-Datenelements steht
  das Trennkennzeichen, daher `01++461100877`.
- `REC`: Rechnungsnummer als Datenelementgruppe `Sammel:Einzel`. Bei einem einzelnen
  Leistungserbringer wird die Einzel-Rechnungsnummer auf `0` gesetzt.
- `SRD`: Leistungserbringergruppe `Abrechnungscode:Tarifkennzeichen`, dann die
  Leistungsart.
- `GES`: `1671,00+++1671,00` — Zuzahlung, Beihilfe und Mehrwertsteuer sind leere
  Kann-Felder. **Nicht** `0,00`: die TA 1 verlangt an dieser Stelle das Trennkennzeichen.
- `UNT`: `8` Segmente einschließlich `UNH` und `UNT`.

### 5.3 PLAA — Kopf und erster Abrechnungsfall

```
UNH+2+PLAA:6'
FKT+01+461100877+109524616+189524616+461100877'
REC+2026070001:0+20260805+1+EUR'
INV+K741852967+2607001'
NAD+Kerzenmacher+Hanna+19480312+Rosenweg+3+12345+Musterstadt'
MAN+202607+++3'
ESK+01+0715'
ELS+01:01:1:003+24,50+++00+1,00+999999998'
…
```

- `FKT` in der PLAA hat **kein** Sammelrechnungs-Feld, dafür zusätzlich das IK des
  Rechnungsstellers — die Segmentnamen sind gleich, die Feldfolge ist es nicht.
- `INV` eröffnet den Abrechnungsfall: Versicherten-Nummer und eindeutige Belegnummer.
- `NAD` im ersten Fall mit Anschrift, im zweiten ohne — dort endet das Segment nach dem
  Geburtsdatum, weil am Segmentende stehende leere Kann-Felder wegfallen dürfen.
- `MAN+202607+++3`: Der Abrechnungszeitraum liegt nach dem 31.12.2016, deshalb ist der
  **Pflegegrad** zu melden und Pflegestufe wie Pflegeklasse bleiben leer.
- `ESK+01+0715`: ein Einsatzkopfsegment **je Einsatz**, Kennzeichen = Kalendertag.
- `ELS`: Leistungsziffer, Einzelpreis, leerer Punktwert, leere Punktzahl,
  `00` im Feld „Dauer/gefahrene Kilometer", Anzahl `1,00`, Beschäftigtennummer.

### 5.4 Abschluss

```
ELS+01:06:0:03+4,50+++00+1,00+999999998'
IAF+1035,40+++1035,40'
UNT+153+2'
UNZ+2+1'
```

`IAF` schließt den Abrechnungsfall ab: Gesamtbrutto, leere Zuzahlung, leere Beihilfe,
Rechnungsbetrag. `UNZ` nennt die Zahl der `UNH` und wiederholt die
Datenaustauschreferenz aus dem `UNB`.

### 5.5 Warum die Datei so viel größer ist als die Vorfassung

4924 statt 1002 Byte — nicht weil mehr abgerechnet würde, sondern weil die
Vorfassung einen ganzen Monat in eine Zeile gepresst hat. Die TA 1 verlangt **ein `ESK`
je Leistungseinsatz** und darunter die einzelnen `ELS`. Aus „20 × Große Morgentoilette"
werden 20 Einsatzkopfsegmente mit je einem `ELS`. Das ist der wesentliche
Strukturunterschied zwischen einer geratenen und einer spezifikationskonformen Datei —
und der Grund, warum ein Validator die Menge nicht aus einem Mengenfeld, sondern aus der
**Zahl der Segmente** ableitet.

## 6. Urbelege

### 6.1 Der Leistungsnachweis

[`urbeleg-leistungsnachweis.html`](urbeleg-leistungsnachweis.html) enthält den
**Papierbeleg** zur elektronischen Abrechnung: je Abrechnungsfall einen
Leistungsnachweis mit Tagesraster, Handzeichen der Pflegekraft, Zusammenstellung und
Unterschriftenfeldern. Im Browser öffnen und drucken (A4 quer, Seitenumbruch je Fall).

Fachlich ist das der **Urbeleg**: Der Pflegebedürftige bestätigt mit seiner Unterschrift
die erbrachten Einsätze. Er geht nicht an die Datenannahmestelle, sondern an die
**Belegannahmestelle** laut Kostenträgerdatei — ein zweiter, vom Dateipärchen getrennter
Weg. Die Kasse hält bei Prüfung den Beleg gegen die elektronische Abrechnung.

| Prüfung | Beleg | `TPFL0001` |
|---|---|---|
| Handzeichen im Tagesraster | 20 / 8 / 31 / 31 | **Anzahl der `ELS`-Segmente** je Leistungsziffer |
| Zusammenstellung je Fall | 635,60 / 1.035,40 | `IAF` der beiden Abrechnungsfälle |
| Summe beider Fälle | 1.671,00 | `GES` der PLGA |
| Versichertennummern | `K741852967`, `M305921844` | `INV` |
| Belegnummern | `2607001`, `2607002` | `INV`, zweites Datenelement |
| Rechnungsbezug | Nr. 2026070001 vom 05.08.2026 | `REC` |

Die TA 1 verlangt ausdrücklich, dass die Belegnummer aus dem `INV`-Segment **auf den
Urbeleg zu übertragen** ist und die Rechnungsnummer vollständig und unverändert auf den
Urbelegen erscheint. Der Beleg trägt beide.

**Der Einsatzkalender erzählt den Fall.** Die Einsatztage sind kein Zufall:

- **Fall `2607001`:** Juli 2026 hat 23 Werktage, abgerechnet sind 20 Einsätze. Die
  Differenz steht als Bemerkung auf dem Beleg — 13.–15.07. stationärer
  Krankenhausaufenthalt. Die hauswirtschaftliche Versorgung läuft dienstags und freitags,
  abzüglich des Dienstags im Krankenhauszeitraum: 8 statt 9.
- **Fall `2607002`:** tägliche Versorgung, 31 Tage, dazu 31 Wegepauschalen.

Eine Abrechnung mit mehr Einsätzen als Handzeichen auf dem Beleg ist genau der Fall, den
eine Kasse absetzt.

**Belastbarkeit:** Der Aufbau des Papierbelegs ist **erfunden**. Für den *elektronischen*
Leistungsnachweis ist die Struktur in TA 1 Abschnitt 4.6.2 belegt (Schema
`PFL_LNW_2.2.0.xsd`); für den papiergebundenen Beleg ist kein Dokument ausgewertet.
Anlage 4 zur TA 1 („Begleitzettel für Urbelege", V 1.0 vom 31.01.2003) existiert und
steht im [Dokumentenregister](../../knowledge-base/data/dokumentenregister.yaml), ist
aber noch nicht beschafft.

**Eine bewusste Abweichung zwischen Beleg und Datei:** Der Beleg schreibt „Große
Morgentoilette", die Datei überträgt Leistungsbezeichnungen gar nicht — nur die
Leistungsziffer `003`. Ein Feldvergleich zwischen Papier und Datei ist also kein
Textvergleich, sondern ein Auflösen der Ziffer über die Vergütungsvereinbarung.

### 6.2 Der Begleitzettel

[`urbeleg-begleitzettel.html`](urbeleg-begleitzettel.html) ist das Deckblatt der
Papiersendung. Die Abrechnung läuft über **zwei getrennte Wege**, die erst beim
Kostenträger wieder zusammenfinden:

```
                          verschlüsseltes Dateipärchen
  Pflegedienst  ─────────────────────────────────────►  Datenannahmestelle  661100423
   461100877               TPFL0001 + .AUF                        │
        │                                                         │
        │             Urbelege + Begleitzettel                    ▼
        └──────────────────────────────────────────►  Belegannahmestelle   661100559
                          Papier, Briefpost                       │
                                                                  ▼
                                                        Kostenträger 109524616
                                                        führt beides zusammen
```

Der Begleitzettel ist die **Klammer** zwischen beiden Wegen. Er trägt genau die
Merkmale, über die sich Papier und Datei verbinden lassen: Rechnungsnummer, Dateiname
und Transfernummer.

Datenannahmestelle, Belegannahmestelle und Kostenträger sind in der Kostenträgerdatei
getrennt geführt und **nicht zwingend dieselbe Stelle**. Das Beispiel besetzt sie mit
drei unterschiedlichen, prüfziffernkorrekten IK, damit eine Implementierung die Rollen
nicht gleichsetzt.

**Zwei Deckblätter, gegensätzliche Datenschutzregeln:**

| | Auftragsdatei `TPFL0001.AUF` | Begleitzettel |
|---|---|---|
| begleitet | die elektronische Datei | den Papierstapel |
| geht an | Datenannahmestelle | Belegannahmestelle |
| Sozialdaten | **verboten** (`S1-ALL-008`) | **enthalten** — Namen, KVNR, Pflegegrad |

Der Grund liegt im Transportweg: Die Auftragsdatei wird **unverschlüsselt** übertragen,
damit die Datenannahmestelle vor der Entschlüsselung routen kann. Der Begleitzettel
liegt im verschlossenen Umschlag bei Belegen, die die Sozialdaten ohnehin enthalten.

### 6.3 PDF-Fassung

Beide Belege liegen zusätzlich als PDF bei. Erzeugt mit Chromium als Druckertreiber:

```bash
chromium --headless --no-pdf-header-footer \
         --print-to-pdf=urbeleg-begleitzettel.pdf urbeleg-begleitzettel.html
```

Maßgeblich ist die HTML-Datei; ändert sie sich, ist das PDF neu zu erzeugen. Die
Seitengröße kommt aus dem `@page`-Block (`A4 landscape` für den Leistungsnachweis,
`A4 portrait` für den Begleitzettel).

## 7. Was dieses Beispiel prüfbar macht

Regel-IDs nach
[`../../knowledge-base/data/pruefregeln.yaml`](../../knowledge-base/data/pruefregeln.yaml).
Die vollständige Liste steht maschinenlesbar in
[`beispiel-metadaten.yaml`](beispiel-metadaten.yaml) unter `erfuellte_regeln` — 57 Regeln.
Die interessantesten:

| Regel | Prüft | Im Beispiel |
|---|---|---|
| `S0-ALL-003` | Transferdateiname bei beiden Dateien identisch | `TPFL0001` / `TPFL0001.AUF` |
| `S0-ALL-005` | Stellen 2–4 sind eine bekannte Verfahrenskennung | `PFL` aus Anlage 4 GGT |
| `S1-ALL-001` | Auftragssatz 348 Byte, `LÄNGE_AUFTRAG` = `00000348` | ✔ |
| `S1-ALL-009` | Muss-Felder gefüllt, Kann-Felder mit Default-Wert | ✔ |
| `S1-ALL-010` | Krypto-Kombination zulässig | `00` + `00` |
| `S1-ALL-012` | `DATEIGRÖßE_NUTZDATEN` = tatsächliche Größe | `000000004924` = 4924 Byte |
| `S1-XI-001` | logischer Dateiname im Feld `DATEINAME` | `PL076001SBK` |
| `S1-XI-002` | Stellen 319–320 = Art der abgegebenen Leistung | `01` |
| `S3-XI-002` | kein `UNA`, Dezimalzeichen Komma | ✔ |
| `S3-XI-003` | PLGA-Segmentfolge `FKT REC SRD UST GES NAM` | ✔ |
| `S3-XI-004` | PLAA-Grammatik und Kardinalitäten | ✔ |
| `S3-XI-005` | auf eine PLGA folgt eine PLAA | 1 PLGA, 1 PLAA |
| `S3-XI-006` | `ESK` aufsteigend nach Tag sortiert | 01…31 |
| `S3-ALL-004` | `UNT`-Zähler = Segmentanzahl | 8 / 153 |
| `S4-ALL-001` | IK-Prüfziffer | 5 IK, alle gültig |
| `S4-XI-002` | IK der Pflegekasse beginnt mit `18` | `189524616` |
| `S4-XI-007` | `ESK`-Kennzeichen ist Kalendertag oder `99` | Kalendertage |
| `S5-ALL-002` | `DATEINAME` = `UNB`-Anwendungsreferenz | `PL076001SBK` |
| `S5-XI-001` | `PLGA.FKT` = `PLAA.FKT` in den IK | ✔ |
| `S5-XI-003` | `GES` = Summe der `IAF` | 635,60 + 1.035,40 = 1.671,00 |
| `S6-ALL-001/002` | Leistungs- ≤ Rechnungs- ≤ Erstellungsdatum | 31.07. ≤ 05.08. = 05.08. |

### Drei Fallen, in die dieses Beispiel tappen lässt

**1. `S1-ALL-008` (keine Sozialdaten im Auftragssatz) als Regex.** Ein
`^[A-Z][0-9]{9}$`-Muster über den Rohsatz findet Treffer, die keine sind: An jeder
Feldgrenze eines positionsbasierten Formats entstehen Zeichenfolgen, die es als Wert
nie gibt. Die Regel ist erst **nach dem Parsen** feldweise auszuwerten.

**2. Das Test-/Echt-Kennzeichen ist keine Gleichheitsprüfung.** Es steht an drei Stellen:
Dateiname Stelle 1 (`T`), `VERFAHREN_KENNUNG` Stelle 20 (`T`), `UNB`-Dateiindikator (`0`).
Der Dateiname kennt aber nur `T` und `E`, der Dateiindikator **drei** Werte: `0` Test,
`1` Erprobung, `2` Echt. Es gilt `T` ↔ {`0`,`1`} und `E` ↔ {`2`}.

**3. Die IK-Prüfziffer ignoriert die Klassifikation.** `109524616` und `189524616`
teilen sie sich. Eine Implementierung, die über die Stellen 1–8 rechnet statt über 3–8,
weist beide zurück — und fällt bei diesem Beispiel garantiert auf.

## 8. Prüfziffern — Nachrechnen

| Wert | Kern (Stellen 3–8) | Prüfziffer |
|---|---|---|
| IK `461100877` | `110087` | `7` |
| IK `661100423` | `110042` | `3` |
| IK `661100559` | `110055` | `9` |
| IK `109524616` | `952461` | `6` |
| IK `189524616` | `952461` | `6` |

Verfahren: Modulo 10 über die Stellen 3–8, Gewichtung von rechts `1-2-1-2-1-2`,
Quersumme der Produkte, Rest modulo 10. **Verifiziert** gegen den Testvektor aus dem
Gemeinsamen Rundschreiben Institutionskennzeichen 02/2026, Nummer 1.2.5:
IK `260326822`, Kern `032682`, Prüfziffer `2`.

| Wert | Kern | Prüfziffer |
|---|---|---|
| KVNR `K741852967` | `11` + `74185296` | `7` |
| KVNR `M305921844` | `13` + `30592184` | `4` |

Die **KVNR-Prüfziffern** verwenden weiterhin die als **Annahme** gekennzeichnete Variante
aus
[`../../knowledge-base/40-stammdaten/02-krankenversichertennummer.md`](../../knowledge-base/40-stammdaten/02-krankenversichertennummer.md):
Buchstabe → zweistellige Zahl (A = 01 … Z = 26), Modulo 10 mit Gewichtung 1·2·1·2·…
**Wie der führende Buchstabe tatsächlich eingeht, ist unbelegt** (❓-11). Ändert die
KVNR-Richtlinie V3.4.0 diese Annahme, sind beide KVNR neu zu rechnen.

## 9. Was mit diesem Beispiel nicht geprüft werden kann

| Bereich | Grund |
|---|---|
| **Stufe 2 — Kryptografie** (`S2-ALL-001` … `S2-ALL-014`) | Nutzdaten liegen im Klartext vor, kein SECON-Umschlag |
| `S1-ALL-006` — Datenannahmestelle zuständig | Kostenträgerdatei (TA 1 Anhang 5) liegt nicht vor |
| `S4-ALL-002` — KVNR-Prüfziffer | Algorithmus unverifiziert (❓-11) |
| `S5-XI-007` — Bündelung bei KIM | Beispiel nutzt den Weg außerhalb der TI |
| `S0-ALL-009` — Datenträgerversand | kein Datenträger |
| Sammelrechnungen, Rechnungsarten `2` und `3` | nur Rechnungsart `1` modelliert |
| `ZUS`, `HIL`, `IMG` | keine Zuschläge, keine Pflegehilfsmittel, keine vollelektronische Abrechnung |
| Negativfälle | das Beispiel ist ein Positivfall; eine Fehlerfixture fehlt noch |

### Nächste sinnvolle Erweiterungen

1. **Negativfixtures** je Prüfstufe — falsche `UNT`-Zähler, `UNA` vorhanden,
   Dezimalpunkt statt Komma, `ESK` unsortiert, Pflegegrad *und* Pflegestufe belegt.
2. **Sammelrechnung** (Rechnungsart `3`, Abrechnungsstelle mit Inkassovollmacht) — der
   Dateiaufbau unterscheidet sich strukturell.
3. **Vollelektronische Abrechnung über KIM** mit XML-Hülle, `IMG`-Segment und
   elektronischem Leistungsnachweis — solange TA 1 6.4.0 gilt; ab 01.02.2027 wandert
   dieser Teil in die neue Technische Anlage 5.
4. **Umlaut-Variante**, sobald Anlage 15 GGT (Zeichensätze) ausgewertet ist.
5. **§ 302-Beispiel**, sobald die dortige Technische Anlage 1 vorliegt.
