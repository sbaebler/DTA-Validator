# Projekt-Scope und Architekturskizze

## 1. Produktidee

**DTA-Validator** — ein Werkzeug, das DTA-Dateien des deutschen GKV-Markts gegen die
geltenden Regelwerke prüft, **bevor** sie an eine Datenannahmestelle gehen.

**Wertversprechen:** Absetzungen und Rechnungskürzungen nach § 303 SGB V vermeiden,
indem Fehler dort gefunden werden, wo sie noch kostenlos zu beheben sind.

## 2. Scope

### In Scope (Ausbaustufe 1)

- Verfahren nach **§ 302 SGB V** (SLGA/SLLA)
- Verfahrensübergreifender **Transport-/Envelope-Layer** (KKS, Dateinamen, Auftragssatz)
- **Kryptografie-Prüfung** nach Anlage 16 GGT (SECON)
- Stammdatenprüfung: **IK**, **KVNR**, **Kostenträgerdatei**
- **CLI** mit JSON- und Report-Ausgabe

### In Scope (spätere Ausbaustufen)

- **§ 105 SGB XI** (PLGA/PLAA) — hohe Wiederverwendung
- **§ 301 SGB V** (Krankenhaus)
- **§ 300 SGB V** (Apotheken)
- KIM-/TI-spezifische Transportprüfungen

### Out of Scope

- Erzeugung von DTA-Dateien (der Validator prüft, er generiert nicht — Ausnahme: Testdaten)
- Versand an Datenannahmestellen
- Vertragsärztliche Abrechnung (KVDT/ADT über die KVen)
- Arbeitgeber-Meldeverfahren (DEÜV, Beitragsnachweise) — als spätere Option dokumentiert
- Fachliche Beratung zu Leistungsansprüchen

## 3. Nutzer und Anwendungsfälle

| Nutzer | Anwendungsfall |
|---|---|
| Leistungserbringer (klein) | Vor dem Versand prüfen, ob die aus der Praxissoftware erzeugte Datei fehlerfrei ist |
| Softwarehersteller | Regressionstests der eigenen DTA-Erzeugung in CI |
| Abrechnungszentrum | Eingangsprüfung von Kundendateien vor der Sammelweiterleitung |
| Datenannahmestelle | Vorprüfung und Fehlerklassifikation |
| Entwickler | Bibliothek in eigene Anwendung einbinden |

## 4. Architekturskizze

```
                       ┌──────────────────────────────────────┐
                       │            Schnittstellen            │
                       │   CLI   │   Library   │  (später:    │
                       │         │             │   HTTP-API)  │
                       └────────────────┬─────────────────────┘
                                        │
                       ┌────────────────▼─────────────────────┐
                       │          Validation Engine           │
                       │  Stufenorchestrierung, Befundsammlung│
                       │  Schweregrad-Policy, Abbruchlogik    │
                       └────────────────┬─────────────────────┘
             ┌──────────────┬───────────┼───────────┬──────────────────┐
             ▼              ▼           ▼           ▼                  ▼
      ┌────────────┐ ┌────────────┐ ┌────────┐ ┌──────────┐ ┌──────────────────┐
      │ Transport  │ │  Crypto    │ │ Parser │ │ Rule     │ │  Stammdaten      │
      │ Layer      │ │  Layer     │ │ Layer  │ │ Engine   │ │  Repository      │
      │            │ │            │ │        │ │          │ │                  │
      │ Dateinamen │ │ PKCS#7/CMS │ │EDIFACT │ │deklarativ│ │ IK-Prüfung       │
      │ Auftrags-  │ │ X.509/CRL  │ │(später │ │e Regeln  │ │ Kostenträgerdatei│
      │ satz       │ │ algorithm- │ │ XML)   │ │aus YAML  │ │ Schlüsseltabellen│
      │ Dateipaar  │ │ agnostisch │ │        │ │          │ │ Positionsnummern │
      └────────────┘ └────────────┘ └────────┘ └──────────┘ └──────────────────┘
                                        │
                       ┌────────────────▼─────────────────────┐
                       │        Regelwerks-Registry           │
                       │  Verfahren × Version × Gültigkeits-  │
                       │  zeitraum → Grammatik + Regelsatz    │
                       └──────────────────────────────────────┘
```

### Leitentscheidungen

| Entscheidung | Begründung |
|---|---|
| **Parser und Regeln strikt trennen** | § 95 SGB IV kündigt die Umstellung auf XML-Verfahren an ⚠️ [Q11]; ein XML-Parser muss später gegen dieselben Fachregeln laufen können |
| **Regeln deklarativ (YAML/DSL), nicht als Code** | Regelwerke ändern sich stichtagsbezogen; ein Update darf kein Release der Kernlogik erfordern |
| **Regelwerks-Registry mit Gültigkeitszeiträumen** | Mehrere Versionen laufen parallel (Übergangsfristen) — REQ-FACH-02/03 |
| **Krypto-Layer algorithmus-agnostisch** | PQC-Migration bis 2031 absehbar ⚠️ [Q38] — REQ-SEC-05 |
| **Stammdaten als importierbare, versionierte Artefakte** | Kostenträgerdateien und Kataloge wechseln unabhängig vom Code |
| **Offline-first** | Sozialdaten dürfen die Umgebung des Nutzers nicht verlassen — REQ-DSGVO-04 |
| **Befunde immer mit Regelwerks-Fundstelle** | Ein Befund ohne Belegstelle ist gegenüber einer Kasse nicht argumentierbar — REQ-FACH-06 |

## 5. Datenmodell (Kern)

```
Verfahren            (id, bezeichnung, rechtsgrundlage)
Regelwerksversion    (verfahren_id, version, stand, gueltig_ab, gueltig_bis, dokument_ref)
Nachrichtentyp       (verfahren_id, kennung, bezeichnung)
Segment              (nachrichtentyp_id, kennung, min, max, reihenfolge)
Feld                 (segment_id, position, name, typ, laenge, pflicht, schluesselart)
Schluesselart        (id, bezeichnung, quelle)
Schluesselwert       (schluesselart_id, wert, bezeichnung, gueltig_ab, gueltig_bis)
Regel                (id, stufe, verfahren_id, schwere, ausdruck, quelle, status)
Befund               (regel_id, schwere, fundstelle, istwert, erwartung)
```

## 6. Technologiewahl — offene Entscheidung

Noch nicht festgelegt; die Wissensbibliothek ist technologieneutral. Relevante Kriterien:

| Kriterium | Bedeutung |
|---|---|
| Krypto-Ökosystem | PKCS#7/CMS, X.509, CRL — Java (BouncyCastle) und Python (`cryptography`, `asn1crypto`) sind hier stark; die Referenz `secon-tool` ist Java ✅ [Q40] |
| Zielgruppe | Kleine Leistungserbringer → einfache Installation spricht für eine einzelne Binary (Go, Rust) oder ein Web-Frontend |
| CI-Einbindung bei Softwareherstellern | CLI mit klaren Exit-Codes, plattformunabhängig |
| Deklarative Regeln | Gute YAML-/Schema-Unterstützung |

> Entscheidung bewusst offen gelassen — sie gehört in den Projektstart, nicht in die
> Wissensbibliothek.

## 7. Abgrenzung zu Marktlösungen

Es existieren etablierte Anbieter (Abrechnungszentren, DMRZ, Praxissoftware-Hersteller),
die DTA-Erzeugung und -Versand anbieten. Der Differenzierungsansatz eines eigenen
Validators liegt in:

- **Unabhängigkeit** von einem Abrechnungsdienstleister
- **Nachvollziehbarkeit**: jeder Befund mit Regelwerks-Fundstelle
- **CI-Fähigkeit** für Softwarehersteller
- **Offline-Betrieb** ohne Datenabfluss

Eine Wettbewerbsanalyse wurde **nicht** durchgeführt und sollte vor der Produktentscheidung
nachgeholt werden.
