# KKS, Auftragsdatei und Dateinamenskonvention

Der gemeinsame Transportrahmen aller GKV-Verfahren — und die **erste Prüfstufe** eines
DTA-Validators.

> **Quellenstand:** Anlage 2 GGT liegt seit dem 01.09.2026 als Primärdokument vor und ist
> ausgewertet (Auftragssatz-Version 1.0, gültig ab 01.01.2025, Stand 10.10.2024, 15 Seiten).
> Der vollständige Feldkatalog steht maschinenlesbar in
> [`../data/auftragssatz.yaml`](../data/auftragssatz.yaml). ✅ [Q7]

## 1. Krankenkassenkommunikationssystem (KKS)

Das KKS ist ein **logischer Standard**, der beschreibt, in welcher Weise Auftrags- und
Nutzdaten ausgetauscht werden. Es ist das Standardverfahren für den Datenaustausch von
Arbeitgebern und Leistungserbringern mit der Sozialversicherung. ⚠️ [Q14][Q14w]

### Das Dateipärchen

| Datei | Inhalt | Verschlüsselung |
|---|---|---|
| **Nutzdatendatei** | Fachliche Abrechnungsdaten | **verschlüsselt** (Anlage 16 / SECON) |
| **Auftragsdatei** | Auftragssatz mit allen transportnotwendigen Informationen | **unverschlüsselt** |

Dass zu **jeder** Nutzdatendatei eine Auftragsdatei zu übermitteln ist, ist für § 105 SGB XI
ausdrücklich festgeschrieben ✅ [Q22e] und ergibt sich für die übrigen Verfahren aus der
Routing-Funktion des Auftragssatzes.

**Ausnahme TI/KIM:** Bei der vollelektronischen Abrechnung über KIM wird **keine
Auftragsdatei** gebildet — die Metadaten wandern in den XML-Header der Nutzdatendatei. ✅ [Q22]
Ein Validator darf das Dateipärchen also nicht bedingungslos erzwingen, sondern nur für den
Weg außerhalb der TI.

### Übertragungsreihenfolge ⚠️ [Q14w]

1. Die verschlüsselte **Nutzdatendatei** wird als separate Datei übertragen
2. **Danach** wird die zugehörige **Auftragsdatei** übertragen
3. Ein Übertragungsvorgang besteht aus genau diesen zwei Dateien in dieser Reihenfolge

Die Auftragsdatei fungiert damit als **Commit-Signal**: Erst wenn sie vorliegt, gilt die
Nutzdatendatei als vollständig übertragen und wird verarbeitet.

### Warum unverschlüsselt?

Die Auftragsdatei muss von der Datenannahmestelle **vor** der Entschlüsselung gelesen
werden können, um Routing und automatisierte Verarbeitung zu ermöglichen. ✅ [Q7]
Daraus folgt datenschutzrechtlich das **Trennungsgebot**: Die Auftragsdatei darf keine
Sozialdaten enthalten.

### Wiederverwendbare Transfernummern ✅ [Q7]

Anlage 2 hält ausdrücklich fest: Bei einer **fehlerhaften Übertragung bleibt die
`TRANSFER_NUMMER` erhalten** und wird bei der Wiederholung wiederverwendet. Daraus folgt die
Pflicht des Empfängers, das Dateipaar unmittelbar nach Empfang unter einem **neuen
systemeindeutigen Dateinamen** abzulegen.

**Konsequenz für den Validator:** Eine Prüfung „Transfernummer für diesen Absender noch nicht
verwendet" ist als **FEHLER** falsch — Wiederholungen sind regelkonform. Sie taugt allenfalls
als Hinweis in Kombination mit `DATUM_ERSTELLUNG`.

## 2. Der Auftragssatz (Anlage 2 GGT) ✅ [Q7]

- Logisch in **vier Objekte** gegliedert, physisch **ein zusammenhängender Satz**.
  Alle Objekte müssen vorhanden sein.
- **Positionsbasiertes Festsatzformat**, keine Trennzeichen.
- **Gesamtlänge: 348 Byte** (Konstante `00000348` im Feld `LÄNGE_AUFTRAG` bei `VERSION = '01'`).
- Zeichensatz: **ISO 8859-1** (Kennung `I1`).

### Spaltenlegende

| Nutzungstyp | | Feldtyp | | Feldart | |
|---|---|---|---|---|---|
| `R` | Routing | `N` | numerisch, rechtsbündig, führende Nullen | `M` | Muss |
| `L` | Logging/Status | `A` | Buchstaben A–Z, linksbündig, Leerzeichen | `m` | bedingtes Muss (fachbezogen geprüft) |
| `K` | KKS-Verfahren | `AN` | Zeichenvorrat `I1`, linksbündig, Leerzeichen | `K` | Kann — **muss** aber mit Default-Wert belegt werden |
| `D` | Datenträger | | | | |
| `I` | interne Nutzung | | | | |
| `A` | allgemein | | | | |
| `S` | Verschlüsselung | | | | |

> `K` bedeutet **nicht** „darf leer bleiben": numerische Felder sind mit `0`, alphanumerische
> mit Leerzeichen zu füllen. Ein Auftragssatz mit Nullbytes oder abgeschnittener Länge ist
> unabhängig von der Feldart fehlerhaft.

### Teil 1 — Allgemeine Beschreibung der Krankenkassen-Kommunikation (1–210)

| Feld | Stellen | Länge | Typ | Art | Inhalt |
|---|---|---|---|---|---|
| `IDENTIFIKATOR` | 1–6 | 6 | A/N | M | Konstante `500000` |
| `VERSION` | 7–8 | 2 | A/N | M | `01` = erste Version |
| `LÄNGE_AUFTRAG` | 9–16 | 8 | A/N | M | Konstante `00000348` bei `VERSION = 01` |
| `SEQUENZ_NR` | 17–19 | 3 | A/N | m | `000` nicht segmentiert, `001`–`098` Teillieferung, `9xx` letzter Teil |
| `VERFAHREN_KENNUNG` | **20–24** | 5 | R/AN | M | Dateityp, Werteliste in Anlage 4 GGT |
| `TRANSFER_NUMMER` | 25–27 | 3 | A/N | M | lfd. Transfernummer, Überlauf `999` → `0` |
| `VERFAHREN_KENNUNG_SPEZIFIKATION` | 28–32 | 5 | R/AN | m | Untergliederung je Verfahren |
| `ABSENDER_EIGNER` | 33–47 | 15 | R/AN | M | verschlüsselt und signiert; bei RZ-Abrechnung das RZ |
| `ABSENDER_PHYSIKALISCH` | 48–62 | 15 | R/AN | M | ggf. Datenübermittlungsstelle |
| `EMPFÄNGER_NUTZER` | 63–77 | 15 | R/AN | M | **Datenannahmestelle mit Entschlüsselungsbefugnis** laut Kostenträgerdatei |
| `EMPFÄNGER_PHYSIKALISCH` | 78–92 | 15 | R/AN | M | nächster Empfänger |
| `FEHLER_NUMMER` | 93–98 | 6 | R/N | M | `000000` = kein Fehler |
| `FEHLER_MAßNAHME` | 99–104 | 6 | R/N | M | `000000` = keine Maßnahme |
| `DATEINAME` | 105–115 | 11 | A/AN | M | **logischer** Dateiname (≠ Transferdateiname) |
| `DATUM_ERSTELLUNG` | 116–129 | 14 | L/N | M | `JHJJMMTThhmmss` |
| `DATUM_ÜBERTRAGUNG_GESENDET` | 130–143 | 14 | L/N | m | vom Absender |
| `DATUM_ÜBERTRAGUNG_EMPFANGEN_START` | 144–157 | 14 | L/N | K | nur vom ersten Empfänger; sonst Nullen |
| `DATUM_ÜBERTRAGUNG_EMPFANGEN_ENDE` | 158–171 | 14 | L/N | K | vom Empfänger |
| `DATEIVERSION` | 172–177 | 6 | A/N | M | Konstante `000000` (unbenutzt) |
| `KORREKTUR` | 178 | 1 | A/N | M | Konstante `0` (unbenutzt) |
| `DATEIGRÖßE_NUTZDATEN` | 179–190 | 12 | A/N | M | Bytes, **unverschlüsselt und unkomprimiert** |
| `DATEIGRÖßE_ÜBERTRAGUNG` | 191–202 | 12 | A/N | M | Bytes **nach** Verschlüsselung/Signatur/Komprimierung |
| `ZEICHENSATZ` | 203–204 | 2 | A/AN | M | `I1` `I5` `I7` `I8` `EB` `P8` `U8` `BI` |
| `KOMPRIMIERUNG` | 205–206 | 2 | A/N | M | `00` `02` `03` `07` `13` `23` |
| `VERSCHLÜSSELUNGSART` | 207–208 | 2 | A/N | M | `00` keine, `03` PKCS#7 |
| `ELEKTRONISCHE_UNTERSCHRIFT` | 209–210 | 2 | A/N | M | `00` keine, `03` PKCS#7 |

### Teil 2 — Bandverarbeitung (211–226)

| Feld | Stellen | Länge | Typ | Art | Bei DFÜ |
|---|---|---|---|---|---|
| `SATZFORMAT` | 211–213 | 3 | D/A | m | `'   '` (Leerzeichen) |
| `SATZLÄNGE` | 214–218 | 5 | D/N | m | `00000` |
| `BLOCKLÄNGE` | 219–226 | 8 | D/N | m | `00000000` |

Bei Bandverarbeitung sind **alle drei** Felder auszufüllen.

### Teil 3 — KKS-Verfahren (227–274)

Diese Felder muss der Absender **nicht** ausfüllen; sie werden im Transportsystem belegt.

| Feld | Stellen | Länge | Typ | Art | Inhalt |
|---|---|---|---|---|---|
| `Status` | 227 | 1 | K/AN | m | Leerzeichen bei Anlieferung; sonst `0`–`8` |
| `Wiederholung` | 228–229 | 2 | K/N | m | max. Übertragungswiederholungen |
| `Übertragungsweg` | 230 | 1 | K/N | m | `1` X.25 … `5` anderer Weg |
| `Verzögerter Versand` | 231–240 | 10 | K/N | m | `JJMMTTSSmm` |
| `Info und Fehlerfelder` | 241–246 | 6 | K/N | m | FTAM-Fehlernummer, `000000` = ok |
| `Variables Info-Feld` | 247–274 | 28 | K/AN | m | Klartextfehlermeldung; im Verfahren `PF` bzw. beim GKV-KomServer die 23-stellige Tracking-ID |

### Teil 4 — Verarbeitung innerhalb eines RZ (275–348)

| Feld | Stellen | Länge | Typ | Art | Inhalt |
|---|---|---|---|---|---|
| `E-MAIL-ADRESSE ABSENDER` | 275–318 | 44 | I/AN | m | optional; darf bis Stelle **344** in `DATEI_BEZEICHNUNG` hineinreichen (70 Zeichen, analog DSKO der DEÜV) |
| `DATEI_BEZEICHNUNG` | 319–348 | 30 | I/AN | m | variabler Bereich; Stellen **347–348** = Anzahl Gesamtpakete bei Dateisplitting |

> ⚠️ **Falle für Parser:** Zwei Felder überlappen fachlich. Die E-Mail-Adresse ist ein
> **feldübergreifendes** Datum von Stelle 275 bis maximal 344, während `DATEI_BEZEICHNUNG`
> formal bei 319 beginnt. Ein Parser, der beide Felder unabhängig ausliest, zerschneidet
> lange E-Mail-Adressen. Für § 105 SGB XI belegt Anhang 1 der TA 1 zusätzlich die Stellen
> **319–320** mit der Art der abgegebenen Leistung ✅ [Q22d] — dieselben Bytes tragen also je
> nach Verfahren unterschiedliche Bedeutung.

### Zulässige Krypto-Kombinationen ✅ [Q7]

| | `VERSCHLÜSSELUNGSART = 00` | `VERSCHLÜSSELUNGSART = 03` |
|---|---|---|
| **`ELEKTRONISCHE_UNTERSCHRIFT = 00`** | ✅ keine Verschlüsselung, keine Unterschrift | ❌ **unzulässig** |
| **`ELEKTRONISCHE_UNTERSCHRIFT = 03`** | ❌ **unzulässig** | ✅ Unterschrift und Verschlüsselung gemäß PKCS#7 |

Das ist eine harte, sofort implementierbare Prüfregel: beide Felder müssen **denselben** Wert
tragen, und nur `00` und `03` sind definiert.

## 3. Dateinamen

Anlage 2 GGT regelt Dateinamen **nicht** verfahrensübergreifend ✅ [Q7]:

| Bereich | Regelung |
|---|---|
| Arbeitgeberverfahren, DRV | `VERFAHREN_KENNUNG` + 6-stellige lfd. Dateinummer aus dem Vorlaufsatz |
| **§ 294 ff. SGB V** | in den technischen Anlagen zu den vertraglichen Regelungen festgelegt |
| Amtliche Statistiken | `kkknnMMJHJJ` (Kassenart, Satzart, Monat, Jahr) |

Der Eintrag im Feld `DATEINAME` **muss nicht identisch** mit dem Transferdateinamen sein.
Im KKS-Verfahren wird der **Transfer**dateiname aus `VERFAHREN_KENNUNG` und
`TRANSFER_NUMMER` gebildet. ✅ [Q7]

### Beispiel § 105 SGB XI ✅ [Q22e]

Anhang 3 zur TA 1 (Pflege) macht beides konkret:

```
physikalischer Dateiname (Transferdateiname), 8 Stellen

  E  P F L  0   0 0 7
  │  └─┬─┘  │   └─┬─┘
  │    │    │     └───── Stellen 6–8: laufende Nummer / Transfernummer
  │    │    └─────────── Stelle 5:    Verfahrensversion, beginnend mit "0"
  │    └──────────────── Stellen 2–4: Verfahren, hier "PFL" (Pflege-Leistungserbringer)
  └───────────────────── Stelle 1:    "T" = Test/Erprobung, "E" = Echtdaten

  Dateipärchen:  EPFL0007.AUF | EPFL0007 | EPFL0008.AUF | EPFL0008
```

```
logischer Dateiname (Feld DATEINAME, Stellen 105–115; UNB-Anwendungsreferenz), 11 Stellen

  P L  0 7 6  0  0 1  S  E K
  └┬┘  └─┬─┘  │  └┬┘  │  └┬┘
   │     │    │   │   │   └── Stellen 10–11: Kassenarten-Kennung (AO BK BN EK IK LK SE)
   │     │    │   │   └────── Stelle 9:      "S" Selbstabrechner, "A" Abrechnungszentrum
   │     │    │   └────────── Stellen 7–8:   lfd. Nummer je Kalenderjahr und Datenannahme
   │     │    └────────────── Stelle 6:      "0" Regeldaten, "1"–"9" Korrekturlieferung
   │     └─────────────────── Stellen 3–5:   Abrechnungszeitraum "MMJ" (Monat + letzte Jahresziffer)
   └───────────────────────── Stellen 1–2:   Absenderklassifikation, "PL" für Pflege
```

Die beiden Namen folgen **unterschiedlichen Systematiken** und dürfen nicht verwechselt
werden. Nur der physikalische Name trägt das Test-/Echt-Kennzeichen.

### Kopplungsregel

> Nutzdatendatei und Auftragsdatei tragen denselben Transferdateinamen; die Auftragsdatei
> zusätzlich die Endung **`.AUF`**. ✅ [Q22e]

**Prüfregel-Kandidaten:**
- `basename(auftrag) == basename(nutzdaten) + '.AUF'`
- Stelle 1 ∈ {`T`, `E`}
- Stellen 2–4 + Stelle 5 ergeben eine gültige `VERFAHREN_KENNUNG` aus Anlage 4 GGT
- Die ersten 5 Stellen des Transferdateinamens **sind** die `VERFAHREN_KENNUNG` im
  Auftragssatz (Stellen 20–24)
- Stellen 6–8 numerisch und identisch mit `TRANSFER_NUMMER` (Stellen 25–27)
- Der logische Dateiname im Feld `DATEINAME` ist mit der `UNB`-Anwendungsreferenz der
  Nutzdaten identisch

## 4. Verfahrenskennungen (Anlage 4 GGT) ✅ [Q20]

**Anlage 4 GGT**, gültig ab **01.01.2026**, Stand 06.11.2025, 47 Seiten, Feldbeschreibung
Version 1.1. Vollständig übernommen nach
[`../data/verfahrenskennungen.yaml`](../data/verfahrenskennungen.yaml) — **322 Einträge** im
Gesamtverzeichnis.

Für den Datenaustausch mit Leistungserbringern gilt der fünfstellige Aufbau
`E|T` + 3-stelliges Verfahren + Versionsziffer:

| Bereich | Kennungen |
|---|---|
| **§ 294 ff. SGB V** | `KAV` KV · `KZV` KZV · `APO` Apotheken · `IMG` Imagedaten (§ 7 der Vereinbarung nach § 300) · `KRH` Krankenhäuser · `REH` Reha · **`SOL` Sonstige Leistungserbringer** · `EBZ` Beantragung/Genehmigung Zahnärzte · `GKH` Grundsatz-DA Krankenhaus |
| **§ 295 Abs. 1b SGB V** | `DIR` (Alt-Verfahren) · `DRB` HzV · `DRC` besondere ambulante Versorgung · `DRI` Integrierte Versorgung · `DRM` § 64d · `DRS` §§ 132e/f — Konvention: alle Selektivverträge `DR` + Buchstabe A–Z |
| **§ 105 SGB XI** | **`PFL`** Datenaustausch nach § 105 SGB XI · **`PFU`** elektronischer Urbeleg nach § 105 Abs. 2 |
| Versichertenkarten | `KVK` |

> ⚠️ **Kein einheitliches Längenschema.** Das fünfstellige Muster gilt für den
> LE-Datenaustausch. Im Verkehr mit der Rentenversicherung sind die Kennungen
> **zweistellig** (`BK`, `TR`, `VM`, …); das Gesamtverzeichnis enthält Einträge von 2 bis 6
> Zeichen (`AN`, `PFL`, `BUPDF`) sowie die Platzhalter `1xx`–`9xx` für interne Verfahren.
> Ein Validator darf die Kennung deshalb **nicht** über eine Längenregel prüfen, sondern nur
> gegen die Werteliste — und zwar bereichsbezogen.

> ⚠️ **Kennungen sind nicht eindeutig.** Dieselbe Kennung steht im Verzeichnis mehrfach für
> verschiedene Verfahren (`BAK`, `BK`, `IKB`, `BMZ`). Die Auflösung gelingt erst zusammen mit
> Absender und Empfänger, nicht aus der Kennung allein.

### Feld `VERFAHREN_KENNUNG_SPEZIFIKATION` (28–32) ✅ [Q20]

Die Werte werden **je Verfahren** festgelegt (typischerweise der Nachrichtentyp, sofern pro
Lieferung eindeutig); das Feld kann auch die Verarbeitungspriorität ausdrücken. Anlage 4
nennt nur Beispiele für Amtliche Statistiken, BAS und GKV-SV und hält ausdrücklich fest:
*„Die Listen werden nicht mit neuen Verfahrensspezifikationen fortgeschrieben."*

**Konsequenz:** Eine verfahrensübergreifende Werteprüfung dieses Feldes ist **nicht möglich**
und wäre falsch. Prüfbar ist nur die Belegung je Fachverfahren.

## 5. Ablaufdiagramm

```
 Erzeugung                        Übertragung                  Annahme
 ─────────                        ───────────                  ───────
 Nutzdaten (Klartext)
        │
        │ SECON: signieren (SignedData)
        │        verschlüsseln (EnvelopedData)
        ▼
 EPFL0007         ──── 1. ────►                          ┌─ Datei zwischenspeichern
                                                          │  unter NEUEM systemeindeutigem
 Auftragssatz erzeugen                                    │  Namen (Transfernummern
 (Klartext, 348 Byte, ISO 8859-1)                         │  wiederholen sich!)
        ▼                                                 ▼
 EPFL0007.AUF     ──── 2. ────►                    Auftragssatz lesen
                                                    → VERFAHREN_KENNUNG (20–24)
                                                    → EMPFÄNGER_NUTZER (63–77)
                                                    → Routing
                                                          │
                                                          ▼
                                                    Entschlüsseln + Signatur prüfen
                                                          │
                                                          ▼
                                                    Fachliche Prüfung (Sektor-TA)
```
