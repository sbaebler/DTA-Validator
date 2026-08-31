# Krankenversichertennummer (KVNR)

## 1. Rechtsgrundlage

**§ 290 SGB V**. Umsetzung: *Richtlinie zum Aufbau und zur Vergabe einer
Krankenversichertennummer* (Gesamtsystem KVNR), **Version 3.4.0 vom 22.08.2024**. ✅ [Q10]

## 2. Aufbau

### Unveränderbarer Teil — 10 Zeichen ⚠️ [Q10w]

```
  A   1 2 3 4 5 6 7 8   9
  │   └──────┬───────┘  │
  │          │           └── Stelle 10: Prüfziffer
  │          └────────────── Stellen 2–9: 8 Ziffern
  └───────────────────────── Stelle 1: Großbuchstabe A–Z
```

- **1 Großbuchstabe (A–Z)** + **8 Ziffern** + **1 Prüfziffer**
- Seit Einführung der elektronischen Gesundheitskarte (2012) werden die ersten zehn
  Stellen **einmalig vergeben und bleiben lebenslang gleich** — auch bei Kassenwechsel

### Vollständige Form — 20 Stellen ⚠️ [Q10w]

| Teil | Länge | Inhalt |
|---|---|---|
| Persönlicher Teil | 10 | unveränderbarer Teil (s. o.) |
| Institutionskennzeichen | 9 | IK der aktuellen Krankenkasse |
| Prüfziffer | 1 | Prüfziffer über den veränderbaren Teil |

> ❓ Die Zusammensetzung "10 + 9 + 1 = 20" stammt aus einer Sekundärquelle und ist gegen
> die KVNR-Richtlinie [Q10] zu verifizieren.

## 3. Prüfziffernberechnung (unveränderbarer Teil)

⚠️ [Q10w]

Die Prüfziffer wird nach dem **Modulo-10-Verfahren** mit den Gewichtungen
**1-2-1-2-1-2-1-2-1-2** berechnet.

> ❓ **Kritische Lücke:** Wie der **führende Großbuchstabe** in die Berechnung eingeht,
> ist aus der Recherche **nicht belegt**. In der Praxis wird der Buchstabe üblicherweise
> in eine zweistellige Zahl umgesetzt (A = 01, B = 02, …, Z = 26), die dann in die
> Gewichtungskette eingeht — **das ist hier aber eine Annahme, kein Beleg**.
>
> Vor Implementierung zwingend aus der KVNR-Richtlinie V3.4.0 [Q10] übernehmen und mit
> Testvektoren absichern.

## 4. Verwendung im Datenaustausch

- Im **`INV`-Segment** ("Information des Versicherten") der Abrechnungsnachrichten ⚠️ [Q30]
- Aus der elektronischen Gesundheitskarte gelesen (Versichertenstammdaten)
- Referenz für die Zuordnung des Abrechnungsfalls zum Kostenträger

## 5. Prüfregel-Kandidaten

| Regel | Schwere |
|---|---|
| Format: `^[A-Z][0-9]{9}$` (unveränderbarer Teil) | Fehler |
| Prüfziffer korrekt | Fehler |
| Bei 20-stelliger Form: eingebettetes IK ist ein gültiges Kassen-IK | Fehler |
| Eingebettetes Kassen-IK stimmt mit dem Empfänger-IK der Abrechnung überein | Warnung ❓ verifizieren |

## 6. Datenschutzhinweis

Die KVNR ist ein **personenbezogenes Sozialdatum**. Für Testdaten und Beispieldateien im
Repository sind **ausschließlich synthetisch erzeugte KVNR** zu verwenden, die die
Prüfziffernregel erfüllen, aber keiner realen Person zugeordnet sind. Keine echten
KVNR in Fixtures, Logs oder Fehlermeldungen.
