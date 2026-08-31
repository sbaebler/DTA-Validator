# KKS, Auftragsdatei und Dateinamenskonvention

Der gemeinsame Transportrahmen aller GKV-Verfahren — und die **erste Prüfstufe** eines
DTA-Validators.

## 1. Krankenkassenkommunikationssystem (KKS)

Das KKS ist ein **logischer Standard**, der beschreibt, in welcher Weise Auftrags- und
Nutzdaten ausgetauscht werden. Es ist das Standardverfahren für den Datenaustausch von
Arbeitgebern und Leistungserbringern mit der Sozialversicherung. ⚠️ [Q14][Q14w]

### Das Dateipärchen ⚠️ [Q14w]

| Datei | Inhalt | Verschlüsselung |
|---|---|---|
| **Nutzdatendatei** | Fachliche Abrechnungsdaten | **verschlüsselt** (Anlage 16 / SECON) |
| **Auftragsdatei** | Auftragssatz mit allen transportnotwendigen Informationen | **unverschlüsselt** |

### Übertragungsreihenfolge ⚠️ [Q14w]

1. Die verschlüsselte **Nutzdatendatei** wird als separate Datei übertragen
2. **Danach** wird die zugehörige **Auftragsdatei** übertragen
3. Ein Übertragungsvorgang besteht aus genau diesen zwei Dateien in dieser Reihenfolge

Die Auftragsdatei fungiert damit als **Commit-Signal**: Erst wenn sie vorliegt, gilt die
Nutzdatendatei als vollständig übertragen und wird verarbeitet.

**Prüfregel-Kandidat:** Eine Nutzdatendatei ohne zugehörige Auftragsdatei (oder umgekehrt)
ist ein Transportfehler, kein Fachfehler.

### Warum unverschlüsselt?

Die Auftragsdatei muss von der Datenannahmestelle **vor** der Entschlüsselung gelesen
werden können, um Routing und automatisierte Verarbeitung zu ermöglichen. ⚠️ [Q7]
Daraus folgt datenschutzrechtlich das **Trennungsgebot**: Die Auftragsdatei darf keine
Sozialdaten enthalten.

## 2. Der Auftragssatz (Anlage 2 GGT)

⚠️ [Q7]

- Der Auftragssatz ist **logisch in mehrere Tabellen (Objekte) gegliedert**, besteht
  **physisch aber aus einem einzigen zusammenhängenden Satz**.
- Es handelt sich um ein **positionsbasiertes Festsatzformat** (keine Segmenttrennzeichen).

### Belegte Felder

| Feld | Position | Bedeutung | Marker |
|---|---|---|---|
| `VERFAHREN_KENNUNG` | **20–24** | Kennung des Fachverfahrens (Werteliste in Anlage 4 GGT) | ⚠️ [Q20] |
| `ABSENDER_EIGNER` | ❓ | Absender/Eigner der Nutzdaten (Identifikation des Senders) | ⚠️ [Q7] |
| `EMPFAENGER` | ❓ | Empfänger, der die Daten erhalten soll | ⚠️ [Q7] |
| `TRANSFER_NUMMER` | ❓ | Laufende Transfernummer, korrespondiert mit dem Dateinamen | ⚠️ [Q7] |

> ❓ **Kritische Lücke:** Die vollständige Feldliste mit Positionen, Längen, Datentypen und
> Pflichtfeld-Kennzeichnung ist **zwingend aus Anlage 2 GGT** [Q7] zu übernehmen, bevor der
> Auftragssatz-Parser implementiert wird. Die obige Tabelle ist unvollständig.

## 3. Dateinamenskonvention

⚠️ [Q7]

### Nutzdatendatei — 8 Stellen

```
  E   R B A   0    1 2 3
  │   └─┬─┘   │    └─┬─┘
  │     │     │      └──── Stellen 6–8: laufende Transfernummer (aufsteigend)
  │     │     └─────────── Stelle 5:    Verfahrensversion (z. B. "0")
  │     └───────────────── Stellen 2–4: Verfahrenskennung (z. B. "RBA")
  └─────────────────────── Stelle 1:    "T" = Test, "E" = Echt/Produktion
```

Beispiel: `ERBA0123`

| Stelle | Inhalt | Werte |
|---|---|---|
| 1 | Test-/Echt-Kennzeichen | `T` = Test, `E` = Echtdaten |
| 2–4 | Verfahrenskennung | 3-stellig, z. B. `RBA` |
| 5 | Verfahrensversion | z. B. `0` |
| 6–8 | Transfernummer | aufsteigend |

### Auftragsdatei

Name der Nutzdatendatei (erste 8 Stellen) **+ Endung `.AUF`**

Beispiel: `ERBA0123.AUF` ⚠️ [Q7]

### Kopplungsregel ⚠️ [Q7]

> Nutzdatendatei und Auftragsdatei müssen in den **ersten 8 Stellen denselben Namen**
> tragen. Die **Endung der Nutzdatendatei wird ignoriert**.

**Prüfregel-Kandidaten:**
- `basename(nutzdaten)[0:8] == basename(auftrag)[0:8]`
- `basename(auftrag).endswith('.AUF')`
- Stelle 1 ∈ {`T`, `E`}
- Stellen 2–4 sind eine gültige Verfahrenskennung (Anlage 4 GGT)
- Stellen 6–8 numerisch
- Das Test-/Echt-Kennzeichen im Dateinamen ist **konsistent** mit dem entsprechenden
  Kennzeichen im Auftragssatz und in den Nutzdaten ❓ (Feldzuordnung verifizieren)

## 4. Verfahrenskennungen (Anlage 4 GGT)

**Anlage 4 GGT — Verfahrenskennungen**, gültig ab **01.01.2026**, Stand 06.11.2025,
47 Seiten. ✅ [Q20]

Abgedeckte Bereiche laut Dokumentbeschreibung ⚠️ [Q20]:
- Datenaustausch mit Arbeitgebern
- Datenaustausch mit der Rentenversicherung
- Datenaustausch zwischen Leistungserbringern und Krankenkassen nach **§ 294 ff. SGB V**
- Datenaustausch zwischen Leistungserbringern und Pflegekassen nach **§ 105 SGB XI**
- Datenübermittlung mit Erstellern von Versichertenkarten
- Datenaustausch zwischen Krankenkassen und Weiterleitungsstellen

> ❓ **Kritische Lücke:** Die konkrete Werteliste der Verfahrenskennungen (z. B. welche
> Kennung für § 302 Heilmittel, welche für § 105 SGB XI) ist **nicht belegt**. 47 Seiten
> Umfang deuten auf eine sehr umfangreiche Tabelle hin. Diese Liste ist die
> **wichtigste einzelne Referenzdatei** für den Validator und muss vollständig aus
> Anlage 4 GGT übernommen werden.

## 5. Ablaufdiagramm

```
 Erzeugung                        Übertragung                  Annahme
 ─────────                        ───────────                  ───────
 Nutzdaten (Klartext)
        │
        │ SECON: signieren (SignedData)
        │        verschlüsseln (EnvelopedData)
        ▼
 ERBA0123          ──── 1. ────►                          ┌─ Datei zwischenspeichern
                                                          │
 Auftragssatz erzeugen                                    │
 (Klartext, Festsatz)                                     │
        ▼                                                 ▼
 ERBA0123.AUF      ──── 2. ────►                    Auftragssatz lesen
                                                    → Verfahrenskennung
                                                    → Absender/Empfänger
                                                    → Routing
                                                          │
                                                          ▼
                                                    Entschlüsseln + Signatur prüfen
                                                          │
                                                          ▼
                                                    Fachliche Prüfung (Sektor-TA)
```
