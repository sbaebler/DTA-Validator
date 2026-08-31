# Domänenüberblick: DTA im GKV-Markt

## 1. Was ist "DTA"?

**DTA** steht historisch für *Datenträgeraustausch* — die Abrechnung von Leistungen
gegenüber gesetzlichen Krankenkassen auf maschinell verwertbaren Datenträgern.
Der Begriff hat sich als Sammelbezeichnung gehalten, obwohl physische Datenträger
heute die Ausnahme sind und der Austausch praktisch vollständig als **elektronische
Datenübertragung (EDI)** stattfindet. ⚠️ [Q1][Q23]

Abzugrenzen ist DTA im GKV-Kontext von:
- **DTAUS** — dem (abgelösten) Zahlungsverkehrsformat der Kreditwirtschaft. Keinerlei fachlicher Bezug.
- **DALE-UV** — dem Datenaustausch mit der gesetzlichen **Unfall**versicherung (DGUV).
  Technisch eng verwandt (gleiche Gemeinsame Grundsätze Technik), fachlich eigenständig.

## 2. Zwei große Familien

Im GKV-Markt existieren zwei getrennte Datenaustausch-Welten, die sich denselben
technischen Unterbau (Gemeinsame Grundsätze Technik, § 95 SGB IV) teilen: ✅ [Q11][Q12]

### A. Leistungserbringer ↔ Krankenkassen (Abrechnung, §§ 294 ff. SGB V)
Der Fokus dieser Wissensbibliothek und des DTA-Validators.
Leistungserbringer (Krankenhäuser, Apotheken, Heil-/Hilfsmittelerbringer, Pflegedienste,
Ärzte, Hebammen …) übermitteln Abrechnungs- und Behandlungsdaten an die Kassen.

### B. Arbeitgeber / Zahlstellen ↔ Sozialversicherung (Meldeverfahren, §§ 28a ff. SGB IV, DEÜV)
DEÜV-Meldungen, Beitragsnachweise, GKV-Monatsmeldung, AAG, EEL, eAU u. a.
Läuft über den **GKV-Kommunikationsserver** im eXTra-XML-Standard. ⚠️ [Q19][Q26]
Siehe [20-verfahren/06-weitere-verfahren.md](../20-verfahren/06-weitere-verfahren.md).

## 3. Akteure und Rollen

| Rolle | Beschreibung |
|---|---|
| **Leistungserbringer (LE)** | Erbringt die Leistung, ist Rechnungssteller. Identifiziert durch **Institutionskennzeichen (IK)**. |
| **Abrechnungszentrum / Rechenzentrum** | Optionaler Dienstleister, der im Auftrag des LE abrechnet. Bei Apotheken (§ 300) faktisch der Regelfall. ⚠️ [Q6] |
| **Datenannahmestelle (DAV/DAS)** | Nimmt verschlüsselte Nutzdaten entgegen, entschlüsselt und verteilt an die Kasse. Verzeichnet in der **Kostenträgerdatei**. ⚠️ [Q15] |
| **Belegannahmestelle** | Nimmt Urbelege (Verordnungen, Leistungsnachweise) entgegen. Ebenfalls in der Kostenträgerdatei. ⚠️ [Q15] |
| **Kostenträger (Krankenkasse / Pflegekasse)** | Empfänger und Zahler. Ebenfalls per IK identifiziert. |
| **GKV-Spitzenverband** | Erlässt Richtlinien und Technische Anlagen, betreibt gkv-datenaustausch.de. ✅ [Q1] |
| **ITSG GmbH** | Betreibt das **Trust Center** (Zertifikate) und die **Systemuntersuchung** (Softwarezertifizierung). ⚠️ [Q13] |
| **ARGE·IK (bei der DGUV)** | Vergibt und pflegt die Institutionskennzeichen. ⚠️ [Q9] |
| **gematik** | Verantwortet die Telematikinfrastruktur (TI) und KIM als künftigen Transportweg. ⚠️ [Q18] |

## 4. Der generische Ablauf einer DTA-Abrechnung

```
 Leistungserbringer                Datenannahmestelle              Krankenkasse
 ─────────────────                 ──────────────────              ────────────
 1. Leistung erbringen
 2. Abrechnungsdatei erzeugen
    (Nachrichten je Sektor,
     z. B. SLGA + SLLA)
 3. Signieren + verschlüsseln
    (PKCS#7/CMS, Anlage 16)
 4. Auftragsdatei erzeugen
    (unverschlüsselt, .AUF)
 5. Übertragen  ───────────────►   6. Auftragsdatei auswerten
    (E-Mail/HTTPS/SFTP/                (Routing, Verfahrenskennung)
     KomServer/KIM)                 7. Entschlüsseln + Signatur prüfen
                                    8. Syntax-/Schlüssel-/Plausibilitätsprüfung
                                    9. Weiterleiten ────────────────►  10. Fachliche Prüfung
                                                                       11. Zahlung / Absetzung
                 ◄──────────────────────────────────────────────────  12. Rückmeldung
                    (Fehlernachricht / Zahlungssatz / Absetzung)
 13. Korrektur / Nachforderung
     mit Verarbeitungskennzeichen
     und Bezug zur Ursprungsrechnung
```

Der **DTA-Validator** setzt an den Schritten 2 und 8 an: er prüft eine erzeugte oder
empfangene Datei, bevor sie produktiv gesendet bzw. verarbeitet wird.

## 5. Das Dateipärchen-Prinzip (KKS)

Alle Verfahren nach §§ 294 ff. SGB V nutzen das **Krankenkassenkommunikationssystem
(KKS)**: übertragen wird immer ein **Paar aus zwei Dateien** ⚠️ [Q14]

1. **Nutzdatendatei** — die eigentlichen Abrechnungsdaten, **verschlüsselt**
2. **Auftragsdatei** — der *Auftragssatz* mit allen Transportinformationen, **unverschlüsselt**

Reihenfolge: erst die Nutzdatendatei, dann die Auftragsdatei. Die Auftragsdatei fungiert
als "Commit"-Signal für die automatisierte Verarbeitung. ⚠️ [Q14][Q7]

Details: [30-technik/02-kks-auftragsdatei-dateinamen.md](../30-technik/02-kks-auftragsdatei-dateinamen.md)

## 6. Warum elektronisch? — Der wirtschaftliche Zwang

§ 303 SGB V verpflichtet die Krankenkassen, bei nicht maschinell verwertbarer
Übermittlung, die der Leistungserbringer zu vertreten hat, die Nacherfassungskosten
per **pauschaler Rechnungskürzung von bis zu 5 v. H. des Rechnungsbetrages** in Rechnung
zu stellen. ✅ [Q4]

Das macht korrekte, maschinell verwertbare Daten unmittelbar zahlungswirksam — und
begründet den Bedarf an einer Validierung *vor* dem Versand.

## 7. Richtungsentscheidung: TI/KIM

Der Transportweg verschiebt sich in die Telematikinfrastruktur:
- Seit Mitte 2025 können alle Bestandteile der DTA-Abrechnung — inkl. Urbelege wie
  Leistungsnachweise — über **KIM** übermittelt werden. ⚠️ [Q18]
- **Ab 01.10.2027** soll die Abrechnung ausschließlich innerhalb der TI erfolgen
  (ursprünglich 01.12.2026, verschoben zur Vermeidung paralleler Abrechnungswege). ⚠️ [Q18]
- Übergangsfrist bis Ende September 2027 für Urbelege in Papierform. ⚠️ [Q18]

❓ Der genaue gesetzliche Anknüpfungspunkt und Wortlaut dieser Fristen ist gegen
SGB V / SGB XI und Anlage 20 GGT zu verifizieren.
