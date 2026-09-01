# EDIFACT-Syntax und Zeichensatz

## 1. Grundprinzip

Die Nutzdatenformate der Verfahren nach §§ 300/301/302 SGB V und § 105 SGB XI setzen auf
**UN/EDIFACT** auf: Datenelemente und Segmente werden durch **vereinbarte Steuerzeichen**
getrennt, sodass innerhalb einer Nachricht nur signifikante Daten übertragen werden und
**nicht gefüllte Datenelemente am Segmentende entfallen können**. ⚠️ [Q1]

Das unterscheidet die Nutzdaten grundlegend vom **positionsbasierten Auftragssatz**
(Anlage 2 GGT), der ein Festsatzformat ist.

## 2. Dateirahmen

Eine Nutzdatendatei besteht aus der Folge **UNB … UNZ**. ✅ [Q22]

| Segment | Rolle |
|---|---|
| `UNA` | **Service String Advice** — legt die Trennzeichen zur Laufzeit fest. Für § 105 SGB XI **nicht vorgesehen** (s. u.); für § 302 SGB V aus Sekundärquellen genannt ⚠️ [Q1] |
| `UNB` | **Kopfsegment der Nutzdatendatei** — eröffnet, identifiziert und beschreibt die Datei ✅ [Q22] |
| `UNH` / `UNT` | Nachrichtenkopf / Nachrichtenende ✅ [Q22] |
| `UNZ` | **Endesegment der Datei** ✅ [Q22] |

### Trennzeichen — verfahrensabhängig, nicht universell

❓-07 ist für § 105 SGB XI entschieden. Die Technische Anlage 1 legt die Trennzeichen
**direkt und unveränderlich** fest und sieht **kein `UNA`-Segment** vor: ✅ [Q22]

| Funktion | § 105 SGB XI | EDIFACT-Default |
|---|---|---|
| innerhalb zusammengesetzter Datenelemente | `:` | `:` |
| Datenelementtrenner | `+` | `+` |
| **Dezimalzeichen** | **`,` (Komma)** | **`.` (Punkt)** |
| Aufhebungs-/Freigabezeichen | `?` | `?` |
| Segmentendezeichen | `'` | `'` |

> ⚠️ **Die eine Abweichung, die zählt.** Das Dezimalzeichen ist das **Komma**. Ein Parser,
> der die EDIFACT-Defaults annimmt oder ein `UNA:+.? '` unterstellt, liest Beträge falsch —
> und zwar ohne Syntaxfehler, weil `1671,00` bei Punkt-Erwartung schlicht als zwei
> Datenelemente scheitert oder als Text durchrutscht. Ein `UNA`-Segment in einer
> § 105-Datei ist selbst ein Befund.

Das Aufhebungszeichen gilt jeweils für das **unmittelbar folgende** Zeichen. Beispiel aus
der TA 1: Luigi D'Angelo wird als `D?'Angelo+Luigi+` übermittelt. ✅ [Q22]

Für §§ 300/301/302 SGB V ist die Trennzeichenfrage **weiter offen** ❓ — die dortigen
Technischen Anlagen liegen noch nicht vor. Die Annahme, sie verhielten sich wie § 105,
ist naheliegend, aber unbelegt.

### Beispielstruktur § 105 SGB XI ✅ [Q22]

```
UNB+UNOC:3+…'                       ← Dateikopf, kein UNA davor
  UNH+…+PLGA:6'                     ← Gesamtaufstellung
    FKT / REC / SRD / UST / GES / NAM
  UNT+…'
  UNH+…+PLAA:6'                     ← Abrechnungsdaten
    FKT / REC / (INV NAD [IMG] MAN (ESK (ELS [ZUS] [HIL])+)+ IAF)+
  UNT+…'
UNZ+…'                              ← Dateiende
```

## 3. Zeichensatz

### § 105 SGB XI ✅ [Q22e]

❓-08 ist für die Pflege beantwortet — und die Antwort ist zweischichtig:

| Ebene | Zeichensatz |
|---|---|
| **Auftragsdatei** (außerhalb der TI) | ISO 7-Bit DIN 66003 DRV 7 bzw. ISO 8-Bit DIN 66303 DRV 8 laut Anhang 1 der TA 1; nach Anlage 2 GGT ISO 8859-1 (`I1`) |
| **EDIFACT-Nutzdaten** | ISO 8859-1 **oder** ISO 7-Bit **oder** ISO 8-Bit — die Wahl steht dem Absender offen |
| **`UNB` Syntax-Kennung** | `UNOC`, Syntax-Version `3` — Groß- und Kleinbuchstaben, Umlaute |
| **XML-Hülle in der TI (KIM)** | **UTF-8 nach DIN SPEC 91379**, nur normative darstellbare Zeichen, **kein BOM** |

Die eingebetteten EDIFACT-Abrechnungsdaten behalten auch **innerhalb** der TI ihren
ISO-Zeichensatz — die UTF-8-Vorgabe gilt nur für den XML-Umschlag. Ein Validator, der die
base64-decodierten Abrechnungsdaten als UTF-8 liest, verstümmelt Umlaute.

### § 301 Abs. 3 SGB V ⚠️ [Q1]

| Norm | Beschreibung |
|---|---|
| **DIN 66303:2000-06** | 8-Bit-Code, deutsche Referenzversion (DRV) |
| **DIN 66003 DRV** | 7-Bit-Code, deutsche Referenzversion |

**Praxisrelevanz:** DIN 66003 (7-Bit DRV) ersetzt die Zeichen `[ \ ] { | } ~` durch
`Ä Ö Ü ä ö ü ß`. Ein Parser, der naiv als ASCII oder UTF-8 liest, produziert bei
Umlauten falsche Ergebnisse. Der Validator braucht eine **explizite, konfigurierbare
Zeichensatz-Dekodierung** und muss unzulässige Zeichen als Fehler melden.

### Kennungen im Auftragssatz ✅ [Q7]

Das Feld `ZEICHENSATZ` (Stellen 203–204) benennt den Zeichensatz der **Nutzdaten**:

`I1` ISO 8859-1 / DIN 66303:2000-06 · `I5` ISO 8859-15 · `I7` ISO 7-Bit DIN 66003 DRV ·
`I8` DIN 66303:1986-11 (DRV8) · `EB` EBCDIC · `P8` IBM-Codepage 850 · `U8` UTF-8 · `BI` binär

**`EB` (EBCDIC) ist im Datenaustausch mit Leistungserbringern nach § 294 ff. SGB V
ausdrücklich unzulässig** — eine direkt implementierbare Prüfregel. `P8` gilt nur nach
bilateraler Vereinbarung, `U8` nur wenn das Fachverfahren es explizit festlegt. Die
normative Beschreibung der Kennungen steht in **Anlage 15 GGT (Zeichensätze)** ✅ [Q12],
die noch nicht ausgewertet ist. ❓

## 4. Konsequenzen für den Parser

| Anforderung | Begründung |
|---|---|
| Trennzeichen **je Verfahren** auflösen, nicht global | § 105 SGB XI legt sie fest (Dezimalzeichen Komma, kein UNA) ✅ [Q22]; für § 302 ist ein UNA aus Sekundärquellen genannt ⚠️ [Q1] |
| Freigabe-/Escape-Zeichen korrekt behandeln | Trennzeichen können in Nutzdaten vorkommen |
| Fehlende Datenelemente am Segmentende tolerieren | Explizit erlaubt ⚠️ [Q1] |
| Zeichensatz konfigurierbar (ISO 8859-1 / DIN 66003 DRV / DIN 66303) | § 301 ⚠️ [Q1], § 105 SGB XI ✅ [Q22e] |
| Zeichensatz aus dem Auftragssatz (Stellen 203–204) übernehmen, nicht raten | `ZEICHENSATZ` benennt ihn verbindlich ✅ [Q7] |
| Bei TI/KIM zwei Zeichensätze gleichzeitig beherrschen | UTF-8 für die XML-Hülle, ISO für die eingebetteten EDIFACT-Daten ✅ [Q22e] |
| Segmentreihenfolge und Kardinalitäten je Nachrichtentyp prüfen | Segmente kommen ein-/mehrfach oder nur in bestimmten Abrechnungsfällen vor ⚠️ [Q1] |
| Zähler-/Summenkonsistenz prüfen (UNZ vs. Anzahl Nachrichten, GES vs. Positionssummen) | Klassische EDIFACT-Kontrollprüfung |

## 5. Abweichende Formate

| Verfahren | Format | Marker |
|---|---|---|
| § 105 SGB XI (außerhalb der TI) | EDIFACT-nahe Segmentsyntax, feste Trennzeichen | ✅ [Q22] |
| § 105 SGB XI (TI/KIM) | XML-Umschlag mit base64-codierten, einzeln signierten EDIFACT- und XML-Teilen | ✅ [Q22] |
| §§ 300/301/302 SGB V | EDIFACT-nahe Segmentsyntax | ⚠️ |
| Auftragssatz (Anlage 2 GGT) | positionsbasiertes Festsatzformat | ⚠️ [Q7] |
| Arbeitgeberverfahren | **eXTra-XML** | ⚠️ [Q17] |
| Reha § 301 (DRV-Bereich) | **XML** | ⚠️ |
| Kostenträgerdateien | eigenes Satzformat (Endungen `KE0`, `KE1`, …) | ⚠️ [Q15] |

§ 95 SGB IV nennt ausdrücklich die "Zeitpunkte der Umstellung einzelner technischer
Verfahren auf XML-basierte Verfahren" als Regelungsgegenstand der GGT ⚠️ [Q11] — die
EDIFACT-Formate sind also mittelfristig ein Auslaufmodell. Der Validator sollte
**Parser und Regelwerk trennen**, damit ein XML-Parser später gegen dieselben
fachlichen Regeln laufen kann.
