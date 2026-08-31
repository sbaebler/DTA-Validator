# Beispiel: § 105 SGB XI (Pflege) — Dateipärchen `TPLG0001` / `TPLG0001.AUF`

Synthetisches Abrechnungsbeispiel eines ambulanten Pflegedienstes gegenüber einer
Pflegekasse. Gedacht als **Fixture** für Parser- und Regelentwicklung, solange die
Technische Anlage 1 zu § 105 Abs. 2 SGB XI noch nicht beschafft ist.

> ## ⚠️ Wie belastbar ist dieses Beispiel?
>
> **Der Transportrahmen ist an den belegten Vorgaben der Wissensbibliothek ausgerichtet.
> Die fachliche Segment- und Feldstruktur von PLGA/PLAA ist erfunden.**
>
> Die Wissensbibliothek belegt für § 105 SGB XI nur, **dass** es die Nachrichtentypen
> PLGA und PLAA gibt und dass sie das strukturelle Gegenstück zu SLGA/SLLA aus § 302
> SGB V sind — **nicht**, aus welchen Segmenten sie bestehen oder welche Felder diese
> Segmente führen. Siehe
> [`../../knowledge-base/20-verfahren/05-para105-sgbxi-pflege.md`](../../knowledge-base/20-verfahren/05-para105-sgbxi-pflege.md).
>
> Dieses Beispiel darf deshalb **nicht** als Referenz für die Erzeugung echter
> Abrechnungsdateien verwendet werden. Es ist eine Struktur-Attrappe mit korrekt
> gerechneten Prüfziffern und in sich konsistenten Zählern und Summen — geeignet, um
> Parser, Zählerlogik und Summenregeln zu entwickeln, bevor die TA 1 vorliegt.
>
> Spalte **Herkunft** in allen Tabellen unten sagt für jedes Feld, woran man ist.

## 1. Datenschutz

Alle Daten sind frei erfunden (REQ-DSGVO-03). Personennamen, Anschriften, KVNR, IK,
Rechnungs- und Beträge sind synthetisch; Prüfziffern wurden nach den in der
Wissensbibliothek dokumentierten Algorithmen gerechnet, damit die Werte formal gültig
sind. IK sind neunstellige Zahlen aus einem endlichen Wertebereich — eine zufällige
Übereinstimmung mit einem real vergebenen IK ist nicht ausschließbar und ohne Bedeutung.

## 2. Der abgebildete Fall

| | |
|---|---|
| **Leistungserbringer** | Ambulanter Pflegedienst Sonnenhof GmbH, Lindenweg 14, 12345 Musterstadt |
| **IK Leistungserbringer** | `261099874` |
| **Empfänger (Datenannahmestelle)** | `109999712` |
| **Belegannahmestelle** | `108999630` |
| **Kostenträger (Pflegekasse)** | `106999146` |
| **Abrechnungszeitraum** | 01.07.2026 – 31.07.2026 |
| **Rechnungsnummer / -datum** | `2026070001` / 05.08.2026 |
| **Dateierstellung** | 05.08.2026, 11:47 |
| **Abrechnungsfälle** | 2 Pflegebedürftige |
| **Rechnungsbetrag** | 1.671,00 EUR |
| **Umsatzsteuer** | steuerfrei (Pflegeleistungen nach SGB XI, § 4 Nr. 16 UStG) |

### Abrechnungsfall 001

| | |
|---|---|
| Versicherte | Hanna Kerzenmacher, geb. 12.03.1948 |
| KVNR | `K741852967` |
| Pflegegrad | 3 |

| Position | Bezeichnung | Menge | Einzelpreis | Betrag |
|---|---|---:|---:|---:|
| `LK03` | Grosse Morgentoilette | 20 | 24,50 | 490,00 |
| `LK15` | Hauswirtschaftliche Versorgung | 8 | 18,20 | 145,60 |
| | **Summe Fall 001** | | | **635,60** |

### Abrechnungsfall 002

| | |
|---|---|
| Versicherter | Otto Brinkmeier, geb. 27.11.1939 |
| KVNR | `M305921844` |
| Pflegegrad | 4 |

| Position | Bezeichnung | Menge | Einzelpreis | Betrag |
|---|---|---:|---:|---:|
| `LK04` | Kleine Morgentoilette mit Lagern | 31 | 28,90 | 895,90 |
| `LK31` | Wegepauschale | 31 | 4,50 | 139,50 |
| | **Summe Fall 002** | | | **1.035,40** |

Beide Beträge liegen unter dem jeweiligen monatlichen Sachleistungsbetrag des
Pflegegrades; ein Eigenanteil entsteht daher nicht und wird in diesem Beispiel auch
nicht modelliert. Leistungskomplexnummern (`LK…`) sind erfunden — real ergeben sie sich
aus dem jeweiligen Landesrahmenvertrag nach § 75 SGB XI.

## 3. Das Dateipärchen

| Datei | Inhalt | Größe |
|---|---|---|
| [`TPLG0001`](TPLG0001) | Nutzdaten (PLGA/PLAA), **Klartext** | 1002 Bytes |
| [`TPLG0001.AUF`](TPLG0001.AUF) | Auftragsdatei, Klartext, Festsatzformat | 128 Bytes |
| [`urbeleg-leistungsnachweis.html`](urbeleg-leistungsnachweis.html) | Urbeleg: Leistungsnachweise beider Abrechnungsfälle, druckbar | 2 Seiten |
| [`urbeleg-begleitzettel.html`](urbeleg-begleitzettel.html) | Begleitzettel für die Urbelege an die Belegannahmestelle | 1 Seite |

### Dateiname

```
  T   P L G   0    0 0 1
  │   └─┬─┘   │    └─┬─┘
  │     │     │      └──── Stellen 6–8: Transfernummer  "001"
  │     │     └─────────── Stelle 5:    Verfahrensversion  "0"
  │     └───────────────── Stellen 2–4: Verfahrenskennung  "PLG"   ❓ erfunden
  └─────────────────────── Stelle 1:    "T" = Testdaten
```

Aufbau nach [`knowledge-base/30-technik/02-kks-auftragsdatei-dateinamen.md`](../../knowledge-base/30-technik/02-kks-auftragsdatei-dateinamen.md).
Die Verfahrenskennung `PLG` ist **erfunden**: Die Werteliste steht in Anlage 4 GGT, die
noch nicht vorliegt — die Wissensbibliothek führt sie als „wichtigste einzelne
Referenzdatei" und als offene Lücke.

### Zwei bewusste Abweichungen von der Realität

| Abweichung | Grund |
|---|---|
| Die Nutzdatendatei ist **unverschlüsselt** | Real wäre `TPLG0001` der SECON-Umschlag (`EnvelopedData` über `SignedData`, Anlage 16 GGT). Hier liegt der **entschlüsselte Inhalt** unter dem Dateinamen, damit die Fixture ohne Schlüsselmaterial nutzbar ist. Prüfstufe 2 ist mit diesem Beispiel folglich **nicht** testbar. |
| Test-, nicht Echtdaten (`T`) | Beispieldaten gehören nie in den Echtdatenpfad. |

## 4. Auftragsdatei `TPLG0001.AUF`

Positionsbasiertes Festsatzformat, 128 Zeichen, keine Trennzeichen, keine Zeilenumbrüche,
rechts mit Leerzeichen aufgefüllt.

> ❗ **Das Satzlayout unten ist bis auf eine Zeile erfunden.** Belegt ist allein die
> Position der Verfahrenskennung (Stellen 20–24). Die vollständige Feldliste steht in
> **Anlage 2 GGT**, die nicht vorliegt; die Wissensbibliothek nennt Stufe 1 deshalb ohne
> dieses Dokument als „nicht implementierbar". Die Gesamtlänge 128 ist ein **Platzhalter**
> und entspricht mit hoher Wahrscheinlichkeit nicht der echten Satzlänge.

| Position | Länge | Feld | Wert | Herkunft |
|---|---:|---|---|---|
| 1–3 | 3 | `SATZART` | `AUF` | erfunden |
| 4–11 | 8 | `DATEINAME_NUTZDATEN` | `TPLG0001` | erfunden (Kopplung selbst belegt) |
| 12–19 | 8 | `ERSTELLUNGSDATUM` (JJJJMMTT) | `20260805` | erfunden |
| **20–24** | **5** | **`VERFAHREN_KENNUNG`** | `PLG0` + Blank | **Position belegt** ⚠️ [Q20] |
| 25 | 1 | `TEST_ECHT_KENNZEICHEN` | `T` | erfunden |
| 26–34 | 9 | `ABSENDER_EIGNER` (IK) | `261099874` | Feld belegt, Position erfunden ⚠️ [Q7] |
| 35–43 | 9 | `EMPFAENGER` (IK) | `109999712` | Feld belegt, Position erfunden ⚠️ [Q7] |
| 44–46 | 3 | `TRANSFER_NUMMER` | `001` | Feld belegt, Position erfunden ⚠️ [Q7] |
| 47–52 | 6 | `ERSTELLUNGSZEIT` (HHMMSS) | `114700` | erfunden |
| 53–60 | 8 | `NUTZDATEN_LAENGE` (Bytes) | `00001002` | erfunden |
| 61–64 | 4 | `ANZAHL_NACHRICHTEN` | `0003` | erfunden |
| 65–72 | 8 | `VERSION_REGELWERK` | `6.4.0` | erfunden (Version selbst belegt ✅ [Q22]) |
| 73–81 | 9 | `ABSENDER_PHYSIKALISCH` (IK) | `261099874` | erfunden |
| 82–128 | 47 | `RESERVE` | Leerzeichen | erfunden |

`ABSENDER_PHYSIKALISCH` trennt den physikalischen Absender vom Eigner der Nutzdaten —
bei Versand über ein Abrechnungszentrum fallen die beiden auseinander. Hier sind sie
identisch, der Pflegedienst versendet selbst.

### Belegter Widerspruch, den dieses Beispiel sichtbar macht

`VERFAHREN_KENNUNG` belegt **fünf** Stellen (20–24), Regel `S1-ALL-003` verlangt aber
Übereinstimmung mit den Stellen **2–5 des Dateinamens** — das sind nur **vier** Zeichen
(`PLG` + Version `0`). Das Beispiel füllt die fünfte Stelle mit einem Leerzeichen und
markiert die Frage damit, statt sie zu verstecken. Zu klären mit Anlage 2 und Anlage 4 GGT:
ob das Feld ein weiteres Zeichen führt, ob die Kennung fünfstellig ist, oder ob die
Positionsangabe in der Sekundärquelle ungenau ist.

## 5. Nutzdatendatei `TPLG0001`

Die Datei enthält **keine Zeilenumbrüche** — Segmente werden ausschließlich durch das
Segmentendezeichen `'` getrennt. Ein Parser darf sich nicht auf Zeilenstruktur verlassen
(manche Sender fügen zusätzlich CR LF ein; beides muss verarbeitbar sein). Zur besseren
Lesbarkeit hier umbrochen:

```
UNA:+.? '
UNB+UNOC:3+261099874+109999712+260805:1147+00001++PLGA++++1'
UNH+00001+PLGA:06:04:00'
FKT+01+261099874+109999712+106999146'
REC+2026070001:20260805+01'
UST+DE999999999+0.00+1'
SKO+0.00+0+30'
GES+1671.00+0.00+0.00+1671.00+EUR'
NAM+Ambulanter Pflegedienst Sonnenhof GmbH+Lindenweg 14+12345+Musterstadt'
UNT+8+00001'
UNH+00002+PLAA:06:04:00'
FKT+01+261099874+109999712+106999146'
REC+2026070001:20260805+01'
INV+K741852967+3+19480312'
NAD+Kerzenmacher:Hanna+Rosenweg 3+12345+Musterstadt'
ESK+001+20260701:20260731'
EPL+LK03+Grosse Morgentoilette+20+24.50+490.00'
EPL+LK15+Hauswirtschaftliche Versorgung+8+18.20+145.60'
GES+635.60+0.00+0.00+635.60+EUR'
UNT+10+00002'
UNH+00003+PLAA:06:04:00'
FKT+01+261099874+109999712+106999146'
REC+2026070001:20260805+01'
INV+M305921844+4+19391127'
NAD+Brinkmeier:Otto+Ahornstrasse 27+12345+Musterstadt'
ESK+002+20260701:20260731'
EPL+LK04+Kleine Morgentoilette mit Lagern+31+28.90+895.90'
EPL+LK31+Wegepauschale+31+4.50+139.50'
GES+1035.40+0.00+0.00+1035.40+EUR'
UNT+10+00003'
UNZ+3+00001'
```

### 5.1 Zeichensatz

Reines ASCII. **Umlaute und ß sind durchgängig transliteriert** (`Grosse` statt `Große`,
`Ahornstrasse` statt `Ahornstraße`) — bewusst, weil der zulässige Zeichensatz für
§ 105 SGB XI nicht belegt ist. Die Wissensbibliothek warnt ausdrücklich davor, die
§ 301-Vorgabe (DIN 66003 DRV 7-Bit / DIN 66303 8-Bit) auf andere Verfahren zu übertragen,
und weist darauf hin, dass DIN 66003 die Zeichen `[ \ ] { | } ~` durch `Ä Ö Ü ä ö ü ß`
ersetzt. Ein ASCII-only-Beispiel ist unter allen in Frage kommenden Kodierungen
byte-identisch und damit als Fixture unempfindlich gegen diese offene Frage.

Sobald der Zeichensatz geklärt ist, sollte **zusätzlich** eine Variante mit echten
Umlauten hinzukommen — die Kodierungsfalle ist genau der Fehler, den ein Validator
finden muss.

### 5.2 Trennzeichen (UNA)

| Zeichen | Funktion |
|---|---|
| `:` | Komponententrenner |
| `+` | Datenelementtrenner |
| `.` | Dezimalzeichen |
| `?` | Freigabezeichen |
| ` ` | reserviert |
| `'` | Segmentendezeichen |

Das sind die **EDIFACT-Defaults**, übernommen aus dem § 302-Beispiel der
Wissensbibliothek. Diese warnt jedoch explizit: ob die GKV-Verfahren die Defaults
verwenden oder abweichende Zeichen vorschreiben, ist **aus der jeweiligen Technischen
Anlage zu verifizieren und darf nicht angenommen werden**. Insbesondere das
Dezimalzeichen ist ein Kandidat für eine Abweichung (`,` statt `.`). Ein Parser muss die
Trennzeichen ohnehin **zur Laufzeit aus UNA lesen**, nicht hartkodieren — dann ist diese
Unsicherheit für ihn folgenlos.

### 5.3 Servicesegmente

| Segment | Element | Wert | Bedeutung | Herkunft |
|---|---|---|---|---|
| `UNB` | S001 | `UNOC:3` | Syntax-Kennung und -Version | erfunden |
| | S002 | `261099874` | Absenderkennung (IK) | Feld belegt ⚠️ [Q1] |
| | S003 | `109999712` | Empfängerkennung (IK) | Feld belegt ⚠️ [Q1] |
| | S004 | `260805:1147` | Datum:Zeit der Erstellung (JJMMTT:HHMM) | erfunden |
| | 0020 | `00001` | Datenaustauschreferenz | erfunden |
| | 0026 | `PLGA` | Anwendungsreferenz / Nachrichtentyp-Kennung | Feld belegt ⚠️ [Q1][Q30] |
| | 0035 | `1` | Testkennzeichen | erfunden |
| `UNH` | 0062 | `00001` … | Nachrichtenreferenznummer | EDIFACT-Standard |
| | S009 | `PLGA:06:04:00` | Typ : Version : Release : Organisation | Mapping erfunden |
| `UNT` | 0074 | `8` / `10` | Segmentanzahl inkl. UNH und UNT | EDIFACT-Standard |
| | 0062 | `00001` … | Referenz, identisch zum UNH | EDIFACT-Standard |
| `UNZ` | 0036 | `3` | Anzahl Nachrichten in der Datei | Segment belegt ⚠️ [Q1] |
| | 0020 | `00001` | Referenz, identisch zur UNB-Datenaustauschreferenz | erfunden |

Die Abbildung der TA-Version **6.4.0** auf `S009` als `06:04:00` ist eine Konstruktion —
die Patch-Stelle des SemVer-Schemas hat in `S009` keinen offensichtlichen Platz. Wie die
TA-Version tatsächlich in `UNH` kodiert wird, ist der TA 1 zu entnehmen. Das Testkennzeichen
`0035 = 1` ist redundant zu Stelle 1 des Dateinamens (`T`) und zu Position 25 der
Auftragsdatei — genau diese Redundanz macht eine verfahrensübergreifende Konsistenzprüfung
möglich (siehe Abschnitt 6).

### 5.4 Nachrichtentyp PLGA — Gesamtaufstellung

Segmentfolge `FKT`, `REC`, `UST`, `SKO`, `GES`, `NAM`. Diese sechs Kennungen sind für
**SLGA** (§ 302) belegt ⚠️ [Q1] und hier **analog** auf PLGA übertragen — die
Wissensbibliothek bezeichnet PLGA/PLAA als strukturelles Gegenstück zu SLGA/SLLA. Ob die
Kennungen in § 105 SGB XI identisch sind, ist **nicht belegt**. Die Feldbelegung
innerhalb der Segmente ist vollständig erfunden.

| Segment | Feld | Wert | Bedeutung |
|---|---:|---|---|
| `FKT` | 1 | `01` | Verarbeitungskennzeichen — hier: Erstabrechnung ❓ Werteliste unbelegt |
| | 2 | `261099874` | Absender-IK (Leistungserbringer) |
| | 3 | `109999712` | Empfänger-IK (Datenannahmestelle) |
| | 4 | `106999146` | Kostenträger-IK (Pflegekasse) |
| `REC` | 1.1 | `2026070001` | Rechnungsnummer |
| | 1.2 | `20260805` | Rechnungsdatum |
| | 2 | `01` | Rechnungsart |
| `UST` | 1 | `DE999999999` | USt-IdNr. des Leistungserbringers |
| | 2 | `0.00` | Steuersatz in Prozent |
| | 3 | `1` | Steuerbefreiungskennzeichen |
| `SKO` | 1 | `0.00` | Skontosatz |
| | 2 | `0` | Skontofrist in Tagen |
| | 3 | `30` | Zahlungsziel in Tagen |
| `GES` | 1 | `1671.00` | Rechnungsbetrag gesamt |
| | 2 | `0.00` | Zuzahlung |
| | 3 | `0.00` | Eigenanteil |
| | 4 | `1671.00` | Zahlbetrag an den Leistungserbringer |
| | 5 | `EUR` | Währung |
| `NAM` | 1–4 | | Name, Straße, PLZ, Ort des Leistungserbringers |

`VKZ = 01` für die Erstabrechnung ist eine **Annahme**. Belegt sind für § 302 nur `02`
(Nachforderung) und `4` (Wiedereinreichung nach Absetzung); die Wissensbibliothek merkt
zusätzlich an, dass die Notation in den Quellen uneinheitlich ist (`02` vs. `2`) und
Feldlänge wie Wertemenge zwingend aus dem Regelwerk zu übernehmen sind.

### 5.5 Nachrichtentyp PLAA — Abrechnungsdaten

Segmentfolge `FKT`, `REC`, `INV`, `NAD`, `ESK`, `EPL`*, `GES`. Herkunft der Kennungen:

| Segment | Kennung stammt aus | Feldbelegung |
|---|---|---|
| `FKT`, `REC`, `GES` | analog PLGA / SLGA ⚠️ | erfunden |
| `INV` | verfahrensübergreifendes Standardsegment ⚠️ [Q30] | erfunden |
| `NAD` | verfahrensübergreifendes Standardsegment ⚠️ [Q30] | erfunden |
| `ESK` | § 302 SLLA, „Einsatzkopfsegment" ⚠️ [Q1] | erfunden |
| `EPL` | **frei erfunden** ❓ | erfunden |

| Segment | Feld | Beispielwert | Bedeutung |
|---|---:|---|---|
| `REC` | 1 | `2026070001:20260805` | Bezug auf die Rechnung der PLGA |
| `INV` | 1 | `K741852967` | KVNR (unveränderbarer Teil, 10 Zeichen) |
| | 2 | `3` | Pflegegrad |
| | 3 | `19480312` | Geburtsdatum |
| `NAD` | 1 | `Kerzenmacher:Hanna` | Nachname : Vorname |
| | 2–4 | | Straße, PLZ, Ort |
| `ESK` | 1 | `001` | laufende Nummer des Abrechnungsfalls in der Datei |
| | 2 | `20260701:20260731` | Leistungszeitraum von : bis |
| `EPL` | 1 | `LK03` | Leistungskomplex- / Positionsnummer |
| | 2 | `Grosse Morgentoilette` | Klartextbezeichnung |
| | 3 | `20` | Menge |
| | 4 | `24.50` | Einzelpreis |
| | 5 | `490.00` | Gesamtpreis der Position |
| `GES` | 1–5 | | Summen des Abrechnungsfalls, Aufbau wie in PLGA |

**Bewusste Vereinfachung:** Die Leistungen sind je Leistungskomplex zu einer Monatsmenge
aggregiert. Real dürfte die TA 1 einen einsatzbezogenen Nachweis verlangen (Datum und
Uhrzeit je Hausbesuch) — dafür spricht schon der Name „Einsatzkopfsegment". Sobald die
TA 1 vorliegt, ist das der wahrscheinlichste Punkt, an dem dieses Beispiel strukturell
umgebaut werden muss.

## 5.6 Urbeleg — der Leistungsnachweis

[`urbeleg-leistungsnachweis.html`](urbeleg-leistungsnachweis.html) enthält den
**Papierbeleg** zur elektronischen Abrechnung: je Abrechnungsfall einen
Leistungsnachweis mit Tagesraster, Handzeichen der Pflegekraft, Zusammenstellung und
Unterschriftenfeldern. Im Browser öffnen und drucken (A4 quer, Seitenumbruch je Fall).

Fachlich ist das der **Urbeleg**: Der Pflegebedürftige bestätigt mit seiner Unterschrift
die erbrachten Einsätze. Er geht nicht an die Datenannahmestelle, sondern an die
**Belegannahmestelle** laut Kostenträgerdatei — ein zweiter, vom Dateipärchen getrennter
Weg. Die Kasse hält bei Prüfung den Beleg gegen die elektronische Abrechnung.

### Deckungsgleichheit mit der DTA-Datei

Der Beleg ist so erzeugt, dass er auf jeder Ebene zur Nutzdatendatei passt:

| Prüfung | Beleg | `TPLG0001` |
|---|---|---|
| Handzeichen im Tagesraster | 20 / 8 / 31 / 31 | Mengen in den `EPL`-Segmenten |
| Zusammenstellung je Fall | 635,60 / 1.035,40 | `GES` der beiden PLAA |
| Summe beider Fälle | 1.671,00 | `GES` der PLGA |
| Versichertennummern | `K741852967`, `M305921844` | `INV`-Segmente |
| Rechnungsbezug | Nr. 2026070001 vom 05.08.2026 | `REC` |

Damit lässt sich der Abgleich Urbeleg ↔ Abrechnung als Testfall abbilden — die Prüfung,
die eine Kasse bei Stichprobe oder Absetzung tatsächlich vornimmt.

### Der Einsatzkalender erzählt den Fall

Die Einsatztage sind kein Zufall, sondern erklären die abgerechneten Mengen:

- **Fall 001:** Juli 2026 hat 23 Werktage, abgerechnet sind aber nur 20 Einsätze. Die
  Differenz steht als Bemerkung auf dem Beleg — 13.–15.07. stationärer
  Krankenhausaufenthalt, in dieser Zeit ruht die häusliche Pflege. Die hauswirtschaftliche
  Versorgung läuft zweimal wöchentlich (Di/Fr), abzüglich des Dienstags im
  Krankenhauszeitraum: 8 statt 9.
- **Fall 002:** tägliche Versorgung, 31 Tage, dazu 31 Wegepauschalen — eine je Anfahrt.

Eine Abrechnung, deren Menge größer ist als die Zahl der Einsätze auf dem Beleg, ist
genau der Fall, den eine Kasse absetzt.

### Belastbarkeit

**Der Aufbau des Belegs ist erfunden.** Für § 302 SGB V definieren Anlage 4 den
Begleitzettel und Anlage 5 den Inhalt der Urbelege; für § 105 SGB XI ist in der
Wissensbibliothek **kein** Dokument zum Urbeleg-Inhalt erfasst. Form, Felder und
Tagesraster orientieren sich an der Praxis ambulanter Pflegedienste, nicht an einem
Regelwerk. Die Leistungskomplexnummern stammen wie in der DTA-Datei aus keinem realen
Landesrahmenvertrag.

Nicht enthalten ist der **Begleitzettel für Urbelege**, mit dem ein Stapel Belege der
Belegannahmestelle zugeordnet wird — für § 105 SGB XI ist auch dessen Aufbau nicht belegt.

### Eine bewusste Abweichung zwischen Beleg und Datei

Der Beleg schreibt **Große Morgentoilette** und **Ahornstraße**, die Nutzdatendatei
**Grosse Morgentoilette** und **Ahornstrasse**. Das ist kein Fehler, sondern die
Zeichensatzfrage aus Abschnitt 5.1 in ihrer praktischen Form: Auf Papier gibt es keine
Kodierungsbeschränkung, in der EDIFACT-Datei ist der zulässige Zeichensatz für
§ 105 SGB XI unbelegt. Ein Validator darf einen Feldvergleich zwischen beiden Welten
deshalb nicht zeichenweise führen, ohne die Transliteration zu berücksichtigen.

## 5.7 Urbeleg — der Begleitzettel

[`urbeleg-begleitzettel.html`](urbeleg-begleitzettel.html) ist das Deckblatt der
Papiersendung: eine Seite A4 hoch, die den Stapel Leistungsnachweise an die
Belegannahmestelle begleitet.

### Wofür er da ist

Die Abrechnung läuft über **zwei getrennte Wege**, die erst beim Kostenträger wieder
zusammenfinden:

```
                          verschlüsseltes Dateipärchen
  Pflegedienst  ─────────────────────────────────────►  Datenannahmestelle  109999712
   261099874                TPLG0001 + .AUF                       │
        │                                                         │
        │             Urbelege + Begleitzettel                    ▼
        └──────────────────────────────────────────►  Belegannahmestelle   108999630
                          Papier, Briefpost                       │
                                                                  ▼
                                                       Kostenträger 106999146
                                                       führt beides zusammen
```

Der Begleitzettel ist die **Klammer** zwischen beiden Wegen. Er trägt genau die
Merkmale, über die sich Papier und Datei verbinden lassen: Rechnungsnummer, Dateiname
und Transfernummer. Fehlt er, liegt ein Stapel unsortierter Belege bei der Kasse, dem
niemand eine Rechnung zuordnen kann.

Drei Rollen, drei verschiedene IK — Datenannahmestelle, Belegannahmestelle und
Kostenträger sind in der Kostenträgerdatei getrennt geführt und **nicht zwingend
dieselbe Stelle**. Das Beispiel besetzt sie deshalb mit drei unterschiedlichen,
prüfziffernkorrekten IK, damit eine Implementierung die Rollen nicht versehentlich
gleichsetzt.

### Zwei Deckblätter, gegensätzliche Datenschutzregeln

Der interessanteste Kontrast im ganzen Beispiel:

| | Auftragsdatei `TPLG0001.AUF` | Begleitzettel |
|---|---|---|
| begleitet | die elektronische Datei | den Papierstapel |
| geht an | Datenannahmestelle | Belegannahmestelle |
| Sozialdaten | **verboten** (`S1-ALL-008`) | **enthalten** — Namen, KVNR, Pflegegrad |

Beides sind Deckblätter, und die Regel ist genau umgekehrt. Der Grund liegt im
Transportweg: Die Auftragsdatei wird **unverschlüsselt** übertragen, damit die
Datenannahmestelle vor der Entschlüsselung routen kann — deshalb das Trennungsgebot.
Der Begleitzettel liegt im verschlossenen Umschlag bei Belegen, die die Sozialdaten
ohnehin enthalten.

### Erzeugt aus den Metadaten

Anders als die übrigen Dateien ist der Begleitzettel **aus
[`beispiel-metadaten.yaml`](beispiel-metadaten.yaml) generiert**, nicht von Hand
geschrieben. Beteiligte, Rechnungsdaten, Fallliste und Summe stammen aus der YAML —
damit kann er nicht von der DTA-Datei abweichen.

### Belastbarkeit

**Der Aufbau ist erfunden.** Die Wissensbibliothek führt für § 302 SGB V *Anlage 4 —
Begleitzettel für Urbelege* mit Quelle und URL ✅ [Q36], aber mit `beschafft: false`;
für § 105 SGB XI ist kein entsprechendes Dokument erfasst. Ein Beschaffungsversuch
während der Erstellung scheiterte an der Netzwerk-Policy der Arbeitsumgebung — die
URL steht im [Dokumentenregister](../../knowledge-base/data/dokumentenregister.yaml)
und ist weiterhin abzurufen. Felder, Reihenfolge und Sendungsnummer sind an der Praxis
orientiert, nicht an Anlage 4.

## 6. Was dieses Beispiel prüfbar macht

Regel-IDs nach
[`knowledge-base/50-anforderungen/02-validierungsregeln.md`](../../knowledge-base/50-anforderungen/02-validierungsregeln.md).
Das Beispiel ist so gebaut, dass es diese Regeln **erfüllt** — es taugt als Positivfall
für eine Implementierung.

| Regel | Prüft | Im Beispiel |
|---|---|---|
| `S0-ALL-001` | Dateipärchen vollständig | beide Dateien vorhanden |
| `S0-ALL-002` | Auftragsdatei endet auf `.AUF` | ✔ |
| `S0-ALL-003` | erste 8 Stellen identisch | `TPLG0001` / `TPLG0001.AUF` |
| `S0-ALL-004` | Stelle 1 ∈ {T, E} | `T` |
| `S0-ALL-007` | Stellen 6–8 numerisch | `001` |
| `S1-ALL-004/005` | Absender- und Empfänger-IK gültig | Prüfziffern korrekt |
| `S1-ALL-007` | Transfernummer = Stellen 6–8 des Dateinamens | `001` = `001` |
| `S1-ALL-008` | Auftragssatz ohne Sozialdaten | keine KVNR, keine Namen |
| `S3-ALL-001` | UNA enthält genau sechs Trennzeichen | ✔ |
| `S3-ALL-002` | Datei beginnt mit UNB, endet mit UNZ | ✔ |
| `S3-ALL-003` | UNZ-Zähler = Anzahl Nachrichten | `3` = 3 |
| `S3-ALL-004` | UNT-Zähler = Segmentanzahl | 8 / 10 / 10 |
| `S3-ALL-005` | Referenzen UNB↔UNZ und UNH↔UNT paarweise gleich | ✔ |
| `S3-ALL-006` | Zeichensatz | reines ASCII |
| `S3-XI-001` | nur PLGA und PLAA in der Datei | ✔ |
| `S4-ALL-001` | IK 9-stellig mit korrekter Prüfziffer | 3 IK, alle gültig |
| `S4-ALL-002` | KVNR `^[A-Z][0-9]{9}$` mit Prüfziffer | 2 KVNR, beide gültig ❓ Algorithmus |
| `S4-ALL-003` | Datumsfelder formal gültig | ✔ |
| `S5-ALL-001` | Absender-IK Auftragssatz = Absender-IK Nutzdaten | `261099874` in beiden |
| `S5-302-001` analog | zu jeder PLGA mindestens eine PLAA | 1 PLGA, 2 PLAA |
| `S5-302-002` analog | Rechnungsbezug PLGA↔PLAA auflösbar | `REC` identisch in allen drei Nachrichten |
| `S5-302-003` analog | Gesamtbetrag = Summe der Positionen | 635,60 + 1.035,40 = 1.671,00 |
| `S5-302-004` analog | Positionsbetrag = Menge × Einzelpreis | alle 4 Positionen |
| `S5-302-007` analog | keine doppelte Rechnungsnummer | eine Rechnung |
| `S6-ALL-001` | Leistungsdatum ≤ Rechnungsdatum | 31.07. ≤ 05.08. |
| `S6-ALL-002` | Rechnungsdatum ≤ Erstellungsdatum | 05.08. = 05.08. |

### Eine Falle, in die dieses Beispiel tappen lässt

`S1-ALL-008` (keine Sozialdaten im Auftragssatz) verführt zu einer Umsetzung als
Mustersuche über den ganzen Satz. Das schlägt fehl: Ein `^[A-Z][0-9]{9}$`-Muster findet
im Auftragssatz zwei Treffer — `T261099874` (Stelle 25 Test-/Echt-Kennzeichen plus
Stellen 26–34 Absender-IK) und `G000120260` (Ende des Dateinamens plus Anfang des
Erstellungsdatums). Beides sind **Feldgrenzen**, keine Versichertennummern; echte
Sozialdaten enthält der Satz nicht.

Die Regel ist deshalb erst **nach dem Parsen** feldweise auszuwerten, nie als Regex über
den Rohsatz. Bei einem positionsbasierten Festsatzformat ohne Trennzeichen erzeugt jede
Feldgrenze Zeichenfolgen, die es als Wert nie gibt.

Zusätzlich prüfbar, weil im Beispiel dreifach redundant kodiert: das
**Test-/Echt-Kennzeichen** — Dateiname Stelle 1 (`T`), Auftragssatz Position 25 (`T`),
UNB-Element 0035 (`1`). Die Wissensbibliothek führt diese Konsistenzprüfung als
Prüfregel-Kandidaten mit noch zu verifizierender Feldzuordnung.

**Nicht** mit diesem Beispiel prüfbar: die gesamte **Stufe 2** (Kryptografie), weil die
Nutzdaten im Klartext vorliegen, sowie alle Regeln, die eine Kostenträgerdatei oder ein
Positionsnummernverzeichnis voraussetzen (`S1-ALL-006`, `S4-302-002/003`).

## 7. Prüfziffern — Nachrechnen

| Wert | Kern | Prüfziffer |
|---|---|---|
| IK `261099874` | Stellen 3–8 = `109987` | `4` |
| IK `109999712` | Stellen 3–8 = `999971` | `2` |
| IK `106999146` | Stellen 3–8 = `699914` | `6` |
| IK `108999630` | Stellen 3–8 = `899963` | `0` |
| KVNR `K741852967` | `11` + `74185296` | `7` |
| KVNR `M305921844` | `13` + `30592184` | `4` |

Die **IK-Prüfziffern** folgen dem in
[`knowledge-base/40-stammdaten/01-institutionskennzeichen.md`](../../knowledge-base/40-stammdaten/01-institutionskennzeichen.md)
dokumentierten Modulo-10-Verfahren über die Stellen 3–8 (Gewichte 2·1·2·1·2·1 von links,
Produkte > 9 minus 9). Die Wissensbibliothek verlangt, dieses Verfahren vor produktivem
Einsatz gegen das Gemeinsame Rundschreiben der ARGE·IK zu verifizieren.

Die **KVNR-Prüfziffern** verwenden die in
[`knowledge-base/40-stammdaten/02-krankenversichertennummer.md`](../../knowledge-base/40-stammdaten/02-krankenversichertennummer.md)
als **Annahme** gekennzeichnete Variante: Buchstabe → zweistellige Zahl (A = 01 … Z = 26),
Modulo 10 mit Gewichtung 1·2·1·2·… über alle zehn Ziffern. **Wie der führende Buchstabe
tatsächlich eingeht, ist unbelegt.** Ändert die KVNR-Richtlinie V3.4.0 diese Annahme,
sind beide KVNR neu zu rechnen.

Beide Algorithmen sind als Pseudocode in den verlinkten Dokumenten hinterlegt.

## 8. Wenn die TA 1 Version 6.4.0 vorliegt

Reihenfolge der Korrekturen an diesem Beispiel, nach Hebelwirkung sortiert:

1. **Segmentkennungen und -reihenfolge** von PLGA/PLAA gegen die TA 1 ersetzen —
   insbesondere `EPL` (frei erfunden) und die Frage, ob PLAA einsatzbezogen statt
   monatsaggregiert aufgebaut ist.
2. **Feldbelegung** aller Segmente ersetzen; Feldlängen, Datentypen, Pflichtfeldstatus
   und Betragsformat (Nachkommastellen, Vorzeichen, Dezimalzeichen) übernehmen.
3. **Trennzeichen** aus der TA 1 bestätigen oder korrigieren — vor allem das Dezimalzeichen.
4. **Zeichensatz** klären und eine Umlaut-Variante des Beispiels ergänzen.
5. **Verfahrenskennung** aus Anlage 4 GGT einsetzen (ersetzt `PLG`, betrifft beide
   Dateinamen und Position 20–24 der Auftragsdatei).
6. **Auftragssatz-Layout** aus Anlage 2 GGT ersetzen (ersetzt Abschnitt 4 vollständig,
   inklusive der Satzlänge).
7. **Verarbeitungskennzeichen** aus dem Schlüsselverzeichnis bestätigen (`01`).
8. **Urbelege** — Leistungsnachweis und Begleitzettel — gegen die Vorgaben für
   § 105 SGB XI prüfen; als nächstliegende Referenz Anlage 4 zu § 302 SGB V beschaffen
   ([Q36], im Dokumentenregister als `beschafft: false` geführt).
9. `vertrauen`-Felder in [`beispiel-metadaten.yaml`](beispiel-metadaten.yaml) anheben.

Beschaffungsstand siehe
[`knowledge-base/60-projekt/02-roadmap-und-offene-punkte.md`](../../knowledge-base/60-projekt/02-roadmap-und-offene-punkte.md).
