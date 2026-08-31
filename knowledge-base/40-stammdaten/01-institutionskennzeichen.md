# Institutionskennzeichen (IK)

Das IK ist die **zentrale Identität** im gesamten GKV-Datenaustausch: Leistungserbringer,
Kostenträger, Datenannahmestellen und Abrechnungszentren werden darüber adressiert.

## 1. Vergabestelle

Die **ARGE·IK** (Arbeitsgemeinschaft Institutionskennzeichen), angesiedelt bei der DGUV,
vergibt und pflegt die Institutionskennzeichen. Hinter jedem IK steht ein Datensatz, auf
dessen Grundlage der Zahlungsverkehr mit den Leistungserbringern abgewickelt wird. ⚠️ [Q9]

<https://www.dguv.de/arge-ik/index.jsp>

## 2. Aufbau

**9 Ziffern**, gegliedert in vier Bereiche: ⚠️ [Q9]

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
| **1–2** | Klassifikation des IK-Inhabers (Art der Institution bzw. Personengruppe) |
| **3–4** | Regionalbereich (geografische Zugehörigkeit innerhalb der Bundesrepublik) |
| **5–8** | Seriennummer |
| **9** | Prüfziffer |

## 3. Prüfziffernberechnung

⚠️ [Q9]

Die Prüfziffer wird **aus den Stellen 3 bis 8** berechnet — die **Klassifikation
(Stellen 1–2) geht nicht ein**. Verfahren: **Modulo 10**.

### Algorithmus

1. Betrachte die Stellen **3–8** (sechs Ziffern)
2. Gewichte **von rechts beginnend** mit `1, 2, 1, 2, 1, 2`
   (äquivalent: von links `2, 1, 2, 1, 2, 1`)
3. Multipliziere jede Ziffer mit ihrem Gewicht
4. Von Produkten **größer 9** wird **9 subtrahiert** (entspricht der Quersumme)
5. Bilde die **Summe** der Ergebnisse
6. Die Prüfziffer ist der **Rest der Summe modulo 10** und wird hinter der Einerstelle
   der Seriennummer angefügt

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

> ❓ **Vor produktivem Einsatz zwingend verifizieren** gegen das *Gemeinsame Rundschreiben
> Institutionskennzeichen (IK)* der ARGE·IK — insbesondere die Gewichtungsrichtung und die
> Behandlung von Produkten > 9. Ein Fehler hier führt zu systematisch falschen
> Validierungsergebnissen. Testvektoren aus echten, öffentlich bekannten IK
> (z. B. Kassen-IK aus Kostenträgerdateien) aufbauen.

## 4. Verwendung im Datenaustausch

| Kontext | Rolle des IK |
|---|---|
| Auftragssatz | Absender (`ABSENDER_EIGNER`) und Empfänger (`EMPFAENGER`) ⚠️ [Q7] |
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
| Klassifikation (Stellen 1–2) passt zur Rolle (LE vs. Kostenträger) | Warnung ❓ Klassifikationstabelle beschaffen |

> ❓ Die **Klassifikationstabelle für die Stellen 1–2** (welcher Wert steht für welche
> Institutionsart) ist nicht recherchiert. Sie ist dem Gemeinsamen Rundschreiben der
> ARGE·IK zu entnehmen und wäre eine wertvolle Prüfregel.
