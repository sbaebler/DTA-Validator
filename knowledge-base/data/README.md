# Maschinenlesbare Referenzdaten

Diese YAML-Dateien sind die strukturierte Fassung der Wissensbibliothek. Sie sind als
Eingabe für Codegenerierung, Tests und die Regelwerks-Registry des Validators gedacht.

| Datei | Inhalt |
|---|---|
| [`verfahren.yaml`](verfahren.yaml) | Alle DTA-Verfahren mit Rechtsgrundlage, Format, Regelwerk und Validator-Priorität |
| [`nachrichtentypen.yaml`](nachrichtentypen.yaml) | Nachrichtentypen und bekannte Segmente je Verfahren |
| [`dokumentenregister.yaml`](dokumentenregister.yaml) | Regelwerke mit Version, Stand, Gültigkeit, URL und Beschaffungsstatus |
| [`pruefregeln.yaml`](pruefregeln.yaml) | Prüfregelkatalog mit Stufe, Schwere und Implementierungsstatus |

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
