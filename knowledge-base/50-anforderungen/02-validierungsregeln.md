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
| `S0-ALL-001` | Zu jeder Nutzdatendatei existiert genau eine Auftragsdatei | FEHLER | ⚠️ [Q14w] |
| `S0-ALL-002` | Auftragsdatei endet auf `.AUF` | FEHLER | ⚠️ [Q7] |
| `S0-ALL-003` | Erste 8 Stellen des Dateinamens sind bei beiden Dateien identisch | FEHLER | ⚠️ [Q7] |
| `S0-ALL-004` | Stelle 1 ∈ {`T`, `E`} | FEHLER | ⚠️ [Q7] |
| `S0-ALL-005` | Stellen 2–4 bilden eine bekannte Verfahrenskennung | FEHLER | ❓ Werteliste aus Anlage 4 GGT |
| `S0-ALL-006` | Stelle 5 ist eine gültige Verfahrensversion | FEHLER | ❓ |
| `S0-ALL-007` | Stellen 6–8 sind numerisch | FEHLER | ⚠️ [Q7] |
| `S0-ALL-008` | Transfernummer wurde für diesen Absender noch nicht verwendet | WARNUNG | ❓ |
| `S0-ALL-009` | Bei Datenträgerversand: Dateien im Wurzelverzeichnis, ISO-9660-Level-1-konforme Namen | FEHLER | ⚠️ [Q21] |

### Stufe 1 — Auftragssatz

| ID | Regel | Schwere | Beleg |
|---|---|---|---|
| `S1-ALL-001` | Auftragssatz hat die vorgeschriebene Gesamtlänge | FEHLER | ❓ Länge unbekannt |
| `S1-ALL-002` | `VERFAHREN_KENNUNG` (Position 20–24) ist gültig | FEHLER | ⚠️ [Q20] |
| `S1-ALL-003` | `VERFAHREN_KENNUNG` stimmt mit den Stellen 2–5 des Dateinamens überein | FEHLER | ❓ Mapping verifizieren |
| `S1-ALL-004` | `ABSENDER_EIGNER` ist ein gültiges IK | FEHLER | ⚠️ [Q7] |
| `S1-ALL-005` | `EMPFAENGER` ist ein gültiges IK | FEHLER | ⚠️ [Q7] |
| `S1-ALL-006` | `EMPFAENGER` ist laut Kostenträgerdatei eine zuständige Datenannahmestelle | FEHLER | ⚠️ [Q15] |
| `S1-ALL-007` | `TRANSFER_NUMMER` stimmt mit den Stellen 6–8 des Dateinamens überein | FEHLER | ❓ |
| `S1-ALL-008` | Auftragssatz enthält keine Sozialdaten (Trennungsgebot) | FEHLER | ⚠️ |
| `S1-ALL-009` | Alle Pflichtfelder des Auftragssatzes sind gefüllt | FEHLER | ❓ Feldkatalog fehlt |

> ❓ **Blocker:** Stufe 1 ist ohne die vollständige Feldliste aus **Anlage 2 GGT** nicht
> implementierbar. Beschaffung hat höchste Priorität.

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
| `S3-ALL-001` | `UNA` (falls vorhanden) enthält genau sechs Trennzeichen | FEHLER | ⚠️ [Q1] |
| `S3-ALL-002` | Datei beginnt mit `UNB` und endet mit `UNZ` | FEHLER | ⚠️ [Q1] |
| `S3-ALL-003` | Nachrichtenzähler in `UNZ` = tatsächliche Anzahl Nachrichten | FEHLER | — |
| `S3-ALL-004` | Segmentzähler in `UNT` = tatsächliche Segmentanzahl je Nachricht | FEHLER | — |
| `S3-ALL-005` | Referenznummern `UNB`/`UNZ` und `UNH`/`UNT` stimmen paarweise überein | FEHLER | — |
| `S3-ALL-006` | Alle Zeichen liegen im zulässigen Zeichensatz | FEHLER | ⚠️ [Q1] |
| `S3-ALL-007` | Freigabezeichen korrekt verwendet | FEHLER | ⚠️ [Q1] |
| `S3-302-001` | Datei enthält ausschließlich Nachrichten vom Typ `SLGA` und `SLLA` | FEHLER | ⚠️ [Q1] |
| `S3-302-002` | Segmentreihenfolge innerhalb `SLGA`/`SLLA` entspricht der Grammatik | FEHLER | ❓ Grammatik fehlt |
| `S3-302-003` | Segmentkardinalitäten eingehalten | FEHLER | ❓ Grammatik fehlt |
| `S3-XI-001` | Datei enthält ausschließlich `PLGA` und `PLAA` | FEHLER | ⚠️ [Q22] |

### Stufe 4 — Feldformate und Schlüsselwerte

| ID | Regel | Schwere | Beleg |
|---|---|---|---|
| `S4-ALL-001` | Alle IK sind 9-stellig, numerisch, mit korrekter Prüfziffer | FEHLER | ⚠️ [Q9] |
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

### Stufe 5 — Referenzielle Integrität und Summen

| ID | Regel | Schwere | Beleg |
|---|---|---|---|
| `S5-ALL-001` | Absender-IK im Auftragssatz = Absender-IK in den Nutzdaten | FEHLER | ❓ Feldzuordnung |
| `S5-302-001` | Zu jeder `SLGA` existiert mindestens eine zugehörige `SLLA` | FEHLER | ⚠️ [Q1] |
| `S5-302-002` | Rechnungsbezug zwischen `SLGA` und `SLLA` ist auflösbar | FEHLER | ⚠️ |
| `S5-302-003` | Gesamtbetrag im `GES`-Segment = Summe der Positionsbeträge | FEHLER | ⚠️ [Q1] |
| `S5-302-004` | Positionsbetrag = Menge × Einzelpreis (± zulässige Rundung) | FEHLER | ⚠️ |
| `S5-302-005` | Zuzahlungs- und Eigenanteilsbeträge konsistent zum Gesamtbetrag | FEHLER | ⚠️ |
| `S5-302-006` | USt.-Angaben (`UST`) konsistent zu den Nettobeträgen | FEHLER | ⚠️ |
| `S5-302-007` | Keine doppelte Rechnungsnummer innerhalb der Datei | FEHLER | — |
| `S5-302-008` | Keine identische Leistungsposition doppelt (gleicher Versicherter, Datum, Positionsnummer) | WARNUNG | — |

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

Die Stufen 0–2 sind weitgehend spezifizierbar, sobald Anlage 2 und Anlage 4 GGT vorliegen.
**Die Stufen 3–6 sind ohne die vollständigen Segment- und Feldkataloge der jeweiligen
sektorspezifischen Technischen Anlage nicht implementierbar.** Alle mit ❓ markierten
Regeln sind Platzhalter mit korrekter Absicht, aber ohne verifizierte Detailvorgabe.

→ Beschaffungsliste in [../60-projekt/02-roadmap-und-offene-punkte.md](../60-projekt/02-roadmap-und-offene-punkte.md)
