# Anleitung: Von den Urbelegen zur DTA-Datei — Erfassung in einer Eingabemaske

Diese Anleitung beschreibt, wie aus den Urbelegen dieses Beispiels
([`urbeleg-leistungsnachweis.html`](urbeleg-leistungsnachweis.html),
[`urbeleg-begleitzettel.html`](urbeleg-begleitzettel.html)) das Dateipärchen
[`TPFL0001`](TPFL0001) / [`TPFL0001.AUF`](TPFL0001.AUF) entsteht — **erfasst in einer
Maske**, nicht von Hand getippt.

Sie richtet sich an zwei Leserkreise:

- **Wer eine Erfassungssoftware baut**: Maskenschnitt, Feldherkunft, Prüfzeitpunkte.
- **Wer den Validator baut**: die Maske ist die Fehlerquelle, gegen die er anläuft. Jede
  der sieben [Negativfixtures](../pflege-105-sgbxi-negativfaelle/) lässt sich auf einen
  Maskenfehler zurückführen — Abschnitt 9 macht das explizit.

> ## Belastbarkeit
>
> **Der Maskenschnitt in dieser Anleitung ist erfunden.** Kein ausgewertetes
> Primärdokument schreibt eine Benutzeroberfläche vor; die Technischen Anlagen regeln das
> Ergebnis, nicht den Weg dorthin. Alles, was hier als Bildschirm, Reihenfolge, Tastenweg
> oder Ergonomie beschrieben ist, ist ein begründeter Vorschlag (⚠️).
>
> **Belegt (✅) ist das, worauf sich die Maske stützt**: der Feldkatalog des
> Auftragssatzes (Anlage 2 GGT), die Segmentgrammatik und Feldbelegung der PLGA/PLAA
> (TA 1 Pflege 6.4.0), die Schlüsselverzeichnisse (TA 3 6.4.0) und der Regelkatalog in
> [`pruefregeln.yaml`](../../knowledge-base/data/pruefregeln.yaml). Wo eine Maskenregel
> unmittelbar aus einer Prüfregel folgt, steht die Regel-ID daneben.
>
> **Nicht belegt (❓)** ist der Aufbau der Papierbelege selbst — siehe README des
> Beispiels, Abschnitt 6. Diese Anleitung nimmt die Belege so, wie sie hier liegen.

---

## 1. Die Ausgangslage: zwei Belege, zwei völlig verschiedene Rollen

Der häufigste Denkfehler beim Maskenschnitt ist, beide Urbelege als Eingabe zu behandeln.
Sie sind es nicht:

| Beleg | Rolle | Konsequenz für die Maske |
|---|---|---|
| **Leistungsnachweis** | **Eingabe.** Unterschrieben vom Pflegebedürftigen, trägt die Handzeichen der Pflegekräfte. Er ist der Rechtsgrund der Abrechnung. | Die Erfassungsmaske bildet ihn nach — Zeile für Zeile, Tag für Tag. |
| **Begleitzettel** | **Ausgabe.** Er enthält keine einzige Information, die nicht schon anderswo erfasst wäre: Rechnungsnummer, Dateiname, Transfernummer, Fallliste, Summe. | Die Maske fragt ihn **nicht ab**, sie **druckt** ihn — aus demselben Datenbestand wie die DTA-Datei. |

Daraus folgt die erste Konstruktionsregel:

> **Der Begleitzettel wird erzeugt, nicht erfasst.** Wer ihn tippen lässt, baut sich eine
> zweite Wahrheit neben die Datei — und damit genau die Abweichung, die die
> Belegannahmestelle findet.

Der Leistungsnachweis wiederum bringt genau **einen** Abrechnungsfall mit. Zwei Belege,
zwei `INV`-Blöcke in der PLAA. Die Zuordnung ist die Belegnummer (`2607001`, `2607002`),
die auf dem Papier steht, weil die TA 1 das ausdrücklich verlangt.

---

## 2. Drei Sorten Felder — und nur eine wird getippt

Bevor irgendein Bildschirm entworfen wird, ist jedes Feld der Zieldatei einer von drei
Klassen zuzuordnen. Das entscheidet mehr über die Fehlerquote als jedes Layout.

| Klasse | Herkunft | Beispiele | Regel |
|---|---|---|---|
| **S — Stammdaten** | einmalig gepflegt, danach nur noch ausgewählt | IK Leistungserbringer, Abrechnungscode, Tarifkennzeichen, USt-Angaben, Kostenträger-IK, Preisliste | wird pro Abrechnungslauf **nicht angefasst** |
| **E — Erfassung** | steht auf dem Leistungsnachweis, sonst nirgends | Einsatztage, Uhrzeit, Handzeichen, Bemerkungen | der **einzige** Tippbereich |
| **A — Abgeleitet** | rechnet die Software, immer | alle Beträge, Segmentzähler, Dateigröße, Prüfziffern, Dateinamen, Transfernummer, Anzahl-Felder | **darf nicht eingebbar sein** |

Die vollständige Zuordnung für dieses Beispiel:

| Zielfeld (Segment.DE) | Wert im Beispiel | Klasse | Quelle |
|---|---|---|---|
| `UNB` Absender | `461100877` | S | Betriebsstammdaten |
| `UNB` Empfänger | `661100423` | S | Kostenträgerdatei → Datenannahmestelle |
| `UNB` Datum/Uhrzeit | `20260805:1147` | A | Systemzeit beim Erzeugen |
| `UNB` Anwendungsreferenz | `PL076001SBK` | A | aus Monat, lfd. Nr., Kassenart gerechnet |
| `UNB` Dateiindikator | `0` | S | Betriebsmodus Test/Echt |
| `FKT` Verarbeitungskennzeichen | `01` | S | Vorgabe „Original" |
| `FKT` IK Leistungserbringer / Kostenträger / Pflegekasse | `461100877` / `109524616` / `189524616` | S | Stammdaten + Kassenauswahl am Fall |
| `REC` Rechnungsnummer | `2026070001:0` | A | Nummernkreis, Einzel-Nr. `0` bei Selbstabrechnern |
| `REC` Rechnungsdatum | `20260805` | E | ein Feld im Laufkopf |
| `REC` Rechnungsart | `1` | S | Vorgabe des Betriebs |
| `REC` Währung | `EUR` | S | Konstante |
| `SRD` Abrechnungscode : Tarifkennzeichen | `36:23000` | S | Betriebsstammdaten |
| `SRD` Leistungsart | `01` | S | Vorgabe des Betriebs |
| `UST` Ordnungsnummer / Befreiung / Grund | `DE999999999` / `J` / `01` | S | Betriebsstammdaten |
| `GES` Gesamtrechnungsbetrag | `1671,00` | A | Σ der `IAF` |
| `NAM` Name / Kontakt | `Pflegedienst Sonnenhof GmbH` | S | Betriebsstammdaten, **max. 30 Stellen** |
| `INV` Versicherten-Nummer | `K741852967` | S | Fallstammdaten |
| `INV` Belegnummer | `2607001` | A | Nummernkreis je Fall und Monat |
| `NAD` Name/Vorname/Geburtsdatum/Anschrift | `Kerzenmacher+Hanna+19480312+…` | S | Fallstammdaten |
| `MAN` Abrechnungsmonat | `202607` | A | aus dem Laufkopf |
| `MAN` Pflegegrad | `3` | S | Fallstammdaten (bescheidgebunden) |
| `ESK` Kennzeichen der Leistungserbringung | `01`, `02`, … | **E** | **Tagesraster** |
| `ESK` Uhrzeit | `0715` | E | Vorgabewert am Fall, je Tag überschreibbar |
| `ELS` Leistungsziffer | `01:01:1:003` | S | Leistungskatalog (Auswahl, nie Freitext) |
| `ELS` Einzelpreis | `24,50` | S | Preisliste zum Leistungsdatum |
| `ELS` Punktwert / Punktzahl | leer | A | ergibt sich aus der Vergütungsart |
| `ELS` Dauer/Kilometer | `00` | A | Konstante bei Vergütungsart 01 und Wegegebühren-Art 01–03 |
| `ELS` Anzahl | `1,00` | A | 1 je Einsatz, sofern nicht ausdrücklich mehrfach |
| `ELS` Beschäftigtennummer | `999999998` | S | Mitarbeiterstamm, über das **Handzeichen** aufgelöst |
| `IAF` Beträge | `635,60+++635,60` | A | Σ der `ELS` des Falls |
| `UNT` / `UNZ` Zähler | `8`, `153`, `2` | A | beim Serialisieren gezählt |
| Auftragssatz, alle 37 Felder | — | A + S | siehe Abschnitt 7 |

**Nichts in der Spalte „A" bekommt ein Eingabefeld.** Nicht ausgegraut, nicht
schreibgeschützt — gar nicht erst als Feld. Ein ausgegrautes Feld lädt zum
„ausnahmsweise doch überschreiben" ein, und genau daraus entstehen die Negativfälle
`n2` (`UNT`-Zähler) und `n3` (Summenabweichung).

---

## 3. Warum ein Tagesraster und kein Mengenfeld

Auf dem Leistungsnachweis steht in der Spalte ganz rechts eine `20`. Die Versuchung ist
groß, in der Maske ein Feld „Anzahl" anzubieten und dort `20` einzutippen. Das ist der
Fehler, an dem die Vorfassung dieses Beispiels gescheitert ist (siehe README, Abschnitt
5.5).

Die TA 1 verlangt **ein `ESK`-Segment je Leistungseinsatz** und darunter die einzelnen
`ELS`. Aus „20 × Große Morgentoilette" werden 20 Einsatzkopfsegmente. Die `20` auf dem
Papier ist keine Eingabe, sondern eine **Quersumme des Tagesrasters** — und damit
ideal als Kontrollwert.

```
  Papier                          Maske                        Datei
  ┌──────────────────┐            ┌──────────────────┐         ┌──────────────┐
  │ MB MB MB – – MB… │  ───────►  │ [x][x][x][ ][ ]… │ ──────► │ ESK+01+0715' │
  │           Anz. 20│            │  erfasst: 20     │         │ ESK+02+0715' │
  └──────────────────┘            │  Beleg:    20  ✓ │         │ ESK+03+0715' │
        Handzeichen               └──────────────────┘         │      …       │
        je Tag                      Quersumme, kein Feld       └──────────────┘
```

Zweiter Grund für das Raster: Die Abwesenheit vom 13.–15.07. ist auf dem Beleg ein
`–`, kein Loch. Ein Mengenfeld verliert die Information, **welche** Tage fehlen; das
Raster hält sie fest — und macht die Bemerkung „stationärer Krankenhausaufenthalt"
prüfbar gegen die Lücke.

---

## 4. Der Maskenschnitt: vier Ebenen

Die Ebenen unterscheiden sich in ihrer **Änderungsfrequenz**. Was sich selten ändert,
darf nicht im Weg stehen, wenn monatlich 60 Belege zu erfassen sind.

| Ebene | Maske | Frequenz | Füllt |
|---|---|---|---|
| **A — Betrieb** | M1 Betriebsstammdaten | einmalig | `NAM`, `SRD`, `UST`, `FKT`-IK, Auftragssatz-Absender |
| | M2 Kassen und Annahmestellen | bei Kostenträgerdatei-Update | `FKT`-IK Kostenträger/Pflegekasse, `UNB`-Empfänger, Belegannahmestelle |
| | M3 Leistungskatalog und Preise | je Vergütungsvereinbarung | `ELS` Leistungsziffer, Einzelpreis |
| | M4 Mitarbeiter | bei Ein-/Austritt | `ELS` Beschäftigtennummer |
| **B — Fall** | M5 Pflegebedürftige | bei Aufnahme, Bescheidänderung | `INV`, `NAD`, `MAN` |
| **C — Lauf** | M6 Abrechnungslauf anlegen | monatlich, einmal | `REC`, Laufkopf |
| | **M7 Einsatzerfassung** | **monatlich, je Fall** | **`ESK`, `ELS`** |
| | M8 Fallabschluss | je Fall | `IAF`, Kontrollsumme |
| **D — Ausgabe** | M9 Lauf prüfen und freigeben | monatlich | `GES`, Regelprüfung |
| | M10 Erzeugen und versenden | monatlich | Dateipärchen, Begleitzettel |

Nur **M7** wird pro Beleg berührt. Alles andere ist Vorbereitung oder Abschluss.

### 4.1 M1 — Betriebsstammdaten

```
┌─ Betriebsstammdaten ─────────────────────────────────────────────────────┐
│                                                                          │
│  Name (Segment NAM, max. 30) [Pflegedienst Sonnenhof GmbH    ] 27/30     │
│  Straße, Nr.                 [Lindenweg 14                   ]           │
│  PLZ, Ort                    [12345] [Musterstadt            ]           │
│                                                                          │
│  IK Leistungserbringer       [461100877]  ✓ Prüfziffer 7                 │
│                              Klassifikation 46 — Pflegeberufe  ✓         │
│  Kontakt (NAM DE 2)          [Abrechnung 030 5550123         ]           │
│                                                                          │
│  Abrechnungscode             [36 ▾] privat gewerblicher Anbieter         │
│  Tarifkennzeichen            [23000]  Tarifbereich 23 Berlin             │
│  Leistungsart                [01 ▾] ambulante Pflege                     │
│  Rechnungsart                [1  ▾] Zahlung an IK Leistungserbringer     │
│                                                                          │
│  USt-Ordnungsnummer          [DE999999999]                               │
│  Umsatzsteuerbefreit         [x] Grund [01 ▾] § 4 Nr. 16 UStG            │
│                                                                          │
│  Betriebsmodus               ( ) Echtdaten   (x) Testdaten               │
└──────────────────────────────────────────────────────────────────────────┘
```

Drei Details, die hier über den späteren Dateiinhalt entscheiden:

- **Die Längenanzeige `27/30` ist kein Komfort, sondern eine Prüfung.**
  `PLGA.NAM.Name 1` ist auf 30 Stellen begrenzt. Die naheliegende Langform „Ambulanter
  Pflegedienst Sonnenhof GmbH" hat 38 Zeichen. Wer sie erst beim Erzeugen abschneidet,
  liefert einen anderen Namen aus, als im Betriebsstamm steht. Die Maske muss bei 30
  hart begrenzen und die Kürzung sichtbar machen.
- **Die IK-Prüfziffer wird sofort gerechnet** (`S4-ALL-001`), über die **Stellen 3–8**.
  Zusätzlich lohnt die Anzeige der Klassifikation: `46` ist ein Pflegedienst, `26` wäre
  ein Krankenhaus. Ein IK mit plausibler Prüfziffer, aber falscher Klassifikation ist der
  Fehler, den die Vorfassung dieses Beispiels enthielt.
- **Der Betriebsmodus ist ein Schalter, kein Feld.** Er steuert später *drei* Stellen
  gleichzeitig: Dateiname Stelle 1 (`T`/`E`), `VERFAHREN_KENNUNG` Stelle 20, und den
  `UNB`-Dateiindikator (`0`/`1`/`2`). Diese drei sind **nicht** gleich zu setzen — es
  gilt `T` ↔ {`0`,`1`} und `E` ↔ {`2`}. Genau deshalb gehört die Ableitung in den Code
  und nicht in die Maske.

### 4.2 M2 — Kassen und Annahmestellen

```
┌─ Kostenträger / Kassen ──────────────────────────────────────────────────┐
│  Kostenträger    [Muster BKK                 ]  IK [109524616] ✓         │
│  Kassenart       [BK ▾] Betriebskrankenkassen                            │
│  Pflegekasse     [Pflegekasse bei der Muster BKK] IK [189524616] ✓       │
│                  ⚠ IK der Pflegekasse muss mit 18 beginnen — erfüllt     │
│  Datenannahmest. [661100423] ✓   Belegannahmest. [661100559] ✓           │
│                  Postfach 11 22, 12345 Musterstadt                       │
└──────────────────────────────────────────────────────────────────────────┘
```

Vier IK, vier Rollen, **keine davon ist mit einer anderen identisch**. Die Maske muss
sie getrennt führen (`S4-XI-002` für die `18`-Regel). Die Versuchung, Datenannahmestelle
und Belegannahmestelle zusammenzulegen, weil sie „ja beide zur Kasse gehören", zerstört
die Adressierung der Papiersendung.

Der Fall Kostenträger `109524616` / Pflegekasse `189524616` ist die Testfalle des
Beispiels: Beide tragen dieselbe Prüfziffer `6`, weil sie sich nur in der
Klassifikation unterscheiden und die Prüfziffer nur aus den Stellen 3–8 gebildet wird.
Eine Maske, die über die Stellen 1–8 rechnet, weist hier **beide** zurück.

### 4.3 M3 — Leistungskatalog

Die Leistungsziffer ist **zusammengesetzt** und wird nie als Ganzes getippt:

```
┌─ Leistungskatalog · Position anlegen ────────────────────────────────────┐
│  Art der abgegebenen Leistung  [01 ▾] ambulante Pflege        (Schl. 2.4)│
│  Vergütungsart                 [01 ▾] Leistungskomplex        (Schl. 2.5)│
│  Qualifikationsabh. Vergütung  [1  ▾] Pflegefachkraft         (Schl. 2.6)│
│  Leistung                      [003]  ← Schlüssel 2.7.1, 3-stellig       │
│                                   ▲ Abschnitt folgt aus der Vergütungsart│
│  Klartext (nur für Beleg/Liste) [Große Morgentoilette              ]     │
│  Einzelpreis                    [    24,50] EUR   gültig ab [01.01.2026] │
│  Koppelleistung je Einsatz      [—      ▾]                               │
│                                                                          │
│  Ergibt Leistungsziffer:  01:01:1:003                                    │
└──────────────────────────────────────────────────────────────────────────┘
```

- **Die vierte Komponente hängt von der zweiten ab** (`S4-XI-006`): Vergütungsart `01`
  löst nach Schlüssel 2.7.1 auf (3 Stellen), Vergütungsart `06` nach 2.7.5 (2 Stellen).
  Die Wegepauschale des zweiten Falls ist deshalb `01:06:0:03` und nicht `01:06:0:003`.
  Die Maske muss die Auswahlliste des vierten Feldes **nach der Wahl der Vergütungsart
  umschalten** — sonst entsteht eine formal gültige, fachlich falsche Ziffer.
- **`Koppelleistung je Einsatz`** ist der Grund, warum im zweiten Fall niemand 31
  Wegepauschalen einzeln anhakt: Am Leistungskomplex `004` wird `06/03` als Koppelleistung
  hinterlegt, und die Erfassung erzeugt sie automatisch je Einsatz. 31 Einsätze, 31
  Wegepauschalen — ohne einen einzigen zusätzlichen Tastendruck.
- **Der Klartext geht nie in die Datei.** „Große Morgentoilette" steht auf dem Papier,
  in der EDIFACT-Datei steht nur `003`. Der Katalog ist die einzige Stelle, an der beide
  Welten verbunden sind — ein Feldvergleich zwischen Beleg und Datei ist deshalb ein
  Auflösen über den Katalog, kein Textvergleich.

### 4.4 M4 — Mitarbeiter: das Handzeichen ist der Schlüssel

Auf dem Beleg stehen `MB`, `TK`, `SR`. In der Datei steht eine neunstellige
Beschäftigtennummer. Die Maske übersetzt:

| Handzeichen | Mitarbeiter | Qualifikation | Beschäftigtennummer | Herkunft |
|---|---|---|---|---|
| `MB` | Pflegefachkraft | 1 | `999999998` | Ersatzwert „neu, ohne Nummer" |
| `TK` | hauswirtschaftl. Fachkraft | 2 | `999999996` | Ersatzwert „Auszubildende(r)" |
| `SR` | Pflegefachkraft | 1 | `999999998` | Ersatzwert „neu, ohne Nummer" |

Die Beschäftigtennummer ist bei ambulanten Pflegediensten **Pflicht** (`S4-XI-008`).
Die Ersatzwerte aus Schlüssel 2.17 sind zulässig, aber die Maske sollte sie sichtbar als
Ersatz kennzeichnen — sonst bleiben sie dauerhaft stehen, auch wenn die echte Nummer
längst vorliegt.

Zweite Funktion des Mitarbeiterstamms: Die **Qualifikation** ist die dritte Komponente
der Leistungsziffer. Trägt der Beleg für den 3. Juli ein `TK` bei Leistung `015`, dann
muss die Ziffer `01:01:**2**:015` lauten. Eine Maske, die Handzeichen und
Leistungskatalog getrennt führt, ohne die Qualifikation abzugleichen, produziert stillen
Unsinn — der Validator sieht ihn nicht, weil beide Werte für sich gültig sind.

### 4.5 M5 — Pflegebedürftige

```
┌─ Pflegebedürftige/r ─────────────────────────────────────────────────────┐
│  Name, Vorname     [Kerzenmacher        ] [Hanna              ]          │
│  Geburtsdatum      [12.03.1948]                                          │
│  Versichertennr.   [K741852967]  ⚠ Prüfziffer nicht verifizierbar        │
│  Anschrift         [Rosenweg] [3] [12345] [Musterstadt        ]          │
│  Pflegekasse       [Pflegekasse bei der Muster BKK ▾] IK 189524616       │
│  Pflegegrad        [3 ▾]  gültig ab [01.02.2024]                         │
│  Standardeinsatz   [07:15]   Standardleistungen [003 ▾] [+]              │
│  Turnus            (x) Mo–Fr  ( ) täglich  ( ) frei                      │
└──────────────────────────────────────────────────────────────────────────┘
```

- **Pflegegrad oder Pflegestufe — nie beides** (`S4-XI-005`). Das Feld hängt am
  Abrechnungszeitraum: bis 31.12.2016 Pflegestufe, danach Pflegegrad. Die Maske sollte
  das Feld **umbenennen**, nicht zwei Felder anbieten. Der einzige Negativfall, der in
  [`../pflege-105-sgbxi-negativfaelle/`](../pflege-105-sgbxi-negativfaelle/) noch fehlt,
  ist genau dieser: beide Felder belegt.
- **Die KVNR-Prüfziffer wird gewarnt, nicht geblockt.** Das Prüfverfahren ist in dieser
  Wissensbibliothek als **unverifiziert** markiert (❓-11, `S4-ALL-002` hat Status
  `experimental`). Eine Maske, die auf einem unbelegten Algorithmus hart blockt, weist
  gültige Nummern ab. Format prüfen (`^[A-Z][0-9]{9}$`) — ja; Prüfziffer als Hinweis —
  ja; Speichern verhindern — nein.
- **Die Anschrift wird immer erfasst**, auch wenn sie nicht immer übertragen wird. Sie
  steht auf dem gedruckten Leistungsnachweis beider Fälle. Ob sie ins `NAD`-Segment
  wandert, entscheidet der Generator: Pflicht ist sie nur, wenn die Versicherten-Nummer
  fehlt (`S4-XI-010`). Das Beispiel zeigt beide zulässigen Varianten — Fall `2607001`
  mit Anschrift, Fall `2607002` ohne, dort endet das Segment nach dem Geburtsdatum.
- **Turnus und Standardleistungen** sind reine Erfassungshilfen. Sie erzeugen den
  Vorschlag, den M7 dann gegen den Beleg korrigiert.

### 4.6 M6 — Abrechnungslauf anlegen

```
┌─ Abrechnungslauf ────────────────────────────────────────────────────────┐
│  Abrechnungsmonat  [Juli 2026 ▾]      Leistungszeitraum 01.–31.07.2026   │
│  Rechnungsdatum    [05.08.2026]                                          │
│  Rechnungsnummer   2026070001        ← Nummernkreis, nicht editierbar    │
│  Einzelrechnungsnr. 0                ← Selbstabrechner                   │
│  Kostenträger      [Muster BKK ▾]     Rechnungsart 1 · Währung EUR       │
│  Fälle im Lauf     [ + Fall aufnehmen ]                                  │
│      2607001  Kerzenmacher, Hanna   ○ offen                              │
│      2607002  Brinkmeier, Otto      ○ offen                              │
└──────────────────────────────────────────────────────────────────────────┘
```

Die Rechnungsnummer kommt aus einem Nummernkreis, nicht aus der Tastatur. Die TA 1
begrenzt die zulässigen Zeichen (`S4-XI-003`): keine Sonderzeichen außer `-` und `/`
als Gliederungszeichen, nicht zwei hintereinander, nicht am Anfang oder Ende. Ein
Nummernkreis nach dem Muster `JJJJMMnnnn` erfüllt das ohne Prüfung; eine freie Eingabe
braucht sie.

**Ein Lauf, eine Leistungsart, eine Rechnungsart** (`S5-XI-006`). Die Maske darf keine
Fälle unterschiedlicher Leistungsart in denselben Lauf aufnehmen — die Prüfung gehört an
die Schaltfläche „Fall aufnehmen", nicht ans Ende.

---

## 5. M7 — Die Einsatzerfassung, das Herzstück

Diese Maske hat eine einzige Aufgabe: **Das Auge soll vom Papier in die Maske springen
können, ohne zu suchen.** Also dieselbe Anordnung, dieselben Spaltenköpfe, dieselbe
Reihenfolge wie auf dem Leistungsnachweis.

```
┌─ Einsatzerfassung ──────────────────────── Fall 2607001 · Beleg 1 von 2 ─┐
│ Kerzenmacher, Hanna · K741852967 · PG 3 · Juli 2026 · Einsatzzeit 07:15  │
├─────────────────────────────────────────────────────────────────────────┤
│                      Mi Do Fr Sa So Mo Di Mi Do Fr Sa So Mo Di Mi Do …   │
│ LK  Leistung   HZ     1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 … │
│ 003 Gr.Morgen. MB    [x][x][x][ ][ ][x][x][x][x][x][ ][ ][ ][ ][ ][x]…  │
│ 015 Hauswirt.  TK    [ ][ ][x][ ][ ][ ][x][ ][ ][x][ ][ ][ ][ ][ ][ ]…  │
├─────────────────────────────────────────────────────────────────────────┤
│ Serie anlegen:  [Mo–Fr]  [Di+Fr]  [täglich]  [alles löschen]            │
│ Abwesenheit:    von [13.07.] bis [15.07.]  Grund [KH-Aufenthalt      ]  │
│                 → 3 Werktage aus allen Zeilen entfernt                  │
├─────────────────────────────────────────────────────────────────────────┤
│ Erfasst      003 = 20     015 =  8     Einsätze gesamt 20               │
│ Laut Beleg   003 = [20]   015 = [ 8]                        ✓ stimmt    │
└─────────────────────────────────────────────────────────────────────────┘
                                            [Fall abschließen]  [F12]
```

### 5.1 Der Erfassungsweg für den ersten Fall

1. **Serie „Mo–Fr" für Zeile `003`.** Setzt 23 Werktage.
2. **Serie „Di+Fr" für Zeile `015`.** Setzt 9 Tage (3, 7, 10, 14, 17, 21, 24, 28, 31).
3. **Abwesenheit 13.–15.07. eintragen.** Entfernt aus `003` die Tage 13, 14, 15 → 20;
   aus `015` den Dienstag 14 → 8. Der Grund wandert in die Bemerkung des Belegs, nicht
   in die Datei.
4. **Kontrollwerte vom Papier abtippen**: `20` und `8`. Die Maske vergleicht.

Vier Handgriffe für 28 `ELS`-Segmente. Der zweite Fall braucht zwei: Serie „täglich"
für `004`, Kontrollwert `31` — die 31 Wegepauschalen entstehen über die Koppelleistung
von selbst.

### 5.2 Die Kontrollwerte sind das eigentliche Sicherheitsnetz

Die Felder `Laut Beleg` sind **Blindeingaben**: Der Erfasser tippt die Zahl vom Papier,
ohne dass die Maske ihre eigene Summe vorher zeigt. Weicht sie ab, gibt es genau zwei
Möglichkeiten — falsch geklickt oder falsch gelesen — und beide werden **sofort** am
offenen Beleg geklärt, nicht drei Wochen später in der Absetzung der Kasse.

Das ist die einzige Prüfung dieser Anleitung, die kein Validator je leisten kann: Der
Validator sieht die Datei, nicht das Papier. **Die Übereinstimmung zwischen Handzeichen
und `ELS`-Segmenten entsteht in der Maske oder gar nicht.**

### 5.3 Sonderfälle, die das Raster können muss

| Fall | Bedienung | Ergebnis in der Datei |
|---|---|---|
| Zwei Einsätze am selben Tag | Doppelklick auf die Zelle → zweite Uhrzeit | zwei `ESK` mit Tag `07`, Uhrzeiten `0715` und `1830` |
| Mehrere Leistungen in einem Einsatz | mehrere Zeilen in derselben Spalte gehakt | **ein** `ESK`, darunter mehrere `ELS` — genau wie am 3. Juli des Beispiels |
| Monatspauschale ohne Tagesbezug | Zeile auf „Monatspauschale" umschalten | `ESK` mit Kennzeichen `99` (`S4-XI-007`) |
| Leistung mit Anzahl > 1 | Zelle mit Zahl statt Haken | `ELS` mit `Anzahl` ≠ `1,00` |
| Zuschlag auf eine Leistung | Aufklappen der Zelle | `ZUS` unter dem `ELS`, Wert mit **5 Nachkommastellen** (`S4-XI-009`) |

Die Sortierung der `ESK` nach Tag und Uhrzeit (`S3-XI-006`) fällt beim Serialisieren aus
dem Raster heraus — sie kann gar nicht falsch werden, solange nicht jemand die Segmente
nachträglich umsortiert. Der Negativfall `n7` beschreibt genau diesen Eingriff.

---

## 6. M8/M9 — Abschluss und Freigabe

```
┌─ Fallabschluss 2607001 ──────────────────────────────────────────────────┐
│  003 Große Morgentoilette          20 × 24,50 =   490,00                 │
│  015 Hauswirtschaftl. Versorgung    8 × 18,20 =   145,60                 │
│                                     Gesamtbrutto   635,60                │
│  Zuzahlung/Eigenanteil    —    Beihilfe    —                             │
│                                     Rechnungsbetrag 635,60  → IAF        │
│  Summe laut Beleg  [   635,60]                              ✓ stimmt     │
└──────────────────────────────────────────────────────────────────────────┘
```

Auch hier: Betrag rechnen lassen, Betrag vom Papier abtippen, vergleichen. Der
Rechnungsbetrag ist Gesamtbrutto abzüglich Zuzahlung und Beihilfe (`S5-XI-004`) — im
Beispiel entsteht kein Eigenanteil, weil beide Fälle unter dem Sachleistungsbetrag ihres
Pflegegrades bleiben.

```
┌─ Lauf prüfen und freigeben ──────────────────────────────────────────────┐
│  Fälle           2      Segmente (Vorschau)  163                         │
│  Σ IAF     1.671,00     GES                  1.671,00     ✓ S5-XI-003    │
│                                                                          │
│  Prüfung gegen den Regelkatalog                                          │
│   ✓ 57 Regeln erfüllt                                                    │
│   ⓘ  S2-*   nicht geprüft — Verschlüsselung erfolgt beim Versand         │
│   ⓘ  S4-ALL-002  KVNR-Prüfziffer: Verfahren unverifiziert                │
│                                                     [Freigeben]  [F12]   │
└──────────────────────────────────────────────────────────────────────────┘
```

Die Freigabe ist die Stelle, an der die **kreuzenden** Prüfungen laufen — die, die einen
einzelnen Beleg nie erwischt: `GES` gegen Σ `IAF`, `PLGA.FKT` gegen `PLAA.FKT`,
`PLGA.REC` gegen `PLAA.REC`, Währungskennzeichen über alle Nachrichten.

---

## 7. M10 — Erzeugen: was die Maske nie gefragt hat

Beim Erzeugen entsteht der gesamte Transportrahmen, **ohne eine einzige weitere
Eingabe**. Was der Generator aus dem bereits Erfassten ableitet:

| Ergebnis | Ableitung | Wert im Beispiel |
|---|---|---|
| Physikalischer Dateiname | Betriebsmodus + Verfahren `PFL` + Version `0` + Transfernummer aus dem Zähler | `TPFL0001` |
| Auftragsdateiname | Nutzdatenname + `.AUF` | `TPFL0001.AUF` |
| Logischer Dateiname | `PL` + Monat `076` + Lieferungsart `0` + lfd. Nr. `01` + `S` + Kassenart `BK` | `PL076001SBK` |
| `VERFAHREN_KENNUNG` | Stellen 1–5 des physikalischen Namens | `TPFL0` |
| `DATEIGROESSE_NUTZDATEN` | Länge der serialisierten Nutzdaten | `000000004924` |
| `UNT`-Zähler | gezählte Segmente je Nachricht | `8`, `153` |
| `UNZ`-Zähler | gezählte Nachrichten | `2` |
| `DATUM_ERSTELLUNG` | Systemzeit | `20260805114700` |
| `DATEI_BEZEICHNUNG` 319–320 | Art der abgegebenen Leistung aus M1 | `01` |
| `DATEI_BEZEICHNUNG` 347–348 | Anzahl Gesamtpakete | `01` |
| Kann-Felder des Auftragssatzes | Default je Feldtyp: `N` → Nullen, `A`/`AN` → Leerzeichen | `00000000000000`, `␣␣␣` |

**Die letzte Zeile ist der meistgemachte Fehler beim Auftragssatz.** Ein leeres
numerisches Kann-Feld ist mit Nullen zu füllen, nicht mit Leerzeichen und nicht mit
Nullbytes (`S1-ALL-009`). Der Satz ist genau 348 Byte lang — jede Verkürzung ist ein
Fehler (`S1-ALL-001`).

Und die Ausgabe hat **zwei Wege**:

```
                          verschlüsseltes Dateipärchen
  Erfassung ─────────────────────────────────────────►  Datenannahmestelle
      │                    TPFL0001 + .AUF                    661100423
      │
      │              Urbelege + Begleitzettel (gedruckt)
      └────────────────────────────────────────────────►  Belegannahmestelle
                          Papier, Briefpost                  661100559
```

Der Begleitzettel wird aus demselben Lauf gedruckt: Fallliste, Versichertennummern,
Pflegegrade, Einzelbeträge, Summe, Rechnungsnummer, Dateiname, Transfernummer. Alles
schon da. Die Maske fragt dafür genau **ein** zusätzliches Feld ab — die Sendungsnummer,
falls der Betrieb einen eigenen Kreis dafür führt.

> **Achtung, gegenläufige Datenschutzregeln.** Der Begleitzettel *enthält* Sozialdaten
> (Namen, KVNR, Pflegegrad) — er liegt im verschlossenen Umschlag bei Belegen, die sie
> ohnehin tragen. Die Auftragsdatei `TPFL0001.AUF` darf **keine** enthalten
> (`S1-ALL-008`), weil sie unverschlüsselt übertragen wird. Ein Generator, der „zur
> besseren Zuordnung" den Versichertennamen ins `VARIABLES_INFO_FELD` schreibt, verletzt
> das Trennungsgebot.

---

## 8. Wann welche Prüfung feuert

Prüfungen so früh wie möglich — aber nicht früher, als die Information vorliegt.

| Zeitpunkt | Prüfungen | Reaktion |
|---|---|---|
| **Feldverlassen** | IK-Prüfziffer (`S4-ALL-001`), IK-Klassifikation, Feldlänge, Datumsformat (`S4-ALL-003`), Zeichensatz, Format Rechnungs-/Belegnummer (`S4-XI-003/004`) | blocken |
| | KVNR-Prüfziffer (`S4-ALL-002`, unverifiziert) | warnen |
| **Fall aufnehmen** | Leistungsart passt zum Lauf (`S5-XI-006`), Pflegegrad zum Zeitraum (`S4-XI-005`), Pflegekassen-IK beginnt mit `18` (`S4-XI-002`) | blocken |
| **Zelle setzen** | Leistung im Katalog zum Leistungsdatum gültig (`S4-XI-001`), Qualifikation passt zum Handzeichen | warnen |
| **Fall abschließen** | Kontrollsumme Einsätze, Kontrollsumme Betrag, `IAF` = Brutto − Zuzahlung − Beihilfe (`S5-XI-004`), Beschäftigtennummer belegt (`S4-XI-008`) | blocken |
| **Lauf freigeben** | `GES` = Σ `IAF` (`S5-XI-003`), `FKT`/`REC`-Gleichheit (`S5-XI-001/002`), Währung einheitlich (`S5-XI-005`), Leistungsdatum ≤ Rechnungsdatum (`S6-ALL-001`) | blocken |
| **Erzeugen** | Segmentgrammatik (`S3-XI-003/004`), Zähler (`S3-ALL-003/004`), Auftragssatz vollständig (`S1-ALL-*`), Dateipärchen (`S0-ALL-*`) | blocken |
| **Vor dem Versand** | vollständiger Validatorlauf über das erzeugte Pärchen | Bericht |

Der letzte Schritt ist der Punkt, an dem dieses Projekt ansetzt: **Der Validator läuft
über das fertige Pärchen, bevor es die Datenannahmestelle sieht.** Er ersetzt die
Maskenprüfungen nicht — er fängt ab, was ein Erfassungsprogramm falsch serialisiert hat,
und das ist eine andere Fehlerklasse als ein Tippfehler.

---

## 9. Fünf Maskenfehler, die genau die Negativfälle erzeugen

Die [Negativfixtures](../pflege-105-sgbxi-negativfaelle/) sind maschinell erzeugte
Einzelabweichungen. Interessant wird die Liste, wenn man sie rückwärts liest — als
Katalog dessen, was eine Erfassungsmaske falsch machen kann:

| Negativfall | Regel | Der Maskenfehler dahinter |
|---|---|---|
| `n1` IK-Prüfziffer | `S4-ALL-001` | IK als Freitext ohne Prüfziffernrechnung beim Feldverlassen — oder Rechnung über die Stellen 1–8 statt 3–8 |
| `n2` `UNT`-Zähler | `S3-ALL-004` | Segmentzähler als Datenfeld statt als Zählergebnis beim Serialisieren |
| `n3` Summenabweichung | `S5-XI-003` | `GES` eingebbar gemacht, statt aus den `IAF` zu summieren |
| `n4` Pärchen unvollständig | `S0-ALL-003` | Auftragsdatei als separater Menüpunkt statt als untrennbarer Teil des Erzeugens |
| `n5` `UNA` vorhanden | `S3-XI-002` | generischer EDIFACT-Serialisierer ohne Verfahrensprofil — schreibt sein Standard-`UNA` |
| `n6` Dezimalpunkt | `S3-XI-002` | Beträge über die Locale-Formatierung der Programmiersprache ausgegeben statt über den Verfahrensschreiber |
| `n7` `ESK` unsortiert | `S3-XI-006` | Einsätze in Erfassungsreihenfolge serialisiert statt nach Tag und Uhrzeit sortiert |

Vier der sieben (`n2`, `n3`, `n5`, `n6`) sind **keine Erfassungsfehler, sondern
Generatorfehler** — sie entstehen nach der letzten Tastatureingabe. Das ist das Argument
für Abschnitt 2: Solange abgeleitete Werte kein Eingabefeld haben, bleibt als Fehlerquelle
nur der Serialisierer, und der ist testbar.

---

## 10. Durchlauf: `TPFL0001` in 14 Schritten

Der vollständige Weg von den beiden Leistungsnachweisen zum Dateipärchen dieses
Verzeichnisses. Vorbedingung: M1–M4 sind gepflegt.

| # | Maske | Eingabe | Wirkung |
|---|---|---|---|
| 1 | M5 | Kerzenmacher, Hanna · 12.03.1948 · `K741852967` · Rosenweg 3 · PG 3 · 07:15 | Fallstamm 1 |
| 2 | M5 | Brinkmeier, Otto · 27.11.1939 · `M305921844` · Ahornstraße 27 · PG 4 · 07:45 | Fallstamm 2 |
| 3 | M6 | Monat Juli 2026, Rechnungsdatum 05.08.2026, Kostenträger Muster BKK | Rechnungsnr. `2026070001`, Belegnrn. `2607001`/`2607002` |
| 4 | M6 | beide Fälle aufnehmen | Lauf mit 2 offenen Fällen |
| 5 | M7 | Fall 1, Zeile `003`, Serie **Mo–Fr** | 23 Einsätze |
| 6 | M7 | Fall 1, Zeile `015`, Serie **Di+Fr** | 9 Einsätze |
| 7 | M7 | Abwesenheit 13.–15.07., Grund „stationärer Krankenhausaufenthalt" | `003` → 20, `015` → 8 |
| 8 | M7 | Kontrollwerte `20` und `8` | ✓ stimmt |
| 9 | M8 | Kontrollsumme `635,60` | ✓ → `IAF+635,60+++635,60` |
| 10 | M7 | Fall 2, Zeile `004`, Serie **täglich** | 31 Einsätze, 31 Wegepauschalen über die Koppelleistung |
| 11 | M7 | Kontrollwert `31` | ✓ stimmt |
| 12 | M8 | Kontrollsumme `1.035,40` | ✓ → `IAF+1035,40+++1035,40` |
| 13 | M9 | Freigeben | `GES+1671,00+++1671,00`, 57 Regeln grün |
| 14 | M10 | Erzeugen | `TPFL0001` + `TPFL0001.AUF` + Begleitzettel |

Erwartetes Ergebnis, nachrechenbar an den Dateien dieses Verzeichnisses:

| Kennzahl | Wert |
|---|---|
| Nachrichten | 2 (PLGA, PLAA) |
| Segmente gesamt | 163 — PLGA 8, PLAA 153, dazu `UNB` und `UNZ` |
| `ESK`-Segmente | 51 = 20 + 31 |
| `ELS`-Segmente | 90 = 20 + 8 + 31 + 31 |
| Nutzdatengröße | 4924 Byte |
| Auftragssatz | 348 Byte |
| Rechnungsbetrag | 1.671,00 EUR |

Vierzehn Schritte für 163 Segmente, davon sechs im Tagesraster — das ist der Maßstab.
Wer für dieselbe Abrechnung 90 Positionszeilen tippt, hat die Maske falsch geschnitten.

---

## 11. Was diese Anleitung offen lässt

| Punkt | Warum offen |
|---|---|
| **Aufbau des Papierbelegs** | Anlage 4 zur TA 1 („Begleitzettel für Urbelege", V 1.0 vom 31.01.2003) ist im [Dokumentenregister](../../knowledge-base/data/dokumentenregister.yaml) erfasst, aber nicht beschafft. Die Maske bildet den *hier* liegenden Beleg nach. |
| **Elektronischer Leistungsnachweis** | TA 1 Abschnitt 4.6.2 (Schema `PFL_LNW_2.2.0.xsd`) beschreibt ihn — dann entfällt die Erfassung ganz und die Maske wird zur Kontrollansicht. Nicht ausgewertet. |
| **Sammelrechnung** | Bei Rechnungsart `3` erfasst die Abrechnungsstelle für mehrere Leistungserbringer; der Laufkopf bekommt eine Ebene mehr. Siehe [`../pflege-105-sgbxi-sammelrechnung/`](../pflege-105-sgbxi-sammelrechnung/) — dort sind einzelne Feldzuordnungen offengelegte Interpretation. |
| **Korrektur und Wiedereinreichung** | Das Verarbeitungskennzeichen in `FKT` kennt mehr als `01`. Welche Maskenwege zu Absetzung, Korrektur und Neuberechnung gehören, ist hier nicht beschrieben. |
| **`ZUS`, `HIL`, `IMG`** | Zuschläge, Pflegehilfsmittel und die vollelektronische Abrechnung kommen im Beispiel nicht vor; die Rasterzelle müsste dafür aufklappbar werden. |
| **Mehrbenutzerbetrieb** | Sperren, Erfassungsjournal, Vier-Augen-Prinzip bei der Freigabe — organisatorisch geboten, hier nicht ausgearbeitet. |

---

## Siehe auch

- [README dieses Beispiels](README.md) — Feld für Feld, Segment für Segment
- [`beispiel-metadaten.yaml`](beispiel-metadaten.yaml) — dieselben Werte maschinenlesbar
- [Validierungsregeln](../../knowledge-base/50-anforderungen/02-validierungsregeln.md) — das 7-stufige Prüfmodell
- [Mindmap technische Anforderungen](../../knowledge-base/30-technik/06-mindmap-technische-anforderungen.md) — alle Vorgaben an eine DTA-Datei auf einer Seite
- [Negativfälle](../pflege-105-sgbxi-negativfaelle/) — was passiert, wenn eine dieser Regeln bricht
