# Weitere Verfahren

## 1. Reha-Einrichtungen (§ 301 Abs. 4, 4a SGB V)

- **Anlage 1 zur Vereinbarung nach § 301 Abs. (4, 4a) SGB V**, Stand **14.03.2024** ✅ [Q29]
- Vorversion: 19.06.2023 ⚠️
- Parallel existiert bei der Deutschen Rentenversicherung ein **XML-basiertes Reha-§301-Verfahren**
  (Reha § 301 XML) für den DRV-Bereich ⚠️ — fachlich abzugrenzen, da die DRV ein anderer
  Kostenträger ist.

## 2. Anschlussrehabilitation

- **Technische Anlage zum Antrag auf Anschlussrehabilitation**, Version 1.1, Stand 15.05.2024 ⚠️
- Bindeglied zwischen Krankenhaus (§ 301) und Reha-Einrichtung

## 3. Hybrid-DRG (§ 115f SGB V)

- **Technische Anlage Hybrid-DRG-AV**, Version 1.2, Stand **12.08.2025** ✅ [Q33]
- Neues, noch junges Verfahren — für einen Validator interessant, weil hier
  Marktlösungen noch nicht etabliert sind

## 4. Klinische Krebsregister

- **Technische Anlage zur elektronischen Abrechnung der Klinischen Krebsregister**,
  Version 1.6, Stand **15.03.2024** ✅ [Q34]

## 5. Datenaustausch GKV-Spitzenverband ↔ Medizinischer Dienst (MD)

- Anlage 2 Anhang 1, Version 2.10, Stand 29.09.2025 ⚠️
- Verfahrensübergreifende Standards für die MD-Kommunikation

## 6. Arbeitgeber- und Zahlstellenverfahren (SGB IV / DEÜV)

Zweite große DTA-Familie im GKV-Markt — technisch auf denselben GGT aufsetzend, fachlich
eigenständig.

| Verfahren | Inhalt | Marker |
|---|---|---|
| **DEÜV-Meldungen** | Meldungen zur Sozialversicherung (An-/Abmeldung, Jahresmeldung, Unterbrechungsmeldung …); Empfänger ist die Krankenkasse des Beschäftigten; einheitlich geregelt in §§ 28a ff. SGB IV | ⚠️ [Q19] |
| **Beitragsnachweise** | Gemeinsame Grundsätze Beitragsnachweis, Fassung 01/2026; Übermittlung nur per systemgeprüftem Entgeltabrechnungsprogramm oder maschineller Ausfüllhilfe (§ 28f Abs. 3 i. V. m. § 95b Abs. 1 SGB IV, § 26 DEÜV) | ✅ [Q26] |
| **GKV-Monatsmeldung** | Monatliche Meldung für Mehrfachbeschäftigte u. a. | ⚠️ [Q26] |
| **AAG** | Erstattungsverfahren U1/U2 | ⚠️ |
| **EEL** | Entgeltersatzleistungen (Entgeltbescheinigung Krankengeld u. a.) | ⚠️ |
| **eAU** | Elektronische Arbeitsunfähigkeitsbescheinigung | ⚠️ |
| **Zahlstellen-Meldeverfahren** | Versorgungsbezüge | ⚠️ |
| **SV-Meldeportal** | Elektronisch gestützte Ausfüllhilfe nach § 95a SGB IV | ⚠️ [Q19] |

**Transport:** eXTra-XML über HTTPS an den **GKV-Kommunikationsserver** (Anlage 13 GGT),
authentifiziert per TLS-Clientzertifikat. ⚠️ [Q17]

**Softwarezertifizierung:** Die **Systemuntersuchung der ITSG** prüft Programme für
Entgelt- und Zahlstellenabrechnung; erfolgreiche Prüfung führt zum **GKV-Zertifikat**. ⚠️ [Q13]

> **Scope-Empfehlung:** Für den DTA-Validator zunächst *out of scope*, aber als potenzielle
> Ausbaustufe dokumentiert — der Security- und Transport-Layer ist derselbe.

## 7. Abgrenzung: DALE-UV (gesetzliche Unfallversicherung)

Der Datenaustausch mit der gesetzlichen Unfallversicherung (DGUV) nutzt dieselben
Gemeinsamen Grundsätze Technik (u. a. dieselbe Auftragsdatei-Struktur ⚠️), ist aber ein
eigenes Vertrags- und Nachrichtenuniversum. Nicht Teil des GKV-Markts im engeren Sinn.
