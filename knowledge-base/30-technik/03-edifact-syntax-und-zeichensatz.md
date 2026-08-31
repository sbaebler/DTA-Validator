# EDIFACT-Syntax und Zeichensatz

## 1. Grundprinzip

Die Nutzdatenformate der Verfahren nach §§ 300/301/302 SGB V und § 105 SGB XI setzen auf
**UN/EDIFACT** auf: Datenelemente und Segmente werden durch **vereinbarte Steuerzeichen**
getrennt, sodass innerhalb einer Nachricht nur signifikante Daten übertragen werden und
**nicht gefüllte Datenelemente am Segmentende entfallen können**. ⚠️ [Q1]

Das unterscheidet die Nutzdaten grundlegend vom **positionsbasierten Auftragssatz**
(Anlage 2 GGT), der ein Festsatzformat ist.

## 2. Dateirahmen

Eine Nutzdatendatei besteht aus der Folge **UNB … UNZ**. ⚠️ [Q1]

| Segment | Rolle | Marker |
|---|---|---|
| `UNA` | **Service String Advice** — legt die Trennzeichen fest. Beginnt mit den Großbuchstaben `UNA`, unmittelbar gefolgt von **sechs** definierten Trennzeichen in festgelegter Reihenfolge. Innerhalb des UNA-Segments selbst werden **keine** Trennzeichen verwendet. ⚠️ [Q1] |
| `UNB` | **Kopfsegment der Nutzdatendatei** — dient zum Eröffnen, Identifizieren und Beschreiben der Datei. Enthält u. a. Absender-/Empfängerkennung und die Nachrichtentyp-Kennung. ⚠️ [Q1][Q30] |
| `UNH` / `UNT` | Nachrichtenkopf / Nachrichtenende (EDIFACT-Standard) ❓ nicht direkt belegt, aber syntaktisch erforderlich |
| `UNZ` | **Endesegment der Datei** ⚠️ [Q1] |

### Beispielstruktur § 302 ⚠️ [Q1]

```
UNA:+.? '
UNB+...'                     ← Dateikopf
  SLGA  (Gesamtaufstellung)  ← wiederholbar
  SLLA  (Abrechnungsdaten)   ← wiederholbar
  SLGA
  SLLA
  ...
UNZ+...'                     ← Dateiende
```

> ❓ Das UNA-Beispiel oben zeigt die EDIFACT-**Default**-Trennzeichen
> (`:` Komponententrenner, `+` Datenelementtrenner, `.` Dezimalzeichen,
> `?` Freigabezeichen, ` ` reserviert, `'` Segmentendezeichen). Ob die GKV-Verfahren
> diese Defaults verwenden oder abweichende Zeichen vorschreiben, ist **aus der jeweiligen
> Technischen Anlage zu verifizieren** und darf nicht angenommen werden.

## 3. Zeichensatz

Für die Datenübermittlung nach § 301 Abs. 3 SGB V sind genannt: ⚠️ [Q1]

| Norm | Beschreibung |
|---|---|
| **DIN 66303:2000-06** | 8-Bit-Code, deutsche Referenzversion (DRV) |
| **DIN 66003 DRV** | 7-Bit-Code, deutsche Referenzversion |

**Praxisrelevanz:** DIN 66003 (7-Bit DRV) ersetzt die Zeichen `[ \ ] { | } ~` durch
`Ä Ö Ü ä ö ü ß`. Ein Parser, der naiv als ASCII oder UTF-8 liest, produziert bei
Umlauten falsche Ergebnisse. Der Validator braucht eine **explizite, konfigurierbare
Zeichensatz-Dekodierung** und muss unzulässige Zeichen als Fehler melden.

> ❓ Für §§ 300/302 SGB V und § 105 SGB XI ist der zulässige Zeichensatz jeweils aus der
> Technischen Anlage zu verifizieren; eine Übertragung der § 301-Vorgabe ist **nicht** zulässig.

## 4. Konsequenzen für den Parser

| Anforderung | Begründung |
|---|---|
| Trennzeichen **aus dem UNA-Segment** lesen, nicht hartkodieren | UNA definiert sie zur Laufzeit ⚠️ [Q1] |
| Freigabe-/Escape-Zeichen korrekt behandeln | Trennzeichen können in Nutzdaten vorkommen |
| Fehlende Datenelemente am Segmentende tolerieren | Explizit erlaubt ⚠️ [Q1] |
| Zeichensatz konfigurierbar (DIN 66003 DRV / DIN 66303) | § 301 ⚠️ [Q1] |
| Segmentreihenfolge und Kardinalitäten je Nachrichtentyp prüfen | Segmente kommen ein-/mehrfach oder nur in bestimmten Abrechnungsfällen vor ⚠️ [Q1] |
| Zähler-/Summenkonsistenz prüfen (UNZ vs. Anzahl Nachrichten, GES vs. Positionssummen) | Klassische EDIFACT-Kontrollprüfung |

## 5. Abweichende Formate

| Verfahren | Format | Marker |
|---|---|---|
| §§ 300/301/302 SGB V, § 105 SGB XI | EDIFACT-nahe Segmentsyntax | ⚠️ |
| Auftragssatz (Anlage 2 GGT) | positionsbasiertes Festsatzformat | ⚠️ [Q7] |
| Arbeitgeberverfahren | **eXTra-XML** | ⚠️ [Q17] |
| Reha § 301 (DRV-Bereich) | **XML** | ⚠️ |
| Kostenträgerdateien | eigenes Satzformat (Endungen `KE0`, `KE1`, …) | ⚠️ [Q15] |

§ 95 SGB IV nennt ausdrücklich die "Zeitpunkte der Umstellung einzelner technischer
Verfahren auf XML-basierte Verfahren" als Regelungsgegenstand der GGT ⚠️ [Q11] — die
EDIFACT-Formate sind also mittelfristig ein Auslaufmodell. Der Validator sollte
**Parser und Regelwerk trennen**, damit ein XML-Parser später gegen dieselben
fachlichen Regeln laufen kann.
