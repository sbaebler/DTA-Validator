#!/usr/bin/env python3
"""Baut aus der Sammelrechnung ein ImageLink-Lieferpaket nach Anlage 1 Anhang 4a (§ 302 SGB V).

Eingabe : leistungsnachweise.pdf (100 Seiten, Reihenfolge = Fallreihenfolge von TSOL0002)
Ausgabe : imagelink-paket/
            D261012.T081200.T1IM000n       ZIP je Sammelrechnung (ohne Endung .zip), n = Transfernummer
            D261012.T081200.T1IM000n.AUF   Auftragssatz, 348 Byte
            zuordnung.csv                  Beleg -> Dokumentidentifikator (Erwartungswerte fuer Tests)

Im ZIP: ein Ordner <ABR>_<Sammelrechnungsnr><Zaehler> mit je Beleg <ID>.PDF + <ID>.XML.

ABWEICHUNG VOM ECHTBETRIEB: Das Paket ist NICHT PKCS#7-signiert/-verschluesselt. Der Auftragssatz fuehrt daher
Verschluesselungsart 00 und Unterschrift 00 (Spezifikation: 03). Komprimierung 03 (ZIP) stimmt.
"""
import csv
import hashlib
import os
import re
import subprocess
import sys
import tempfile
import zipfile
from xml.sax.saxutils import escape

HIER = os.path.dirname(os.path.abspath(__file__))
import importlib.util  # noqa: E402


def _lade(name, pfad):
    spec = importlib.util.spec_from_file_location(name, pfad)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


# Beide Ordner heissen ihr Skript generate.py; daher explizit unter getrennten Namen laden.
# "generate" muss die 45000er-Fassung sein, weil das Sammelrechnungs-Skript sie so importiert.
g = _lade("generate", os.path.join(HIER, "..", "hilfsmittel-302-inkontinenz-45000", "generate.py"))
sg = _lade("generate_sammel", os.path.join(HIER, "generate.py"))

ABR = "SUE"                         # ABR-Kuerzel, 3-stellig laut Text (Beispiel der Spezifikation zeigt 7 Zeichen)
DOKUMENTKLASSE = "ER_SOLE_HIMI_ON"
ERSTELLZEIT = "2026-10-12T08:12:00Z"
ZIP_ZEIT = (2026, 10, 12, 8, 12, 0)
TRANSFER_ZEIT = ("261012", "081200")
MAX_IMAGES_JE_ORDNER = 500
BESCHREIBUNG = "AOK Systems GmbH"   # laut XSD fest (xs:attribute fixed); Dokument: "von annehmender Stelle zu definieren"
BELEGANNAHME = "661100559"
PAKET = os.path.join(HIER, "imagelink-paket")


def dokument_id(sammel, einzel, beleg, zaehler):
    n = "%s_%s%s%s%02d" % (ABR, sammel, einzel, beleg, zaehler)
    assert len(n) <= 40 and re.fullmatch(r"[A-Za-z0-9_]+", n), n
    return n


def xml_fuer(f, sammel, einzel, beleg, dok, vorgang):
    def nd(bez, typ, wert):
        return ('<VariablesNutzdatum Bezeichner="%s"><%s>%s</%s></VariablesNutzdatum>' % (bez, typ, escape(str(wert)), typ))
    return """<?xml version="1.0" encoding="UTF-8"?>
<eAkte_Dokumentdatensatz Versionsnummer="00000100" Beschreibung="%s" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="eAkteDokument.xsd">
<eAkte_Dokument Dokumentidentifikator="%s" Vorgangsidentifikator="%s" Vorgangsumfang="001">
<Dokumentklasse>%s</Dokumentklasse>
<Eingangskanal>2</Eingangskanal>
<Erstellungszeitpunkt>%s</Erstellungszeitpunkt>
<Zugriffschutz>0</Zugriffschutz>
<KassenInstitutionskennzeichen>%s</KassenInstitutionskennzeichen>
<Ordnungsbegriffe><Ordnungsbegriff Ordnungsbegriffstyp="PKKVDE">%s</Ordnungsbegriff></Ordnungsbegriffe>
<VariableNutzdaten>
%s
</VariableNutzdaten>
</eAkte_Dokument>
</eAkte_Dokumentdatensatz>
""" % (BESCHREIBUNG, dok, vorgang, DOKUMENTKLASSE, ERZEIT, f["ik_kt"], f["kvnr"], "\n".join([
        nd("Sammelrechnungsnummer", "NutzdatumString", sammel),
        nd("Einzelrechnungsnummer", "NutzdatumString", einzel),
        nd("Rechnungsdatum", "NutzdatumDate", "%s-%s-%s" % (sg.ERSTELLT[:4], sg.ERSTELLT[4:6], sg.ERSTELLT[6:])),
        nd("Rechnungsart", "NutzdatumString", "3"),
        nd("Belegnummer", "NutzdatumString", beleg),
        nd("Leistungserbringer", "NutzdatumInteger", F_IK_LE),
    ]))


ERZEIT = ERSTELLZEIT


def _id_normalisieren(data):
    """pdfseparate schreibt je Aufruf eine zufaellige /ID in den Trailer; fuer reproduzierbare Pakete festsetzen.
    Der Trailer steht hinter der Xref-Tabelle, die Offsets bleiben gueltig."""
    fest = b"/ID [<" + b"00" * 16 + b"> <" + b"00" * 16 + b">] /Root"
    neu, n = re.subn(rb"/ID \[.*?\] /Root", fest, data, count=1, flags=re.S)
    assert n == 1
    return neu


def seiten_trennen(pdf, n, ziel):
    subprocess.run(["pdfseparate", pdf, os.path.join(ziel, "s-%d.pdf")], check=True)
    out = []
    for i in range(1, n + 1):
        p = os.path.join(ziel, "s-%d.pdf" % i)
        out.append(_id_normalisieren(open(p, "rb").read()))
    return out


def seitentext(pdf_bytes):
    with tempfile.NamedTemporaryFile(suffix=".pdf") as t:
        t.write(pdf_bytes)
        t.flush()
        return subprocess.run(["pdftotext", t.name, "-"], check=True, capture_output=True, text=True).stdout


def zip_schreiben(pfad, eintraege):
    with zipfile.ZipFile(pfad, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in sorted(eintraege):
            zi = zipfile.ZipInfo(name, date_time=ZIP_ZEIT)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, data)


def main():
    global F_IK_LE
    sel, meta = sg.auswahl()
    F_IK_LE = meta["ik_le"]
    pdf = os.path.join(HIER, "leistungsnachweise.pdf")
    with tempfile.TemporaryDirectory() as tmp:
        seiten = seiten_trennen(pdf, len(sel), tmp)
    assert len(seiten) == 100
    os.makedirs(PAKET, exist_ok=True)
    zeilen = []
    transfer = 0
    for kt in sg.ANTEIL:
        fs = [f for f in sel if f["kt"] == kt]
        sammel = g.sammelrechnungsnr("SU", sg.ERSTELLT, kt)
        einzel = g.EINZELRECHNUNGSNR
        transfer += 1
        zipname = "D%s.T%s.T1IM0%03d" % (TRANSFER_ZEIT[0], TRANSFER_ZEIT[1], transfer)
        eintraege = []
        ordner_zaehler, im_ordner = 1, 0
        for f in fs:
            idx = sel.index(f)
            text = seitentext(seiten[idx])
            beleg = g.belegnr_str(f["belegnr"])
            assert beleg in text and f["kvnr"] in text, "Seite %d passt nicht zu Beleg %s" % (idx + 1, beleg)
            if im_ordner == MAX_IMAGES_JE_ORDNER:
                ordner_zaehler, im_ordner = ordner_zaehler + 1, 0
            im_ordner += 1
            ordner = "%s_%s%02d" % (ABR, sammel, ordner_zaehler)
            dok = dokument_id(sammel, einzel, beleg, 1)
            vorgang = dok[:-2]
            eintraege.append(("%s/%s.PDF" % (ordner, dok), seiten[idx]))
            eintraege.append(("%s/%s.XML" % (ordner, dok), xml_fuer(f, sammel, einzel, beleg, dok, vorgang).encode("utf-8")))
            zeilen.append([zipname, ordner, dok, vorgang, sammel, einzel, beleg, f["ik_kt"], f["kvnr"], DOKUMENTKLASSE,
                           idx + 1, hashlib.sha256(seiten[idx]).hexdigest()])
        zip_schreiben(os.path.join(PAKET, zipname), eintraege)
        groesse = os.path.getsize(os.path.join(PAKET, zipname))
        am = dict(meta, ik_le=sg.IK_ABR)
        auf = g.auftragssatz(am, groesse, transfer="%03d" % transfer, appref=("T1IM0%03d" % transfer).ljust(11),
                             erstellt="20" + TRANSFER_ZEIT[0], uhrzeit=TRANSFER_ZEIT[1][:4], verfahren="T1IM0",
                             komprimierung="03", verschluesselung="00", unterschrift="00", empfaenger=BELEGANNAHME)
        open(os.path.join(PAKET, zipname + ".AUF"), "wb").write(auf)
        print(zipname, len(fs), "Belege,", groesse, "Byte")
    with open(os.path.join(PAKET, "zuordnung.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter=";", lineterminator="\n")
        w.writerow(["zip", "ordner", "dokumentidentifikator", "vorgangsidentifikator", "sammelrechnungsnr",
                    "einzelrechnungsnr", "belegnummer", "ik_kostentraeger", "kvnr", "dokumentklasse", "seite_in_pdf",
                    "pdf_sha256"])
        w.writerows(zeilen)


if __name__ == "__main__":
    main()
