# Konstellation: Vollelektronische Abrechnung über KIM — `TPFL0003`

Derselbe Fall wie im Positivfall [`pflege-105-sgbxi/`](../pflege-105-sgbxi/), aber auf
dem **zweiten** der beiden in der TA 1 vorgesehenen Transportwege: über KIM innerhalb
der Telematikinfrastruktur, mit **elektronischen** statt papiergebundenen
Leistungsnachweisen.

> ## Wie belastbar ist dieses Beispiel?
>
> **Die EDIFACT-Abrechnungsdaten (`TPFL0003`) sind so belastbar wie der Positivfall** —
> es ist dieselbe, primärquellen-geprüfte Struktur, nur um das `IMG`-Segment ergänzt,
> dessen Inhalt (Leistungsnachweis-ID als UUID) in
> [`knowledge-base/data/nachrichtentypen.yaml`](../../knowledge-base/data/nachrichtentypen.yaml)
> belegt ist. **Der XML-Umschlag in [`kim-nachricht-skizze.txt`](kim-nachricht-skizze.txt)
> ist dagegen ausdrücklich keine belegte Struktur** — er bildet nur die in
> [`knowledge-base/20-verfahren/05-para105-sgbxi-pflege.md`](../../knowledge-base/20-verfahren/05-para105-sgbxi-pflege.md)
> Abschnitt 9 dokumentierte *inhaltliche* Grobgliederung ab (welche Angaben
> transportiert werden), nicht die tatsächlichen Elementnamen aus
> `PFL_basis_2.2.0.xsd` / `PFL_ABR_2.2.0.xsd` — diese Schemata liegen nicht
> ausgewertet vor (siehe [Dokumentenregister](../../knowledge-base/data/dokumentenregister.yaml)).
> Diese Datei ist deshalb eine **Skizze**, kein Fixture für einen XML-Parser.

## 1. Warum dieser Weg strukturell anders ist

Zwei Wege, deren Wahl **fachlich determiniert** ist — belegt in
[`knowledge-base/30-technik/04-transportwege.md`](../../knowledge-base/30-technik/04-transportwege.md):

| | außerhalb der TI (Positivfall) | innerhalb der TI (KIM, dieses Beispiel) |
|---|---|---|
| **Wann** | papiergebundene Leistungsnachweise | elektronische Leistungsnachweise |
| **Auftragsdatei** | ja, `TPFL0001.AUF` | **nein** |
| **Nutzdatenformat** | EDIFACT, unverschlüsselt in diesem Beispiel | EDIFACT-Kern **eingebettet** in einen XML-Umschlag |
| **Verschlüsselung** | SECON (Anlage 16 GGT) | Ende-zu-Ende durch das KIM-Clientmodul |
| **Komprimierung** | zulässig | **nein** |

**Deshalb hat dieses Verzeichnis keine `.AUF`-Datei** — nicht vergessen, sondern
Teil der Konstellation: „Auftragsdatei: **nein**" für den KIM-Weg. Ein Validator, der
das Fehlen einer Auftragsdatei immer als Fehler behandelt (wie er es für den
Positivfall zu Recht täte), muss stattdessen zuerst erkennen, über welchen
Transportweg eine Datei gekommen ist.

Vollelektronisch abrechenbar sind nach TA 1 nur die Leistungsarten `01` (ambulante
Pflege — der Fall dieses Beispiels), `07` (Verhinderungspflege) und `10`
(Entlastungsleistungen, nur durch Leistungserbringer der ambulanten Pflege).

## 2. Die Nutzdatendatei `TPFL0003`

Byte-für-Byte identisch mit [`pflege-105-sgbxi/TPFL0001`](../pflege-105-sgbxi/TPFL0001),
mit genau einer strukturellen Ergänzung: einem `IMG`-Segment je Abrechnungsfall,
direkt nach `NAD` und vor `MAN` — exakt an der Stelle, die die Grammatik
`FKT REC (INV NAD IMG? MAN …)+` vorsieht.

```
INV+K741852967+2607001'
NAD+Kerzenmacher+Hanna+19480312+Rosenweg+3+12345+Musterstadt'
IMG+03bd5493-fcb1-48b2-becb-894c67a0d45a'
MAN+202607+++3'
…
```

```
INV+M305921844+2607002'
NAD+Brinkmeier+Otto+19391127'
IMG+89307955-d530-4bfd-a77f-b532a25cb440'
MAN+202607+++4'
…
```

- **`IMG`-Inhalt:** laut Nachrichtenkatalog nur die Leistungsnachweis-ID als UUID —
  „muss zur IMG-Angabe im PLAA passen" heißt: dieselbe UUID muss auch in der
  begründenden Unterlage der KIM-Nachricht auftauchen (siehe unten). Das Segment
  selbst (Trennzeichen, ob ein einzelnes Datenelement oder eine
  Datenelementgruppe) ist **nicht feldgenau belegt** — hier als ein einzelnes
  Datenelement `IMG+<UUID>'` umgesetzt, der einfachsten mit der Grammatik
  vereinbaren Form.
- **`UNT`-Zähler der PLAA:** `155` statt `153` — die zwei zusätzlichen `IMG`-Segmente
  sind mitgezählt. Alles andere (Beträge, `IAF`, `GES`, IK, Prüfziffern) ist
  unverändert.
- **Gültigkeit befristet:** Das `IMG`-Segment entfällt ab TA 1 **6.5.0** — die
  Verknüpfung Abrechnungsfall ↔ elektronischer Leistungsnachweis wird dort anders
  gelöst (neue Technische Anlage 5, ab 01.02.2027). Diese Konstellation gilt also nur
  unter TA 1 6.4.0, wie der übrige Positivfall auch.

## 3. Der KIM-Umschlag

[`kim-nachricht-skizze.txt`](kim-nachricht-skizze.txt) füllt die in der
Wissensbibliothek dokumentierte Grobstruktur mit den Werten dieses Beispiels — als
lesbare Skizze, nicht als XSD-konforme Datei. Sie zeigt die beiden Fakten, auf die es
ankommt:

1. **Zwei Zeichensätze gleichzeitig:** Die XML-Hülle ist UTF-8 nach DIN SPEC 91379,
   ohne BOM. Die darin eingebetteten EDIFACT-Abrechnungsdaten (`TPFL0003`) behalten
   ihren eigenen ISO-Zeichensatz (`I1`/`I7`/`I8`) — ein Parser, der die
   base64-dekodierten Abrechnungsdaten als UTF-8 liest, verstümmelt Umlaute (siehe
   auch [`pflege-105-sgbxi-umlaute/`](../pflege-105-sgbxi-umlaute/)).
2. **Die Leistungsnachweis-ID verbindet zwei Ebenen:** dieselbe UUID steht im
   `IMG`-Segment der EDIFACT-Datei **und** als `LeistungsnachweisID` in der
   begründenden Unterlage der KIM-Nachricht. Eine Implementierung kann darüber
   prüfen, ob jedem `IMG` tatsächlich eine passende Unterlage beiliegt — und
   umgekehrt, ob keine Unterlage ohne zugehöriges `IMG` mitgeschickt wurde.

## 4. Was dieses Beispiel nicht leistet

| Bereich | Grund |
|---|---|
| Signaturprüfung (CAdES, SMC-B) | keine echten Zertifikate, keine echte Signatur |
| Struktur des elektronischen Leistungsnachweises selbst (`PFL_LNW_2.2.0.xsd`) | nicht ausgewertet — nur seine ID und Einbettung sind hier modelliert |
| VZD-Lookup der KIM-Adresse | Adressen sind erfunden, kein Verzeichnisdienst angebunden |
| Fehlernachricht (`EPFL0_FEH_…`) | nur der Erfolgsfall ist abgebildet |
| exakte XML-Elementnamen | siehe Belastbarkeitshinweis oben — bewusst als Skizze markiert |

## 5. Dateien

| Datei | Inhalt | Größe |
|---|---|---|
| [`TPFL0003`](TPFL0003) | Nutzdaten, EDIFACT mit `IMG`, 165 Segmente | 5006 Byte |
| [`kim-nachricht-skizze.txt`](kim-nachricht-skizze.txt) | inhaltliche Skizze des KIM-Umschlags | — |

Keine `TPFL0003.AUF` — das ist hier kein Versehen, sondern der Punkt des Beispiels
(Abschnitt 1).
