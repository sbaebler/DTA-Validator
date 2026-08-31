# Wissensbibliothek: Datenträgeraustausch (DTA) im deutschen GKV-Markt

Diese Bibliothek sammelt die **fachlichen und technischen Anforderungen** an den
Datenträgeraustausch- bzw. elektronischen Datenaustauschverfahren (DTA/EDI) zwischen
Leistungserbringern, Abrechnungszentren und den gesetzlichen Krankenkassen in Deutschland.

Sie ist die Arbeitsgrundlage für das Software-Projekt **DTA-Validator** (Prüfung von
DTA-Nachrichten gegen Syntax-, Schlüssel- und Plausibilitätsregeln).

---

## ⚠️ Verifizierungsstatus — bitte zuerst lesen

Diese Bibliothek wurde per Web-Recherche erstellt. In der Ausführungsumgebung war der
**direkte Abruf der Primärdokumente (PDF) von `gkv-datenaustausch.de` und verwandten
Domains durch die Netzwerk-Egress-Policy blockiert**. Es konnte ausschließlich die
Websuche genutzt werden.

Konsequenz: Inhalte stammen überwiegend aus Suchtreffer-Zusammenfassungen und
Dokument-Metadaten (Titel, Version, Stand, Gültigkeitsdatum), **nicht** aus dem
vollständigen Fließtext der Technischen Anlagen.

Jede Aussage ist deshalb mit einem Vertrauens-Marker versehen:

| Marker | Bedeutung |
|---|---|
| ✅ | Aus Gesetzestext oder eindeutigen Dokument-Metadaten (Titel/Version/Stand/Gültigkeit) belegt |
| ⚠️ | Sekundärquelle / Suchtreffer-Zusammenfassung — Primärdokument nicht gelesen |
| ❓ | Widersprüchlich oder unvollständig — **vor Implementierung zwingend verifizieren** |

**Verbindlich sind ausschließlich die Originaldokumente** unter
<https://www.gkv-datenaustausch.de>. Vor jeder Implementierung eines Prüfregelsatzes ist
die jeweils gültige Fassung der Technischen Anlage zu beschaffen und gegen
[`data/dokumentenregister.yaml`](data/dokumentenregister.yaml) abzugleichen.

Stand der Recherche: **31.08.2026**

---

## Struktur

| Verzeichnis | Inhalt |
|---|---|
| [`00-ueberblick/`](00-ueberblick/) | Domänenüberblick, Glossar, Quellenverzeichnis |
| [`10-rechtsgrundlagen/`](10-rechtsgrundlagen/) | SGB-Normen, Sanktionen, Fristen |
| [`20-verfahren/`](20-verfahren/) | Fachliche Anforderungen je Sektor (§§ 300, 301, 301a, 302 SGB V, § 105 SGB XI, …) |
| [`30-technik/`](30-technik/) | GGT, KKS, Auftragsdatei, EDIFACT-Syntax, Transportwege, Security (SECON) |
| [`40-stammdaten/`](40-stammdaten/) | IK, Krankenversichertennummer, Kostenträgerdateien, Schlüssel-/Positionsnummernverzeichnisse |
| [`50-anforderungen/`](50-anforderungen/) | Nummerierter Anforderungskatalog + Validierungsregeln für den Validator |
| [`60-projekt/`](60-projekt/) | Scope, Architekturskizze, Roadmap, offene Punkte |
| [`data/`](data/) | Maschinenlesbare Referenzdaten (YAML) für Codegenerierung und Tests |

## Empfohlener Einstieg

1. [Domänenüberblick](00-ueberblick/01-domaenenueberblick.md) — wer tauscht was mit wem aus
2. [Verfahrensübersicht](20-verfahren/00-verfahrensuebersicht.md) — die Sektoren im Vergleich
3. [KKS, Auftragsdatei, Dateinamen](30-technik/02-kks-auftragsdatei-dateinamen.md) — der gemeinsame Transportrahmen
4. [Mindmap: Technische Anforderungen an eine DTA-Datei](30-technik/06-mindmap-technische-anforderungen.md) — alle technischen Vorgaben auf einer Seite
5. [Anforderungskatalog](50-anforderungen/01-anforderungskatalog.md) — nummerierte Requirements
6. [Projekt-Scope](60-projekt/01-projekt-scope-und-architektur.md) — was der Validator können soll

## Pflege dieser Bibliothek

- Jede Aussage braucht eine Quellenangabe in Form `[Qxx]` mit Auflösung in
  [`00-ueberblick/03-quellenverzeichnis.md`](00-ueberblick/03-quellenverzeichnis.md).
- Neue Dokumentversionen werden in [`data/dokumentenregister.yaml`](data/dokumentenregister.yaml)
  nachgeführt (Version, Stand, Gültig-ab, URL).
- Wird ein ⚠️/❓-Punkt gegen das Primärdokument verifiziert, Marker auf ✅ setzen und
  Fundstelle (Kapitel/Seite) ergänzen.
