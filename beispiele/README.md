# Beispieldateien

Synthetische DTA-Dateipärchen als **Fixtures** für die Entwicklung von Parser und
Regelwerk. Ergänzung zur [Wissensbibliothek](../knowledge-base/) — dort steht, *was*
gelten soll; hier liegt, *woran* man es ausprobieren kann.

| Beispiel | Verfahren | Inhalt | Belastbarkeit |
|---|---|---|---|
| [`pflege-105-sgbxi/`](pflege-105-sgbxi/) | § 105 SGB XI (PLGA/PLAA) | Monatsabrechnung eines ambulanten Pflegedienstes, 2 Abrechnungsfälle, 1.671,00 EUR | ✅ **gegen die Primärdokumente gebaut** (TA 1 6.4.0, TA 3 6.4.0, Anlage 2 und 4 GGT); nur die Stammdaten sind erfunden |
| [`pflege-105-sgbxi-negativfaelle/`](pflege-105-sgbxi-negativfaelle/) | § 105 SGB XI | 7 Dateipärchen des Positivfalls, je mit genau einem eingebauten Fehler | ✅ mechanische Einzelabweichungen vom obigen Positivfall, Diff pro Fall dokumentiert |
| [`pflege-105-sgbxi-sammelrechnung/`](pflege-105-sgbxi-sammelrechnung/) | § 105 SGB XI, Rechnungsart 3 | Dieselbe Abrechnung über eine Abrechnungsstelle mit Inkassovollmacht, verschachtelte PLGA-Ebenen | ⚠️ Verschachtelung und Sammelrechnungs-Kennzeichen belegt; einzelne Feldzuordnungen bei Rechnungsart 3 sind offengelegte Interpretation |
| [`pflege-105-sgbxi-kim/`](pflege-105-sgbxi-kim/) | § 105 SGB XI, TI/KIM | Dieselbe Abrechnung mit `IMG`-Segment und skizziertem KIM-Umschlag, ohne Auftragsdatei | ⚠️ EDIFACT-Teil so belastbar wie der Positivfall; der XML-Umschlag ist ausdrücklich eine unbelegte Skizze |
| [`pflege-105-sgbxi-umlaute/`](pflege-105-sgbxi-umlaute/) | § 105 SGB XI | Dieselbe Abrechnung mit Umlauten und dem TA-1-eigenen Freigabezeichen-Beispiel („D?'Angelo") | ✅ Freigabezeichen-Fall wörtlich aus der TA 1 übernommen; Umlaut-Zulässigkeit selbst folgt nur aus der allgemeinen Zeichensatzregel |

## Grundsätze

**Nur synthetische Daten.** Keine echten Versichertendaten, keine echten Namen, keine
echten Rechnungen — REQ-DSGVO-03. Prüfziffern werden nach den in der Wissensbibliothek
dokumentierten Algorithmen gerechnet, damit die erfundenen Werte formal gültig sind.

**Belastbarkeit offenlegen.** Die Wissensbibliothek unterscheidet konsequent zwischen
belegtem Wissen ✅, Sekundärquellen ⚠️ und offenen Punkten ❓. Beispieldateien müssen
dasselbe leisten: Jede README hier sagt pro Segment und pro Feld, ob der Aufbau belegt,
aus einem verwandten Verfahren analog übernommen oder schlicht erfunden ist. Wo eine
Technische Anlage noch fehlt, ist der überwiegende Teil erfunden — ein Beispiel, das das
verschweigt, richtet mehr Schaden an als es nützt.

**Kein Erzeugungs-Vorbild.** Diese Dateien taugen zum Testen eines Validators, nicht als
Muster für die Erzeugung echter Abrechnungsdateien. Auch wo die Struktur gegen die
Technische Anlage verifiziert ist, bleiben Preise, Leistungsnummern und Stammdaten
erfunden — sie ergeben sich real aus Vergütungsvereinbarungen und Kostenträgerdateien.

**Beim Erscheinen eines Primärdokuments nachziehen.** Das Pflegebeispiel wurde am
01.09.2026 vollständig neu aufgebaut, nachdem die TA 1 vorlag; die Vorfassung war
strukturell falsch. Der Abschnitt „Was sich gegenüber der Vorfassung geändert hat" in
[`pflege-105-sgbxi/README.md`](pflege-105-sgbxi/README.md) hält die Unterschiede fest —
sie sind die beste vorhandene Liste typischer Fehlannahmen über EDIFACT im GKV-Umfeld.

**Konsistenz vor Vollständigkeit.** Zähler (`UNT`, `UNZ`), Referenzen (`UNB`↔`UNZ`,
`UNH`↔`UNT`), Summen und Prüfziffern stimmen in sich — daran lässt sich Regellogik
entwickeln, auch wenn die Feldsemantik noch geraten ist.

## Aufbau eines Beispielverzeichnisses

| Datei | Inhalt |
|---|---|
| `README.md` | Fallbeschreibung, Feldtabellen mit Herkunftsangabe, Regelabdeckung, Korrekturliste |
| `<DATEINAME>` | Nutzdatendatei (Klartext) |
| `<DATEINAME>.AUF` | Auftragsdatei |
| `urbeleg-leistungsnachweis.html` | Urbeleg: der vom Versicherten unterschriebene Leistungsnachweis, druckbar |
| `urbeleg-begleitzettel.html` | Deckblatt der Papiersendung an die Belegannahmestelle |
| `urbeleg-*.pdf` | dieselben Belege als PDF, aus dem HTML gedruckt |
| `beispiel-metadaten.yaml` | Erwartungswerte maschinenlesbar: Beteiligte, Summen, Zähler, erfüllte Regel-IDs |
| `erfassung-anleitung.md` | optional: wie aus den Urbelegen in einer Eingabemaske das Dateipärchen entsteht |

`beispiel-metadaten.yaml` folgt den Feldkonventionen aus
[`knowledge-base/data/README.md`](../knowledge-base/data/README.md) — insbesondere
`vertrauen: belegt | sekundaer | offen`.

Nur das Pflegebeispiel trägt bisher eine Erfassungsanleitung:
[`pflege-105-sgbxi/erfassung-anleitung.md`](pflege-105-sgbxi/erfassung-anleitung.md)
beschreibt den Weg vom unterschriebenen Leistungsnachweis über eine Eingabemaske zum
Dateipärchen — Maskenschnitt, Feldherkunft, Prüfzeitpunkte. Der Maskenschnitt selbst ist
erfunden; kein ausgewertetes Primärdokument schreibt eine Oberfläche vor.

## Was noch fehlt

Die sieben Negativfälle, die Sammelrechnung, die vollelektronische Abrechnung über
KIM und die Umlaut-Konstellation sind jetzt vorhanden (siehe Tabelle oben) — alle
für § 105 SGB XI, weil dort als einzigem Verfahren die Primärdokumente ausgewertet
sind.

Offen bleibt:

- **Weitere Negativfälle** für die übrigen rund 50 im Positivfall erfüllten Regeln —
  die sieben vorhandenen decken je einen Fall aus den Prüfstufen 0, 3, 4 und 5 ab,
  nicht die gesamte Regelliste.
- **Feldgenaue Klärung von Rechnungsart 2/3.** Das Sammelrechnungs-Beispiel legt
  offen, welche Feldzuordnungen dafür nur Interpretation sind (siehe dessen README,
  Abschnitt „Offene Fragen") — eine Auswertung von TA 1 Abschnitt 4.5 im Detail
  würde diese Lücke schließen.
- **Der elektronische Leistungsnachweis selbst** (`PFL_LNW_2.2.0.xsd`) und die
  übrigen KIM-Bestandteile (`PFL_basis_2.2.0.xsd`, `PFL_ABR_2.2.0.xsd`) — das
  KIM-Beispiel bildet nur die grobe Hülle nach, nicht deren tatsächliche
  XML-Struktur.
- **Ein § 302-Beispiel**, sobald die dortige Technische Anlage 1 vorliegt.
