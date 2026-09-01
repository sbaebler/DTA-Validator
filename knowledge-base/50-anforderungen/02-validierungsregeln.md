# Validierungsregeln — Prüfstufenmodell

## 1. Die sieben Prüfstufen

Ein DTA-Validator sollte in klar getrennten Stufen arbeiten. Jede Stufe hat eine eigene
Fehlerklasse und eine eigene Abbruchsemantik.

```
 ┌─────────────────────────────────────────────────────────────────┐
 │ Stufe 0  Dateipärchen und Namenskonvention                      │  Transportfehler
 ├─────────────────────────────────────────────────────────────────┤
 │ Stufe 1  Auftragssatz (Anlage 2 GGT)                            │  Transportfehler
 ├─────────────────────────────────────────────────────────────────┤
 │ Stufe 2  Kryptografie (Anlage 16 / SECON)                       │  Sicherheitsfehler
 ├─────────────────────────────────────────────────────────────────┤
 │ Stufe 3  Syntax (UNA/UNB/…/UNZ, Zeichensatz, Segmentgrammatik)  │  Syntaxfehler
 ├─────────────────────────────────────────────────────────────────┤
 │ Stufe 4  Feldformate und Schlüsselwerte                         │  Formatfehler
 ├─────────────────────────────────────────────────────────────────┤
 │ Stufe 5  Referenzielle Integrität und Summen                    │  Konsistenzfehler
 ├─────────────────────────────────────────────────────────────────┤
 │ Stufe 6  Fachliche Plausibilität                                │  Plausibilitätsfehler
 └─────────────────────────────────────────────────────────────────┘
```

**Abbruchregel:** Schlägt eine Stufe mit einem `FEHLER` fehl, sind die Ergebnisse aller
höheren Stufen nicht mehr aussagekräftig und werden als `nicht geprüft` gekennzeichnet —
nicht als „bestanden".

## 2. Regelkatalog

Regel-ID-Schema: `<STUFE>-<VERFAHREN>-<NR>`, z. B. `S0-ALL-001`, `S4-302-017`.
`ALL` = verfahrensübergreifend.

### Stufe 0 — Dateipärchen und Namenskonvention

| ID | Regel | Schwere | Beleg |
|---|---|---|---|
| `S0-ALL-001` | Zu jeder Nutzdatendatei existiert genau eine Auftragsdatei (**nicht** bei TI/KIM) | FEHLER | ✅ [Q22e] |
| `S0-ALL-002` | Auftragsdatei trägt den Transferdateinamen der Nutzdatendatei plus `.AUF` | FEHLER | ✅ [Q22e] |
| `S0-ALL-003` | Transferdateiname bei beiden Dateien identisch | FEHLER | ✅ [Q22e] |
| `S0-ALL-004` | Stelle 1 ∈ {`T`, `E`} | FEHLER | ✅ [Q20] |
| `S0-ALL-005` | Stellen 2–4 bilden eine bekannte Verfahrenskennung des Bereichs | FEHLER | ✅ [Q20] |
| `S0-ALL-006` | Stelle 5 ist eine Ziffer (Verfahrensversion, beginnend mit `0`) | FEHLER | ✅ [Q20] |
| `S0-ALL-007` | Stellen 6–8 sind numerisch | FEHLER | ✅ [Q7] |
| `S0-ALL-008` | Wiederkehrende Transfernummer melden — **als HINWEIS, nicht als Fehler** | HINWEIS | ✅ [Q7] |
| `S0-ALL-009` | Bei Datenträgerversand: Dateien im Wurzelverzeichnis, ISO-9660-Level-1-konforme Namen | FEHLER | ⚠️ [Q21] |

> **Korrektur 01.09.2026:** `S0-ALL-008` lautete „Transfernummer wurde für diesen Absender
> noch nicht verwendet" (WARNUNG). Das war falsch. Anlage 2 GGT schreibt vor, dass die
> `TRANSFER_NUMMER` bei fehlerhafter Übertragung **erhalten bleibt und wiederverwendet
> wird**; die Eindeutigkeit muss der Empfänger durch Umbenennung herstellen. ✅ [Q7]

### Stufe 1 — Auftragssatz

| ID | Regel | Schwere | Beleg |
|---|---|---|---|
| `S1-ALL-001` | Auftragssatz ist genau **348 Byte** lang; `LÄNGE_AUFTRAG` = `00000348` | FEHLER | ✅ [Q7] |
| `S1-ALL-002` | `VERFAHREN_KENNUNG` (Stellen 20–24) ist gültig | FEHLER | ✅ [Q20] |
| `S1-ALL-003` | `VERFAHREN_KENNUNG` = Stellen **1–5** des Transferdateinamens | FEHLER | ✅ [Q7][Q22e] |
| `S1-ALL-004` | `ABSENDER_EIGNER` (33–47) trägt eine gültige Identifikation (IK 9, Absendernummer 8, KV 4, KZV 5), linksbündig | FEHLER | ✅ [Q7] |
| `S1-ALL-005` | `EMPFÄNGER_NUTZER` (63–77) und `EMPFÄNGER_PHYSIKALISCH` (78–92) tragen eine Identifikation desselben Typs | FEHLER | ✅ [Q7] |
| `S1-ALL-006` | `EMPFÄNGER_NUTZER` ist laut Kostenträgerdatei eine zuständige Datenannahmestelle | FEHLER | ⚠️ [Q15] |
| `S1-ALL-007` | `TRANSFER_NUMMER` (25–27) = Stellen 6–8 des Transferdateinamens | FEHLER | ✅ [Q7][Q22e] |
| `S1-ALL-008` | Auftragssatz enthält keine Sozialdaten (Trennungsgebot) | FEHLER | ⚠️ |
| `S1-ALL-009` | Muss-Felder gefüllt, Kann-Felder mit Default-Wert belegt (`N`→`0`, `A`/`AN`→Leerzeichen) | FEHLER | ✅ [Q7] |
| `S1-ALL-010` | `VERSCHLÜSSELUNGSART` = `ELEKTRONISCHE_UNTERSCHRIFT`; nur `00`+`00` und `03`+`03` zulässig | FEHLER | ✅ [Q7] |
| `S1-ALL-011` | `ZEICHENSATZ` aus der Werteliste; `EB` (EBCDIC) bei § 294 ff. SGB V unzulässig | FEHLER | ✅ [Q7] |
| `S1-ALL-012` | `DATEIGRÖßE_NUTZDATEN` = tatsächliche unverschlüsselte Größe; `DATEIGRÖßE_ÜBERTRAGUNG` = übertragene Größe | FEHLER | ✅ [Q7] |
| `S1-ALL-013` | Konstantenfelder: `IDENTIFIKATOR` = `500000`, `DATEIVERSION` = `000000`, `KORREKTUR` = `0` | FEHLER | ✅ [Q7] |
| `S1-ALL-014` | `KOMPRIMIERUNG` ∈ {`00`,`02`,`03`,`07`,`13`,`23`}; `01`,`04`,`05`,`06` sind nicht belegt | FEHLER | ✅ [Q7] |
| `S1-ALL-015` | Bei DFÜ: `SATZFORMAT` Leerzeichen, `SATZLÄNGE` `00000`, `BLOCKLÄNGE` `00000000` | FEHLER | ✅ [Q7] |
| `S1-XI-001` | `DATEINAME` (105–115) entspricht dem logischen Dateinamen `PL`+`MMJ`+Art+lfd. Nr.+`S`\|`A`+Kassenart | FEHLER | ✅ [Q22e] |
| `S1-XI-002` | `DATEI_BEZEICHNUNG` Stellen 319–320 tragen die Art der abgegebenen Leistung | FEHLER | ✅ [Q22d] |

> ✅ **Blocker aufgelöst (01.09.2026):** Anlage 2 GGT liegt vor. Der vollständige
> Feldkatalog steht in [`../data/auftragssatz.yaml`](../data/auftragssatz.yaml),
> die Werteliste der Verfahrenskennungen in
> [`../data/verfahrenskennungen.yaml`](../data/verfahrenskennungen.yaml).
> **Stufe 0 und Stufe 1 sind damit implementierungsreif.**

### Stufe 2 — Kryptografie

| ID | Regel | Schwere | Beleg |
|---|---|---|---|
| `S2-ALL-001` | Nutzdatendatei ist wohlgeformtes PKCS#7/CMS | FEHLER | ⚠️ [Q8] |
| `S2-ALL-002` | Äußerer ContentType = `EnvelopedData` | FEHLER | ⚠️ [Q8] |
| `S2-ALL-003` | Innerer ContentType = `SignedData` | FEHLER | ⚠️ [Q8] |
| `S2-ALL-004` | Inhaltsverschlüsselung = AES-256-CBC | FEHLER | ⚠️ [Q8] |
| `S2-ALL-005` | Digest-Algorithmus = SHA-256 | FEHLER | ⚠️ [Q8] |
| `S2-ALL-006` | RSA-Schlüssellänge ≥ 4096 Bit | FEHLER | ⚠️ [Q8] |
| `S2-ALL-007` | Signatur verifiziert erfolgreich | FEHLER | ⚠️ [Q27] |
| `S2-ALL-008` | Signaturzertifikat zeitlich gültig | FEHLER | ⚠️ [Q8] |
| `S2-ALL-009` | Zertifikatskette bis zu akzeptierter Trust-Center-Root auflösbar | FEHLER | ⚠️ [Q8] |
| `S2-ALL-010` | Zertifikat nicht gesperrt (CRL ausgewertet) | FEHLER | ⚠️ [Q8] |
| `S2-ALL-011` | `KeyUsage` passt zum Verwendungszweck | FEHLER | ⚠️ [Q8] |
| `S2-ALL-012` | Empfängerzertifikat gehört zum IK der adressierten Datenannahmestelle | FEHLER | ⚠️ |
| `S2-ALL-013` | Signaturverfahren = RSASSA-PSS, Key-Encryption = RSAES-OAEP | FEHLER/WARNUNG | ❓ Verbindlichkeit klären |
| `S2-ALL-014` | Zertifikat läuft in weniger als 60 Tagen ab | WARNUNG | — |

### Stufe 3 — Syntax

| ID | Regel | Schwere | Beleg |
|---|---|---|---|
| `S3-ALL-001` | `UNA` (falls vorhanden) enthält genau sechs Trennzeichen — **gilt nicht für § 105 SGB XI**, dort ist kein `UNA` vorgesehen | FEHLER | ✅ [Q22] |
| `S3-ALL-002` | Datei beginnt mit `UNB` und endet mit `UNZ` | FEHLER | ⚠️ [Q1] |
| `S3-ALL-003` | Nachrichtenzähler in `UNZ` = tatsächliche Anzahl Nachrichten | FEHLER | — |
| `S3-ALL-004` | Segmentzähler in `UNT` = tatsächliche Segmentanzahl je Nachricht | FEHLER | — |
| `S3-ALL-005` | Referenznummern `UNB`/`UNZ` und `UNH`/`UNT` stimmen paarweise überein | FEHLER | — |
| `S3-ALL-006` | Alle Zeichen liegen im Zeichensatz, den `ZEICHENSATZ` (203–204) deklariert | FEHLER | ✅ [Q7] |
| `S3-ALL-007` | Freigabezeichen korrekt verwendet | FEHLER | ⚠️ [Q1] |
| `S3-302-001` | Datei enthält ausschließlich Nachrichten vom Typ `SLGA` und `SLLA` | FEHLER | ⚠️ [Q1] |
| `S3-302-002` | Segmentreihenfolge innerhalb `SLGA`/`SLLA` entspricht der Grammatik | FEHLER | ❓ Grammatik fehlt |
| `S3-302-003` | Segmentkardinalitäten eingehalten | FEHLER | ❓ Grammatik fehlt |
| `S3-XI-001` | Datei enthält ausschließlich `PLGA` und `PLAA` | FEHLER | ✅ [Q22] |
| `S3-XI-002` | Kein `UNA`; Trennzeichen fest `:` `+` `,` `?` `'` — Dezimalzeichen ist das **Komma** | FEHLER | ✅ [Q22] |
| `S3-XI-003` | `PLGA` = `FKT` `REC` `SRD` `UST` `GES` `NAM`, je genau einmal; `UST` entfällt in der Sammelrechnungs-`PLGA` | FEHLER | ✅ [Q22] |
| `S3-XI-004` | `PLAA` folgt `FKT REC (INV NAD IMG? MAN (ESK (ELS ZUS* HIL?)+)+ IAF)+` | FEHLER | ✅ [Q22] |
| `S3-XI-005` | Auf eine `PLGA` folgt eine `PLAA` — außer bei Sammelrechnung, dort folgt nur einmal eine `PLGA` | FEHLER | ✅ [Q22] |
| `S3-XI-006` | `ESK` je Abrechnungsfall aufsteigend nach Kennzeichen der Leistungserbringung und Uhrzeit | FEHLER | ✅ [Q22] |
| `S3-XI-007` | Nachrichtentypversion im `UNH` ist die stichtagsgültige (aktuell `6`); `PLGA` und `PLAA` dürfen abweichen | FEHLER | ✅ [Q22] |

### Stufe 4 — Feldformate und Schlüsselwerte

| ID | Regel | Schwere | Beleg |
|---|---|---|---|
| `S4-ALL-001` | Alle IK sind 9-stellig, numerisch, Prüfziffer Modulo 10 über die Stellen 3–8, Gewichtung von rechts `1-2-1-2-1-2`, Quersumme der Produkte | FEHLER | ✅ [Q9b] |
| `S4-ALL-002` | KVNR entspricht `^[A-Z][0-9]{9}$` mit korrekter Prüfziffer | FEHLER | ❓ Algorithmus |
| `S4-ALL-003` | Datumsfelder sind formal gültige Kalenderdaten | FEHLER | — |
| `S4-ALL-004` | Betragsfelder entsprechen dem vorgegebenen Format (Nachkommastellen, Vorzeichen) | FEHLER | ❓ |
| `S4-ALL-005` | Pflichtfelder gefüllt, Feldlängen eingehalten | FEHLER | ❓ Feldkatalog |
| `S4-302-001` | Verarbeitungskennzeichen aus zulässiger Werteliste | FEHLER | ❓ Werteliste aus Anlage 3 |
| `S4-302-002` | Hilfsmittelpositionsnummer 10-stellig; existiert im Verzeichnis oder folgt `…900`-Ersatzregel | FEHLER | ⚠️ [Q24] |
| `S4-302-003` | Heilmittelpositionsnummer im Positionsnummernverzeichnis enthalten | FEHLER | ⚠️ [Q24] |
| `S4-302-004` | Verwendeter Schlüsselwert ist zum Leistungsdatum gültig | FEHLER | ⚠️ [Q1] |
| `S4-301-001` | Schlüssel entsprechen § 301 Anlage 2 in der stichtagsgültigen Version | FEHLER | ⚠️ [Q5] |
| `S4-300-001` | PZN gültig oder zulässiges Sonderkennzeichen | FEHLER | ⚠️ [Q35] |
| `S4-XI-001` | Schlüsselausprägungen entsprechen der TA 3 in stichtagsgültiger Version | FEHLER | ✅ [Q22g] |
| `S4-XI-002` | `IK der Pflegekasse` beginnt mit `18` | FEHLER | ✅ [Q22] |
| `S4-XI-003` | Rechnungsnummer: keine Sonderzeichen außer `-` und `/`, keine Doppelung, kein Anfang/Ende damit | FEHLER | ✅ [Q22] |
| `S4-XI-004` | Eindeutige Belegnummer nur aus Buchstaben, Ziffern, `/` und `-` | FEHLER | ✅ [Q22] |
| `S4-XI-005` | `MAN`: entweder Pflegestufe oder Pflegegrad, stichtagsabhängig; Pflegeklasse nur teil-/vollstationär bis 31.12.2016 | FEHLER | ✅ [Q22] |
| `S4-XI-006` | `ELS.Leistung` wird über die Vergütungsart aufgelöst (2.7.1 … 2.7.8) | FEHLER | ✅ [Q22g] |
| `S4-XI-007` | `ESK.Kennzeichen der Leistungserbringung` ∈ `01`–`31` oder `99` (nur fixe Monatspauschalen) | FEHLER | ✅ [Q22] |
| `S4-XI-008` | Beschäftigtennummer belegt bei ambulanten Diensten und § 77 SGB XI; sonst Ersatzwert `999999996/7/8` | FEHLER | ✅ [Q22][Q22g] |
| `S4-XI-009` | `ZUS.Wert` mit allen 5 Nachkommastellen | FEHLER | ✅ [Q22] |
| `S4-XI-010` | `INV.Versicherten-Nummer` ohne Füllzeichen; fehlt sie, ist die Anschrift im `NAD` zu übermitteln | FEHLER | ✅ [Q22] |

### Stufe 5 — Referenzielle Integrität und Summen

| ID | Regel | Schwere | Beleg |
|---|---|---|---|
| `S5-ALL-001` | `ABSENDER_EIGNER` im Auftragssatz = Absenderbezeichnung im `UNB` | FEHLER | ✅ [Q7][Q22] |
| `S5-ALL-002` | `DATEINAME` im Auftragssatz = Anwendungsreferenz im `UNB` (logischer Dateiname) | FEHLER | ✅ [Q22e] |
| `S5-302-001` | Zu jeder `SLGA` existiert mindestens eine zugehörige `SLLA` | FEHLER | ⚠️ [Q1] |
| `S5-302-002` | Rechnungsbezug zwischen `SLGA` und `SLLA` ist auflösbar | FEHLER | ⚠️ |
| `S5-302-003` | Gesamtbetrag im `GES`-Segment = Summe der Positionsbeträge | FEHLER | ⚠️ [Q1] |
| `S5-302-004` | Positionsbetrag = Menge × Einzelpreis (± zulässige Rundung) | FEHLER | ⚠️ |
| `S5-302-005` | Zuzahlungs- und Eigenanteilsbeträge konsistent zum Gesamtbetrag | FEHLER | ⚠️ |
| `S5-302-006` | USt.-Angaben (`UST`) konsistent zu den Nettobeträgen | FEHLER | ⚠️ |
| `S5-302-007` | Keine doppelte Rechnungsnummer innerhalb der Datei | FEHLER | — |
| `S5-302-008` | Keine identische Leistungsposition doppelt (gleicher Versicherter, Datum, Positionsnummer) | WARNUNG | — |
| `S5-XI-001` | `PLGA.FKT` = `PLAA.FKT` in Verarbeitungskennzeichen, IK LE, IK Kostenträger, IK Pflegekasse | FEHLER | ✅ [Q22] |
| `S5-XI-002` | `PLGA.REC` = `PLAA.REC` in Datum, Rechnungsart, Währung (Rechnungsnummer außer bei Sammelrechnung) | FEHLER | ✅ [Q22] |
| `S5-XI-003` | `PLGA.GES.Gesamtrechnungsbetrag` = Summe der `PLAA.IAF.Rechnungsbeträge` | FEHLER | ✅ [Q22] |
| `S5-XI-004` | `IAF.Rechnungsbetrag` = Gesamtbrutto ./. Zuzahlung/Eigenanteil ./. Beihilfe | FEHLER | ✅ [Q22] |
| `S5-XI-005` | Währungskennzeichen in allen `PLGA`/`PLAA` einer Datei identisch | FEHLER | ✅ [Q22] |
| `S5-XI-006` | Innerhalb einer `PLGA` nur `PLAA` derselben Leistungsart; je Datei nur eine Rechnungsart | FEHLER | ✅ [Q22] |
| `S5-XI-007` | Bei KIM: je Nutzdatendatei nur **eine** Pflegekasse und **eine** Leistungsart | FEHLER | ✅ [Q22] |

### Stufe 6 — Fachliche Plausibilität

| ID | Regel | Schwere | Beleg |
|---|---|---|---|
| `S6-ALL-001` | Leistungsdatum ≤ Rechnungsdatum | FEHLER | — |
| `S6-ALL-002` | Rechnungsdatum ≤ Erstellungsdatum der Datei | FEHLER | — |
| `S6-ALL-003` | Leistungsdatum liegt nicht unplausibel weit in der Vergangenheit (Verjährung/Ausschlussfristen) | WARNUNG | ❓ Fristen recherchieren |
| `S6-302-001` | Korrekturrechnung (VKZ ≠ Erstabrechnung) hat einen gültigen Bezug zur Ursprungsrechnung | FEHLER | ⚠️ [Q25b] |
| `S6-302-002` | Bei VKZ = Wiedereinreichung nach Absetzung ist der Absetzungsbezug vorhanden | FEHLER | ⚠️ [Q25b] |
| `S6-302-003` | Leistungszeitraum liegt innerhalb der Gültigkeit der zugrunde liegenden Verordnung | WARNUNG | ⚠️ |
| `S6-302-004` | Abgerechnete Positionsnummer passt zum Leistungsbereich des Leistungserbringers | WARNUNG | ⚠️ |
| `S6-302-005` | Kostenträger-IK passt zum in der KVNR eingebetteten Kassen-IK | WARNUNG | ❓ |

## 3. Schweregrade

| Grad | Bedeutung | Konsequenz |
|---|---|---|
| `FEHLER` | Verstoß gegen eine verbindliche Regelwerksvorgabe; Datei wird abgesetzt oder abgewiesen | Versand verhindern; CLI-Exit ≠ 0 |
| `WARNUNG` | Formal zulässig, aber mit hohem Absetzungsrisiko oder Hinweis auf Datenfehler | Versand möglich, Sichtprüfung empfohlen |
| `HINWEIS` | Informativ (z. B. veralteter Stammdatenstand, ablaufendes Zertifikat) | Keine Konsequenz |

## 4. Aufbau eines Befunds

```json
{
  "regel_id": "S4-302-002",
  "schwere": "FEHLER",
  "verfahren": "302",
  "regelwerk": { "dokument": "§ 302 Anlage 1", "version": "…", "fundstelle": "…" },
  "meldung": "Hilfsmittelpositionsnummer nicht im Verzeichnis und nicht ...900-konform",
  "fundstelle": {
    "datei": "ESLA0042",
    "nachricht": 3,
    "segment": "…",
    "segment_index": 17,
    "feld": "…"
  },
  "istwert": "<maskiert>",
  "erwartung": "10-stellige Positionsnummer aus dem Hilfsmittelverzeichnis",
  "status": "experimental"
}
```

`status: experimental` kennzeichnet Regeln, deren Quelle noch nicht gegen das
Primärdokument verifiziert ist (alle ❓-Regeln oben).

**Datenschutz:** `istwert` darf keine Sozialdaten im Klartext enthalten — bei
personenbezogenen Feldern maskieren oder nur die Fundstelle nennen (REQ-DSGVO-02).

## 5. Was dieser Katalog noch nicht leisten kann

**Stand 01.09.2026:** 103 Regeln, davon 50 mit `status: spezifiziert`.

| Bereich | Stand |
|---|---|
| **Stufe 0 und 1** (Dateipärchen, Auftragssatz) | ✅ implementierungsreif — Anlage 2 und Anlage 4 GGT liegen vor |
| **Stufe 3–6 für § 105 SGB XI** | ✅ implementierungsreif — TA 1 6.4.0 und TA 3 6.4.0 liegen vor |
| **Stufe 2** (Kryptografie) | ⚠️ Anlage 16 GGT fehlt noch |
| **Stufe 3–6 für §§ 300/301/302 SGB V** | ❓ sektorspezifische Technische Anlagen fehlen |
| Stammdatenabhängige Regeln (Kostenträgerdatei, Positionsnummern, Hilfsmittelverzeichnis) | ❓ Verzeichnisse fehlen |

Alle mit ❓ markierten Regeln sind Platzhalter mit korrekter Absicht, aber ohne
verifizierte Detailvorgabe.

→ Beschaffungsliste in [../60-projekt/02-roadmap-und-offene-punkte.md](../60-projekt/02-roadmap-und-offene-punkte.md)
