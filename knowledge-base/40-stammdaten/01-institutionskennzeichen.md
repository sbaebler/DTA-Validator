# Institutionskennzeichen (IK)

Das IK ist die **zentrale Identität** im gesamten GKV-Datenaustausch: Leistungserbringer,
Kostenträger, Datenannahmestellen und Abrechnungszentren werden darüber adressiert.

## 1. Vergabestelle

Die **ARGE·IK** (Arbeitsgemeinschaft Institutionskennzeichen), angesiedelt bei der DGUV,
vergibt und pflegt die Institutionskennzeichen. Hinter jedem IK steht ein Datensatz, auf
dessen Grundlage der Zahlungsverkehr mit den Leistungserbringern abgewickelt wird. ⚠️ [Q9]

<https://www.dguv.de/arge-ik/index.jsp>

> **Quellenstand:** Das *Gemeinsame Rundschreiben Institutionskennzeichen 02/2026* liegt
> vor; Nummer 1.2 (Aufbau, Klassifikation, Regionalbereich, Seriennummer, Prüfziffer)
> sowie die Anlagen 1 und 2.1/2.2 sind ausgewertet. ✅ [Q9b]
> Eine Nachfolgeausgabe **04/2027** ist bereits veröffentlicht und noch nicht ausgewertet.

## 2. Aufbau

**9 Ziffern**, gegliedert in vier Bereiche: ✅ [Q9b]

```
  1 2   3 4   5 6 7 8   9
  └┬┘   └┬┘   └──┬──┘   │
   │     │        │      └── Stelle 9:    Prüfziffer
   │     │        └───────── Stellen 5–8: Seriennummer
   │     └────────────────── Stellen 3–4: Regionalbereich
   └──────────────────────── Stellen 1–2: Klassifikation des IK-Inhabers
```

| Stellen | Inhalt |
|---|---|
| **1–2** | Klassifikation des IK-Inhabers (Art der Institution bzw. Personengruppe), Anlage 1 |
| **3–4** | Regionalbereich, Anlage 2.1 (Leistungserbringer) bzw. Anlage 2.2 (Kassen, KVen, Apotheken, Sozialhilfeträger) |
| **5–8** | Seriennummer, teilweise kontingentiert (Anlage 1) |
| **9** | Prüfziffer, **berechnet aus den Stellen 3–8** |

### Zwei Regionalschlüssel-Systematiken ✅ [Q9b]

Das ist die Falle bei der Auswertung: Die Stellen 3–4 werden **je nach Klassifikation
unterschiedlich** aufgelöst.

| Anlage | Gilt für | Beispiel Berlin |
|---|---|---|
| **2.1** | Leistungserbringer, Rechenzentren, Abrechnungsstellen | `11`, `31`, `51`, `71`, `91` |
| **2.2** | Krankenkassen, **Pflegekassen**, Kassenärztliche Vereinigungen, Ärzte, Apotheken, Sozialhilfeträger, Krebsregister, Beihilfestellen | `95` (`96` reserviert) |

Anlage 2.1 gliedert nach Bundesländern mit mehreren Überlaufbereichen je Land; Anlage 2.2
gliedert feiner nach Kassenbezirken (z. B. `84` München-Stadt, `53` Frankfurt) und
reserviert `99` für Bundesorganisationen.

### Für die Leistungserbringer-Verfahren wichtige Klassifikationen ✅ [Q9b]

| Klassifikation | Geltungsbereich |
|---|---|
| `10` | Krankenversicherungsträger |
| **`18`** | **Pflegekassen der Krankenversicherungsträger** |
| `20` / `21` | Kassenärztliche / Kassenzahnärztliche Vereinigungen |
| `26` | Krankenhäuser |
| `46` | Kranken- und Altenpfleger, Haushaltshilfen, Hauspfleger |
| `51` | Alten- und Pflegeheime, Tages- und Kurzzeitpflege |
| `54` / `57` | ambulante bzw. stationäre Vorsorge- und Rehabilitationseinrichtungen |
| `58` | DiGA-Hersteller |
| `59` | Sonstige Erbringer von Leistungen i. S. des SGB |
| `60` | Krankentransportunternehmen |
| `66` | Abrechnungsstellen, Rechenzentren, Rechnungsprüfstellen |
| `68` | Softwarehersteller |
| `97`–`99` | Verwendung im Ermessen des Anwenders |

Das erklärt, warum die TA 1 zu § 105 SGB XI verlangt, dass das `IK der Pflegekasse`
**immer mit `18` beginnt** ✅ [Q22] — eine direkt implementierbare Prüfregel (`S4-XI-002`).

## 3. Prüfziffernberechnung

✅ [Q9b] — ❓-10 ist damit geklärt.

Die Prüfziffer wird **aus den Stellen 3 bis 8** berechnet — die **Klassifikation
(Stellen 1–2) geht nicht ein**. Verfahren: **Modulo 10, von rechts beginnend mit der
Gewichtung 1·2·1·2·1·2**.

### Algorithmus

1. Betrachte die Stellen **3–8** (sechs Ziffern)
2. Gewichte **von rechts beginnend** mit `1, 2, 1, 2, 1, 2`
   (äquivalent: von links `2, 1, 2, 1, 2, 1`)
3. Multipliziere jede Ziffer mit ihrem Gewicht
4. Bilde von jedem Produkt die **Quersumme** — bei zweistelligen Produkten (höchstens 18)
   ist das gleichbedeutend mit „minus 9"
5. Bilde die **Summe** der Quersummen
6. Die Prüfziffer ist der **Rest der Summe modulo 10** und wird hinter der Einerstelle
   der Seriennummer angefügt

### Testvektor aus der Quelle ✅ [Q9b]

IK `260326822`, Kern `032682`:

| | | | | | | |
|---|---:|---:|---:|---:|---:|---:|
| Wert | 0 | 3 | 2 | 6 | 8 | 2 |
| Multiplikator | 2 | 1 | 2 | 1 | 2 | 1 |
| Produkt | 0 | 3 | 4 | 6 | 16 | 2 |
| Quersumme | 0 | 3 | 4 | 6 | **7** | 2 |

Summe 22, 22 mod 10 = **2**. Vollständiges IK: `260326822`.

### Referenzimplementierung (Pseudocode)

```python
def ik_pruefziffer(ik: str) -> int:
    """Erwartet mindestens die Stellen 1-8 eines IK. Liefert die Pruefziffer (Stelle 9)."""
    kern = ik[2:8]                        # Stellen 3-8 (0-basiert: Index 2..7)
    gewichte = [2, 1, 2, 1, 2, 1]         # von links; entspricht 1,2,1,2,1,2 von rechts
    summe = 0
    for ziffer, gewicht in zip(map(int, kern), gewichte):
        produkt = ziffer * gewicht
        if produkt > 9:
            produkt -= 9
        summe += produkt
    return summe % 10


def ik_gueltig(ik: str) -> bool:
    return len(ik) == 9 and ik.isdigit() and int(ik[8]) == ik_pruefziffer(ik)
```

> ✅ **Verifiziert** gegen das Gemeinsame Rundschreiben Institutionskennzeichen 02/2026,
> Nummer 1.2.5. Der dort gerechnete Testvektor `260326822` stimmt mit dem Pseudocode
> überein; Gewichtungsrichtung und Quersummenbildung sind bestätigt.
>
> Für eine Testsuite empfiehlt sich zusätzlich mindestens ein reales, öffentlich bekanntes
> Kassen-IK aus einer Kostenträgerdatei — der Testvektor der Quelle deckt keinen Fall ab,
> in dem die Summe ein Vielfaches von 10 ergibt (Prüfziffer `0`).

## 4. Verwendung im Datenaustausch

| Kontext | Rolle des IK |
|---|---|
| Auftragssatz | `ABSENDER_EIGNER` (33–47), `ABSENDER_PHYSIKALISCH` (48–62), `EMPFÄNGER_NUTZER` (63–77), `EMPFÄNGER_PHYSIKALISCH` (78–92) — je 15 Stellen, IK linksbündig ✅ [Q7] |
| E-Mail-Betreffzeile | Betriebsnummer **oder IK** ⚠️ [Q16] |
| `FKT`-Segment | Absender-/Empfänger-IK der Nachricht ⚠️ |
| Kostenträgerdatei | IK der Daten- und Belegannahmestellen ⚠️ [Q15] |
| KVNR (20-stellige Form) | 9 Stellen IK der Krankenkasse ⚠️ [Q10w] |
| SLGA/SLLA | Mehrere Abrechnungsfälle mit identischem IK gemeinsam übermittelbar ⚠️ [Q30] |

## 5. Prüfregel-Kandidaten

| Regel | Schwere |
|---|---|
| IK ist genau 9-stellig und rein numerisch | Fehler |
| Prüfziffer (Stelle 9) korrekt | Fehler |
| IK ist in der Kostenträgerdatei bekannt | Fehler (bei Empfänger) / Warnung (bei Dritten) |
| Absender-IK im Auftragssatz = Absender-IK in den Nutzdaten (`FKT`) | Fehler ❓ Feldzuordnung verifizieren |
| Klassifikation (Stellen 1–2) passt zur Rolle (LE vs. Kostenträger) | Warnung ✅ [Q9b] |
| `IK der Pflegekasse` in `PLGA.FKT`/`PLAA.FKT` beginnt mit `18` | Fehler ✅ [Q22] (`S4-XI-002`) |

> **Zwei Fallen bei der Prüfziffer:**
>
> 1. Die **Klassifikation geht nicht ein**. Zwei IK, die sich nur in den Stellen 1–2
>    unterscheiden, haben dieselbe Prüfziffer — etwa eine Krankenkasse (`10…`) und die bei
>    ihr errichtete Pflegekasse (`18…`) mit gleichem Regionalbereich und gleicher
>    Seriennummer. Eine Implementierung, die über die Stellen 1–8 rechnet, weist beide
>    zurück.
> 2. Der **Regionalbereich lässt sich nicht ohne die Klassifikation auflösen**. Anlage 2.1
>    und Anlage 2.2 vergeben dieselben Zahlen an unterschiedliche Regionen. Eine
>    Plausibilitätsprüfung „Regionalbereich existiert" muss also zuerst über die
>    Klassifikation entscheiden, welche Tabelle gilt.
