#!/usr/bin/env python3
"""Sammelrechnung ueber 100 Abrechnungsfaelle des 45.000er-Beispiels, mit Leistungsnachweisen.

Entnimmt die ersten 50/30/20 Faelle der drei Kostentraeger aus
../hilfsmittel-302-inkontinenz-45000 (identische KVNR, Belegnummern und Positionen)
und erzeugt:
  TSOL0002                  Nutzdaten (je Kostentraeger Sammel-SLGA, SLGA, SLLA)
  TSOL0002.AUF              Auftragssatz
  leistungsnachweise.html   100 Leistungsnachweise (Lieferschein/Empfangsbestaetigung), eine Seite je Fall
  begleitzettel.html        je Kostentraeger ein Begleitzettel
  *.pdf                     Druckfassungen (nur mit --pdf und installiertem Chromium)
  beispiel-kennzahlen.yaml
Aufruf: python3 generate.py [--pdf]
"""
import hashlib
import html
import os
import shutil
import subprocess
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HIER, "..", "hilfsmittel-302-inkontinenz-45000"))
import generate as g  # noqa: E402

ANTEIL = {"1": 50, "2": 30, "3": 20}
ERSTELLT = "20261012"
IK_ABR = g.mk_ik("66", "12", "3344")       # Abrechnungsstelle, Klassifikation 66
APPREF = "SL086002ABK"
NAME_LE = "Musterhaus Homecare GmbH"


def auswahl():
    _, _, meta = g.erzeuge(45000, 302)
    alle = meta["faelle_daten"]
    sel = []
    for kt, n in ANTEIL.items():
        sel += [f for f in alle if f["kt"] == kt][:n]
    return sel, meta


def nutzdaten(sel, ik_le):
    seg = ["UNB+UNOC:3+%s+%s+%s:0812+2+%s+0" % (IK_ABR, "661100423", ERSTELLT, APPREF)]
    nr = 0
    summen = []

    def nachricht(typ, inhalt):
        nonlocal nr
        nr += 1
        seg.append("UNH+%d+%s:1" % (nr, typ))
        seg.extend(inhalt)
        seg.append("UNT+%d+%d" % (len(inhalt) + 2, nr))

    for kt in ANTEIL:
        fs = [f for f in sel if f["kt"] == kt]
        ik_kt = fs[0]["ik_kt"]
        sammel_nr = "2026100%d90" % int(kt)
        brutto = sum(f["brutto"] for f in fs)
        zuz = sum(f["zuzahlung"] for f in fs)
        ges = "GES+%s+%s++%s+%s" % (g.eur(brutto), g.eur(zuz), g.eur(brutto - zuz), g.eur(g.mwst_ct(brutto)))
        nam = "NAM+Abrechnungsstelle Sued GmbH+Inkassovollmacht " + NAME_LE
        nachricht("SLGA", ["FKT+01+J+%s+%s++%s" % (IK_ABR, ik_kt, IK_ABR),
                           "REC+%s:0+%s+3+EUR" % (sammel_nr, ERSTELLT), ges, nam])
        fkt = "FKT+01+%s+%s+%s" % (ik_le, ik_kt, IK_ABR)
        rec = "REC+%s:1+%s+3+EUR" % (sammel_nr, ERSTELLT)
        nachricht("SLGA", ["FKT+01++%s+%s+%s" % (IK_ABR, ik_kt, IK_ABR), rec, "UST+DE999999999+J+01", ges, nam])
        slla = [fkt, rec]
        for f in fs:
            slla += ["INV+%s+%07d" % (f["kvnr"], f["belegnr"]),
                     "NAD+%s+%s+%s" % (f["name"], f["vorname"], f["geburt"]),
                     "ESK+" + f["leistungstag"]]
            slla += ["EHE+%s+00+%d+%s+%s+07" % (p["hmnr"], p["anzahl"], g.eur(p["preis"]), g.eur(p["gesamt"]))
                     for p in f["positionen"]]
            slla.append("IAF+%s+%s++%s" % (g.eur(f["brutto"]), g.eur(f["zuzahlung"]), g.eur(f["brutto"] - f["zuzahlung"])))
        nachricht("SLLA", slla)
        summen.append((kt, ik_kt, sammel_nr, len(fs), 5 * len(fs), brutto, zuz))
    seg.append("UNZ+%d+2" % nr)
    return "'".join(seg) + "'", summen, nr, len(seg)


CSS = """
body{margin:0;background:#e9e9ea;color:#111;font:12px/1.45 -apple-system,"Segoe UI",Roboto,sans-serif}
.beleg{background:#fff;width:190mm;min-height:270mm;box-sizing:border-box;padding:14mm;margin:8mm auto;
box-shadow:0 1px 4px rgba(0,0,0,.18);page-break-after:always}
.band{background:#3a3a3c;color:#fff;text-align:center;letter-spacing:.14em;font-size:9px;font-weight:700;
padding:4px;margin:-14mm -14mm 8mm}
h1{font-size:19px;margin:0 0 2px}h2{font-size:11px;text-transform:uppercase;letter-spacing:.09em;color:#444;margin:14px 0 4px}
table{border-collapse:collapse;width:100%}th,td{border:1px solid #bbb;padding:3px 6px;text-align:left;font-size:11px}
th{background:#f2f2f3}.r{text-align:right}tfoot td{font-weight:700;background:#f2f2f3}
.sig{display:flex;gap:30px;margin-top:40px;font-size:10px;color:#555}.sig div{flex:1}
.linie{border-top:1px solid #111;height:34px;margin-bottom:3px}
footer{margin-top:18px;border-top:1px solid #ddd;padding-top:5px;font-size:9px;color:#888}
@page{size:A4;margin:0}
@media print{body{background:#fff}.beleg{margin:0;box-shadow:none;width:auto}}
"""


def seite(titel, inhalt):
    return "<!doctype html><html lang=\"de\"><head><meta charset=\"utf-8\"><title>%s</title><style>%s</style></head><body>%s</body></html>" % (
        html.escape(titel), CSS, inhalt)


def leistungsnachweis(f, lfd):
    d = f["leistungstag"]
    zeilen = "".join(
        "<tr><td>%d</td><td>%s</td><td>%s</td><td class=r>%d</td><td class=r>%s</td><td class=r>%s</td></tr>" % (
            i, p["hmnr"], html.escape(p["bez"]) + (" (Ersatznummer 900)" if p["hmnr"].endswith("900") else ""),
            p["anzahl"], g.eur(p["preis"]), g.eur(p["gesamt"]))
        for i, p in enumerate(f["positionen"], 1))
    return """<section class=beleg><div class=band>SYNTHETISCHER URBELEG — KEINE ECHTEN DATEN</div>
<h1>Leistungsnachweis / Lieferschein</h1><div>Hilfsmittelversorgung Inkontinenz &middot; Lieferung %s.%s.%s &middot; Nachweis %03d von 100</div>
<h2>Leistungserbringer</h2><table><tr><th>Name</th><td>%s</td><th>IK</th><td>%s</td></tr></table>
<h2>Versicherte(r)</h2><table>
<tr><th>Name</th><td>%s, %s</td><th>Geburtsdatum</th><td>%s.%s.%s</td></tr>
<tr><th>KVNR</th><td>%s</td><th>Kostenträger-IK</th><td>%s</td></tr>
<tr><th>Belegnummer</th><td>%07d</td><th>Rechnungsnummer</th><td>%s</td></tr></table>
<h2>Gelieferte Hilfsmittel</h2><table><thead><tr><th>Pos.</th><th>Hilfsmittelpositionsnr.</th><th>Bezeichnung</th><th class=r>Menge</th><th class=r>Einzelpreis EUR</th><th class=r>Gesamt EUR</th></tr></thead>
<tbody>%s</tbody><tfoot><tr><td colspan=5>Bruttobetrag (MwSt. 7 %%: %s EUR enthalten)</td><td class=r>%s</td></tr>
<tr><td colspan=5>Gesetzliche Zuzahlung (Versicherte/r)</td><td class=r>%s</td></tr>
<tr><td colspan=5>Rechnungsbetrag an Kostenträger</td><td class=r>%s</td></tr></tfoot></table>
<h2>Empfangsbestätigung</h2><div>Die Lieferung wurde vollständig und unbeschädigt entgegengenommen.</div>
<div class=sig><div><div class=linie></div>Ort, Datum</div><div><div class=linie></div>Unterschrift Versicherte(r) / Bevollmächtigte(r)</div></div>
<footer>Synthetischer Beleg zu den Beispieldaten des DTA-Validators. Aufbau ist eine Skizze: Anlage 5 (Inhalt der Urbelege) zu § 302 liegt nicht vor.</footer></section>""" % (
        d[6:8], d[4:6], d[0:4], lfd, NAME_LE, F_IK_LE, html.escape(f["name"]), html.escape(f["vorname"]),
        f["geburt"][6:8], f["geburt"][4:6], f["geburt"][0:4], f["kvnr"], f["ik_kt"], f["belegnr"],
        "2026100%d90:1" % int(f["kt"]), zeilen, g.eur(g.mwst_ct(f["brutto"])), g.eur(f["brutto"]),
        g.eur(f["zuzahlung"]), g.eur(f["brutto"] - f["zuzahlung"]))


def begleitzettel(sel, summen):
    out = []
    for kt, ik_kt, sn, nf, npos, br, zu in summen:
        belege = [f for f in sel if f["kt"] == kt]
        out.append("""<section class=beleg><div class=band>SYNTHETISCHER URBELEG — KEINE ECHTEN DATEN</div>
<h1>Begleitzettel für Urbelege</h1><div>Sammelrechnung %s &middot; Rechnungsdatum 12.10.2026</div>
<h2>Absender</h2><table><tr><th>Rechnungssteller</th><td>Abrechnungsstelle Sued GmbH</td><th>IK</th><td>%s</td></tr>
<tr><th>Leistungserbringer</th><td>%s</td><th>IK</th><td>%s</td></tr></table>
<h2>Empfänger</h2><table><tr><th>Kostenträger-IK</th><td>%s</td></tr></table>
<h2>Inhalt der Sendung</h2><table><tr><th>Leistungsnachweise</th><td>%d</td></tr><tr><th>Positionen</th><td>%d</td></tr>
<tr><th>Belegnummern</th><td>%07d bis %07d</td></tr><tr><th>Bruttobetrag EUR</th><td>%s</td></tr>
<tr><th>Zuzahlungen EUR</th><td>%s</td></tr><tr><th>Rechnungsbetrag EUR</th><td>%s</td></tr></table>
<footer>Synthetisch. Anlage 4 zu § 302 (Begleitzettel) liegt nicht vor; Felder sind eine Skizze.</footer></section>""" % (
            sn, IK_ABR, NAME_LE, F_IK_LE, ik_kt, nf, npos, belege[0]["belegnr"], belege[-1]["belegnr"],
            g.eur(br), g.eur(zu), g.eur(br - zu)))
    return "".join(out)


def pdf(htmlpfad):
    exe = shutil.which("chromium") or shutil.which("chromium-browser") or next(iter(__import__("glob").glob("/opt/pw-browsers/chromium-*/chrome-linux*/chrome")), None)
    if not exe:
        print("Chromium fehlt, PDF uebersprungen:", htmlpfad)
        return
    ziel = htmlpfad[:-5] + ".pdf"
    subprocess.run([exe, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    "--print-to-pdf=" + ziel, "file://" + htmlpfad], check=True, capture_output=True)


def main():
    global F_IK_LE
    sel, meta = auswahl()
    F_IK_LE = meta["ik_le"]
    assert len(sel) == 100
    daten, summen, n_nachr, n_seg = nutzdaten(sel, F_IK_LE)
    raw = daten.encode("latin-1")
    open(os.path.join(HIER, "TSOL0002"), "wb").write(raw)
    am = dict(meta, ik_le=IK_ABR)   # Absender = Abrechnungsstelle
    auf = g.auftragssatz(am, len(raw), transfer="002", appref=APPREF, erstellt=ERSTELLT)
    open(os.path.join(HIER, "TSOL0002.AUF"), "wb").write(auf)
    ln = "".join(leistungsnachweis(f, i) for i, f in enumerate(sel, 1))
    p1 = os.path.join(HIER, "leistungsnachweise.html")
    p2 = os.path.join(HIER, "begleitzettel.html")
    open(p1, "w", encoding="utf-8").write(seite("Leistungsnachweise Sammelrechnung", ln))
    open(p2, "w", encoding="utf-8").write(seite("Begleitzettel Sammelrechnung", begleitzettel(sel, summen)))
    if "--pdf" in sys.argv:
        pdf(p1)
        pdf(p2)
    with open(os.path.join(HIER, "beispiel-kennzahlen.yaml"), "w") as f:
        f.write("# Erwartungswerte, erzeugt von generate.py\nfaelle: 100\npositionen: 500\nnachrichten: %d\nsegmente: %d\n"
                % (n_nachr, n_seg))
        f.write("nutzdaten_bytes: %d\nnutzdaten_sha256: %s\nik_abrechnungsstelle: \"%s\"\nik_leistungserbringer: \"%s\"\n"
                % (len(raw), hashlib.sha256(raw).hexdigest(), IK_ABR, F_IK_LE))
        f.write("gesamtbrutto_eur: \"%s\"\nsammelrechnungen:\n" % g.eur(sum(s[5] for s in summen)))
        for kt, ik_kt, sn, nf, npos, br, zu in summen:
            f.write("  - {sammelrechnungsnummer: \"%s\", ik_kostentraeger: \"%s\", faelle: %d, positionen: %d, "
                    "brutto_eur: \"%s\", zuzahlung_eur: \"%s\"}\n" % (sn, ik_kt, nf, npos, g.eur(br), g.eur(zu)))
    print(len(sel), "Faelle,", len(raw), "Byte,", n_nachr, "Nachrichten")


if __name__ == "__main__":
    main()
