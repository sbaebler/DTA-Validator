#!/usr/bin/env python3
"""Prueft das ImageLink-Paket gegen Anhang 4a/4b und gegen die DTA TSOL0002.

Pruefungen (Quelle: knowledge-base/data/imagelink.yaml):
  P01 XML validiert gegen XSD Anhang 4b
  P02 Dateinamen: <= 40 Zeichen, nur A-Z a-z 0-9 _, Endung .PDF/.XML (Grossbuchstaben), PDF und XML gleichnamig
  P03 Dokumentidentifikator = Dateiname; Vorgangsidentifikator = Dokumentidentifikator ohne Zaehler; Vorgangsumfang = Anzahl
  P04 Nutzdaten stimmen mit dem DTA-Satz ueberein (REC, INV, IK, KVNR, Kostentraeger-IK)
  P05 Ordnername <ABR>_<Sammelrechnungsnr 14><Zaehler 2>; <= 500 Images je Ordner; ZIP <= 2 GB
  P06 Auftragssatz: Verfahren T1IM0, Komprimierung 03, Groesse = ZIP-Groesse, Satzlaenge 348
  P07 Jeder DTA-Fall der Sammelrechnung hat genau ein Dokument, kein Dokument ohne Fall
  P08 PDF beginnt mit %PDF und ist lesbar (pdfinfo)

Aufruf: python3 pruefe_paket.py [paketverzeichnis] [dta]   Exitcode 0 = keine Fehler
"""
import os
import re
import subprocess
import sys
import tempfile
import zipfile

from lxml import etree

HIER = os.path.dirname(os.path.abspath(__file__))
XSD = os.path.join(HIER, "..", "..", "..", "knowledge-base", "data", "schemas", "Anhang_04b_Anlage_1_TP5_20220519.xsd")


def dta_faelle(pfad):
    """Liest aus der Nutzdatei je INV: Beleg, KVNR sowie REC und FKT der zugehoerigen SLLA."""
    segs = open(pfad, "rb").read().decode("latin-1").split("'")[:-1]
    faelle, rec, fkt, typ = {}, None, None, None
    for s in segs:
        e = s.split("+")
        if e[0] == "UNH":
            typ = e[2].split(":")[0]
        elif typ == "SLLA" and e[0] == "FKT":
            fkt = e
        elif typ == "SLLA" and e[0] == "REC":
            rec = e
        elif typ == "SLLA" and e[0] == "INV":
            sammel, einzel = rec[1].split(":")
            faelle[(sammel, einzel, e[2])] = dict(kvnr=e[1], rechnungsdatum=rec[2], rechnungsart=rec[3],
                                                  ik_le=fkt[2], ik_kt=fkt[3])
    return faelle


def pruefe(paket, dta):
    fehler = []
    f = lambda code, msg: fehler.append("%s %s" % (code, msg))  # noqa: E731
    schema = etree.XMLSchema(etree.parse(XSD))
    faelle = dta_faelle(dta)
    gesehen = set()
    namen = sorted(n for n in os.listdir(paket) if not n.endswith((".AUF", ".csv")))
    for zn in namen:
        zpfad = os.path.join(paket, zn)
        if os.path.getsize(zpfad) > 2 * 1024**3:
            f("P05", "%s: ZIP > 2 GB" % zn)
        auf = open(zpfad + ".AUF", "rb").read().decode("latin-1")
        if len(auf) != 348:
            f("P06", "%s.AUF: Satzlaenge %d" % (zn, len(auf)))
        if auf[19:24] != "T1IM0" and auf[19:24] != "E1IM0":
            f("P06", "%s.AUF: Verfahrenskennung %r" % (zn, auf[19:24]))
        if auf[204:206] != "03":
            f("P06", "%s.AUF: Komprimierung %r (erwartet 03)" % (zn, auf[204:206]))
        if int(auf[178:190]) != os.path.getsize(zpfad) or int(auf[190:202]) != os.path.getsize(zpfad):
            f("P06", "%s.AUF: Dateigroesse stimmt nicht mit ZIP ueberein" % zn)
        with zipfile.ZipFile(zpfad) as z:
            eintraege = [i for i in z.infolist() if not i.is_dir()]
            ordner = {}
            for i in eintraege:
                teile = i.filename.split("/")
                if len(teile) != 2:
                    f("P05", "%s: %s nicht in flacher Ordnerstruktur" % (zn, i.filename))
                    continue
                ordner.setdefault(teile[0], {}).setdefault(teile[1].rsplit(".", 1)[0], {})[teile[1].rsplit(".", 1)[1]] = i
            for on, docs in ordner.items():
                m = re.fullmatch(r"([A-Z0-9]{3})_([A-Za-z0-9]{14})(\d{2})", on)
                if not m:
                    f("P05", "%s: Ordnername %s verletzt <ABR>_<Sammelrechnungsnr 14><Zaehler 2>" % (zn, on))
                if len(docs) > 500:
                    f("P05", "%s/%s: %d Images (max. 500)" % (zn, on, len(docs)))
                for dok, teile in docs.items():
                    if not re.fullmatch(r"[A-Za-z0-9_]{1,40}", dok):
                        f("P02", "%s: Dateiname %r unzulaessig oder > 40 Zeichen" % (zn, dok))
                    if set(teile) != {"PDF", "XML"}:
                        f("P02", "%s/%s: Endungen %s (erwartet PDF und XML in Grossbuchstaben)" % (zn, dok, sorted(teile)))
                        continue
                    pdf = z.read(teile["PDF"])
                    if not pdf.startswith(b"%PDF"):
                        f("P08", "%s/%s: kein PDF" % (zn, dok))
                    else:
                        with tempfile.NamedTemporaryFile(suffix=".pdf") as t:
                            t.write(pdf)
                            t.flush()
                            if subprocess.run(["pdfinfo", t.name], capture_output=True).returncode != 0:
                                f("P08", "%s/%s: PDF nicht lesbar" % (zn, dok))
                    try:
                        doc = etree.fromstring(z.read(teile["XML"]))
                    except etree.XMLSyntaxError as e:
                        f("P01", "%s/%s: XML nicht wohlgeformt: %s" % (zn, dok, e))
                        continue
                    if not schema.validate(doc):
                        f("P01", "%s/%s: %s" % (zn, dok, schema.error_log.last_error.message))
                    d = doc.find("eAkte_Dokument")
                    if d is None:
                        continue
                    if d.get("Dokumentidentifikator") != dok:
                        f("P03", "%s/%s: Dokumentidentifikator %r" % (zn, dok, d.get("Dokumentidentifikator")))
                    if d.get("Vorgangsidentifikator") != dok[:-2]:
                        f("P03", "%s/%s: Vorgangsidentifikator %r" % (zn, dok, d.get("Vorgangsidentifikator")))
                    if d.get("Vorgangsumfang") != "001":
                        f("P03", "%s/%s: Vorgangsumfang %r (1 Dokument je Vorgang)" % (zn, dok, d.get("Vorgangsumfang")))
                    nd = {v.get("Bezeichner"): "".join(v.itertext()).strip() for v in d.iter("VariablesNutzdatum")}
                    key = (nd.get("Sammelrechnungsnummer"), nd.get("Einzelrechnungsnummer"), nd.get("Belegnummer"))
                    if len(key[0] or "") != 14 or len(key[1] or "") != 6 or len(key[2] or "") != 10:
                        f("P04", "%s/%s: Laengen Sammel/Einzel/Beleg %s" % (zn, dok, [len(x or "") for x in key]))
                    fall = faelle.get(key)
                    if fall is None:
                        f("P07", "%s/%s: kein DTA-Fall zu %s" % (zn, dok, key))
                        continue
                    if key in gesehen:
                        f("P07", "%s/%s: Fall %s mehrfach geliefert" % (zn, dok, key))
                    gesehen.add(key)
                    pk = d.find("Ordnungsbegriffe/Ordnungsbegriff[@Ordnungsbegriffstyp='PKKVDE']")
                    erwartet = {
                        "KVNR": (pk.text if pk is not None else None, fall["kvnr"]),
                        "Kostentraeger-IK": (d.findtext("KassenInstitutionskennzeichen"), fall["ik_kt"]),
                        "Leistungserbringer": (nd.get("Leistungserbringer"), fall["ik_le"]),
                        "Rechnungsart": (nd.get("Rechnungsart"), fall["rechnungsart"]),
                        "Rechnungsdatum": (nd.get("Rechnungsdatum", "").replace("-", ""), fall["rechnungsdatum"]),
                    }
                    for name, (ist, soll) in erwartet.items():
                        if ist != soll:
                            f("P04", "%s/%s: %s %r != DTA %r" % (zn, dok, name, ist, soll))
    # P07: DTA-Faelle der gelieferten Sammelrechnungen vollstaendig
    gelieferte_sammel = {k[0] for k in gesehen}
    for k in faelle:
        if k[0] in gelieferte_sammel and k not in gesehen:
            f("P07", "DTA-Fall %s ohne Dokument" % (k,))
    return fehler, len(gesehen)


if __name__ == "__main__":
    paket = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HIER, "imagelink-paket")
    dta = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HIER, "TSOL0002")
    fehler, n = pruefe(paket, dta)
    for x in fehler:
        print("FEHLER", x)
    print("%d Dokumente geprueft, %d Fehler" % (n, len(fehler)))
    sys.exit(1 if fehler else 0)
