# Konzept: Serverdienst zur Zuordnung von Urbelegen (Image-Link-Verfahren)

Status: **Entwurf zur Diskussion**, Stand 23.10.2026. Kein Code vorhanden.

## 1. Ziel

Ein serverseitiger Dienst, der

1. in einem **DTA-Verzeichnis** Abrechnungsdateien (Nutzdatei + Auftragsdatei) findet,
2. in einem **Beleg-Verzeichnis** eingescannte bzw. elektronische Urbelege findet,
3. jeden Beleg dem passenden **Rechnungssatz** (Abrechnungsfall) der DTA zuordnet und
4. als Ergebnis eine **Image-Link-Datei** schreibt, die Belege und DTA-Rechnungssätze verknüpft.

Nicht zugeordnete Belege und Fälle ohne Beleg werden nicht still verworfen, sondern in einem
Prüfbericht und einer Review-Queue ausgewiesen.

## 2. Belastbarkeit und Abgrenzung

> **Das Format der Image-Link-Datei ist in der Wissensbibliothek nicht belegt.** Bekannt ist nur
> der Rahmen (siehe Tabelle). Die Spezifikation (Satzaufbau, Dateinamen, Verfahrenskennung,
> Zeichensatz, Verknüpfungsschlüssel) muss beschafft werden, bevor der Writer gebaut wird.
> Das Konzept kapselt das Format deshalb in einem austauschbaren **Format-Adapter**.

| Aussage | Stand |
|---|---|
| Verfahrenskennung `IMG` = „Imagedaten nach § 7 der Vereinbarung nach § 300 SGB V" | ✅ Anlage 4 GGT |
| Verfahrenskennung `PFU` = elektronischer Urbeleg nach § 105 Abs. 2 SGB XI | ✅ Anlage 4 GGT |
| § 105: `INV.Belegnummer` muss der Belegnummer auf dem Urbeleg entsprechen | ✅ TA 1 6.4.0 |
| § 105 bis TA 1 6.4.0: Segment `IMG` (Leistungsnachweis-ID, UUID) verknüpft Fall und elektronischen Nachweis; ab 6.5.0 entfallen, Verknüpfung „anders gelöst" | ✅ / ❓ wie |
| Für § 302: Urbelege + Begleitzettel (Anlage 4), Inhalt der Urbelege (Anlage 5), Annahme durch Belegannahmestelle | ⚠️ Titel belegt, Inhalt nicht ausgewertet |
| Aufbau und Name der **Image-Link-Datei** | ❓ **offen** |

**Scope-Konflikt:** Das Projekt erklärt „Erzeugung von DTA-Dateien" als Out of Scope
(`01-projekt-scope-und-architektur.md`). Die Image-Link-Datei ist ein erzeugtes Artefakt. Vorschlag:
eigenes Modul `imagelink` neben dem Validator, das die DTA nur **liest** und nie verändert.
Das Ergebnis wird anschließend vom Validator geprüft (siehe Abschnitt 8).

## 3. Verzeichnisse und Eingaben

```
/srv/imagelink/
  mandanten/<ik>/
    dta/
      eingang/      Nutzdatei + .AUF (Dateipärchen), vom Abrechnungssystem abgelegt
    belege/
      eingang/      PDF/TIFF/JPEG, ggf. + Sidecar (.json/.xml/.txt)
    arbeit/         Zwischenergebnisse (Seitenbilder, OCR-Texte), nur Dienst
    ausgang/        Image-Link-Datei + Prüfbericht
    quarantaene/    unlesbare / widersprüchliche Eingaben
    archiv/         verarbeitete Eingaben, unveränderlich, mit Hash
```

Regeln:

- **Dateipärchen** (Nutzdatei + `.AUF`) werden über den Auftragssatz gelesen: Verfahrenskennung,
  Absender-IK, Dateiname, Datei- und Übertragungsgröße. Ein Pärchen ohne Gegenstück wartet,
  verfällt nach konfigurierbarer Zeit in die Quarantäne.
- **Stabile Einlieferung:** eine Datei gilt erst als eingeliefert, wenn ihre Größe über N Sekunden
  unverändert ist oder ein Marker (`.ready`) vorliegt. Verzeichnisse liegen oft auf SMB/NFS;
  Dateisystem-Events sind dort unzuverlässig, daher **Polling** als Grundlage, Events nur als Beschleunigung.
- **Verschlüsselung:** Echte DTA werden vor dem Versand nach SECON verschlüsselt. Der Dienst arbeitet
  auf der **Klartext-Nutzdatei vor der Verschlüsselung**; ein verschlüsseltes Pärchen
  (`VERSCHLUESSELUNGSART` ≠ `00`) wird erkannt und mit klarer Meldung abgelehnt.
- **Beleg-Container:** Ein Scanner liefert oft *eine* PDF mit vielen Seiten (so auch das Beispiel
  `leistungsnachweise.pdf`, 100 Seiten). Ein **Splitter** zerlegt solche Dateien in Einzelbelege
  (Trennung per Trennblatt-Barcode, Wechsel der erkannten Belegnummer oder feste Seitenzahl).

## 4. Datenmodell

| Entität | Inhalt (Auszug) |
|---|---|
| `DtaPaerchen` | Mandant (IK), Dateiname, SHA-256, Verfahrenskennung, Erstellzeit, Status |
| `Rechnung` | Rechnungsnummer, IK Kostenträger, Rechnungsart, Sammelrechnung ja/nein |
| `Rechnungssatz` | Schlüssel (siehe unten), KVNR, Name/Geburtsdatum (nur im Speicher/verschlüsselt), Leistungsdatum, Brutto, Zuzahlung, Positionszahl |
| `Beleg` | Dateiname, SHA-256, Seitenbereich, Typ (Leistungsnachweis, Verordnung, …), erkannte Merkmale |
| `Zuordnung` | Beleg ↔ Rechnungssatz, Verfahren (Regel/OCR/manuell), Konfidenz, Status, Bearbeiter |
| `Lauf` | Eingaben (Hashes), Konfiguration, Ergebnis, Prüfbericht, Ausgabedatei |

**Schlüssel eines Rechnungssatzes:** `(IK Leistungserbringer, Rechnungsnummer, Belegnummer)`.
Die Belegnummer allein ist nur innerhalb einer Rechnung eindeutig; bei Sammelrechnungen kommt die
Einzelrechnungsnummer (`:1`) hinzu. Die KVNR ist **kein** Schlüssel (ein Versicherter kann mehrere
Sätze haben), sondern Plausibilisierung.

## 5. Zuordnungsverfahren (Kaskade)

Jede Stufe liefert Kandidaten mit Konfidenz. Zuordnung automatisch nur bei **genau einem** Kandidaten
über Schwelle; sonst Review.

| Stufe | Quelle | Konfidenz | Beispiel |
|---|---|---|---|
| 1 | **Sidecar / Dateiname** nach vereinbarter Konvention (`<Rechnungsnr>_<Belegnr>.pdf`) | hoch | vom Scan-System gesetzt |
| 2 | **Maschinenlesbarer Code** (Barcode/QR) mit Belegnummer | hoch | Aufkleber vom Lieferschein |
| 3 | **Textextraktion** der Belegnummer (PDF-Textlayer, sonst OCR), Bezeichnung „Belegnummer" | mittel–hoch | Leistungsnachweis im Beispiel druckt `Belegnummer 0000001` |
| 4 | **Gegenprüfung** der Kandidaten über KVNR, Geburtsdatum, Lieferdatum, Bruttobetrag, Positionsnummern | erhöht/senkt Konfidenz | Betrag 113,10 im Beleg = `IAF` |
| 5 | **Manuell** in der Review-Oberfläche | — | Rest |

Konfliktregeln: mehrere Belege je Satz sind erlaubt (z. B. Verordnung + Lieferschein), ein Beleg für
mehrere Sätze nur bei Sammelbelegen (explizit zu erlauben). Widersprüche zwischen Stufe 3 und 4
(Belegnummer passt, Betrag nicht) führen **nicht** zur automatischen Zuordnung, sondern zum Befund.

## 6. Verarbeitungsablauf

```
Eingang erkannt → stabil? → Pärchen/Beleg klassifiziert → Parser (Streaming)
   → Rechnungssätze in Index (DB) ┐
   → Belege splitten, Merkmale extrahieren ┘ → Zuordnungskaskade
   → Vollständigkeitsprüfung → Review (falls nötig) → Image-Link schreiben
   → Nachprüfung → Archivierung + Bericht
```

Zustände je Lauf: `ERKANNT → EINGELESEN → ZUGEORDNET → IN_PRUEFUNG → FREIGEGEBEN → GESCHRIEBEN → ARCHIVIERT`
(Fehlerzweig `QUARANTAENE`). Alle Übergänge werden protokolliert.

- **Idempotenz:** Ein Lauf ist durch die Hashes seiner Eingaben und die Konfigurationsversion bestimmt.
  Gleiche Eingaben liefern dieselbe Image-Link-Datei (byte-identisch, ohne Zeitstempel im Inhalt, außer das Format verlangt ihn).
- **Nachlieferung:** Kommen Belege später, wird ein neuer Lauf auf demselben DTA-Stand gestartet;
  bestehende bestätigte Zuordnungen bleiben erhalten.
- **DTA-Änderung:** Ändert sich die DTA (neuer Hash), werden Zuordnungen verworfen, die auf geänderte
  Sätze zeigen, und erneut vorgeschlagen. Freigaben werden **nicht** übernommen.

## 7. Image-Link-Datei (Ausgabe)

Der **Format-Adapter** trennt Zuordnungslogik vom Dateiformat:

```
interface ImageLinkWriter { schreibe(zuordnungen, kontext) -> Datei, Auftragssatz? }
```

- Adapter `spec-v?` — wird nach Beschaffung der Spezifikation implementiert (❓).
- Adapter `json-neutral` — maschinenlesbarer Dump der Zuordnung für Tests und Review, **kein** Austauschformat.

Zu klären, sobald die Spezifikation vorliegt: Satzaufbau (fest/variabel), Zeichensatz, Dateiname und
Verfahrenskennung (`IMG`? `PFU`? andere), Verknüpfungsschlüssel (Rechnungsnummer, Belegnummer, UUID), ob die Datei eine
eigene Auftragsdatei erhält, ob Belegdateien beigepackt/komprimiert werden, Größenlimits, Reihenfolge.

Pflichtprüfungen **vor** dem Schreiben (konfigurierbar, Standard = Fehler):

| Prüfung | Schwere |
|---|---|
| Jeder Rechnungssatz, für den ein Urbeleg vorgeschrieben ist, hat ≥ 1 Beleg | Fehler |
| Jeder Beleg ist genau einem Satz (oder erlaubtem Sammelbezug) zugeordnet | Fehler |
| Belegdatei lesbar, Format/Größe zulässig, Hash gespeichert | Fehler |
| Belegnummer im Beleg = `INV`-Belegnummer | Fehler |
| Betragsabgleich Beleg ↔ Satz | Warnung (Fehler nur bei Konfiguration) |
| Satz ohne Zuordnung wegen Review offen | Blocker für Freigabe |

Nach dem Schreiben: Rücklesen der Datei, Vergleich mit dem Zuordnungsmodell, optional Lauf des
Validators auf Nutzdatei + Image-Link (Verknüpfungsschlüssel existieren in der DTA).

## 8. Architektur

```
 Verzeichnis-Poller ─► Job-Queue ─► Worker ─┬─ DTA-Parser (Streaming, aus Validator-Kern)
                                            ├─ Beleg-Pipeline (Splitter, PDF-Text, OCR, Barcode)
                                            ├─ Zuordnungs-Engine (Kaskade, Konfidenz)
                                            └─ Format-Adapter (Writer) + Prüfregeln
 Datenbank (PostgreSQL; SQLite für Einzelplatz)   Objektablage = Dateisystem (Hash-adressiert)
 HTTP-API + Web-UI (Review, Berichte, Konfiguration)   Audit-Log (append-only)
```

- **Kern-Wiederverwendung:** DTA-Parser und IK-/KVNR-Prüfungen kommen aus dem Validator-Kern. Die
  Zuordnung braucht nur `INV`, `NAD`, Summen; der Parser liest streamend und hält je Satz nur das Nötige.
- **Nebenläufigkeit:** je Mandant ein Lauf zugleich; Beleg-Pipeline parallelisierbar (OCR ist der teure Teil).
- **Betrieb:** Container oder systemd-Dienste; Konfiguration in YAML je Mandant; Metriken und Health-Endpunkt.
- **Technologie (Vorschlag, offen):** Python (Wiederverwendung der YAML-Referenzdaten, gute
  PDF-/OCR-Bibliotheken) mit Hintergrund-Workern; OCR über Tesseract, PDF-Text über poppler/pdfminer, Barcode über zxing/zbar.

## 9. Sicherheit und Datenschutz

Die Eingaben enthalten **Sozialdaten** (Name, KVNR, Leistungen).

- Zugriff nur über Mandantentrennung (IK) und Rollen: Betrieb, Sachbearbeitung (Review), Lesen (Bericht).
- Verschlüsselung der Ablage (Volume-Verschlüsselung), TLS für API/UI, keine Klartext-KVNR in Logs und Fehlermeldungen
  (maskiert, z. B. `K74185…67`).
- Dienstkonto mit **Nur-Lese-Zugriff** auf `dta/eingang`; Schreibzugriff nur auf `ausgang`, `arbeit`, `archiv`.
- Aufbewahrung und Löschung je Mandant konfigurierbar (Arbeitskopien kurz, Archiv nach Vorgabe des Auftraggebers);
  Löschung protokolliert. Auftragsverarbeitung nach Art. 28 DSGVO ist vertraglich zu regeln, wenn der Dienst für Dritte betrieben wird.
- Revisionssicherheit: Hash jeder Eingabe und Ausgabe, append-only Audit-Log, Freigabe nur namentlich.

## 10. Leistungsziele und Tests

| Größe | Ziel (Annahme, zu validieren) |
|---|---|
| DTA mit 45.000 Positionen / 9.000 Fällen (2,4 MB) einlesen und indizieren | < 5 s, Speicher < 500 MB |
| 9.000 Einzelbelege zuordnen (Stufe 1–2) | < 2 min ohne OCR |
| OCR-Anteil | Durchsatz durch Worker-Zahl skalierbar, Fortschrittsanzeige |

Testbasis aus diesem Repository (alle synthetisch):

- `beispiele/ultra-big-bills/hilfsmittel-302-inkontinenz-45000/` — großer DTA, Lastfall.
- `beispiele/ultra-big-bills/hilfsmittel-302-inkontinenz-sammelrechnung-100/` — 100 Fälle mit
  `leistungsnachweise.pdf` (eine PDF, 100 Seiten, Belegnummer im Text, Reihenfolge wie DTA) —
  **Abnahmetest für Splitter und Stufe 3**: erwartet 100 Belege, 100 eindeutige Zuordnungen.
- Zu ergänzen: Negativfälle (fehlender Beleg, doppelter Beleg, vertauschte Belegnummer, falscher Betrag,
  Beleg ohne Satz, unlesbarer Scan, DTA nach Zuordnung geändert).

## 11. Anforderungen (Vorschlag)

| ID | Anforderung | Priorität |
|---|---|---|
| REQ-IL-01 | Der Dienst erkennt Dateipärchen im DTA-Verzeichnis und liest Auftragssatz und Rechnungssätze, ohne die DTA zu verändern. | MUSS |
| REQ-IL-02 | Jeder Beleg wird genau einem Rechnungssatz zugeordnet oder als offen ausgewiesen. | MUSS |
| REQ-IL-03 | Automatische Zuordnung erfolgt nur bei eindeutigem Kandidaten über Schwelle. | MUSS |
| REQ-IL-04 | Mehrseitige Sammel-PDFs werden in Einzelbelege getrennt. | MUSS |
| REQ-IL-05 | Die Image-Link-Datei wird über einen austauschbaren Format-Adapter geschrieben. | MUSS |
| REQ-IL-06 | Jeder Lauf ist reproduzierbar (Eingabe-Hashes, Konfigurationsversion) und auditierbar. | MUSS |
| REQ-IL-07 | Personenbezogene Daten erscheinen nicht unmaskiert in Logs. | MUSS |
| REQ-IL-08 | Review-Oberfläche für offene und konfliktbehaftete Zuordnungen. | SOLL |
| REQ-IL-09 | Ergebnis wird mit dem Validator gegengeprüft. | SOLL |

## 12. Offene Punkte

1. **Spezifikation der Image-Link-Datei** beschaffen (für § 302 und ggf. § 300/§ 105 getrennt) — blockiert den Writer.
2. Inhalt der Urbelege (§ 302 Anlage 5) und Begleitzettel (Anlage 4) auswerten: welche Belegarten sind je Leistungsbereich Pflicht?
3. Wie werden Verordnung, Genehmigung und Lieferschein bei Hilfsmitteln dem Fall zugeordnet — ein Beleg oder mehrere, mit eigener Kennzeichnung?
4. Format und Größenlimits der Belegbilder (PDF/TIFF, Auflösung, Farbtiefe) laut Spezifikation.
5. Zulässigkeit eines Dienstes **vor** der Verschlüsselung im Abrechnungsprozess des Betreibers (Einbindung in die bestehende Kette).
6. Mandantenmodell: Betrieb für einen Leistungserbringer oder als Dienstleister für viele (Auswirkung auf Datenschutz und Betrieb).
7. Entscheidung Scope: eigenes Modul im Repository oder eigenes Projekt, das den Validator-Kern als Bibliothek nutzt.

## 13. Vorgehen

| Phase | Inhalt |
|---|---|
| 0 | Spezifikation beschaffen, Offene Punkte 1–3 klären |
| 1 | Poller, DTA-Index, Dateinamen-Zuordnung (Stufe 1), `json-neutral`-Adapter, Prüfbericht |
| 2 | Splitter, PDF-Text, Belegnummer-Extraktion (Stufe 3), Gegenprüfung (Stufe 4) |
| 3 | Review-UI, Rollen, Audit, Betrieb |
| 4 | Spezifischer Writer, Validator-Gegenprüfung, OCR/Barcode, Lasttests |
