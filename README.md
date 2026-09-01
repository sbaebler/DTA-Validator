# DTA-Validator

Validierung von DTA-Dateien (Datenträgeraustausch / elektronischer Datenaustausch) im
deutschen GKV-Markt — Prüfung von Abrechnungsdaten gegen die geltenden Regelwerke,
**bevor** sie an eine Datenannahmestelle gehen.

> **Status: Vorprojekt.** Es existiert noch kein Code. Aktueller Stand ist die
> Wissensbibliothek mit den recherchierten fachlichen und technischen Anforderungen.
>
> **Stand 01.09.2026:** Die Primärdokumente **Anlage 2 GGT** (Auftragsdatei),
> **Anlage 4 GGT** (Verfahrenskennungen), **§ 105 SGB XI Technische Anlage 1 V 6.4.0**
> nebst Anhängen und **Technische Anlage 3** (Schlüsselverzeichnisse) sowie das
> **Gemeinsame Rundschreiben Institutionskennzeichen** liegen ausgewertet vor. Damit sind
> die Prüfstufen 0 und 1 (Dateipärchen, Auftragssatz) verfahrensübergreifend und die
> Prüfstufen 3–6 für § 105 SGB XI implementierungsreif spezifiziert. Für §§ 300/301/302
> SGB V fehlen die sektorspezifischen Technischen Anlagen weiterhin.

## Wissensbibliothek

Die vollständigen Anforderungen liegen unter **[`knowledge-base/`](knowledge-base/)**:

| Bereich | Inhalt |
|---|---|
| [Domänenüberblick](knowledge-base/00-ueberblick/01-domaenenueberblick.md) | Akteure, Rollen, generischer Ablauf, Dateipärchen-Prinzip |
| [Glossar](knowledge-base/00-ueberblick/02-glossar.md) | Begriffe und Abkürzungen |
| [Quellenverzeichnis](knowledge-base/00-ueberblick/03-quellenverzeichnis.md) | Belegstellen mit URLs |
| [Rechtsgrundlagen](knowledge-base/10-rechtsgrundlagen/01-gesetzliche-grundlagen.md) | §§ 294–303 SGB V, § 105 SGB XI, § 95 SGB IV, Fristen |
| [Verfahren](knowledge-base/20-verfahren/00-verfahrensuebersicht.md) | §§ 300, 301, 301a, 302 SGB V, § 105 SGB XI und weitere |
| [Technik](knowledge-base/30-technik/01-ggt-und-anlagen.md) | GGT, KKS, Auftragsdatei, EDIFACT, Transportwege, SECON |
| [Mindmap Technik](knowledge-base/30-technik/06-mindmap-technische-anforderungen.md) | Alle technischen Anforderungen an eine DTA-Datei auf einer Seite |
| [Stammdaten](knowledge-base/40-stammdaten/01-institutionskennzeichen.md) | IK, KVNR, Kostenträgerdateien, Schlüsselverzeichnisse |
| [Anforderungskatalog](knowledge-base/50-anforderungen/01-anforderungskatalog.md) | Nummerierte Requirements (REQ-*) |
| [Validierungsregeln](knowledge-base/50-anforderungen/02-validierungsregeln.md) | 7-stufiges Prüfmodell mit Regelkatalog |
| [Projekt](knowledge-base/60-projekt/01-projekt-scope-und-architektur.md) | Scope, Architekturskizze, Roadmap, offene Punkte |
| [Referenzdaten](knowledge-base/data/) | Maschinenlesbare YAML-Fassung |

Zwei Referenzdateien sind direkt aus Primärdokumenten abgeleitet und implementierungsreif:

| Datei | Inhalt | Quelle |
|---|---|---|
| [`auftragssatz.yaml`](knowledge-base/data/auftragssatz.yaml) | Feldkatalog des Auftragssatzes — 37 Felder, Stellen 1–348 | Anlage 2 GGT |
| [`verfahrenskennungen.yaml`](knowledge-base/data/verfahrenskennungen.yaml) | Werteliste der Verfahrenskennungen — 322 Einträge | Anlage 4 GGT |

## Beispieldateien

Unter **[`beispiele/`](beispiele/)** liegen synthetische DTA-Dateipärchen als Fixtures für
Parser- und Regelentwicklung.

| Beispiel | Verfahren | Inhalt |
|---|---|---|
| [Pflege](beispiele/pflege-105-sgbxi/) | § 105 SGB XI (PLGA/PLAA) | Monatsabrechnung eines ambulanten Pflegedienstes, 2 Abrechnungsfälle, mit Urbelegen |

Alle Stammdaten sind erfunden. Struktur und Feldbelegung des Pflegebeispiels sind gegen
die Primärdokumente gebaut (TA 1 6.4.0, TA 3 6.4.0, Anlage 2 und Anlage 4 GGT); Preise,
Leistungskomplexnummern und Beteiligte sind synthetisch. Als Vorlage für die Erzeugung
echter Abrechnungsdateien sind die Fixtures deshalb nicht geeignet.

## Warum

§ 303 SGB V verpflichtet die Krankenkassen, bei nicht maschinell verwertbarer Übermittlung
die Nacherfassungskosten per **pauschaler Rechnungskürzung von bis zu 5 % des
Rechnungsbetrages** in Rechnung zu stellen. Fehlerhafte Abrechnungsdateien sind damit
unmittelbar zahlungswirksam — der Validator soll Fehler dort finden, wo ihre Behebung
noch nichts kostet.

## Nächste Schritte

Die Prüfstufen 0 und 1 sind nicht mehr blockiert und können implementiert werden. Für die
übrigen Stufen sind die restlichen Primärdokumente zu beschaffen (allen voran § 302
Anlage 1 und 3 sowie Anlage 16 GGT) und die offenen Punkte zu klären — siehe
**[Roadmap und offene Punkte](knowledge-base/60-projekt/02-roadmap-und-offene-punkte.md)**.

## Lizenz

Siehe [LICENSE](LICENSE). Die verlinkten Regelwerke des GKV-Spitzenverbandes und anderer
Herausgeber unterliegen deren eigenen Nutzungsbedingungen.
