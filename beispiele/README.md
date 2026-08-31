# Beispieldateien

Synthetische DTA-Dateipärchen als **Fixtures** für die Entwicklung von Parser und
Regelwerk. Ergänzung zur [Wissensbibliothek](../knowledge-base/) — dort steht, *was*
gelten soll; hier liegt, *woran* man es ausprobieren kann.

| Beispiel | Verfahren | Inhalt | Belastbarkeit |
|---|---|---|---|
| [`pflege-105-sgbxi/`](pflege-105-sgbxi/) | § 105 SGB XI (PLGA/PLAA) | Monatsabrechnung eines ambulanten Pflegedienstes, 2 Abrechnungsfälle, 1.671,00 EUR | Transportrahmen belegt orientiert, **Fachstruktur erfunden** |

## Grundsätze

**Nur synthetische Daten.** Keine echten Versichertendaten, keine echten Namen, keine
echten Rechnungen — REQ-DSGVO-03. Prüfziffern werden nach den in der Wissensbibliothek
dokumentierten Algorithmen gerechnet, damit die erfundenen Werte formal gültig sind.

**Belastbarkeit offenlegen.** Die Wissensbibliothek unterscheidet konsequent zwischen
belegtem Wissen ✅, Sekundärquellen ⚠️ und offenen Punkten ❓. Beispieldateien müssen
dasselbe leisten: Jede README hier sagt pro Segment und pro Feld, ob der Aufbau belegt,
aus einem verwandten Verfahren analog übernommen oder schlicht erfunden ist. Solange die
Technischen Anlagen nicht beschafft sind, ist der überwiegende Teil erfunden — ein
Beispiel, das das verschweigt, richtet mehr Schaden an als es nützt.

**Kein Erzeugungs-Vorbild.** Diese Dateien taugen zum Testen eines Validators, nicht als
Muster für die Erzeugung echter Abrechnungsdateien. Das gilt, bis die jeweilige Technische
Anlage vorliegt und die Struktur gegen sie verifiziert wurde.

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
| `beispiel-metadaten.yaml` | Erwartungswerte maschinenlesbar: Beteiligte, Summen, Zähler, erfüllte Regel-IDs |

`beispiel-metadaten.yaml` folgt den Feldkonventionen aus
[`knowledge-base/data/README.md`](../knowledge-base/data/README.md) — insbesondere
`vertrauen: belegt | sekundaer | offen`.

## Was noch fehlt

Zu jedem Positivfall gehört langfristig ein **Negativfall-Satz**: Dateien mit je genau
einem eingebauten Fehler (falsche Prüfziffer, Zähler stimmt nicht, Summe weicht ab,
Dateipärchen unvollständig, unzulässiges Zeichen), damit sich für jede Regel nachweisen
lässt, dass sie auch wirklich anschlägt. Sinnvoll wird das, sobald die Regeln
implementiert sind und die Fachstruktur nicht mehr geraten ist.
