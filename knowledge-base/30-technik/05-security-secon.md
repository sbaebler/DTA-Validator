# Security-Schnittstelle (SECON) — Anlage 16 GGT

**Anlage 16 GGT — Security-Schnittstelle**, gültig ab **01.01.2026**, Stand 02.09.2025,
94 Seiten. ✅ [Q8]

Ergänzend: **Best Practice zur Security-Schnittstelle** ✅ [Q27]

## 1. Grundverfahren

Die Verarbeitung erfolgt nach **PKCS#7** (Cryptographic Message Syntax). ⚠️ [Q8][Q27]

| Schritt | ContentType | Marker |
|---|---|---|
| Signieren der Nachricht | **`SignedData`** | ⚠️ [Q8] |
| Verschlüsseln der signierten Nachricht | **`EnvelopedData`** | ⚠️ [Q8] |

Reihenfolge: **erst signieren, dann verschlüsseln** (die signierte Nachricht wird
verschlüsselt). ⚠️ [Q8]

Nutzdaten **müssen** elektronisch signiert und mit einem **gültigen Zertifikat**
verschlüsselt werden. ⚠️ [Q27]

## 2. Kryptografische Parameter

| Parameter | Vorgabe | Marker |
|---|---|---|
| **Session Key / Inhaltsverschlüsselung** | **AES**, **256 Bit**, **CBC-Modus** | ⚠️ [Q8] |
| **RSA-Schlüssellänge (Teilnehmer)** | **4096 Bit** (Standard) | ⚠️ [Q8] |
| **Interchange Key** | **4096 Bit** | ⚠️ [Q8] |
| **Hashfunktion** | **SHA-256** (Standard) | ⚠️ [Q8][Q12] |
| **Signaturverfahren (Migration)** | **RSASSA-PSS** | ⚠️ [Q27] |
| **Message-Key-Verschlüsselung (Migration)** | **EME-OAEP / RSAES-OAEP** | ⚠️ [Q27] |

Die Migration auf 4096 Bit, RSASSA-PSS und RSAES-OAEP war zur Erfüllung der
BSI-Empfehlungen **für 2023 geplant**. ⚠️ [Q27]

> ❓ Ob RSASSA-PSS/OAEP inzwischen verpflichtend oder noch optional neben PKCS#1 v1.5 sind,
> **muss aus der aktuellen Anlage 16 (Fassung 02.09.2025) verifiziert werden**. Das ist
> für einen Validator ein Ja/Nein-Unterschied bei der Signaturprüfung.

## 3. Zertifikate

⚠️ [Q8]

- Zertifikate in **ASN.1-Syntax** nach dem **X.509**-Standard
- Folgende **Extensions müssen unterstützt** werden:
  - `SubjectKeyIdentifier`
  - `AuthorityKeyIdentifier`
  - `KeyUsage`
  - `CertificatePolicies`
  - `SubjectAlternativeName`
  - `BasicConstraints`
  - `CRLDistributionPoints`
- Zertifikate haben eine **definierte Gültigkeitsdauer**, innerhalb derer signierter und
  verschlüsselter Datenaustausch mit den Sozialversicherungsträgern erfolgen kann

### Schlüsselverwaltung ⚠️ [Q8]

- Jeder Teilnehmer richtet einen **eigenen Keystore mit seinem privaten Schlüssel** ein
- Für die öffentlichen Schlüssel der Kommunikationspartner ist ein **LDAP-Server** mit
  Zertifikaten vorzusehen; das Schema des Directory Information Tree richtet sich nach
  **Kapitel 4.6.2 "LDAP-Verzeichnis" der Anlage 16**

## 4. Trust Center

| Betreiber | Rolle | Marker |
|---|---|---|
| **ITSG GmbH** | Trust Center der GKV; Zertifikate für Entgeltabrechnungs- und Leistungserbringer-Abrechnungssoftware | ⚠️ [Q13] |
| **DKTIG** | Weiteres Trust Center; gemeinsames Certification Practice Statement mit der ITSG (V1.00) | ⚠️ [Q13b] |

### Zertifikatsbeantragung (ITSG) ⚠️ [Q13]

1. Die Abrechnungssoftware (oder ein separates Verschlüsselungstool) beantragt ein
   elektronisches Zertifikat beim ITSG Trust Center
2. Bei Erst- und Erneuerungsanträgen erfolgt **Identifizierung und Authentifizierung über
   das ITSG-Registrierungsportal**
3. Die **elektronischen Schlüssel werden parallel in der verwendeten Software generiert**
   (der private Schlüssel verlässt die Software nicht)
4. Die Registrierungsstelle prüft die Angaben und leitet bei erfolgreicher Prüfung die
   Zertifikatserstellung ein

Die ITSG veröffentlicht **öffentliche Zertifikate und Verzeichnisse** (u. a. das
Annahmestellenverzeichnis). ⚠️ [Q13]

### Softwarezertifizierung ⚠️ [Q13]

Die **Systemuntersuchung der ITSG** prüft Abrechnungsprogramme für Entgelt- und
Zahlstellenabrechnung; erfolgreiche Prüfung führt zum **GKV-Zertifikat**.

> ❓ Ob und in welcher Form eine vergleichbare Zertifizierungspflicht für
> **§ 302-Abrechnungssoftware** besteht, ist nicht belegt und muss geklärt werden (❓-16a).
> Für **§ 105 SGB XI** ist die Frage beantwortet: Abschnitt 4.2.1 der Vereinbarung nach
> § 105 Abs. 2 SGB XI lässt nur Software zu, die die technischen Anforderungen erfüllt;
> der Nachweis erfolgt über eine **Softwareprüfung nach Anhang 4 der TA 1** (Prüfkatalog
> und Selbsterklärung), nicht über eine ITSG-Systemuntersuchung. ✅ [Q22]
>
> Beides ist für die Positionierung des DTA-Validators als Produkt relevant: Wo eine
> Prüfpflicht besteht, ist ein vorgelagerter Validator kein Ersatz, sondern die
> Vorstufe zum Prüfkatalog.

## 5. Kryptografie-Roadmap: BSI TR-02102 und PQC

⚠️ [Q27][Q38]

- Die BSI-Pressemitteilung vom **11.02.2026** nennt konkrete **Abkündigungsfristen für
  klassische asymmetrische Verfahren**; entsprechend sind **Anpassungen an Anlage 16 GGT
  erforderlich**, um TR-02102 zu erfüllen. ⚠️ [Q27]
- **BSI TR-02102-1 (Ausgabe 2026)** enthält Empfehlungen zur Migration auf
  Post-Quanten-Kryptografie. ⚠️ [Q38]
- Klassische Schlüsseleinigungsverfahren sollen nur noch **bis Ende 2031** verwendet werden. ⚠️ [Q38]
- Seit 2025 werden **hybride Verfahren** (klassisch + **ML-KEM**, FIPS 203) empfohlen. ⚠️ [Q38]

**Architekturkonsequenz:** Die Krypto-Schicht des Validators muss **algorithmus-agnostisch**
gebaut werden (Provider-/Strategy-Muster), damit eine PQC-Migration keine Änderung an der
Fach- oder Parserschicht erfordert.

## 6. Referenzimplementierung

**`DieTechniker/secon-tool`** — Open-Source-Werkzeug zur Ver- und Entschlüsselung nach
GKV-SECON, veröffentlicht von der Techniker Krankenkasse. ✅ [Q40]

<https://github.com/DieTechniker/secon-tool>

Empfehlung: als **Referenz und Interoperabilitäts-Testpartner** verwenden — insbesondere
um die eigene Implementierung gegen eine von einer Krankenkasse veröffentlichte
Implementierung gegenzuprüfen. Lizenz und Eignung vor Einbindung prüfen.

## 7. Prüfregel-Kandidaten für den Validator

| Prüfung | Ebene |
|---|---|
| Nutzdatendatei ist eine wohlgeformte PKCS#7/CMS-Struktur | Struktur |
| Äußerer ContentType = `EnvelopedData`, innerer = `SignedData` | Struktur |
| Inhaltsverschlüsselung = AES-256-CBC | Algorithmus |
| Digest-Algorithmus = SHA-256 | Algorithmus |
| RSA-Schlüssellänge ≥ 4096 Bit | Algorithmus |
| Signaturzertifikat zeitlich gültig | Zertifikat |
| Zertifikatskette bis zu einer akzeptierten Trust-Center-Root auflösbar | Zertifikat |
| CRL-/Sperrstatus geprüft (`CRLDistributionPoints` ausgewertet) | Zertifikat |
| `KeyUsage` passend zu Signatur bzw. Verschlüsselung | Zertifikat |
| Empfängerzertifikat gehört zum IK der Datenannahmestelle laut Kostenträgerdatei | Fachlich |
| Auftragsdatei enthält **keine** verschlüsselten Inhalte und keine Sozialdaten | Datenschutz |
