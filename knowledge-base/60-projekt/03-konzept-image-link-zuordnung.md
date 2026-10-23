# Konzept: Serverdienst zur Zuordnung von Urbelegen (ImageLink-Verfahren, § 302 SGB V)

Status: **Entwurf zur Diskussion**, Stand 23.10.2026 (überarbeitet nach Auswertung der Spezifikation). Kein Code vorhanden.

## 1. Ziel

Ein serverseitiger Dienst, der

1. in einem **DTA-Verzeichnis** Abrechnungsdateien (Nutzdatei + Auftragsdatei) findet,
2. in einem **Beleg-Verzeichnis** eingescannte bzw. elektronische Urbelege findet,
3. jeden Beleg dem passenden **Rechnungssatz** (Abrechnungsfall) der DTA zuordnet und
4. daraus das **ImageLink-Lieferpaket** erzeugt: je Beleg ein PDF mit zugehöriger XML-Metadatendatei, gepackt als ZIP, mit Auftragsdatei.

Nicht zugeordnete Belege und Fälle ohne Beleg werden nicht still verworfen, sondern in einem
Prüfbericht und einer Review-Queue ausgewiesen.

## 2. Die Spezifikation (belegt)

Das Verfahren ist in **Anlage 1 Anhang 4a** (Stand 14.07.2022, V 001, ab 01.09.2022, 23 Seiten) und dem
XML-Schema **Anhang 4b** beschrieben. Auswertung: [`data/imagelink.yaml`](../data/imagelink.yaml),
Quellen Q41/Q42. Die Kernpunkte, die das Konzept bestimmen:

| Punkt | Inhalt |
|---|---|
| **Es gibt keine einzelne „Image-Link-Datei".** | Geliefert wird ein **ZIP** mit je Urbeleg einem **PDF-Image** und einer gleichnamigen **XML-Metadatendatei** (Endung `.XML`). Die „Zuordnung" steckt in Dateiname und XML-Nutzdaten. |
| Bezug Image ↔ Metadaten | identischer Dateiname (max. 40 Stellen) = `Dokumentidentifikator`; mehrere Dokumente eines Abrechnungsfalls tragen denselben `Vorgangsidentifikator`, `Vorgangsumfang` = Anzahl. |
| Bezug zum DTA-Rechnungssatz | Nutzdaten der XML: `Sammelrechnungsnummer` (14), `Einzelrechnungsnummer` (6), `Rechnungsdatum`, `Rechnungsart` (alle aus `REC`), `Belegnummer` (10, aus `INV`), `Leistungserbringer`-IK, `KassenInstitutionskennzeichen`, optional KVNR als Ordnungsbegriff `PKKVDE`. |
| Dokumentklassen | Hilfsmittel: Einzelrechnung `ER_SOLE_HIMI_ON` (Verordnung/zahlungsbegründender Beleg, signiert) und `ER_SOLE_HIMI_M` (Merge, ohne Signatur, niedrige Auflösung); Sammelrechnung `SR_SOLE_HIMI_ON`. |
| Paket | Ordner je Stapel (max. **500 Images**, 1000 Dateien), ZIP max. **2 GB**; Ordnername `<ABR-Kürzel 3>_<Sammelrechnungsnr 14><Zähler 2>` bzw. `<IK 9>_<lfd. Nr. 8><Zähler 2>`. |
| Transport | Auftragsdatei `.AUF` mit Verfahrenskennung `E1IM0` (Test `T1IM0`), Komprimierung `03` ZIP, Verschlüsselung `03` und Unterschrift `03` (PKCS#7), SFTP-Push, ISO 8859-1. |
| Optional | Nutzung nur nach Vereinbarung zwischen Lieferant und Kostenträger. |

**Wichtige Einschränkungen der Quelle:** Das Dokument ist erkennbar von AOK Systems geprägt (`Beschreibung` fest
„AOK Systems GmbH", Referenzbeschreibung „Multicom-Nutzer"), enthält Tippfehler und Widersprüche (Liste in
`imagelink.yaml`, u. a. Länge des ABR-Kürzels, Eingangskanal, Verfahrenskennung `1IM` ist in unserer Auswertung von Anlage 4 GGT nicht als Eintrag geführt)
und sagt **nichts** zu Bildformat, Auflösung, Farbtiefe der PDF. Ob jede Kasse es gleich anwendet, ist offen.
Die Urbeleg-Inhalte regelt Anlage 5 (V 4.0, 27.09.2018), den Begleitzettel Anlage 4 (V 2.0, 2006); beide sind ausgewertet (Abschnitt 2a).

**Passung zu den Beispieldaten:** Die Fixtures unter `beispiele/ultra-big-bills/` verwenden Rechnungsnummern
wie `2026100190:0` und 7-stellige Belegnummern; die Spezifikation nennt 14 / 6 / 10 Stellen. Das ist
im Fixture anzupassen, bevor es als ImageLink-Testbasis taugt.

**Scope-Konflikt:** Das Projekt erklärt „Erzeugung von DTA-Dateien" als Out of Scope. Das ImageLink-Paket ist ein
erzeugtes Artefakt. Vorschlag: eigenes Modul `imagelink` neben dem Validator, das die DTA nur **liest** und nie
verändert; Ergebnis wird mit dem Validator gegengeprüft (Abschnitt 7).

## 2a. Urbelege und Begleitzettel (Anlage 4 und 5, belegt)

Auswertung: [`data/urbelege.yaml`](../data/urbelege.yaml). Was für den Dienst folgt:

- **Der Urbeleg trägt die Zuordnungsmerkmale selbst.** Auf dem Verordnungsblatt (Hilfsmittel: Muster 16) stehen
  *Rechnungsnummer mit Belegnummer*, *Hilfsmittelnummer/Faktor/Taxe*, *Gesamtsumme brutto* und *Zuzahlungsbetrag*; bei Seh- und
  Hörhilfen sowie Berechtigungsschein zusätzlich IK des Leistungserbringers. Das trägt Stufe 3 (Belegnummer) und
  Stufe 4 (Betrag, Positionsnummern) der Zuordnung unmittelbar.
- **Die Empfangsbestätigung steht auf der Verordnung** (Feld v), nicht auf einem eigenen Lieferschein. Ein getrennter
  Leistungsnachweis ist in Anlage 5 nicht vorgesehen und gilt nur kraft Vereinbarung. Die synthetischen „Leistungsnachweise"
  der Beispieldaten sind daher eine Variante, kein Regelfall.
- **Begleitzettel (Anlage 4):** zwingend, **je Gesamtrechnung**; bei Abrechnungsstellen für jede Gesamtrechnung innerhalb
  einer Sammelrechnung. Pflichtinhalt: IK und Name der Krankenkasse, Name/Anschrift und IK des Leistungserbringers bzw. der
  Abrechnungsstelle, Rechnungsnummer und -datum, Anzahl der Urbelege; Abrechnungsstellen zusätzlich **erste und letzte
  Belegnummer**. Der Dienst kann ihn vollständig aus DTA und Zuordnung erzeugen, braucht dazu aber Name der Krankenkasse
  (aus Kostenträgerdatei) und Anschrift des Leistungserbringers (Mandantenstammdaten).
- **Offen:** Ob und wie der Begleitzettel im ImageLink-Paket mitgeliefert wird, regeln weder Anlage 4 noch Anhang 4a.
  Beide Anlagen beschreiben Papierbelege mit Musterständen 2000–2017.

## 3. Verzeichnisse und Eingaben

```
/srv/imagelink/
  mandanten/<ik>/
    dta/eingang/        Nutzdatei + .AUF (Dateipärchen), vom Abrechnungssystem abgelegt
    belege/eingang/     PDF/TIFF/JPEG, ggf. + Sidecar (.json/.xml/.txt)
    arbeit/             Zwischenergebnisse (Seitenbilder, OCR-Texte), nur Dienst
    ausgang/            ZIP-Paket, .AUF, Prüfbericht
    quarantaene/        unlesbare / widersprüchliche Eingaben
    archiv/             verarbeitete Eingaben, unveränderlich, mit Hash
```

- **Dateipärchen** werden über den Auftragssatz gelesen (Verfahrenskennung, Absender-IK, Dateiname, Größen).
  Ein Pärchen ohne Gegenstück wartet und verfällt nach konfigurierbarer Zeit in die Quarantäne.
- **Stabile Einlieferung:** Datei gilt erst als eingeliefert, wenn ihre Größe über N Sekunden unverändert ist oder ein
  Marker (`.ready`) vorliegt. Auf SMB/NFS sind Dateisystem-Events unzuverlässig, daher **Polling** als Grundlage.
- **Verschlüsselung:** Echte DTA sind vor dem Versand SECON-verschlüsselt. Der Dienst arbeitet auf der
  **Klartext-Nutzdatei**; ein verschlüsseltes Pärchen (`VERSCHLUESSELUNGSART` ≠ `00`) wird erkannt und abgelehnt.
  Das **ausgehende** ImageLink-Paket wird dagegen selbst signiert und verschlüsselt (PKCS#7, Anlage 16 GGT) — das braucht
  Zertifikate des Leistungserbringers bzw. Abrechners und eine Schlüsselverwaltung.
- **Beleg-Container:** Scanner liefern oft *eine* PDF mit vielen Seiten (so das Beispiel `leistungsnachweise.pdf`).
  Ein **Splitter** zerlegt in Einzelbelege (Trennblatt-Barcode, Wechsel der erkannten Belegnummer oder feste Seitenzahl).
  Die Spezifikation spricht von „Vorgangstrennblättern" als Mittel der Vorgangsbildung.

## 4. Datenmodell

| Entität | Inhalt (Auszug) |
|---|---|
| `DtaPaerchen` | Mandant (IK), Dateiname, SHA-256, Verfahrenskennung, Erstellzeit, Status |
| `Sammelrechnung` | Sammelrechnungsnummer (14), Rechnungsdatum, Rechnungsart, IK Kostenträger, Rechnungssteller-IK |
| `Rechnungssatz` | Einzelrechnungsnummer (6), Belegnummer (10), KVNR, Leistungsdatum, Brutto, Zuzahlung, Positionszahl; personenbezogene Felder nur verschlüsselt/im Speicher |
| `Beleg` | Dateiname, SHA-256, Seitenbereich, Dokumentklasse (`ER_SOLE_HIMI_ON`/`_M`), erkannte Merkmale |
| `Zuordnung` | Beleg ↔ Rechnungssatz, Verfahren (Regel/OCR/manuell), Konfidenz, Status, Bearbeiter |
| `Begleitzettel` | je Gesamtrechnung: Kassen-IK/-Name, Rechnungsnummer/-datum, Anzahl Urbelege, erste/letzte Belegnummer |
| `Paket` | Stapel/Ordner, Dokumentidentifikatoren, Zähler, ZIP-Hash, `.AUF`, Transfernummer |
| `Lauf` | Eingaben (Hashes), Konfiguration, Ergebnis, Prüfbericht |

**Schlüssel eines Rechnungssatzes:** `(IK Leistungserbringer, Sammelrechnungsnummer, Einzelrechnungsnummer, Belegnummer)`.
Das entspricht den Nutzdaten der XML und zugleich der Bildung des Vorgangsidentifikators. Die KVNR ist **kein** Schlüssel,
sondern Plausibilisierung.

## 5. Zuordnungsverfahren (Kaskade)

Jede Stufe liefert Kandidaten mit Konfidenz. Automatisch zugeordnet wird nur bei **genau einem** Kandidaten über Schwelle.

| Stufe | Quelle | Konfidenz |
|---|---|---|
| 1 | **Sidecar / Dateiname** nach Konvention; bereits ImageLink-konforme Namen (`<ABR>_<Sammel><Einzel><Beleg><Zähler>`) lassen sich direkt zerlegen | hoch |
| 2 | **Barcode/QR** mit Belegnummer bzw. Dokumentidentifikator | hoch |
| 3 | **Textextraktion** der Belegnummer (PDF-Textlayer, sonst OCR) | mittel–hoch |
| 4 | **Gegenprüfung** über KVNR, Geburtsdatum, Lieferdatum, Bruttobetrag, Positionsnummern | erhöht/senkt Konfidenz |
| 5 | **Manuell** in der Review-Oberfläche | — |

Konfliktregeln: mehrere Dokumente je Satz sind erlaubt und gewollt (Verordnung, Empfangsbestätigung, Genehmigung;
Zähler `01…`, `Vorgangsumfang` = Anzahl). Ein Beleg für mehrere Sätze nur als Sammelbeleg auf Ebene `SR_*`. Widersprüche
zwischen Stufe 3 und 4 führen **nicht** zur automatischen Zuordnung, sondern zum Befund.

## 6. Verarbeitungsablauf

```
Eingang erkannt → stabil? → klassifiziert → DTA-Parser (Streaming) → Index der Rechnungssätze
   Belege splitten → Merkmale extrahieren → Zuordnungskaskade → Vollständigkeitsprüfung
   → Review (falls nötig) → Paket bauen (Ordner, XML je PDF, ZIP, .AUF) → signieren/verschlüsseln
   → Nachprüfung → Archivierung + Bericht
```

Zustände je Lauf: `ERKANNT → EINGELESEN → ZUGEORDNET → IN_PRUEFUNG → FREIGEGEBEN → PAKET_ERSTELLT → ARCHIVIERT`
(Fehlerzweig `QUARANTAENE`). Alle Übergänge werden protokolliert.

- **Idempotenz:** gleiche Eingaben und Konfiguration ergeben dasselbe Paket (XML ohne wechselnde Inhalte; `Erstellungszeitpunkt`
  ist der Scan-/Erstellzeitpunkt des Belegs, nicht der Laufzeitpunkt).
- **Stapelbildung:** automatisch nach Grenzen der Spezifikation (500 Images je Ordner, 2 GB je ZIP, Zähler `01…` je Ordner/ZIP).
- **Nachlieferung / DTA-Änderung:** wie bisher — neuer Lauf; Zuordnungen auf geänderte Sätze werden verworfen, Freigaben nicht übernommen.

## 7. Ausgabe und Prüfungen

Je Beleg wird erzeugt:

- `<Dokumentidentifikator>.PDF` — das Image (Multi-PDF, bei Dokumentklasse `…_ON` signiert),
- `<Dokumentidentifikator>.XML` — Wurzel `eAkte_Dokumentdatensatz`, `Versionsnummer` 100, `Dokumentklasse`, `Eingangskanal` 2,
  `Erstellungszeitpunkt`, `Zugriffschutz`, `KassenInstitutionskennzeichen`, `Ordnungsbegriffe` (z. B. `PKKVDE`),
  `VariableNutzdaten` (Sammel-/Einzelrechnungsnummer, Rechnungsdatum, Rechnungsart, Belegnummer, Leistungserbringer).

Die Ausgabe läuft über einen **Format-Adapter** (`imagelink-302-anhang4a` als Standard), damit abweichende Kassenvarianten
(z. B. `Beschreibung`, Eingangskanal) konfigurierbar bleiben.

Pflichtprüfungen **vor** dem Schreiben (Standard = Fehler):

| Prüfung | Schwere |
|---|---|
| XML validiert gegen XSD Anhang 4b | Fehler |
| Dateiname ≤ 40 Zeichen, nur erlaubte Zeichen, `.XML` großgeschrieben, PDF/XML gleichnamig | Fehler |
| `Dokumentidentifikator` = Dateiname; `Vorgangsidentifikator` bei allen Dokumenten eines Falls gleich; `Vorgangsumfang` = Anzahl | Fehler |
| Nutzdaten stimmen mit dem DTA-Satz überein (REC, INV, IK, Kostenträger-IK) | Fehler |
| Belegnummer 10 Stellen, Sammelrechnungsnr 14, Einzelrechnungsnr 6 | Fehler |
| Jeder Satz mit Urbeleg-Pflicht hat ≥ 1 Dokument der erwarteten Klasse | Fehler |
| Jeder Beleg ist genau einem Satz (oder erlaubtem Sammelbezug) zugeordnet | Fehler |
| ≤ 500 Images je Ordner, ZIP ≤ 2 GB | Fehler |
| Auftragssatz: `E1IM0`/`T1IM0`, Komprimierung 03, Verschlüsselung 03, Unterschrift 03, Größen stimmen | Fehler |
| Betragsabgleich Beleg ↔ Satz | Warnung |
| Begleitzettel je Gesamtrechnung vorhanden, Anzahl Urbelege und erste/letzte Belegnummer stimmen mit der Zuordnung | Fehler |
| Offene Review-Fälle | Blocker für Freigabe |

Nach dem Schreiben: ZIP entpacken und gegen das Modell prüfen; optional Lauf des Validators auf Nutzdatei + Paket.

## 8. Architektur

```
 Verzeichnis-Poller ─► Job-Queue ─► Worker ─┬─ DTA-Parser (Streaming, aus Validator-Kern)
                                            ├─ Beleg-Pipeline (Splitter, PDF-Text, OCR, Barcode)
                                            ├─ Zuordnungs-Engine (Kaskade, Konfidenz)
                                            └─ Paket-Builder (XML, ZIP, .AUF, PKCS#7) + Prüfregeln
 Datenbank (PostgreSQL; SQLite für Einzelplatz)   Objektablage = Dateisystem (Hash-adressiert)
 HTTP-API + Web-UI (Review, Berichte, Konfiguration)   Audit-Log (append-only)
```

Wiederverwendung: DTA-Parser sowie IK-/KVNR-Prüfungen aus dem Validator-Kern. Nebenläufigkeit: je Mandant ein Lauf zugleich,
Beleg-Pipeline parallelisierbar. Betrieb als Container oder systemd-Dienste, YAML-Konfiguration je Mandant, Metriken und
Health-Endpunkt. Technologie (Vorschlag, offen): Python mit Hintergrund-Workern; Tesseract (OCR), poppler/pdfminer (PDF-Text),
zxing/zbar (Barcode), XML-Validierung mit lxml gegen das XSD, PKCS#7 über eine geprüfte Bibliothek (Referenz:
`DieTechniker/secon-tool`, Q40).

## 9. Sicherheit und Datenschutz

Die Eingaben enthalten **Sozialdaten**.

- Mandantentrennung (IK) und Rollen: Betrieb, Sachbearbeitung (Review), Lesen (Bericht).
- Verschlüsselung der Ablage, TLS für API/UI, keine Klartext-KVNR in Logs und Fehlermeldungen (maskiert).
- Dienstkonto mit **Nur-Lese-Zugriff** auf `dta/eingang`; Schreibzugriff nur auf `ausgang`, `arbeit`, `archiv`.
- **Private Schlüssel** für PKCS#7-Signatur/Verschlüsselung in HSM/Keystore, nicht im Dateisystem der Eingaben.
- Aufbewahrung/Löschung je Mandant konfigurierbar, Löschung protokolliert. Auftragsverarbeitung (Art. 28 DSGVO), wenn der Dienst für Dritte läuft.
- Revisionssicherheit: Hash jeder Eingabe und Ausgabe, append-only Audit-Log, Freigabe nur namentlich.

## 10. Leistungsziele und Tests

| Größe | Ziel (Annahme, zu validieren) |
|---|---|
| DTA mit 45.000 Positionen / 9.000 Fällen (2,4 MB) einlesen und indizieren | < 5 s, Speicher < 500 MB |
| 9.000 Einzelbelege zuordnen (Stufe 1–2) und in 18 Ordner à ≤ 500 Images verpacken | < 3 min ohne OCR |
| OCR-Anteil | über Worker-Zahl skalierbar, Fortschrittsanzeige |

Testbasis (alle synthetisch): `beispiele/ultra-big-bills/…-45000/` (Lastfall) und `…-sammelrechnung-100/` mit
`leistungsnachweise.pdf` (eine PDF, 100 Seiten, Belegnummer im Text, Reihenfolge wie DTA) — **Abnahmetest für Splitter und
Stufe 3**: 100 Belege, 100 eindeutige Zuordnungen, 100 PDF/XML-Paare, XSD-valide. Voraussetzung: Fixture auf Nummernformate
der Spezifikation anpassen (Abschnitt 2). Zu ergänzen: Negativfälle (fehlender Beleg, doppelter Beleg, vertauschte
Belegnummer, falscher Betrag, Beleg ohne Satz, unlesbarer Scan, > 500 Images, ungültiger Dateiname, XSD-Verstoß, DTA nach
Zuordnung geändert).

## 11. Anforderungen (Vorschlag)

| ID | Anforderung | Priorität |
|---|---|---|
| REQ-IL-01 | Der Dienst erkennt Dateipärchen im DTA-Verzeichnis und liest Auftragssatz und Rechnungssätze, ohne die DTA zu verändern. | MUSS |
| REQ-IL-02 | Jeder Beleg wird genau einem Rechnungssatz zugeordnet oder als offen ausgewiesen. | MUSS |
| REQ-IL-03 | Automatische Zuordnung nur bei eindeutigem Kandidaten über Schwelle. | MUSS |
| REQ-IL-04 | Mehrseitige Sammel-PDFs werden in Einzelbelege getrennt. | MUSS |
| REQ-IL-05 | Je Beleg entsteht ein PDF/XML-Paar nach Anhang 4a mit XSD-valider XML und regelkonformen Dateinamen. | MUSS |
| REQ-IL-06 | Pakete respektieren 500 Images je Ordner und 2 GB je ZIP; Auftragssatz gemäß `E1IM0`. | MUSS |
| REQ-IL-07 | Jeder Lauf ist reproduzierbar (Eingabe-Hashes, Konfigurationsversion) und auditierbar. | MUSS |
| REQ-IL-08 | Personenbezogene Daten erscheinen nicht unmaskiert in Logs. | MUSS |
| REQ-IL-09 | Review-Oberfläche für offene und konfliktbehaftete Zuordnungen. | SOLL |
| REQ-IL-10 | Kassenspezifische Abweichungen (Beschreibung, Eingangskanal, Dokumentklassen) sind konfigurierbar. | SOLL |
| REQ-IL-11 | Ergebnis wird mit dem Validator gegengeprüft. | SOLL |
| REQ-IL-12 | Je Gesamtrechnung wird ein Begleitzettel nach Anlage 4 mit Anzahl Urbelege sowie erster und letzter Belegnummer erzeugt oder geprüft. | MUSS |

## 12. Offene Punkte

1. **Anlage 4/5 sind ausgewertet.** Offen bleibt: Gelten die Musterstände (2000–2017) für elektronische Verordnungen unverändert? Wird der Begleitzettel im ImageLink-Paket mitgeliefert (und in welcher Form)? Sind Lieferschein/Empfangsbestätigung als eigener Beleg zu liefern (nur kraft Vereinbarung)?
2. **Kassenvereinbarung:** Das Verfahren ist optional und je Kostenträger zu vereinbaren. Welche Kassen nutzen es, mit welchen Abweichungen (Kürzel, `Beschreibung`, Dokumentklassen, SFTP-Ziele)?
3. **Widersprüche** der Spezifikation (Liste in `imagelink.yaml`) mit einer annehmenden Stelle klären: Länge ABR-Kürzel, Eingangskanal, `Beschreibung`, Verfahrenskennung `1IM` (in unserer Auswertung von Anlage 4 GGT nicht als Eintrag geführt).
4. **PDF-Anforderungen** (Auflösung, Farbtiefe, PDF/A, Signaturform) — Anhang 4a sagt dazu nichts.
5. **Belegnummer-Format:** Wie wird die 10-stellige DTA-Belegnummer auf die 7-stellige der Praxissoftware abgebildet; Fixture anpassen.
6. **Neuere Fassung**: Das Portal führt Anhang 4a (14.07.2022) als aktuell; ob TA 1 V22 (21.05.2026, ab 01.02.2027) oder neue Anhänge (z. B. „Anhang 6 — Elektronische Leistungsbestätigung", laut Portalrecherche aufgeführt, Fundstelle nicht selbst geprüft, **nicht ausgewertet**) das Verfahren berühren, ist zu prüfen.
7. **Zertifikate und Schlüssel** für PKCS#7: Wer signiert und verschlüsselt (Leistungserbringer oder Abrechner), welche Zertifikate, welche Empfänger-Schlüssel?
8. **Einbindung in die Abrechnungskette** vor der SECON-Verschlüsselung der DTA; Mandantenmodell (ein Leistungserbringer oder viele).
9. Entscheidung Scope: eigenes Modul im Repository oder eigenes Projekt mit dem Validator-Kern als Bibliothek.

## 13. Vorgehen

| Phase | Inhalt |
|---|---|
| 0 | Offene Punkte 1–4 klären, Begleitzettel-Generator auf Anlage 4 prüfen, Fixture auf Spezifikationsformate anpassen |
| 1 | Poller, DTA-Index, Dateinamen-Zuordnung (Stufe 1), XML-Builder mit XSD-Validierung, Prüfbericht (ohne Signatur) |
| 2 | Splitter, PDF-Text, Belegnummer-Extraktion (Stufe 3), Gegenprüfung (Stufe 4), Stapelbildung, ZIP, `.AUF` |
| 3 | Review-UI, Rollen, Audit, Betrieb |
| 4 | PKCS#7-Signatur/-Verschlüsselung, OCR/Barcode, Validator-Gegenprüfung, Lasttests |
