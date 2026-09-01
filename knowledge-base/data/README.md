# Maschinenlesbare Referenzdaten

Diese YAML-Dateien sind die strukturierte Fassung der Wissensbibliothek. Sie sind als
Eingabe für Codegenerierung, Tests und die Regelwerks-Registry des Validators gedacht.

| Datei | Inhalt | Quelle |
|---|---|---|
| [`verfahren.yaml`](verfahren.yaml) | Alle DTA-Verfahren mit Rechtsgrundlage, Format, Regelwerk und Validator-Priorität | gemischt |
| [`nachrichtentypen.yaml`](nachrichtentypen.yaml) | Nachrichtentypen, Segmente und Kardinalitäten je Verfahren | § 105 SGB XI ✅ TA 1 6.4.0 |
| [`auftragssatz.yaml`](auftragssatz.yaml) | **Vollständiger Feldkatalog des Auftragssatzes** — 37 Felder, Stellen 1–348, lückenlos | ✅ Anlage 2 GGT |
| [`verfahrenskennungen.yaml`](verfahrenskennungen.yaml) | **Werteliste der Verfahrenskennungen** — 322 Einträge plus Bereichsregeln für den LE-Datenaustausch | ✅ Anlage 4 GGT |
| [`dokumentenregister.yaml`](dokumentenregister.yaml) | Regelwerke mit Version, Stand, Gültigkeit, URL und Beschaffungsstatus | Portalseiten + Primärdokumente |
| [`pruefregeln.yaml`](pruefregeln.yaml) | Prüfregelkatalog mit Stufe, Schwere und Implementierungsstatus | abgeleitet |

`auftragssatz.yaml` und `verfahrenskennungen.yaml` sind die **abgeleiteten strukturierten
Regeldateien** zu Anlage 2 und Anlage 4 GGT. Die PDFs selbst liegen bewusst nicht im
Repository (Urheber- und Nutzungsrechte); jede Datei nennt Dokumenttitel, Version, Stand
und URL, sodass sich jeder Eintrag am Primärdokument nachschlagen lässt.

## Feld `vertrauen` / `status`

Beide Felder kodieren, wie belastbar ein Eintrag ist:

| Wert | Bedeutung |
|---|---|
| `belegt` / `spezifiziert` | Aus Gesetzestext oder eindeutigen Dokument-Metadaten belegt bzw. gegen das Primärdokument verifiziert |
| `sekundaer` / `entwurf` | Aus Sekundärquelle; Absicht klar, Detailvorgabe nicht verifiziert |
| `offen` / `experimental` | Nicht belegt oder widersprüchlich — **nicht produktiv verwenden** |

Zusätzlich nennt `blocker` bei Prüfregeln, welche Information zur Umsetzung noch fehlt,
und `prioritaet_beschaffung` im Dokumentenregister die Dringlichkeit der Dokumentbeschaffung.

## Pflege

- Neue Regelwerksversion → `dokumentenregister.yaml` ergänzen (alte Fassung mit
  `gueltig_bis` behalten, nicht löschen — Übergangsfristen brauchen beide).
- Primärdokument ausgewertet → `beschafft: true` setzen und `vertrauen` anheben.
- Regel verifiziert → `status` von `experimental`/`entwurf` auf `spezifiziert` heben und
  `quelle` um die konkrete Fundstelle (Kapitel/Seite) ergänzen.

## Syntaxprüfung

```bash
python3 -c "import yaml,glob; [yaml.safe_load(open(f)) for f in glob.glob('knowledge-base/data/*.yaml')]"
```

Zusätzlich für `auftragssatz.yaml` — der Feldkatalog muss die Stellen 1 bis 348
**lückenlos und überlappungsfrei** abdecken:

```bash
python3 - <<'EOF'
import yaml
felder = yaml.safe_load(open('knowledge-base/data/auftragssatz.yaml'))['felder']
pos = 1
for f in felder:
    assert f['von'] == pos, (f['name'], 'erwartet', pos, 'ist', f['von'])
    assert f['bis'] - f['von'] + 1 == f['laenge'], f['name']
    pos = f['bis'] + 1
assert pos - 1 == 348
print('Feldkatalog lueckenlos, Satzlaenge 348')
EOF
```
