# Kostenträgerdateien und Annahmestellen

## 1. Was die Kostenträgerdatei ist

Die **Kostenträgerdatei** ist das **amtliche Verzeichnis der Daten- und Belegannahmestellen**.
Sie enthält die aktuellen Informationen darüber, an welche Stelle (Datenträger,
elektronische Übertragung) und an welche Belegannahmestelle die Abrechnung eines
bestimmten Kostenträgers zu richten ist. ⚠️ [Q15]

Ohne sie kann kein Routing stattfinden: Der Empfänger-IK im Auftragssatz und die
Zieladresse des Transportwegs stammen aus der Kostenträgerdatei.

## 2. Sektorspezifische Ausgaben

Die Kostenträgerdateien werden **je Leistungsbereich getrennt** veröffentlicht: ⚠️ [Q15]

| Sektor | Portalseite |
|---|---|
| Sonstige Leistungserbringer (§ 302) | `.../sonstige_leistungserbringer/kostentraegerdateien_sle/` |
| Apotheken (§ 300) | `.../apotheken/kostentraegerdateien/` |
| Pflege (§ 105 SGB XI) | `.../pflege/kostentraegerdateien_pflege/` |

Für den Krankenhausbereich (§ 301) existieren stattdessen **Informationsstrukturdaten**. ⚠️ [Q5f]

## 3. Format

⚠️ [Q15]

- Dateien tragen Endungen wie **`KE0`, `KE1`, …** (fortlaufende Ausgabestände)
- Die Datei enthält Angaben zu allgemeinem Aufbau, logischem Datenmodell, Dateiaufbau
  und Schlüsselverzeichnissen

> ❓ **Kritische Lücke:** Die konkrete **Satzartenstruktur** der Kostenträgerdatei
> (Feldpositionen, Satzarten, Verkettungslogik zwischen Kostenträger, Datenannahmestelle
> und Belegannahmestelle) ist **nicht recherchiert**. Sie ist für den Validator zentral,
> weil sie die Routing-Prüfungen ermöglicht. Beschaffung über [Q15].

## 4. Rollen im Routing

```
 Leistungserbringer (IK)
        │
        │  Kostenträgerdatei nachschlagen:
        │  „Welche Datenannahmestelle ist für Kostenträger X
        │   und Leistungsbereich Y zuständig?"
        ▼
 Datenannahmestelle (IK)  ── entschlüsselungsbefugt ──►  Kostenträger / Krankenkasse (IK)
        │
 Belegannahmestelle (IK)  ◄── Urbelege / Begleitzettel
```

| Rolle | Aufgabe | Marker |
|---|---|---|
| **Datenannahmestelle** | Nimmt verschlüsselte Nutzdaten entgegen, ist zur Entschlüsselung befugt, prüft und verteilt weiter | ⚠️ [Q15] |
| **Belegannahmestelle** | Nimmt Urbelege (Verordnungen, Leistungsnachweise) mit Begleitzettel entgegen | ⚠️ [Q15][Q36] |
| **Kostenträger** | Fachlicher Empfänger und Zahler | ⚠️ |

Beispiel für eine entschlüsselungsbefugte Datenannahmestelle außerhalb der GKV:
die **Datenstelle der Rentenversicherung (DSRV)** für bestimmte Übertragungsarten. ⚠️ [Q14]

## 5. Betriebliche Anforderungen an den Validator

| Anforderung | Begründung |
|---|---|
| Kostenträgerdatei muss **importierbar und versioniert** vorgehalten werden | Ausgabestände wechseln (KE0, KE1, …) |
| Import muss **je Sektor getrennt** erfolgen | Getrennte Veröffentlichung ⚠️ [Q15] |
| Validierungsergebnis muss den **verwendeten Ausgabestand** nennen | Nachvollziehbarkeit bei Absetzungen |
| Ein veralteter Stand muss als **Warnung** sichtbar sein | Falsches Routing = Absetzung |
| Kein automatischer Download ohne Nutzerentscheidung | Quelle ist eine externe Behördenseite; Aktualität und Integrität sind zu bestätigen |

## 6. Prüfregel-Kandidaten

| Regel | Schwere |
|---|---|
| Empfänger-IK im Auftragssatz existiert in der Kostenträgerdatei als Datenannahmestelle | Fehler |
| Kostenträger-IK in den Nutzdaten existiert in der Kostenträgerdatei | Fehler |
| Die gewählte Datenannahmestelle ist für **diesen Kostenträger und diesen Leistungsbereich** zuständig | Fehler |
| Der genutzte Transportweg ist für diese Annahmestelle zugelassen | Fehler ❓ Feld in KTR-Datei verifizieren |
| Verwendeter Ausgabestand der Kostenträgerdatei ist der aktuelle | Warnung |
