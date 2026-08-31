# Transportwege

Die GGT definieren mehrere zulässige Übertragungswege; welche im Einzelfall erlaubt sind,
regelt die jeweilige sektorspezifische Technische Anlage und die Kostenträgerdatei.

## Übersicht

| Weg | GGT-Anlage | Status | Marker |
|---|---|---|---|
| E-Mail (SMTP) | **7** | etabliert | ✅ [Q16] |
| HTTP / HTTPS | **8** | etabliert | ⚠️ [Q12] |
| FTP / SFTP / FTPS | **9** | etabliert | ⚠️ [Q12] |
| GKV-Kommunikationsserver | **13** | Arbeitgeberverfahren | ✅ [Q17] |
| Kommunikationsserver DRV | **17** | RV-Verfahren | ✅ [Q17b] |
| Physische Datenträger | **14** | Auslaufmodell | ✅ [Q21] |
| KIM in der TI | **20** | **Zielarchitektur ab 2027** | ✅ [Q18] |
| FTAM | (historisch, Anlage 5 nennt es für DSRV) | veraltet | ⚠️ [Q31] |

## 1. E-Mail (Anlage 7 GGT)

Gültig ab 01.07.2016, Stand 23.06.2016, 17 Seiten. ✅ [Q16]

**Harte Regeln** ⚠️ [Q16]:
- Pro E-Mail darf **immer nur eine Nutzdaten- und eine Auftragsdatei** übermittelt werden.
- **Mehrere Anhänge sind unzulässig** — zu viele Anhänge führen zu Verarbeitungsfehlern.
- Die **Betreffzeile** muss bestimmte Angaben enthalten, u. a. **Betriebsnummer oder
  Institutionskennzeichen**.
- Die E-Mail muss an die **korrekte Adresse** (laut Kostenträgerdatei) gehen.

## 2. HTTP/HTTPS (Anlage 8) und FTP-Familie (Anlage 9)

⚠️ [Q12] — Inhalte nicht recherchiert. Zu klären:
- TLS-Versionen und Cipher-Suites
- Client-Authentifizierung
- Verzeichnisstrukturen und Quittungsmechanismen bei (S)FTP

## 3. GKV-Kommunikationsserver (Anlage 13)

⚠️ [Q17]

- **Zentraler Zugang ("Gateway") für alle Arbeitgebermeldungen** in die Datenaustauschverfahren
- Übertragung als **XML-Dateien im eXTra-Standard** über eine **HTTPS-Verbindung**,
  die vom Arbeitgeber offengehalten werden muss
- Authentifizierung des Absenders beim **TLS-Handshake** über ein **TLS-Clientzertifikat**
- Nach Identifikation und Autorisierung werden die zugehörigen **Rückmeldungen** an den
  Arbeitgeber übertragen (Abholprinzip in derselben Verbindung)
- Der Arbeitgeber **muss das Serverzertifikat prüfen** und die Verbindung bei Fehlern
  abbrechen; ggf. sind Root- und Intermediate-Zertifikate in die Software zu importieren

## 4. Physische Datenträger (Anlage 14)

Der Datenaustausch mit physischen Datenträgern ist für **ausgewählte Verfahren** von
Leistungserbringern möglich. ⚠️ [Q21]

Belegte Vorgaben ⚠️ [Q21]:

| Medium | Vorgabe |
|---|---|
| Diskette / CD-ROM | Keine Kennsätze erforderlich; **unmittelbar nach Erstellung Schreibschutz aktivieren** |
| DVD | Nur **DVD-R** und **DVD+R**; **12 cm** Durchmesser; Rohlingstyp **DVD 5**, max. **4,7 GB**; Format **UDF**; Dateinamen nach **ISO 9660 Level 1** |
| DVD-Struktur | **Keine Unterverzeichnisse**; **alle Dateien im Wurzelverzeichnis** |

ISO 9660 Level 1 bedeutet 8.3-Dateinamen in Großbuchstaben — was exakt zur
8-stelligen Nutzdatendatei plus `.AUF` passt.

## 5. KIM in der Telematikinfrastruktur (Anlage 20)

Gültig ab 01.01.2023, Stand 17.11.2022, 4 Seiten. ✅ [Q18]

**KIM** (Kommunikation im Medizinwesen, vormals KOM-LE) ist ein sicherer E-Mail-Dienst
ausschließlich für registrierte, authentifizierte TI-Teilnehmer. ⚠️ [Q18]

**Belegte technische Vorgaben** ⚠️ [Q18]:
- Als **Signaturverfahren für Dateien ist CMS (CAdES) Enveloping** zu verwenden;
  Stapelsignatur bzw. Komfortsignatur der TI stehen zur Verfügung
- Pro KIM-Nachricht darf **nur eine Nutzdatendatei** übertragen werden; mehrere Dateien
  in einer Nachricht sind nicht möglich
- Der **Dateiname ist in die Betreffzeile** der KIM-Nachricht einzutragen

**Roadmap** ⚠️ [Q18b]:
- Seit Mitte 2025: alle Bestandteile der DTA-Abrechnung inkl. Urbelege über KIM übermittelbar
- Übergangsfrist bis **30.09.2027** für Urbelege in Papierform
- **Ab 01.10.2027**: Abrechnung ausschließlich innerhalb der TI (verschoben von 01.12.2026,
  um parallele Abrechnungswege zu vermeiden) — ❓ Rechtsgrundlage verifizieren

**Architekturkonsequenz:** Das "eine Nutzdatendatei pro Nachricht"-Prinzip gilt bei KIM
wie bei E-Mail. Ein Validator, der Transportregeln prüft, kann diese Regel
transportwegübergreifend modellieren.

## 6. Auswahl des Transportwegs

Der jeweils zulässige Weg und die konkrete Adresse (E-Mail-Adresse, Host, IK der
Annahmestelle) stehen in der **Kostenträgerdatei** des Sektors. ⚠️ [Q15]
→ [40-stammdaten/03-kostentraegerdateien-und-annahmestellen.md](../40-stammdaten/03-kostentraegerdateien-und-annahmestellen.md)
