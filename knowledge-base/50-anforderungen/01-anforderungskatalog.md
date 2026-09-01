# Anforderungskatalog

Nummerierte Anforderungen als Grundlage für Backlog und Abnahme.

**Konventionen**
- ID-Schema: `REQ-<Bereich>-<Nr>`
- Priorität: `MUSS` / `SOLL` / `KANN`
- Spalte *Beleg*: Vertrauens-Marker aus der Wissensbibliothek (✅ / ⚠️ / ❓)
- Eine Anforderung mit ❓ ist **nicht umsetzungsreif** — die Quelle muss zuerst
  verifiziert werden.

---

## A. Rechtlich-fachlicher Rahmen (`REQ-FACH`)

| ID | Anforderung | Prio | Beleg |
|---|---|---|---|
| REQ-FACH-01 | Das System validiert Abrechnungsdaten **vor** dem Versand, um Rechnungskürzungen nach § 303 SGB V und Absetzungen zu vermeiden. | MUSS | ✅ |
| REQ-FACH-02 | Das System unterstützt **mehrere Regelwerksversionen parallel** und wählt die anzuwendende Version anhand des fachlich maßgeblichen Datums (Leistungsdatum / Abrechnungsmonat / Datenlieferungsquartal), nicht anhand des Systemdatums. | MUSS | ✅ |
| REQ-FACH-03 | Das System bildet Übergangsfristen ab, in denen zwei Regelwerksversionen gleichzeitig zulässig sind (z. B. § 302 Anlage 3 V21/V22 bis 30.04.2027). | MUSS | ⚠️ |
| REQ-FACH-04 | Das System unterscheidet **Test-** und **Echtbetrieb** und kennzeichnet Ergebnisse entsprechend. | MUSS | ⚠️ |
| REQ-FACH-05 | Das System unterstützt das **Korrekturverfahren** (Verarbeitungskennzeichen, Bezug zur Ursprungsrechnung) und prüft dessen Konsistenz. | MUSS | ⚠️ |
| REQ-FACH-06 | Jedes Prüfergebnis nennt die **angewandte Regelwerksversion** und die **Fundstelle** der Regel. | MUSS | — |
| REQ-FACH-07 | Das System prüft die Vollständigkeit der Urbeleg-Begleitinformationen (Begleitzettel nach § 302 Anlage 4). | SOLL | ⚠️ |

## B. Verfahrensabdeckung (`REQ-VERF`)

| ID | Anforderung | Prio | Beleg |
|---|---|---|---|
| REQ-VERF-01 | Verfahren nach **§ 302 SGB V** (SLGA/SLLA) wird vollständig unterstützt. | MUSS | ⚠️ |
| REQ-VERF-02 | Verfahren nach **§ 105 SGB XI** (PLGA/PLAA) wird unterstützt. | SOLL | ⚠️ |
| REQ-VERF-03 | Verfahren nach **§ 301 SGB V** (AUFN/ENTL/RECH/…) wird unterstützt. | KANN | ⚠️ |
| REQ-VERF-04 | Verfahren nach **§ 300 SGB V** wird unterstützt. | KANN | ⚠️ |
| REQ-VERF-05 | Die Architektur erlaubt das Hinzufügen weiterer Verfahren (§ 295 Abs. 1b, Hybrid-DRG, Reha) **ohne Änderung am Kern**. | MUSS | — |
| REQ-VERF-06 | Verfahrensspezifische Regelwerke sind als **Daten** (Deklaration), nicht als Code hinterlegt. | SOLL | — |

## C. Transport- und Envelope-Prüfung (`REQ-TRANS`)

| ID | Anforderung | Prio | Beleg |
|---|---|---|---|
| REQ-TRANS-01 | Das System prüft die **Dateinamenskonvention** der Nutzdatendatei (8 Stellen: T/E, Verfahren, Version, Transfernummer) und unterscheidet dabei den **physikalischen** vom **logischen** Dateinamen. | MUSS | ✅ [Q20][Q22e] |
| REQ-TRANS-02 | Das System prüft, dass Nutzdaten- und Auftragsdatei denselben **Transferdateinamen** tragen und die Auftragsdatei auf `.AUF` endet. Bei Übermittlung über KIM entfällt die Auftragsdatei. | MUSS | ✅ [Q22e] |
| REQ-TRANS-03 | Das System parst und validiert den **Auftragssatz** (Anlage 2 GGT) als positionsbasiertes Festsatzformat fester Länge **348 Byte** über alle 37 Felder. | MUSS | ✅ [Q7] |
| REQ-TRANS-04 | Das System prüft die **Verfahrenskennung** (Auftragssatz Stellen 20–24) gegen die Werteliste aus Anlage 4 GGT — **bereichsbezogen**, nicht über eine Längenregel. | MUSS | ✅ [Q20] |
| REQ-TRANS-05 | Das System prüft die **Konsistenz zwischen Dateiname, Auftragssatz und Nutzdaten** (Verfahrenskennung, Transfernummer, logischer Dateiname ↔ `UNB`-Anwendungsreferenz, Absender-IK, Test-/Echt-Kennzeichen als Zuordnung `T` ↔ {`0`,`1`} und `E` ↔ {`2`}). | MUSS | ✅ [Q7][Q22e] |
| REQ-TRANS-06 | Das System prüft transportwegspezifische Regeln, mindestens: genau **eine Nutzdaten- und eine Auftragsdatei pro E-Mail bzw. KIM-Nachricht**. | SOLL | ⚠️ |
| REQ-TRANS-07 | Das System stellt sicher, dass die Auftragsdatei **keine Sozialdaten** enthält (Trennungsgebot). | MUSS | ⚠️ |
| REQ-TRANS-08 | Das System unterstützt die Prüfung von Dateien für die Übertragung per **KIM** (Dateiname im Betreff, eine Nutzdatendatei pro Nachricht). | SOLL | ⚠️ |

## D. Syntaxprüfung (`REQ-SYN`)

| ID | Anforderung | Prio | Beleg |
|---|---|---|---|
| REQ-SYN-01 | Das System liest die **Trennzeichen aus dem UNA-Segment** und hartkodiert sie nicht. | MUSS | ⚠️ |
| REQ-SYN-02 | Das System prüft den **Dateirahmen UNB … UNZ** inkl. Zählerkonsistenz. | MUSS | ⚠️ |
| REQ-SYN-03 | Das System unterstützt die im Auftragssatz-Feld `ZEICHENSATZ` deklarierbaren Kodierungen (mindestens `I1` ISO 8859-1, `I7` DIN 66003 DRV, `I8` DIN 66303) und meldet unzulässige Zeichen; `EB` (EBCDIC) ist bei § 294 ff. SGB V zurückzuweisen. | MUSS | ✅ [Q7] |
| REQ-SYN-04 | Das System behandelt das EDIFACT-**Freigabezeichen** korrekt. | MUSS | — |
| REQ-SYN-05 | Das System toleriert **weggelassene, leere Datenelemente am Segmentende**. | MUSS | ⚠️ |
| REQ-SYN-06 | Das System prüft **Segmentreihenfolge und Kardinalitäten** je Nachrichtentyp. | MUSS | ⚠️ |
| REQ-SYN-07 | Das System prüft **Feldtypen, -längen und Pflichtfelder** je Segment. | MUSS | ✅ [Q22] für § 105 SGB XI, ❓ für §§ 300/301/302 |

## E. Stammdaten- und Schlüsselprüfung (`REQ-STAMM`)

| ID | Anforderung | Prio | Beleg |
|---|---|---|---|
| REQ-STAMM-01 | Das System validiert **Institutionskennzeichen** (9-stellig, Modulo-10-Prüfziffer über Stellen 3–8). | MUSS | ⚠️ ❓ Algorithmus verifizieren |
| REQ-STAMM-02 | Das System validiert die **Krankenversichertennummer** (Format und Prüfziffer). | MUSS | ❓ Buchstabenbehandlung unklar |
| REQ-STAMM-03 | Das System prüft IK gegen die importierte **Kostenträgerdatei** (Datenannahmestelle, Belegannahmestelle, Kostenträger). | MUSS | ⚠️ ❓ Satzstruktur fehlt |
| REQ-STAMM-04 | Das System prüft **Hilfsmittelpositionsnummern** gegen das Hilfsmittelverzeichnis inkl. `…900`-Ersatzregel. | SOLL | ⚠️ |
| REQ-STAMM-05 | Das System prüft **Heilmittelpositionsnummern** gegen das Positionsnummernverzeichnis. | SOLL | ⚠️ |
| REQ-STAMM-06 | Alle Schlüsseltabellen sind **gültigkeitszeitraumbezogen** modelliert (`gueltig_ab` / `gueltig_bis`). | MUSS | ⚠️ |
| REQ-STAMM-07 | Stammdatenimporte sind **versioniert und nachvollziehbar**; das Prüfprotokoll nennt den verwendeten Ausgabestand. | MUSS | — |
| REQ-STAMM-08 | Ein veralteter Stammdatenstand erzeugt eine **Warnung**. | SOLL | — |

## F. Plausibilitäts- und Summenprüfung (`REQ-PLAUS`)

| ID | Anforderung | Prio | Beleg |
|---|---|---|---|
| REQ-PLAUS-01 | Das System prüft die **Summenkonsistenz** zwischen Gesamtaufstellung (SLGA/PLGA) und Einzelpositionen (SLLA/PLAA). | MUSS | ⚠️ |
| REQ-PLAUS-02 | Das System prüft **rechnerische Konsistenz** je Position (Menge × Einzelpreis = Positionsbetrag, Zuzahlungen, USt.). | MUSS | ⚠️ |
| REQ-PLAUS-03 | Das System prüft **Datumsplausibilitäten** (Leistungsdatum ≤ Rechnungsdatum, Leistungszeitraum innerhalb Verordnungsgültigkeit). | SOLL | ⚠️ |
| REQ-PLAUS-04 | Das System prüft **referenzielle Integrität** zwischen SLGA und SLLA (Rechnungsbezug, IK-Übereinstimmung). | MUSS | ⚠️ |
| REQ-PLAUS-05 | Das System erkennt **Doppelabrechnungen** innerhalb einer Datei. | SOLL | — |
| REQ-PLAUS-06 | Beim Korrekturverfahren prüft das System, dass ein **gültiger Bezug zur Ursprungsrechnung** existiert. | MUSS | ⚠️ |

## G. Kryptografie und Sicherheit (`REQ-SEC`)

| ID | Anforderung | Prio | Beleg |
|---|---|---|---|
| REQ-SEC-01 | Das System kann Nutzdaten nach **Anlage 16 GGT (PKCS#7/CMS)** entschlüsseln und verifizieren. | MUSS | ⚠️ |
| REQ-SEC-02 | Das System prüft die Schachtelung **`EnvelopedData` über `SignedData`**. | MUSS | ⚠️ |
| REQ-SEC-03 | Das System prüft die Algorithmen: **AES-256-CBC** (Inhalt), **SHA-256** (Digest), **RSA ≥ 4096 Bit**. | MUSS | ⚠️ |
| REQ-SEC-04 | Das System validiert **X.509-Zertifikate** inkl. Kette, Gültigkeitszeitraum, `KeyUsage` und Sperrstatus (CRL). | MUSS | ⚠️ |
| REQ-SEC-05 | Die Krypto-Schicht ist **algorithmus-agnostisch** implementiert, um die PQC-Migration (BSI TR-02102) ohne Eingriff in Parser und Fachlogik zu ermöglichen. | MUSS | ⚠️ |
| REQ-SEC-06 | **Private Schlüssel verlassen die Anwendung nicht** und werden nicht protokolliert. | MUSS | ⚠️ |
| REQ-SEC-07 | Das System unterstützt die Beschaffung/Nutzung von Zertifikaten des **ITSG Trust Center** und den LDAP-Bezug öffentlicher Schlüssel. | KANN | ⚠️ |

## H. Datenschutz (`REQ-DSGVO`)

| ID | Anforderung | Prio | Beleg |
|---|---|---|---|
| REQ-DSGVO-01 | **Entschlüsselte Nutzdaten werden nicht persistiert**, außer der Nutzer verlangt es ausdrücklich. | MUSS | — |
| REQ-DSGVO-02 | **Logs und Fehlermeldungen enthalten keine Sozialdaten** (KVNR, Name, Diagnose); Referenzen erfolgen über Positionsnummern/Zeilennummern. | MUSS | — |
| REQ-DSGVO-03 | **Testfixtures im Repository enthalten ausschließlich synthetische Daten**; echte Versichertendaten sind ausgeschlossen. | MUSS | — |
| REQ-DSGVO-04 | Eine **lokale Ausführung ohne Datenabfluss** ist möglich (kein Zwang zu Cloud-Verarbeitung). | MUSS | — |
| REQ-DSGVO-05 | Für den produktiven Einsatz wird eine **Auftragsverarbeitungs- und Löschkonzept-Dokumentation** bereitgestellt. | SOLL | — |

## I. Ergebnisaufbereitung und Betrieb (`REQ-OPS`)

| ID | Anforderung | Prio | Beleg |
|---|---|---|---|
| REQ-OPS-01 | Jeder Befund hat **Schweregrad** (Fehler / Warnung / Hinweis), **eindeutige Regel-ID**, **Fundstelle** (Datei, Segment, Feld, Zeile) und **Regelwerks-Fundstelle**. | MUSS | — |
| REQ-OPS-02 | Ergebnisse sind maschinenlesbar (**JSON**) und menschenlesbar (Report) verfügbar. | MUSS | — |
| REQ-OPS-03 | Das System ist als **CLI** nutzbar und CI-tauglich (Exit-Code nach Schweregrad). | MUSS | — |
| REQ-OPS-04 | Das System ist als **Bibliothek** einbindbar. | SOLL | — |
| REQ-OPS-05 | Prüfregeln sind **einzeln aktivier-/deaktivierbar** und konfigurierbar in der Schwere. | SOLL | — |
| REQ-OPS-06 | Das System verarbeitet große Dateien **speichereffizient** (Streaming statt vollständigem Einlesen). | SOLL | — |
| REQ-OPS-07 | Das System ist **offline lauffähig**; Stammdatenaktualisierung ist ein bewusster, separater Schritt. | MUSS | — |

## J. Qualitätssicherung (`REQ-QS`)

| ID | Anforderung | Prio | Beleg |
|---|---|---|---|
| REQ-QS-01 | Für jede Prüfregel existiert mindestens ein **Positiv- und ein Negativtestfall**. | MUSS | — |
| REQ-QS-02 | Prüfziffernalgorithmen (IK, KVNR) sind mit **Testvektoren** abgesichert. | MUSS | — |
| REQ-QS-03 | Die SECON-Implementierung wird gegen eine **unabhängige Referenz** (z. B. `DieTechniker/secon-tool`) gegengeprüft. | SOLL | ✅ |
| REQ-QS-04 | Jede Regel referenziert ihre **Quelle inkl. Regelwerksversion und Fundstelle**; Regeln ohne verifizierte Quelle sind als `experimental` markiert. | MUSS | — |
